# Challenge 5: Whispers in the Medina - A Dual-Stego Pursuit

## 🎯 Challenge Overview
**Difficulty**: Medium  
**Category**: Digital Forensics  
**Points**: 500  
**Flag Format**: `SecurinetsENIT{...}`

---

## 📖 Story Background
In the winding alleys of the Tunis medina, a mysterious figure was captured on camera—face hidden, intent unclear. Our informant insists it's The Zodiac, leaving yet another breadcrumb in plain sight. The photo looks ordinary, but past experience tells us the eye can be deceived.

---

## 🎁 Challenge Files
- `whispers_in_the_medina.png` - The provided image containing hidden evidence (no metadata)

---

## 🎯 Objective
Your mission is to:
1. **Analyze the image** and hunt for hidden data beyond the obvious
2. **Extract hidden data** using advanced steganography techniques
3. **Reconstruct the complete flag** from multiple hidden chunks
4. **Submit the flag** in the correct format

---

## 💡 Hints
- **Hint 1**: The eye can be deceived—look where eyes don’t see.
- **Hint 2**: Surface-level LSB won’t be enough. Go deeper.
- **Hint 3**: Colors lie—indexed palettes can whisper secrets.
- **Hint 4**: The flag is split across different hiding techniques.

---

## 🔍 Tools You'll Need
- **Python** with PIL/OpenCV - For image processing
- **Steganography tools** - For multi-layer LSB extraction
- **PNG palette/LevelDB/hex tools** - For palette inspection and byte-level analysis
- **Custom scripts** - For multi-layer extraction and reconstruction

---

## 🚀 Getting Started
1. Download `whispers_in_the_medina.png`
2. Verify there’s no revealing metadata
3. Look for hidden data using multiple techniques
4. Extract and combine the flag chunks

---

## 🏆 Success Criteria
- Successfully extract the first flag chunk using multi-layer LSB steganography
- Successfully extract the second flag chunk using palette-based steganography
- Combine both chunks to reconstruct the complete flag
- Submit the flag in the correct format

---

## 🎭 Character: The Zodiac
A shadow moving through Tunisia, leaving cryptic evidence embedded in the most mundane artifacts.

---

## 🌍 Setting: Tunis Medina
The historic maze where echoes, colors, and patterns conceal more than they reveal.

---

**Good luck, Agent. Follow the shadow.** 🕵️‍♂️

---

*Part of the Digital Forensics CTF series. Think like an investigator—every layer matters.*

