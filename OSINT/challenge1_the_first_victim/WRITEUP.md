# Challenge 1: The First Victim - Writeup

## Solution Walkthrough

### Step 1: Social Media Investigation
Search for Amira El Youssfi on LinkedIn and Twitter to gather information about the victim.

**LinkedIn Investigation:**
- Visit https://www.linkedin.com/in/amira-el-youssfi-801121384/
- Review her professional profile and recent posts
- Note her role as Senior Software Engineer in cybersecurity

**Twitter Investigation:**
- Visit https://x.com/AYoussfi1122
- Review her recent posts and activity
- Look for any comments or replies

### Step 2: Flag Discovery
The flag is hidden across multiple comments on Amira's Twitter posts. Each letter of the flag is base64 encoded and posted as individual comments.

**Flag Discovery Process:**
1. Investigate Amira's Twitter account https://x.com/AYoussfi1122
2. Look through her recent posts and examine all comments
3. Find base64 encoded letters in various comments
4. Decode each base64 string to reveal individual letters
5. Reconstruct the complete flag: `SecurinetsENIT{N3V3R_GO1NG_T0_0UTSM4RT_4_M4N_WH0_TH1NKS_THR1CE}`

**Base64 Decoding Example:**
- Each letter of the flag is individually base64 encoded
- For example: 'S' becomes 'Uw==', 'e' becomes 'ZQ==', etc.
- Players must find all encoded letters and decode them to reconstruct the flag

### Step 3: Analysis
The flag reveals a cryptic message about the killer's mindset: "NEVER GOING TO OUTSMART A MAN WHO THINKS THRICE"

This suggests the killer is confident and methodical, thinking multiple steps ahead. The message was left on September 25, 2025, the day of Amira's murder.

## Flag
`SecurinetsENIT{N3V3R_GO1NG_T0_0UTSM4RT_4_M4N_WH0_TH1NKS_THR1CE}`


## Key Learning Points
1. **Social Media Investigation**: Always check all platforms for hidden clues
2. **Comment Analysis**: Pay attention to comments and replies, not just posts
3. **Base64 Decoding**: Learn to identify and decode base64 encoded content
4. **Pattern Recognition**: Look for unusual or suspicious content across multiple posts
5. **Data Reconstruction**: Piece together fragmented information from multiple sources

## Tools Used
- LinkedIn search and profile analysis
- Twitter account investigation
- Comment and reply analysis
- Base64 decoding tools

