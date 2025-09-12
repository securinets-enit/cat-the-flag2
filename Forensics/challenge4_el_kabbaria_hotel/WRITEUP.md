# Challenge 4: El Kabbaria Hotel - Complete Writeup

## Challenge Overview

**Scenario:** The Zodiac is staying at El Kabbaria Hotel in Tunis, using the hotel's Wi-Fi to upload evidence to darknet forums. A Gorjeni Special Agent has infiltrated the network and captured the traffic with Wireshark before the evidence gets lost in Tor nodes.

**Objective:** Extract 7 images from the network capture and reconstruct the flag from their metadata.

**Flag Format:** `SecurinetsENIT{N3v3r_Tru5T_4_Fr33_W1F1_1n_3L_K4BB4R14!!}`

---

## Solution Approaches

This challenge can be solved using two main approaches:
1. **Wireshark GUI** - Visual analysis with filtering and export capabilities
2. **tshark Command Line** - Automated extraction and analysis

Both approaches will lead to the same solution, but the tools and techniques differ.

---

## Approach 1: Wireshark GUI Walkthrough

### Step 1: Open the PCAP File
1. Launch Wireshark
2. Open `challenge_files/el_kabbaria_hotel_capture.pcap`
3. You should see 1200 packets spanning approximately 15 minutes

### Step 2: Analyze Network Traffic
1. **Overview Analysis:**
   - Look at the Protocol Hierarchy (Statistics → Protocol Hierarchy)
   - Notice the mix of protocols: HTTP, HTTPS, DNS, ARP, TCP, UDP
   - Observe the realistic web browsing patterns

2. **Identify HTTP Traffic:**
   - Apply filter: `http`
   - Look for POST requests and response bodies containing image data
   - Notice the Base64-encoded content in HTTP bodies

### Step 3: Find Image Data
1. **Search for Large HTTP Packets:**
   - Look for HTTP packets with large payloads (11KB-58KB)
   - Filter: `http and frame.len > 10000`
   - These packets contain Base64 encoded image data

2. **Identify Image Packets:**
   - **157 large HTTP packets** contain image data
   - Images are chunked across multiple consecutive packets
   - Look for packets with similar source/destination IPs
   - Check packet sizes - image chunks are 11KB-58KB each

3. **Image Distribution:**
   - Images are distributed throughout the 1200 packets
   - Each image spans multiple large HTTP packets
   - Look for patterns of consecutive large packets
   - Images are well-ordered but spread around the capture

4. **Special Packet:**
   - **Packet 69:** Contains DuckDuckGo search query

### Step 4: Extract Images
1. **Method 1 - Follow TCP Stream:**
   - Right-click on a packet containing image data
   - Select "Follow" → "TCP Stream"
   - Look for Base64-encoded image data
   - Copy the Base64 data (without HTTP headers)

2. **Method 2 - Export Objects:**
   - Go to File → Export Objects → HTTP
   - Look for any objects that might be images
   - Note: This might not work for all images due to encoding

3. **Method 3 - Manual Extraction:**
   - Select packets containing image data
   - Right-click → "Copy" → "As Raw Bytes"
   - Paste into a text editor and clean up HTTP headers
   - Extract only the Base64 payload

4. **Method 4 - Filter Large Packets:**
   - Apply filter: `http and frame.len > 10000`
   - This will show all 157 image packets
   - Look for consecutive packets with similar IPs
   - Follow TCP streams to extract complete images
   - **Special:** Go to packet 69 for DuckDuckGo search

### Step 5: Decode Images
1. **For Single Base64 Encoded Images:**
   - Use online Base64 decoders or command line tools
   - Save as `.jpg` or `.webp` files

2. **For Double Base64 Encoded Images:**
   - Decode the Base64 data twice
   - First decode gives you another Base64 string
   - Second decode gives you the actual image data

3. **Command Line Decoding:**
   ```bash
   # Single decode
   echo "base64_string" | base64 -d > image.jpg
   
   # Double decode
   echo "base64_string" | base64 -d | base64 -d > image.jpg
   ```

### Step 6: Extract Flag Parts from Metadata
1. **Install ExifTool:**
   ```bash
   sudo apt-get install exiftool
   ```

2. **Extract Metadata:**
   ```bash
   exiftool image.jpg
   ```

