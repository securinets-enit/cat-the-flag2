#!/usr/bin/env python3
"""
Robust solver for El Kabbaria Hotel challenge PCAP.

Usage:
    python3 solve_from_pcap.py el_kabbaria_hotel_capture.pcap
"""

import os
import sys
import re
import base64
import subprocess
from collections import defaultdict, OrderedDict
from scapy.all import rdpcap, TCP, Raw, IP

# ---------- Config ----------
OUT_DIR_IMAGES = "reconstructed_images"
OUT_DIR_BLOBS  = "extracted_blobs"
MEDIA_DIR = "media_files"   # also scan these with exiftool
MIN_B64_LEN = 80           # heuristic: consider base64-like sequences >= this length
B64_RE = re.compile(rb'([A-Za-z0-9+/]{%d,}={0,2})' % MIN_B64_LEN)
PART_TEXT_RE = re.compile(r'Part\s*0*([0-9]+)\s*[:\-]\s*(.+)', re.IGNORECASE)
INLINE_PART_RE = re.compile(r'Part[0-9]+\s*:\s*[^ \r\n]+', re.IGNORECASE)
DUCK_RE = re.compile(rb'duckduckgo\.com[^\r\n]*q=([^&\s\r\n]+)|GET\s+/\?q=([^&\s\r\n]+)', re.IGNORECASE)
B64TOKEN_RE = re.compile(r'\b[A-Za-z0-9+/]{8,}={0,2}\b')

# ---------- Utilities ----------

def ensure_dir(d):
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)

def try_b64_decode(b):
    """Try base64 decode bytes b; return decoded bytes or None."""
    try:
        # pad to multiple of 4
        padding = (-len(b)) % 4
        if padding:
            b = b + b'=' * padding
        return base64.b64decode(b, validate=False)
    except Exception:
        return None

def looks_like_base64_ascii(bs):
    """Return True if bs looks like ascii base64 text (only base64 chars and =)."""
    try:
        s = bs.decode('ascii', errors='ignore')
    except:
        return False
    return bool(re.fullmatch(r'[A-Za-z0-9+/=\s]+', s))

def save_file(path, data):
    with open(path, "wb") as f:
        f.write(data)

def run_exiftool(path):
    """Return exiftool output (str) or empty string if exiftool not available."""
    try:
        res = subprocess.run(['exiftool', path], capture_output=True, text=True, timeout=15)
        return res.stdout + (("\n" + res.stderr) if res.stderr else "")
    except FileNotFoundError:
        return ""
    except Exception:
        return ""

# ---------- PCAP scanning helpers ----------

def find_duckduckgo_queries(packets):
    """Return list of (packet_index (1-based), decoded_query_str)."""
    hits = []
    for i, pkt in enumerate(packets, start=1):
        if Raw in pkt:
            raw = bytes(pkt[Raw].load)
            m = DUCK_RE.search(raw)
            if m:
                try:
                    import urllib.parse
                    # Handle both patterns: group(1) for duckduckgo.com format, group(2) for GET /?q= format
                    query_bytes = m.group(1) if m.group(1) else m.group(2)
                    q = urllib.parse.unquote(query_bytes.decode(errors='ignore'))
                except:
                    query_bytes = m.group(1) if m.group(1) else m.group(2)
                    q = query_bytes.decode(errors='ignore')
                hits.append((i, q))
    return hits

def collect_tcp_segments(packets):
    """
    Build per-direction flow segments.
    Returns dict flow_key -> list of (seq, payload_bytes, ts).
    flow_key is (src_ip, src_port, dst_ip, dst_port).
    """
    flows = defaultdict(list)
    for pkt in packets:
        if TCP in pkt and Raw in pkt and IP in pkt:
            ip = pkt[IP]
            tcp = pkt[TCP]
            payload = bytes(pkt[Raw].load)
            seq = int(tcp.seq) if hasattr(tcp, "seq") else None
            key = (ip.src, int(tcp.sport), ip.dst, int(tcp.dport))
            flows[key].append((seq, payload, float(pkt.time)))
    return flows

