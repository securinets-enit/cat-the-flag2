# – Poor Hacker

## The Core Idea
This challenge is a **disk forensics case**. A seized disk image hides traces of a home-made “killswitch.” Players must mount the image, explore hidden dot-directories, and discover a Python script that decrypts a payload and connects to `google.com`. The twist: the image’s `/etc/hosts` secretly maps `google.com` to an attacker-controlled IP. Reversing the trivial encryption reveals the flag.

---

## Attack Vectors
- **Hidden files** in user home directories (dot-folders).  
- **Malicious Python script** with simple obfuscation.  
- **Tampered `/etc/hosts`** redirecting traffic to attacker IP.  

---

## Rabbit Holes
- Analyzing the legit project files in detail.  
- Checking your own `/etc/hosts` instead of the one on the disk.  
- Overthinking the encryption: it’s simple base64, XOR or something of that sort I haven't decided yet.  

---

## Tips
- Search for keywords like `google`, `enc`, or `hosts` in the image.  
- Inspect dotfiles and shell histories.  
- Static analysis is enough: no need to execute. ( I may ask the player to replicate the attacker's request and retreieve a custom HTTP header or something) 

---

## Learning Outcomes
Players practice **disk mounting, hidden file discovery, trivial malware reversing, and resolver tampering detection** — all core skills in digital forensics.