3. **Look for Flag Parts:**
   - Each image contains a flag part in different metadata fields
   - Flag parts are Base64 encoded as "PartXX:chunkedflag"
   - Decode the Base64 to get the actual flag part

### Step 7: Reconstruct the Flag
1. **Collect All Flag Parts:**
   - Part01: N3v3r
   - Part02: _Tru5T
   - Part03: _4_Fr33_
   - Part04: W1F1
   - Part05: _1n
   - Part06: _3L
   - Part07: _K4BB4R14!!

2. **Assemble the Flag:**
   - Combine parts in order: Part01 + Part02 + Part03 + Part04 + Part05 + Part06 + Part07
   - Add the flag format: `SecurinetsENIT{...}`

---

## Approach 2: tshark Command Line Walkthrough

### Step 1: Analyze the PCAP Structure
```bash
# Get basic statistics
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -q -z io,phs

# Count packets by protocol
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -q -z ptype,tree
```

### Step 2: Find HTTP Traffic
```bash
# List all HTTP requests
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http" -T fields -e frame.number -e ip.src -e ip.dst -e http.request.method -e http.request.uri

# Find HTTP POST requests (likely to contain images)
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http.request.method == POST" -T fields -e frame.number -e ip.src -e ip.dst -e http.request.uri
```

### Step 3: Extract Base64 Data
```bash
# Find all large HTTP packets containing image data
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http and frame.len > 10000" -T fields -e frame.number -e frame.len

# Extract HTTP response bodies containing Base64
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http" -T fields -e http.file_data | grep -E "^[A-Za-z0-9+/=]+$" | head -20

# Count total image packets
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http and frame.len > 10000" -T fields -e frame.number | wc -l
```

### Step 3.5: Image Packet Analysis
The PCAP contains 157 large HTTP packets with image data:

```bash
# List all large packets (should show 157 packets)
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http and frame.len > 10000" -T fields -e frame.number -e frame.len

# Show packet size distribution
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http and frame.len > 10000" -T fields -e frame.len | sort -n | uniq -c

# Find DuckDuckGo search packet
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "frame.number == 69" -T fields -e frame.number -e ip.src -e ip.dst -e http.request.uri
```

### Step 4: Automated Solution
The easiest approach is to use the provided solver:

```bash
# Run the automated solver
python3 solution_files/solver.py challenge_files/el_kabbaria_hotel_capture.pcap
```

This will:
- Extract all images from the PCAP automatically
- Decode both single and double Base64 encoded images
- Extract flag parts from metadata
- Reconstruct the complete flag
- Show the DuckDuckGo search query in packet #69
- Display the next challenge password

### Step 4.5: Manual Image Extraction
If you want to extract images manually:

```bash
# Create output directory
mkdir -p extracted_images

# Extract all large HTTP packets and look for Base64 data
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap \
       -Y "http and frame.len > 10000" \
       -T fields -e http.file_data | \
grep -E "^[A-Za-z0-9+/=]+$" | \
while read -r line; do
    # Try to decode as image
    echo "$line" | base64 -d > "extracted_images/temp_$(date +%s).jpg" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Extracted potential image"
    fi
done
```

### Step 5: Advanced tshark Extraction
```bash
# Extract all HTTP POST data
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http.request.method == POST" -T fields -e http.file_data > post_data.txt

# Extract all HTTP response bodies
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http.response" -T fields -e http.file_data > response_data.txt

# Look for specific patterns
grep -E "^[A-Za-z0-9+/=]{100,}$" post_data.txt | head -10
grep -E "^[A-Za-z0-9+/=]{100,}$" response_data.txt | head -10
```

