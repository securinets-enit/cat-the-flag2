# Challenge 5: Whispers in the Medina - Challenge Summary

## 📋 Challenge Overview
**Name**: Whispers in the Medina  
**Difficulty**: Medium  
**Category**: Digital Forensics  
**Points**: 500  
**Estimated Time**: 30-45 minutes  

---

## 🎯 Challenge Objective
Players must use advanced digital forensics techniques to:
1. Extract the first flag chunk using multi-layer LSB steganography
2. Extract the second flag chunk using palette-based steganography
3. Combine both chunks to reconstruct the complete flag

---

## 📁 Files Provided to Players
- `whispers_in_the_medina.png` - The main challenge file (image with hidden data)

---

## 🔑 Solution Path

### Step 1: Multi-Layer LSB Extraction
**Technique**: Multi-Layer LSB Steganography  
**Chunk**: `SecurinetsENIT{D4MN_R1GHT!_`  
**Method**: Extract from 1st, 2nd, and 3rd LSB layers

### Step 2: Palette-Based Extraction
**Technique**: Palette-Based Steganography  
**Chunk**: `TH3_EY3_C4N_B3_D3C31V3D!}`  
**Method**: Analyze PNG color palette modifications

### Step 3: Flag Reconstruction
**Result**: Combine both chunks to get complete flag:  
`SecurinetsENIT{D4MN_R1GHT!_TH3_EY3_C4N_B3_D3C31V3D!}`

---

## 🔗 Connection to Previous Challenges
This challenge builds upon the previous forensics challenges by introducing:
- Advanced steganography techniques
- Multi-layer data hiding
- Palette-based steganography
- Complex flag reconstruction

---

## 🛠️ Required Tools
- **Python** with PIL/OpenCV - For image processing
- **Steganography tools** - For LSB extraction
- **Hex editor** - For file analysis
- **Custom scripts** - For multi-layer extraction

---

## 💡 Hint Strategy
1. **Hint 1**: Directs to visual deception
2. **Hint 2**: Suggests multiple layers
3. **Hint 3**: Points to color-based hiding
4. **Hint 4**: Confirms flag splitting
5. **Hint 5**: Emphasizes multiple techniques

---

## 🎭 Story Elements
- **Setting**: Tunisia (continuing the investigation)
- **Character**: The Zodiac (mysterious villain)
- **Role**: Gorjeni Investigation Unit agent
- **Theme**: Advanced forensic investigation

---

## ✅ Success Criteria
- Successfully extract first chunk using multi-layer LSB
- Successfully extract second chunk using palette analysis
- Combine chunks to reconstruct complete flag
- Submit flag in correct format: `SecurinetsENIT{...}`

---

## 🚨 Common Issues
- Players might only try single LSB layer
- Palette analysis might be overlooked
- Chunk combination might be missed
- Custom extraction scripts might be needed

---

## 🔍 Verification
The challenge has been tested and verified:
- Multi-layer LSB extraction works correctly
- Palette-based extraction succeeds
- Flag reconstruction produces correct result
- Challenge maintains appropriate difficulty level

---

## 📊 Difficulty Assessment
**Hard** - Suitable for advanced players with:
- Deep understanding of steganography
- Knowledge of PNG palette structure
- Ability to write custom extraction scripts
- Experience with multi-technique challenges

---

*This challenge serves as an excellent test of advanced digital forensics skills while maintaining engagement through story elements and progressive difficulty.*