def reassemble_flow(segments):
    """
    segments: list of (seq, payload, ts)
    returns bytes of reassembled stream (best-effort), ordering by seq then ts, handling gaps by concatenation.
    """
    if not segments:
        return b''
    # Some segments may have None seq (rare); sort by ts in that case
    seq_known = [s for s in segments if s[0] is not None]
    seq_unknown = [s for s in segments if s[0] is None]
    if seq_known:
        # normalize seq using minimal seq as base
        seqs = sorted(seq_known, key=lambda x: x[0])
        base = seqs[0][0]
        # create mapping offset->payload, using offset = seq - base
        pieces = {}
        for seq, payload, ts in seq_known:
            offset = seq - base
            if offset < 0:
                # wrap; heuristically add 2**32
                offset = (seq + (1<<32)) - base
            # if duplicate offset, keep earliest ts
            if offset in pieces:
                # keep longer or earlier
                existing_ts = pieces[offset][1]
                if ts < existing_ts:
                    pieces[offset] = (payload, ts)
            else:
                pieces[offset] = (payload, ts)
        # merge pieces by increasing offset
        ordered_offsets = sorted(pieces.keys())
        out = bytearray()
        cur_pos = 0
        for off in ordered_offsets:
            payload, ts = pieces[off]
            if off > cur_pos:
                # gap: just append payload (can't fill), move cur_pos
                out.extend(b'\x00' * (off - cur_pos))  # placeholder zeros for gap
                cur_pos = off
            # append payload, possible overlap
            append_from = 0
            if off < cur_pos:
                append_from = cur_pos - off
            out.extend(payload[append_from:])
            cur_pos = off + len(payload)
        # append unknown-seq payloads by timestamp at the end
        for seq, payload, ts in sorted(seq_unknown, key=lambda x: x[2]):
            out.extend(payload)
        return bytes(out)
    else:
        # fallback: order by timestamp
        return b''.join([p for (_s, p, _t) in sorted(segments, key=lambda x: x[2])])

# ---------- Extraction logic ----------

def extract_b64_blobs_from_data(data_bytes):
    """
    Return list of unique base64 blob bytes found in data_bytes.
    Looks for HTTP bodies (after double CRLF) and long base64 sequences across the stream.
    """
    found = []
    # 1) search for HTTP request/response bodies: split on double CRLF and consider the tail as body
    parts = re.split(b'\r\n\r\n', data_bytes)
    if len(parts) > 1:
        # check sequences after headers
        for i in range(len(parts)-1):
            body = b'\r\n\r\n'.join(parts[i+1:])  # rest of stream after header i
            # find long base64 sequences in body
            for m in B64_RE.finditer(body):
                b64blob = m.group(1)
                if b64blob not in found:
                    found.append(b64blob)
    # 2) global search for long base64 anywhere
    for m in B64_RE.finditer(data_bytes):
        b64blob = m.group(1)
        if b64blob not in found:
            found.append(b64blob)
    return found

