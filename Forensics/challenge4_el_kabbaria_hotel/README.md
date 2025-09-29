# Challenge 4: El Kabbaria Hotel - Digital Forensics Challenge

## Challenge Description

The Zodiac is staying at El Kabbaria Hotel in Tunis, using the hotel's Wi-Fi to upload evidence to darknet forums. A Gorjeni Special Agent has infiltrated the network and captured the traffic with Wireshark before the evidence gets lost in Tor nodes.

**Your Mission:** Extract the flag from the captured network traffic.

## Scenario

- **Location:** El Kabbaria Hotel, Tunis, Tunisia
- **Suspect:** The Zodiac (serial killer)
- **Agent:** Gorjeni Special Agent
- **Evidence:** 7 photos uploaded to darknet forums
- **Capture:** Network traffic with Wireshark

## Challenge Structure

```
challenge4_el_kabbaria_hotel/
├── README.md                           # This file
├── challenge_files/
│   └── el_kabbaria_hotel_capture.pcap  # Main challenge file (1200 packets, 15 minutes)
├── solution_files/
│   └── solve_complete.py               # Complete solution script
└── media_files/                        # Original images with flag metadata
    ├── zodiac_slogan_cipher.jpg
    ├── zodiac_symbol.webp
    ├── zodiac_victim_drawing.jpg
    ├── eliminated_detective.jpg
    ├── target_politician.jpg
    ├── encrypted_communication_notes.jpg
    └── encrypted_notes.jpg
```

## Challenge Details

### Network Traffic
- **Duration:** 15 minutes
- **Packets:** 1200 (8.6MB total)
- **Protocols:** HTTP (637), TCP (931), ARP (40), DNS, ICMP
- **Content:** Rich realistic web activity, Tunisian context, darknet references
- **Image Packets:** 157 large HTTP packets (11KB-58KB) containing Base64 image data

### Evidence Images
The Zodiac uploaded 7 images to darknet forums. Each image contains a part of the flag in its metadata:

1. **zodiac_slogan_cipher.jpg** - Zodiac slogan with hidden message
2. **zodiac_symbol.png** - Personal Zodiac symbol
3. **zodiac_victim_drawing.jpg** - Abstract drawing with victim
4. **eliminated_detective.jpg** - Photo of eliminated police officer
5. **target_politician.jpg** - Surveillance photo of Tunisian politician
6. **encrypted_communication_notes.jpg** - Encrypted communication notes
7. **encrypted_notes.jpg** - Additional encrypted notes

### Flag Structure
- Each image contains a flag part in the format: `PartXX:chunkedflag`
- Flag parts are Base64 encoded in different metadata fields
- Final flag format: `SecurinetsENIT{reconstructed_flag}`

### Image Encoding
- **3 images:** Double Base64 encoded (raw → Base64 → Base64)
- **4 images:** Single Base64 encoded (raw → Base64)
- Images are chunked across multiple large HTTP packets (11KB-58KB each)
- **157 image packets** total containing Base64 encoded image data

### Special Packet
- **Packet 69:** Contains a DuckDuckGo search query
- **Search Query:** `Y0u_M1GHT_W4NN4_K33P_TH1S_T1CK3T_4R0UND_EL_C0NTR0LEUR_B3SH_Y4TLA3_L3L_M3TRO`
- **Purpose:** Password for the next challenge

## Solution Approach

### Method 1: Automated Solution
```bash
# PCAP approach (analyzes network traffic and extracts images)
python3 solution_files/solver.py el_kabbaria_hotel_capture.pcap

# Direct approach (uses original images for verification)
python3 solution_files/solver.py --direct
```

### Method 2: Manual Solution
1. **Analyze PCAP:** Open the capture file in Wireshark
2. **Find Images:** Look for large HTTP packets (11KB-58KB) containing Base64 image data
3. **Extract Images:** Use "Follow TCP Stream" to extract Base64 data from image packets
4. **Decode Images:** Handle single and double Base64 encoding
5. **Extract Metadata:** Use ExifTool to read image metadata
6. **Decode Flag Parts:** Base64 decode the flag parts from metadata
7. **Reconstruct Flag:** Combine all flag parts in order
8. **Find Password:** Extract the DuckDuckGo search query from packet 69

### Method 3: Detailed Walkthrough
For comprehensive step-by-step instructions with both Wireshark GUI and tshark command-line approaches, see the **[WRITEUP.md](WRITEUP.md)** file.

## Tools Needed

- **Python 3** - For automated solver
- **Wireshark** - PCAP analysis (optional for manual approach)
- **ExifTool** - Image metadata extraction
- **Base64 decoder** - Decode flag parts
- **Text editor** - Manual analysis

## Quick Start

The challenge can be solved with a single command:

```bash
python3 solution_files/solver.py el_kabbaria_hotel_capture.pcap
```

This will automatically:
- Extract all 7 images from the PCAP
- Decode both single and double Base64 encoded images
- Extract flag parts from image metadata
- Reconstruct the complete flag
- Display the DuckDuckGo search query for the next challenge
- Show the next challenge password: `Y0u_M1GHT_W4NN4_K33P_TH1S_T1CK3T_4R0UND_EL_C0NTR0LEUR_B3SH_Y4TLA3_L3L_M3TRO`

## Hints

1. Look for HTTP POST requests to darknet forums
2. Check HTTP response bodies for image data
3. Images are spread across multiple packets
4. Flag parts are in different EXIF fields for each image
5. Packet 69 contains the next challenge password
6. Some images are double Base64 encoded

## Progressive Hints 

### Hint 1 
🔍 **Network Analysis:** Look for HTTP traffic with large payloads. Images are encoded in Base64 and spread across multiple packets.

### Hint 2
📸 **Image Detection:** Look for large HTTP packets (11KB-58KB) using filter `http and frame.len > 10000`. There are 157 such packets containing image data.

### Hint 3
🔐 **Encoding Types:** Some images are double Base64 encoded. If single decoding doesn't work, try decoding twice. Use the automated solver for reliable extraction.

### Hint 4
📋 **Metadata Fields:** Flag parts are stored in different EXIF metadata fields: Software, Subject, Artist, ImageDescription, UserComment, Copyright, and LensModel.

### Hint 5
🔢 **Flag Parts:** Each image contains exactly one flag part in the format "PartX:chunkedflag" (Base64 encoded). Look for patterns like "Part1:", "Part2:", etc. The solver will find all 7 parts automatically.

### Hint 6
🎯 **Special Packet:** Check packet 69 (Frame 69 in Wireshark) for a special DuckDuckGo search that contains the password for the next challenge.

### Hint 7
🏆 **Flag Assembly:** Combine all 7 flag parts in order (Part01 through Part07) and add the SecurinetsENIT{} wrapper. The complete flag is 47 characters long.

## Expected Flag

The final flag should be: `SecurinetsENIT{N3v3r_Tru5T_4_Fr33_W1F1_1n_3L_K4BB4R14!!}`

## Difficulty

**Medium** - Requires network forensics, steganography, and metadata analysis skills.

## Author
C4spr0x1A
