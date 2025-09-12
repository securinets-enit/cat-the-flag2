# 🔍 Chrome Footprints Challenge - Detailed Writeup

## Challenge Overview
**Name:** Chrome Footprints in Sidi Bou Said  
**Category:** Digital Forensics  
**Difficulty:** Medium  
**Flag:** `SecurinetsENIT{1nchallah_T3arRs0u_W_Tj1b0u_Tw3m4!}`

---

## 📖 Challenge Description

After intercepting network traffic at a cafe, investigators discovered a public computer kiosk in Sidi Bou Said, Tunisia, that was used by the Zodiac. The kiosk's Chrome browser profile contains digital footprints that lead to a hidden flag.

---

## 🎯 Step-by-Step Solution

### Step 1: Initial Analysis

Players start by examining the Chrome profile structure:

```bash
ls -la profile/Default/
```

**Expected Output:**
```
Extensions/
History
Local Extension Settings/
Cache/
Bookmarks
Downloads
Preferences
Local State
```

### Step 2: Identify Suspicious Extensions

Players examine the Extensions directory:

```bash
ls -la profile/Default/Extensions/
```

**Found Extensions:**
- `mplghmkobfajdnppdjmclfcachmezzzz` (Zodiac-Helper)
- `pmgloihbdckpkjgnlbhedfdbclololol` (Machmoum Password Manager)

### Step 3: Examine Extension Manifests

**Zodiac-Helper Extension:**
```bash
cat profile/Default/Extensions/mplghmkobfajdnppdjmclfcachmezzzz/0.1.37/manifest.json
```

**Key Findings:**
- Extension name: "Zodiac-Helper"
- Permissions: storage, tabs, cookies, webRequest
- Content scripts for cafe.tn domains

**Machmoum Password Manager:**
```bash
cat profile/Default/Extensions/pmgloihbdckpkjgnlbhedfdbclololol/1.0.2/manifest.json
```

**Key Findings:**
- Extension name: "Machmoum Password Manager"
- Description mentions "jasmine-scented security"
- Author: "C4spr0x1A"

### Step 4: Analyze Extension Code

**Zodiac-Helper Background Script:**
```bash
cat profile/Default/Extensions/mplghmkobfajdnppdjmclfcachmezzzz/0.1.37/background.js
```

**Key Findings:**
- Encrypted flag chunks stored in local storage
- Key hint: "jasmine_essence_2024"
- Vault functionality mentioned

**Machmoum Password Manager Background Script:**
```bash
cat profile/Default/Extensions/pmgloihbdckpkjgnlbhedfdbclololol/1.0.2/background.js
```

**Key Findings:**
- Master key: "jasmine_2024"
- Encryption key hint: "machmoum_essence"
- Tunisia timezone setting

### Step 5: Find Encrypted Data

Players discover the Local Extension Settings:

```bash
ls -la "profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/"
```

**Found Files:**
- `000001.log`
- `000002.log`
- `000003.log`
- `000004.log`

### Step 6: Extract Base64 Chunks

**File Contents:**
```bash
cat "profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/000001.log"
cat "profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/000002.log"
cat "profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/000003.log"
cat "profile/Default/Local Extension Settings/mplghmkobfajdnppdjmclfcachmezzzz/000004.log"
```

**Extracted Chunks:**
- `PgQAHR8GGwgZEiYmJA==`
- `Ow5cAwILCQEDFAUyNQ==`
- `UAkfPQZdGD40NzkF`
- `RA9dFDw8GlwYWUwc`

### Step 7: Find Decryption Method

**Vault HTML Page:**
```bash
cat profile/Default/Extensions/mplghmkobfajdnppdjmclfcachmezzzz/0.1.37/vault.html
```

**Key Findings:**
- Method: XOR
- Key Hint: "jasmine_essence_2024"
- Data chunks stored in extension settings

### Step 8: Derive Decryption Key

**Key Discovery Process:**
1. Source: "jasmine_essence_2024"
2. Context: Machmoum is traditional Tunisian jasmine
3. Extraction: "machmoum" (the essence of jasmine)

### Step 9: Perform Decryption

**Python Script:**
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
```

**Output:** `SecurinetsENIT{1nchallah_T3arRs0u_W_Tj1b0u_Tw3m4!}`

---

## 🔧 Technical Details

### File Structure
```
chrome_footprints_challenge/
├── profile/
│   └── Default/
│       ├── Extensions/
│       │   ├── mplghmkobfajdnppdjmclfcachmezzzz/ (Zodiac-Helper)
│       │   └── pmgloihbdckpkjgnlbhedfdbclololol/ (Machmoum PM)
│       ├── History (SQLite database)
│       ├── Local Extension Settings/ (Encrypted data)
│       ├── Cache/ (Additional clues)
│       ├── Bookmarks (Browsing patterns)
│       ├── Downloads (Downloaded files)
│       ├── Preferences (Browser settings)
│       └── Local State (Configuration)
```

### Key Files Analysis

**1. Extension Files:**
- Contain the main logic and encrypted data
- Provide hints about decryption method
- Include cultural context

**2. Local Extension Settings:**
- Store encrypted flag chunks
- Use LevelDB log format
- Contain base64 encoded data

**3. History Database:**
- Shows browsing patterns
- Includes extension usage
- Provides context clues

**4. Cache Files:**
- Additional hints and context
- HTML snippets with clues
- Security-related information

**5. Bookmarks:**
- Shows research interests
- Contains extension links
- Provides cultural context

**6. Downloads:**
- Shows downloaded extensions
- Research documents
- Security guides

**7. Preferences:**
- Browser settings
- Username hints
- Security configurations

**8. Local State:**
- Additional configuration
- Encryption settings
- Extension statistics

---

## 🏆 Success Criteria

Players must successfully:
1. ✅ Identify suspicious extensions
2. ✅ Locate encrypted data chunks
3. ✅ Find decryption method hints
4. ✅ Derive the decryption key
5. ✅ Perform XOR decryption
6. ✅ Extract the flag

**Final Flag:** `SecurinetsENIT{1nchallah_T3arRs0u_W_Tj1b0u_Tw3m4!}`

---

## 🚨 Common Issues & Solutions

### Issue 1: Players can't find encrypted data
**Solution:** Guide them to Local Extension Settings directory

### Issue 2: Players don't understand key derivation
**Solution:** Explain the cultural context of machmoum/jasmine

### Issue 3: Players struggle with XOR decryption
**Solution:** Provide decryption examples and code

### Issue 4: Players get distracted by red herrings
**Solution:** Focus on extension analysis and encrypted data

---

## 📊 Challenge Statistics

**Expected Solve Time:** 30-45 minutes  
**Difficulty Progression:** Easy → Medium → Hard  
**Success Rate:** 70-80% (with hints)  
**Common Stuck Points:** Key derivation, XOR decryption

---

## 🔧 Tools Required

- **Basic Forensics:** strings, grep, file
- **Database:** sqlite3
- **Text Analysis:** Any text editor
- **Decryption:** Python (recommended)

---

## 📝 Additional Notes

- The challenge maintains cultural authenticity
- All data is realistic and believable
- The solution path is logical and discoverable
- The difficulty scales appropriately
- Multiple hints are available throughout

**Created by:** C4spr0x1A  
**Date:** 2024  
**Version:** 1.0