# – Poor Hacker

## The Core Idea
This challenge is a **disk forensics case**. A seized disk image hides traces of a home-made “killswitch.” Players must mount the image, explore hidden dot-directories, and discover a Python script that decrypts a payload and connects to `google.com` via https.

The twist: the image’s `/etc/hosts` secretly maps `google.com` to an attacker-controlled IP. 
People, especially when using AI, completely forget the script and what the script does. So instead of gathering more intel on the attacker's tooling (as said in the description), players were chasing other ctf-like thoughts like trying some stegano on legit files, which created rabbit holes i din't even plan to put. 
Rerversing the simple script gives you the first flag easily, but the second one which was initally 500 points and got increased in the last hours to 1000pts was the twist. Instead of just leaving a valued script the hacker uses and communicates with a token, players moved on. That was the mistake. 

It looks like the hacker communicates with `api.google.com` which doesn't exist, via `https` on its default port with an Authorization token. Players are supposed to see where does that `api.google.com` actually map and replcate what the hacker did. 

---

## Attack Vectors
- **Hidden files** in user home directories (dot-folders).  
- **Malicious Python script** with simple obfuscation.  
- **Tampered `/etc/hosts` and many more files required for the routing in Linux systems** redirecting traffic to attacker IP.  
---

## Rabbit Holes
- Analyzing the legit project files in detail.  
- Looking for stegano and othermp3 and placeholder files and completely forgetting the script.
- Checking your own `/etc/hosts` instead of the one on the disk. THIS WAS TOO COMMON.
- Overthinking the encryption: it’s simple base64, XOR or something of that sort I haven't decided yet.  

---

## Tips
- Inspect dotfiles and shell histories.  
- Static analysis is enough: no need to execute.


---

## Learning Outcomes
Players practice **disk mounting, hidden file discovery, and RESOLVER TEMPERING ** — all core skills in digital forensics.

---

## EASTER EGG 
The thing about this task, is using `strings` could and will lead to getting the decryption script, and then simply get the flag. 

So for that, i made an easter egg since people will neglect going through the files of the image or anything of that sort if they get the flag.
The easter egg is replicating what the attacker did and retreiving another flag from the `api.google.com` and `google.com` which resolve to another ip not the real google's ips. 

Because the idea is that the tooling of the attacker is a bit twisted, since he has a custom nameserver and a cutom DNS resolution mechanism. Because we often tend to think about the DNS resolution being made with a public provider directly which can be found in basic google search, i made it point to another DNS IP.


```bash
curl  -H "Authorization: Bearer SecurinetsENIT{837b8d424c0445ab3a51f1100da61a4b}" https://34.163.251.7/ -k
{"flag":"SecurinetsENIT{d06076ce3a0f542bada9c84ed02f3cb8}"}
```