def decode_and_save_blob(b64bytes, out_prefix, idx):
    """
    Try decode b64bytes and save decoded content as files.
    Returns list of saved file paths (possibly multiple if further decoding finds images).
    """
    saved = []
    decoded = try_b64_decode(b64bytes)
    if decoded is None:
        # try ascii cleanup then decode
        try:
            s = b64bytes.decode('ascii', errors='ignore')
            s_clean = ''.join(s.split())
            decoded = try_b64_decode(s_clean.encode('ascii'))
        except:
            decoded = None

    if decoded is None:
        # Not decodable
        blob_path = os.path.join(OUT_DIR_BLOBS, f"{out_prefix}_blob_{idx}.b64")
        save_file(blob_path, b64bytes)
        return [blob_path]

    # detect common image magic bytes
    def detect_and_write(data_bytes, fname_base):
        out = []
        if data_bytes.startswith(b'\xff\xd8\xff'):
            path = os.path.join(OUT_DIR_IMAGES, fname_base + ".jpg")
            save_file(path, data_bytes); out.append(path)
        elif data_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            path = os.path.join(OUT_DIR_IMAGES, fname_base + ".png")
            save_file(path, data_bytes); out.append(path)
        elif data_bytes.startswith(b'RIFF') and b'WEBP' in data_bytes[:16]:
            path = os.path.join(OUT_DIR_IMAGES, fname_base + ".webp")
            save_file(path, data_bytes); out.append(path)
        elif data_bytes.startswith(b'GIF8'):
            path = os.path.join(OUT_DIR_IMAGES, fname_base + ".gif")
            save_file(path, data_bytes); out.append(path)
        else:
            # not an image; save as .bin
            path = os.path.join(OUT_DIR_BLOBS, fname_base + ".bin")
            save_file(path, data_bytes); out.append(path)
        return out

    # primary decoded
    fname_base = f"{out_prefix}_{idx:03d}"
    saved += detect_and_write(decoded, fname_base)

    # If decoded is ascii and itself looks like base64 (double-encoded), try decode again
    if looks_like_base64_ascii(decoded):
        candidate = re.sub(rb'\s+', b'', decoded)
        second = try_b64_decode(candidate)
        if second:
            fname_base2 = fname_base + "_d2"
            saved += detect_and_write(second, fname_base2)

    return saved

def scan_reconstructed_images_for_parts(image_files):
    """
    Run exiftool on images (if available) and scan metadata / raw bytes for "PartN:..." fragments.
    Returns dict part_num -> content (first occurrence wins).
    """
    parts = {}
    # check exiftool availability
    exif_available = True
    try:
        subprocess.run(['exiftool','-ver'], capture_output=True, text=True, timeout=5)
    except Exception:
        exif_available = False

    # For every image, run exiftool and parse output, then fallback to scanning raw bytes
    for img in image_files:
        print(f"[+] Inspecting metadata/raw of {img}")
        metadata_text = ""
        if exif_available:
            metadata_text = run_exiftool(img)
        # also add filename
        metadata_text += "\nFILENAME: " + os.path.basename(img)
        # 1) look for explicit plaintext Part patterns
        for m in PART_TEXT_RE.finditer(metadata_text):
            try:
                idx = int(m.group(1))
                val = m.group(2).strip()
                if idx not in parts:
                    parts[idx] = val
            except:
                pass
        # 2) look for inline '|' followed by base64 tokens (ExifTool output included these in your example)
        for token in re.findall(r'\|\s*([A-Za-z0-9+/=]{8,})', metadata_text):
            b = token.encode()
            dec = try_b64_decode(b)
            if dec:
                # decoded may contain PartN:...
                try:
                    s = dec.decode('utf-8', errors='ignore')
                except:
                    s = ""
                for m in PART_TEXT_RE.finditer(s):
                    try:
                        idx = int(m.group(1))
                        val = m.group(2).strip()
                        if idx not in parts:
                            parts[idx] = val
                    except:
                        pass
        # 3) search any long base64-like tokens in metadata and decode then search for Part patterns
        for tok in B64TOKEN_RE.findall(metadata_text):
            b = tok.encode()
            dec = try_b64_decode(b)
            if dec:
                try:
                    s = dec.decode('utf-8', errors='ignore')
                except:
                    s = ""
                for m in PART_TEXT_RE.finditer(s):
                    try:
                        idx = int(m.group(1))
                        val = m.group(2).strip()
                        if idx not in parts:
                            parts[idx] = val
                    except:
                        pass
        # 4) fallback: scan raw file bytes for base64 sequences, decode & search
        try:
            with open(img, "rb") as fh:
                raw = fh.read()
            for m in B64_RE.finditer(raw):
                b64b = m.group(1)
                dec = try_b64_decode(b64b)
                if dec:
                    try:
                        s = dec.decode('utf-8', errors='ignore')
                    except:
                        s = ""
                    for m2 in PART_TEXT_RE.finditer(s):
                        try:
                            idx = int(m2.group(1))
                            val = m2.group(2).strip()
                            if idx not in parts:
                                parts[idx] = val
                        except:
                            pass
        except Exception:
            pass

    return parts

