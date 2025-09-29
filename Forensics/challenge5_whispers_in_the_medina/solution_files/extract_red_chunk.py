#!/usr/bin/env python3
"""
Extract the multi-layer LSB chunk from Red channel planes 0,1,2.
The payload is length-prefixed (32-bit big-endian) then UTF-8 text.

Usage:
  python3 extract_red_chunk.py --input ../media_files/whispers_in_the_medina.png
"""

import argparse
from pathlib import Path
from PIL import Image


def extract_bits_from_red(img_path: Path, planes=(0, 1, 2)):
    img = Image.open(img_path).convert('RGB')
    r, g, b = img.split()
    rp = r.load()
    w, h = img.size
    bits = []
    for plane in planes:
        mask = 1 << plane
        for y in range(h):
            for x in range(w):
                bits.append(1 if (rp[x, y] & mask) else 0)
    return bits


def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        out.append(byte)
    return bytes(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=str(Path(__file__).resolve().parent.parent / 'media_files' / 'whispers_in_the_medina.png'))
    args = parser.parse_args()

    img_path = Path(args.input)
    bits = extract_bits_from_red(img_path)
    raw = bits_to_bytes(bits)
    if len(raw) < 4:
        print('[-] Not enough data')
        return
    L = int.from_bytes(raw[:4], 'big')
    chunk_bytes = raw[4:4+L]
    try:
        chunk = chunk_bytes.decode('utf-8')
    except Exception as e:
        print('[-] Decode error:', e)
        return
    print('[+] Extracted chunk:')
    print(chunk)


if __name__ == '__main__':
    main()


