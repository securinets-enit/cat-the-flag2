# Challenge 8: DAMAZE — The Infinite Archive

## 🎯 Overview
- **Category**: Digital Forensics
- **Difficulty**: Medium–Hard
- **Points**: 400
- **Flag**: `SecurinetsENIT{F33L1NG_W4RM3D_UP_Y3T?}`

## 🧩 Story
A drive image revealed a “final gift” from the Zodiac: a labyrinth of archives inside archives. Somewhere, one path leads to a message meant only for the patient.

## 🕹️ Goal
Extract through a pseudo-infinite maze of nested archives and recover the final flag from `READ_ME.txt`.

## 🔍 What to Expect
- Depth > 300 levels (automation recommended!)
- Branching layers: only one branch continues (`k33p_g01ng_*`)
- Decoy branches: `wr0ng_w4y_*`
- Mixed formats: `.zip`, `.7z`, `.tar.gz`
- Occasional passworded layers (password token embedded in the continue folder name)
- Breadcrumbs: `progress.txt` every N layers; password hint `note.txt` alongside continue folder
- OS artifacts: `__MACOSX/`, `.DS_Store`, `Thumbs.db`

## 🧭 Hints
- Prefer the folder named like `k33p_g01ng_<token>`; that `<token>` is the password when needed.
- If extraction fails with “Wrong password”, list the archive first; the listing reveals the `k33p_g01ng_<token>` name.
- Script your way through: manual extraction won’t scale.

## 📦 Files
- `media_files/damaze_start.zip` — Entry point archive

## 🛠️ Suggested Tooling
- `7z` (p7zip-full) for .zip/.7z
- `tar`/`gzip` for .tar.gz
- Python or shell scripting

## ✅ Success Criteria
- Reach the terminal layer and read `READ_ME.txt` with the final flag.

Good luck. The maze waits.