# ---------- Main pipeline ----------

def main(pcap_path):
    if not os.path.exists(pcap_path):
        print("PCAP not found:", pcap_path); sys.exit(1)

    ensure_dir(OUT_DIR_IMAGES)
    ensure_dir(OUT_DIR_BLOBS)

    print("[*] Loading PCAP (this may take a while)...")
    packets = rdpcap(pcap_path)

    # 1) find DuckDuckGo query
    ddg_hits = find_duckduckgo_queries(packets)
    if ddg_hits:
        print("[+] DuckDuckGo occurrences found:")
        for pktnum, q in ddg_hits:
            print(f"    packet #{pktnum}: {q}")
    else:
        print("[-] No DuckDuckGo query found in PCAP payloads")

    # 2) collect TCP segments and reassemble flows
    flows = collect_tcp_segments(packets)
    print(f"[*] Collected {len(flows)} directional TCP flows with payloads")

    extracted_blob_files = []
    blob_index = 0

    # For each flow, reassemble and extract base64 blobs
    for flow_key, segments in flows.items():
        reasm = reassemble_flow(segments)
        if not reasm:
            continue
        # extract b64 blobs from this reassembled stream
        blobs = extract_b64_blobs_from_data(reasm)
        if blobs:
            for b in blobs:
                blob_index += 1
                saved = decode_and_save_blob(b, out_prefix=f"flow_{flow_key[0]}_{flow_key[2]}", idx=blob_index)
                extracted_blob_files.extend(saved)

    # 3) Also do a raw sweep on all Raw payloads (in case small flows missed)
    all_raw = b"".join([bytes(pkt[Raw].load) for pkt in packets if Raw in pkt])
    more_blobs = extract_b64_blobs_from_data(all_raw)
    for b in more_blobs:
        blob_index += 1
        saved = decode_and_save_blob(b, out_prefix="global", idx=blob_index)
        extracted_blob_files.extend(saved)

    print(f"[*] Saved {len(extracted_blob_files)} decoded files/blobs (images or bins) into {OUT_DIR_IMAGES}/{OUT_DIR_BLOBS}")

    # 4) Scan reconstructed images and media_files with exiftool + raw scan for PartN fragments
    image_files = []
    # include reconstructed images
    for root, _, files in os.walk(OUT_DIR_IMAGES):
        for f in files:
            image_files.append(os.path.join(root, f))
    # include local media_files (original images) as well
    for root, _, files in os.walk(MEDIA_DIR):
        for f in files:
            path = os.path.join(root, f)
            if path not in image_files:
                image_files.append(path)

    print(f"[*] Inspecting {len(image_files)} images (reconstructed + originals) for metadata parts...")
    parts = scan_reconstructed_images_for_parts(image_files)
    if parts:
        print("[+] Flag parts found:")
        for n in sorted(parts.keys()):
            print(f"   Part{n}: {parts[n]}")
        # assemble
        assembled = ''.join([parts[n] for n in sorted(parts.keys())])
        flag = f"SecurinetsENIT{{{assembled}}}"
        print("\n🎉 Reconstructed FLAG:", flag)
    else:
        print("[-] No 'PartN' fragments found in image metadata/raw. You can inspect files in:")
        print("   ", OUT_DIR_IMAGES, OUT_DIR_BLOBS)
        print("Try running exiftool manually on reconstructed files if needed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solve_from_pcap.py el_kabbaria_hotel_capture.pcap"); sys.exit(1)
    main(sys.argv[1])
