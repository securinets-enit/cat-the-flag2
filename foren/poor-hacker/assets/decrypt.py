import base64

ENCRYPTED_TOKEN = "D+>b+1_T5K3<E1HFEk!oK~fu26ir`E165Z>P#OeQ7g$IDR8m4!1qD+`15F$l"
XOR_KEY = "mysecretkey"
CAESAR_SHIFT = 13

# Base85 decode
xor_encrypted_bytes = base64.b85decode(ENCRYPTED_TOKEN)

# XOR decrypt
key_bytes = XOR_KEY.encode()
caesar_encrypted_bytes = bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(xor_encrypted_bytes)])
caesar_encrypted_text = caesar_encrypted_bytes.decode('utf-8')

# Reverse Caesar
def reverse_caesar_cipher(text, shift):
    result = ""
    for c in text:
        if 'a' <= c <= 'z':
            result += chr(((ord(c)-ord('a')-shift)%26)+ord('a'))
        elif 'A' <= c <= 'Z':
            result += chr(((ord(c)-ord('A')-shift)%26)+ord('A'))
        else:
            result += c
    return result

final_token = reverse_caesar_cipher(caesar_encrypted_text, CAESAR_SHIFT)
print(final_token)

