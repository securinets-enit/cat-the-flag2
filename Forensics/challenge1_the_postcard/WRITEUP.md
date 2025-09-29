# Challenge 1: The Postcard from the Zodiac - Writeup

## 🎯 Challenge Summary
**Difficulty**: Easy  
**Category**: Digital Forensics  
**Points**: 100  
**Flag**: `SecurinetsENIT{M3t4D4TA_C4n_R3v34L_Th3_D4rkN355}`

---

## 🔍 Step-by-Step Solution

### Step 1: Initial Analysis
The challenge provides a single file: `postcard.jpg`

This is a postcard image from Tunisia that appears to be a normal tourist postcard at first glance.

### Step 2: Metadata Examination
The first clue is in the challenge description: "Check the metadata carefully - every field might hold a clue"

Using **ExifTool** to examine the metadata:
```bash
exiftool postcard.jpg
```

**Key Metadata Fields Found:**
- **Artist**: "The Zodiac"
- **Copyright**: "Gorjeni Investigation Unit"
- **UserComment**: "Tr4cK_Th3_Tr41l" ⭐ **This is the password!**
- **XPComment**: "Tr4cK_Th3_Tr41l"
- **GPS Coordinates**: 36.8065°N, 10.1815°E (Tunis, Tunisia)
- **DateTime**: 2025:01:15 14:30:00

### Step 3: Steganography Extraction
The password "Tr4cK_Th3_Tr41l" is used with **Steghide** to extract hidden content:

```bash
steghide extract -sf postcard.jpg -p "Tr4cK_Th3_Tr41l"
```

This extracts a hidden file: `Zodiac.jpg`

### Step 4: Analyzing the Hidden Image
The extracted image `Zodiac.jpg` contains:
- A mysterious figure (The Zodiac)
- The flag: `SecurinetsENIT{M3t4D4TA_C4n_R3v34L_Th3_D4rkN355}`

### Step 5: Bonus Discovery
For the next challenge, players should examine the metadata of the extracted `Zodiac.jpg`:

```bash
exiftool Zodiac_small.jpg
```

**Hidden Clue Found:**
- **UserComment**: "https://pastebin.com/6KRtTQVP"
- **XPComment**: "https://pastebin.com/6KRtTQVP"

This pastebin link contains the password for the next challenge's zip file: `P4cK3t_N1nj4`

---

## 🛠️ Tools Used
1. **ExifTool** - For metadata analysis
2. **Steghide** - For steganography extraction
3. **Image Viewer** - To examine the extracted content

---

## 🔑 Key Learning Points
1. **Metadata Analysis**: Always check image metadata for hidden clues
2. **Steganography**: Images can contain hidden files using steganography tools
3. **Password Discovery**: The password was cleverly hidden in the UserComment field
4. **Chain of Evidence**: The challenge leads to the next one through the pastebin link

---

## 🎭 Story Elements
- **The Zodiac**: The mysterious villain leaving clues
- **Gorjeni Investigation Unit**: The player's role as a forensic investigator
- **Tunisia Setting**: Authentic location with GPS coordinates
- **Postcard Theme**: Classic spy/mystery trope

---

## 🚨 Common Pitfalls
1. **Missing Metadata**: Players might skip metadata analysis
2. **Wrong Password**: The password has special characters and numbers
3. **Steghide Usage**: Players need to know the correct steghide syntax
4. **File Extraction**: The hidden file might not be immediately visible

---

## 💡 Hint Strategy
- **Hint 1**: Directs players to metadata
- **Hint 2**: Emphasizes thorough metadata examination
- **Hint 3**: Suggests steganography involvement
- **Hint 4**: Confirms steganography tools are needed

---

## 🏆 Flag Submission
**Flag**: `SecurinetsENIT{M3t4D4TA_C4n_R3V34L_Th3_D4rkN355}`

The flag emphasizes that metadata can reveal hidden information, fitting the challenge theme perfectly.

---

## 🔗 Connection to Next Challenge
This challenge sets up the next one by:
- Introducing the Zodiac character
- Establishing the Tunisia setting
- Providing the pastebin link password for the next challenge
- Creating a narrative flow between challenges

---

*This writeup demonstrates the complete solution path while maintaining the mystery and engagement of the original challenge.* 