# 🔍 Chrome Footprints Challenge - Organizer Guide

## 📋 Challenge Overview

**Challenge Name:** Chrome Footprints in Sidi Bou Said  
**Category:** Digital Forensics  
**Difficulty:** Intermediate to Advanced  
**Estimated Time:** 15-25 minutes  
**Points:** 500  

## 🎯 Challenge Description

After intercepting the network traffic at the cafe, our investigation led us to a public computer kiosk in the picturesque village of Sidi Bou Said. The Zodiac, always one step ahead, had used this kiosk to access the internet before disappearing into the narrow, blue-and-white streets.

**Local witnesses reported:** A mysterious figure spent several hours at the kiosk, browsing extensively about local culture, music, and... something called "machmoum." The kiosk attendant mentioned the person seemed particularly interested in traditional Tunisian music and kept muttering about "tracking the trail."

## 🏆 Flag

**Flag:** `SecurinetsENIT{1nchallah_T3arRs0u_W_Tj1b0u_Tw3m4!}`

**Flag Location:** The flag is hidden in the encrypted data chunks stored in the Local Extension Settings of the Zodiac-Helper extension. Players must:
1. Find the base64 encoded chunks in `profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/`
2. Decode the chunks and combine them
3. Apply XOR decryption with the key "machmoum"
4. Extract the flag from the decrypted data

## 🔧 Technical Details

### **File Structure:**
```
chrome_footprints_challenge/
├── profile/
│   └── Default/
│       ├── Extensions/
│       │   └── mplghmkobfajdnppdjmclfcachmezzzz/ (Zodiac-Helper)
│       ├── History (SQLite database)
│       └── Local Extension Settings/ (Encrypted data chunks)
```

### **Key Files:**
1. **Extension Files:** Contains the main logic and encrypted data
2. **History Database:** Shows browsing patterns and extension usage
3. **Local Extension Settings:** Contains the encrypted flag chunks

## 🧩 Solution Path

### **Step 1: Initial Analysis (2-3 minutes)**
- Players examine the Chrome profile structure
- Identify suspicious extensions (Zodiac-Helper)
- Notice the machmoum/jasmine theme

### **Step 2: Extension Investigation (5-7 minutes)**
- Examine extension manifest files
- Check extension background scripts
- Look for encrypted data or vault functionality

### **Step 3: Data Discovery (3-5 minutes)**
- Find encrypted data chunks in Local Extension Settings
- Discover the vault.html page with decryption interface
- Identify the XOR encryption method

### **Step 4: Key Discovery (5-8 minutes)**
- Find hints about "jasmine_essence_2024" as key source
- Realize the actual key is "machmoum" (extracted from jasmine essence)
- Understand the cultural context

### **Step 5: Decryption (2-3 minutes)**
- Combine the base64 chunks
- Apply XOR decryption with "machmoum" key
- Extract the flag

## 🔍 Detailed Solution

### **1. Finding the Encrypted Data**

The encrypted data is stored in the Local Extension Settings for the Zodiac-Helper extension:

```bash
# Location: profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/
# Files: 000001.log, 000002.log, 000003.log, 000004.log

# Content:
k:pref://helper/chunk/1
v:PgQAHR8GGwgZEiYmJA==

k:pref://helper/chunk/2
v:Ow5cAwILCQEDFAUyNQ==

k:pref://helper/chunk/3
v:UAkfPQZdGD40NzkF

k:pref://helper/chunk/4
v:RA9dFDw8GlwYWUwc
```

### **2. Discovering the Decryption Method**

Players can find hints in multiple places:

**Extension Background Script:**
```javascript
const vaultData = {
    encrypted: true,
    method: "XOR",
    keySource: "jasmine_essence_2024",
    chunks: [...]
};
```

**Vault HTML Page:**
```html
<p><strong>Method:</strong> XOR with jasmine essence</p>
<p><strong>Key Source:</strong> jasmine_essence_2024</p>
```

### **3. Finding the Key**

The key discovery requires understanding the cultural context:

- **Key Source:** "jasmine_essence_2024"
- **Actual Key:** "machmoum" (the essence of jasmine)
- **Context:** Machmoum is the traditional Tunisian name for jasmine

### **4. Decryption Process**

```python
import base64

# The base64 chunks
chunks = [
    'PgQAHR8GGwgZEiYmJA==',
    'Ow5cAwILCQEDFAUyNQ==', 
    'UAkfPQZdGD40NzkF',
    'RA9dFDw8GlwYWUwc'
]

# Decode all chunks
decoded_data = b''
for chunk in chunks:
    decoded_data += base64.b64decode(chunk)

# XOR with 'machmoum' key
key = b'machmoum'
result = b''
for i, byte in enumerate(decoded_data):
    result += bytes([byte ^ key[i % len(key)]])

print(result.decode('utf-8'))
# Output: SecurinetsENIT{1nchallah_T3arRs0u_W_Tj1b0u_Tw3m4!}
```

## 🛠️ Tools Required

- **Basic Forensics Tools:** strings, grep, file
- **Database Tools:** sqlite3
- **Text Editors:** Any text editor
- **Programming:** Python for decryption (optional)

## 🎯 Hints for Players

### **Level 1 (Easy):**
- Check the browsing history for patterns
- Look for suspicious extensions

### **Level 2 (Medium):**
- Examine extension files carefully
- Look for encrypted data storage

### **Level 3 (Medium):**
- Find the decryption method
- Understand the key derivation

### **Level 4 (Medium):**
- Apply XOR decryption
- Extract the flag

## 🚨 Common Issues

### **Players might get stuck on:**
1. **Finding the encrypted data** - Guide them to Local Extension Settings
2. **Understanding the key** - Hint about jasmine essence extraction
3. **XOR decryption** - Provide decryption examples

## 🔧 Technical Notes

### **File Integrity:**
- All files are properly formatted
- SQLite database is valid
- Extension manifests are correct
- Base64 data is properly encoded

### **Testing:**
- Tested with multiple forensics tools
- Verified decryption process
- Confirmed flag extraction

---

**Created by:** C4spr0x1A  
**Date:** 2025  
**Category:** Digital Forensics