### Step 6: Automated Flag Extraction
```bash
# Create a comprehensive extraction script
cat > solve_challenge.sh << 'EOF'
#!/bin/bash

echo "=== El Kabbaria Hotel Challenge - tshark Solution ==="
echo "Extracting images and flag parts..."

# Create output directory
mkdir -p extracted_images

# Extract all potential Base64 data
tshark -r challenge_files/el_kabbaria_hotel_capture.pcap -Y "http" -T fields -e http.file_data | \
grep -E "^[A-Za-z0-9+/=]+$" | \
while read -r line; do
    # Check for image signatures
    if echo "$line" | grep -q "^/9j/4AAQSkZJRgABA\|^UklGR\|^iVBORw0KGgo"; then
        echo "Found image data, attempting decode..."
        echo "$line" | base64 -d > "extracted_images/temp_$(date +%s).jpg" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Successfully decoded image"
        fi
    fi
done

# Extract metadata from all images
echo "Extracting flag parts from metadata..."
for img in extracted_images/*.jpg; do
    if [ -f "$img" ]; then
        echo "Analyzing $img..."
        exiftool "$img" | grep -E "(Software|Subject|Artist|ImageDescription|UserComment|Copyright|LensModel)" | \
        while read -r line; do
            if echo "$line" | grep -q "Part[0-9][0-9]:"; then
                echo "Found flag part: $line"
                # Extract and decode Base64
                flag_part=$(echo "$line" | sed 's/.*: *//' | base64 -d 2>/dev/null)
                if [ $? -eq 0 ]; then
                    echo "Decoded: $flag_part"
                fi
            fi
        done
    fi
done
EOF

chmod +x solve_challenge.sh
./solve_challenge.sh
```

---

## Detailed Technical Analysis

### Network Traffic Analysis

The PCAP contains realistic network traffic simulating a hotel Wi-Fi environment:

1. **Protocol Distribution:**
   - **HTTP:** 637 packets (web browsing and file uploads)
   - **TCP:** 931 packets (reliable data transmission)
   - **ARP:** 40 packets (local network discovery)
   - **DNS:** Domain name resolution
   - **ICMP:** Network diagnostics

2. **Realistic Web Activity:**
   - 80+ different websites visited
   - 500+ realistic interactions
   - Tunisian context (local news, Arabic content)
   - Mixed language content (Arabic, French, English)

3. **Image Upload Patterns:**
   - **157 large HTTP packets** (11KB-58KB each) contain image data
   - Images uploaded via HTTP POST requests
   - Base64 encoding (single and double)
   - Chunked across multiple consecutive packets
   - **8.6MB total PCAP size** with rich realistic content

### Image Encoding Details

1. **Single Base64 Encoding (4 images):**
   - Raw image data → Base64 → HTTP body
   - Easier to extract and decode
   - Look for standard image signatures

2. **Double Base64 Encoding (3 images):**
   - Raw image data → Base64 → Base64 → HTTP body
   - Requires two decoding steps
   - More challenging to identify

### Metadata Flag Storage

Each image stores a flag part in different metadata fields:

| Image | Metadata Field | Flag Part | Base64 Encoded |
|-------|----------------|-----------|----------------|
| zodiac_slogan_cipher.jpg | Software | Part01:N3v3r | Yes |
| zodiac_symbol.webp | Subject | Part02:_Tru5T | Yes |
| zodiac_victim_drawing.jpg | Artist | Part03:_4_Fr33_ | Yes |
| eliminated_detective.jpg | ImageDescription | Part04:W1F1 | Yes |
| target_politician.jpg | UserComment | Part05:_1n | Yes |
| encrypted_notes.jpg | Copyright | Part06:_3L | Yes |
| encrypted_communication_notes.jpg | LensModel | Part07:_K4BB4R14!! | Yes |

### Special Packet Analysis

**Packet 69 (Frame 69 in Wireshark):**
- Contains DuckDuckGo search query
- Query: `Y0u_M1GHT_W4NN4_K33P_TH1S_T1CK3T_4R0UND_EL_C0NTR0LEUR_B3SH_Y4TLA3_L3L_M3TRO`
- This is the password for the next challenge

---

## Troubleshooting Common Issues

### Issue 1: Base64 Decoding Errors
**Problem:** `base64: invalid input`
**Solution:** 
- Ensure you're extracting only the Base64 payload
- Remove HTTP headers and whitespace
- Check for double encoding

### Issue 2: Image File Corruption
**Problem:** Images won't open or are corrupted
**Solution:**
- Verify Base64 data integrity
- Try different decoding approaches
- Check for missing chunks

### Issue 3: Missing Flag Parts
**Problem:** Can't find all 7 flag parts
**Solution:**
- Check all metadata fields, not just comments
- Use `exiftool -all` to see all metadata
- Verify Base64 decoding of metadata values

### Issue 4: Wrong Flag Order
**Problem:** Flag parts in wrong order
**Solution:**
- Sort by Part number (Part01, Part02, etc.)
- Don't rely on file names for order
- Check the metadata field values

---

## Advanced Techniques

