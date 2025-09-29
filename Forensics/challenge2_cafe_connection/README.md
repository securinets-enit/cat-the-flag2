# Challenge 2: The Café Connection

## 🎯 Challenge Overview
- **Difficulty**: Easy
- **Category**: Network Forensics
- **Points**: 100
- **Flag Format**: `SecurinetsENIT{...}`

## 📖 Story
Back at HQ, your team traces the Zodiac to a bustling café near Bab El Bhar. Our field agent mirrored a snippet of the café Wi‑Fi traffic while the suspect was on the network. The Zodiac likes to hide in plain HTTP sight and make jokes at our expense.

Your handler slid a password across the desk: the one you pulled from the pastebin in Challenge 1. Inside the zip is the packet capture.

Good hunting, agent. The coffee’s hot, the packets are hotter. 

> “Listen to the café, agent. Even coffee grinders whisper…” — Captain Gorjeni

## 🧩 Objective
- Open the provided zip with the password from the pastebin (`P4cK3t_N1nj4`)
- Inspect the captured HTTP traffic
- Recover the hidden message the Zodiac smuggled through the café proxy
- Submit the flag

## 🛠️ Tools
- Wireshark or tshark
- Any text editor / terminal

## 🚀 Getting Started
1. Unzip: `unzip -P P4cK3t_N1nj4 cafe_connection.zip`
2. Open `cafe_connection.pcap` in Wireshark
3. Filter on HTTP responses: `http`
4. Inspect the headers of server responses from `172.16.10.20` (port 80)
5. Notice a pattern across responses that can spell a message

## 💡 Hints
- “Sizes can speak when headers are loud.”
- Look at a header that tells how big a response is.
- Sort responses by time and read that header across requests.

## ✅ Submission
- Flag: `SecurinetsENIT{4r3_Y0u_R34LLY_4_N1Nj4??}`