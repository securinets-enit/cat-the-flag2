# Challenge 5: Whispers in the Medina — Writeup

## Overview
A lone silhouette crossing the alleys of Tunis. The Zodiac was seen again, and this time he left a message where the eye cannot help but look—but must also learn to see. This challenge blends a highly visible stego cue with a deeper, multi-layer extraction, rewarding players who check both planes and bits.

- **File**: `whispers_in_the_medina.png`
- **Category**: Digital Forensics (Medium)
- **Techniques**: Visible bit-plane stego, multi-layer LSB stego
- **Final Flag**: `SecurinetsENIT{D4MN_R1GHT!_TH3_EY3_C4N_B3_D3C31V3D!}`

---

## Step 1 — Visible Plane Recon (StegSolve)
Open the image in StegSolve and inspect the color bit-planes.

- Navigate to Blue channel bit-plane 0 (B-0).
- A large, crisp message is visible:

```
TH3_EY3_C4N_B3_D3C31V3D!}
```

This is the second chunk of the flag. Its presence in a single plane is intentional—players who know to check planes are immediately rewarded.

---

## Step 2 — Hidden Chunk via Multi-Layer LSB
The first chunk is embedded across multiple LSB planes of the Red channel. It is stored as a length‑prefixed UTF‑8 payload and spans Red planes 0, 1, and 2.

- **Chunk target**: `SecurinetsENIT{D4MN_R1GHT!_`
- **Encoding**: 32‑bit big‑endian length prefix + UTF‑8 bytes
- **Carriers**: Red bit-planes [0, 1, 2], raster-scan order

### Extraction Approach (Reference Python)
```python
from PIL import Image

def extract_bits_from_red(img_path, planes=(0,1,2)):
    img = Image.open(img_path).convert('RGB')
    r, g, b = img.split()
    rp = r.load()
    w, h = img.size
    bits = []
    for plane in planes:
        mask = 1 << plane
        for y in range(h):
            for x in range(w):
                bits.append(1 if (rp[x,y] & mask) else 0)
    return bits

def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        out.append(byte)
    return bytes(out)

bits = extract_bits_from_red('whispers_in_the_medina.png')
raw = bits_to_bytes(bits)
L = int.from_bytes(raw[:4], 'big')
chunk = raw[4:4+L].decode('utf-8')
print(chunk)
```

Expected output:
```
SecurinetsENIT{D4MN_R1GHT!_
```

---

## Step 3 — Reassemble the Flag
Concatenate both chunks in order:

```
SecurinetsENIT{D4MN_R1GHT!_  +  TH3_EY3_C4N_B3_D3C31V3D!}
```

Final Flag:
```
SecurinetsENIT{D4MN_R1GHT!_TH3_EY3_C4N_B3_D3C31V3D!}
```

---

## Notes for Organizers
- The visible message is placed in Blue LSB (plane 0) for immediate discovery in StegSolve.
- The hidden message uses Red planes (0–2) with a length prefix to make extraction unambiguous.
- The image contains no EXIF/C2PA metadata.

## Common Pitfalls
- Only checking grayscale planes and missing color-specific planes.
- Assuming single-plane LSB only; ignoring multi-layer carriers.
- Misreading byte order of the length prefix (it’s big-endian).

## Recommended Hints (Progressive)
1. “The eye lies in color.”
2. “A single bit can shout; others whisper together.”
3. “Red remembers more than Blue reveals.”

---

Prepared for the Digital Forensics CTF storyline: The Zodiac’s trail now echoes through the medina—bold on the surface, cunning underneath.