### Using Python for Automated Extraction
```python
import base64
import subprocess
import re

def extract_images_from_pcap(pcap_file):
    # Use tshark to extract HTTP data
    cmd = f"tshark -r {pcap_file} -Y 'http' -T fields -e http.file_data"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Find Base64 image data
    image_patterns = [
        r'^/9j/4AAQSkZJRgABA',  # JPEG
        r'^UklGR',               # WebP
        r'^iVBORw0KGgo'          # PNG
    ]
    
    images = []
    for line in result.stdout.split('\n'):
        if any(re.match(pattern, line) for pattern in image_patterns):
            try:
                # Try single decode first
                decoded = base64.b64decode(line)
                if decoded.startswith(b'\xff\xd8\xff'):  # JPEG signature
                    images.append(('single', decoded))
                else:
                    # Try double decode
                    double_decoded = base64.b64decode(decoded)
                    if double_decoded.startswith(b'\xff\xd8\xff'):
                        images.append(('double', double_decoded))
            except:
                continue
    
    return images

def extract_flag_from_metadata(image_data):
    # Save image temporarily
    with open('temp_image.jpg', 'wb') as f:
        f.write(image_data)
    
    # Extract metadata 

    result = subprocess.run(['exiftool', 'temp_image.jpg'], 
                          capture_output=True, text=True)
    
    # Look for flag parts
    flag_fields = ['Software', 'Subject', 'Artist', 'ImageDescription', 
                   'UserComment', 'Copyright', 'LensModel']
    
    for line in result.stdout.split('\n'):
        for field in flag_fields:
            if field in line and 'Part' in line:
                # Extract and decode Base64
                match = re.search(r'Part\d+:[A-Za-z0-9+/=]+', line)
                if match:
                    return match.group(0)
    
    return None
```

### Using Wireshark Lua Scripts
```lua
-- Lua script for Wireshark to extract Base64 data
local function extract_base64_data()
    local tap = Listener.new("http", "http")
    
    function tap.packet(pinfo, tvb)
        local http_data = tvb:range(0, tvb:len()):string()
        
        -- Look for Base64 image data
        if string.match(http_data, "^[A-Za-z0-9+/=]+$") and 
           (string.match(http_data, "^/9j/4AAQSkZJRgABA") or
            string.match(http_data, "^UklGR") or
            string.match(http_data, "^iVBORw0KGgo")) then
            
            print("Found Base64 image data in packet " .. pinfo.number)
            -- Save to file
            local file = io.open("extracted_data_" .. pinfo.number .. ".txt", "w")
            file:write(http_data)
            file:close()
        end
    end
end
```

---

## Final Solution Verification

After extracting all images and flag parts, verify your solution:

1. **Check Flag Parts:**
   - Part1: N3v3r
   - Part2: _Tru5T
   - Part3: _4_Fr33_
   - Part4: W1F1
   - Part5: _1n
   - Part6: _3L
   - Part7: _K4BB4R14!!

2. **Assemble Flag:**
   - Combine: N3v3r_Tru5T_4_Fr33_W1F1_1n_3L_K4BB4R14!!
   - Add format: SecurinetsENIT{N3v3r_Tru5T_4_Fr33_W1F1_1n_3L_K4BB4R14!!}

3. **Verify Special Packet:**
   - Check packet 69 for DuckDuckGo search
   - Password: Y0u_M1GHT_W4NN4_K33P_TH1S_T1CK3T_4R0UND_EL_C0NTR0LEUR_B3SH_Y4TLA3_L3L_M3TRO

4. **Automated Verification:**
   ```bash
   # Run the solver to verify everything works
   python3 solution_files/solver.py challenge_files/el_kabbaria_hotel_capture.pcap
   ```
   This should output:
   - DuckDuckGo search found in packet #69
   - All 7 flag parts found
   - Complete flag reconstruction
   - Next challenge password

---

## Conclusion

This challenge tests multiple forensics skills:
- Network traffic analysis
- Protocol understanding
- Base64 encoding/decoding
- Metadata extraction
- Image forensics
- Pattern recognition

The solution requires both technical knowledge and systematic analysis to successfully extract and reconstruct the flag from the network capture.

**Final Flag:** `SecurinetsENIT{N3v3r_Tru5T_4_Fr33_W1F1_1n_3L_K4BB4R14!!}`
