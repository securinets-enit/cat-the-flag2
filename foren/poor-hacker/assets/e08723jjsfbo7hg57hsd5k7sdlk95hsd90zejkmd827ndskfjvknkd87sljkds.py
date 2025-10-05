ds.py 
import base64
import requests

# --- Configuration for our Multi-Layered Encryption ---

XOR_KEY = "mysecretkey"

CAESAR_SHIFT = 13



def reverse_caesar_cipher(text, shift):
    decrypted_text = ""
    for char in text:
        if 'a' <= char <= 'z':
            decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        else:
            decrypted_char = char
        decrypted_text += decrypted_char
    return decrypted_text

def apply_xor_cipher(data, key):
    key_bytes = key.encode('utf-8')
    decrypted_bytes = bytearray()
    for i in range(len(data)):
        decrypted_bytes.append(data[i] ^ key_bytes[i % len(key_bytes)])
    return decrypted_bytes


def decrypt_token(encrypted_token):
    try:
        print("Step 1: Decoding from Base85...")
        xor_encrypted_bytes = base64.b85decode(encrypted_token)
        print(f"  -> Result (bytes): {xor_encrypted_bytes}")

        print("Step 2: Applying XOR cipher...")
        caesar_encrypted_bytes = apply_xor_cipher(xor_encrypted_bytes, XOR_KEY)
        caesar_encrypted_text = caesar_encrypted_bytes.decode('utf-8')
        print(f"  -> Result (text): {caesar_encrypted_text}")

        print("Step 3: Applying reverse Caesar cipher...")
        original_token = reverse_caesar_cipher(caesar_encrypted_text, CAESAR_SHIFT)
        print(f"  -> Final Token: {original_token}")

        return original_token

    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        return None


def request_custom_tools(token):
    """Makes a request to a placeholder URL with the decrypted token."""
    url = "https://api.google.com/tools/custom"  # A placeholder URL
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        print(f"\nMaking a request to {url} with the decrypted token...")
        response = requests.get(url, headers=headers)

        print(f"Request finished with status code: {response.status_code}")
        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the web request: {e}")
        return None

# --- Main Execution ---

if __name__ == "__main__":
    ENCRYPTED_TOKEN = "D+>b+1_T5K3<E1HFEk!oK~fu26ir`E165Z>P#OeQ7g$IDR8m4!1qD+`15F$l"


    print("--- Starting Decryption Process ---")
    final_token = decrypt_token(ENCRYPTED_TOKEN)

    if final_token:
        print("\n--- Decryption Successful ---")
        request_custom_tools(final_token)
    else:
        print("\n--- Decryption Failed ---")

