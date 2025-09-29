# Challenge 1: The Postcard from the Zodiac - Challenge Summary

## 📋 Challenge Overview
**Name**: The Postcard from the Zodiac  
**Difficulty**: Easy  
**Category**: Digital Forensics  
**Points**: 100  
**Estimated Time**: 10-15 minutes  

---

## 🎯 Challenge Objective
Players must use digital forensics techniques to:
1. Extract metadata from a postcard image
2. Find a hidden password in the metadata
3. Use steganography to extract a hidden image
4. Discover the flag within the hidden image

---

## 📁 Files Provided to Players
- `postcard.jpg` - The main challenge file (1.5MB)

---

## 🔑 Solution Path

### Step 1: Metadata Analysis
**Tool**: ExifTool or any metadata viewer  
**Command**: `exiftool postcard.jpg`  
**Key Finding**: Password `Tr4cK_Th3_Tr41l` in UserComment field

### Step 2: Steganography Extraction
**Tool**: Steghide  
**Command**: `steghide extract -sf postcard.jpg -p "Tr4cK_Th3_Tr41l"`  
**Result**: Extracts `Zodiac.jpg`

### Step 3: Flag Discovery
**Content**: The extracted image contains the flag:  
`SecurinetsENIT{M3t4D4TA_C4n_R3v34L_Th3_D4rkN355}`

---

## 🔗 Connection to Next Challenge
The extracted `Zodiac.jpg` contains metadata with a pastebin link:
- **URL**: https://pastebin.com/6KRtTQVP
- **Content**: Password `P4cK3t_N1nj4` for the next challenge's zip file

---

## 🛠️ Required Tools
- **ExifTool** - For metadata analysis
- **Steghide** - For steganography extraction
- **Image viewer** - To examine extracted content

---

## 💡 Hint Strategy
1. **Hint 1**: Directs to metadata
2. **Hint 2**: Emphasizes thorough examination
3. **Hint 3**: Suggests steganography
4. **Hint 4**: Confirms tool requirements

---

## 🎭 Story Elements
- **Setting**: Tunisia (authentic GPS coordinates)
- **Character**: The Zodiac (mysterious villain)
- **Role**: Gorjeni Investigation Unit agent
- **Theme**: Classic spy/mystery investigation

---

## ✅ Success Criteria
- Successfully extract hidden image using steganography
- Identify the flag in the extracted content
- Submit flag in correct format: `SecurinetsENIT{...}`

---

## 🚨 Common Issues
- Players might skip metadata analysis
- Steghide syntax errors
- Missing the password in UserComment field
- Not examining the extracted image thoroughly

---

## 🔍 Verification
The challenge has been tested and verified:
- Metadata extraction works correctly
- Steghide extraction succeeds with password
- Hidden image contains the flag
- Connection to next challenge is established

---

## 📊 Difficulty Assessment
**Easy** - Suitable for beginners with basic digital forensics knowledge
- Clear metadata clues
- Straightforward steganography
- Obvious flag format
- Good learning opportunity for basic tools

---

*This challenge serves as an excellent introduction to digital forensics concepts while maintaining engagement through story elements and progressive difficulty.* 