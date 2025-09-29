# Challenge 8: DAMAZE — The Infinite Archive (Organizer Summary)

## Overview
- Category: Digital Forensics
- Difficulty: Medium–Hard (automation encouraged)
- Points: 400
- Starting file: `media_files/damaze_start.zip`
- Final flag: `SecurinetsENIT{F33L1NG_W4RM3D_UP_Y3T?}`

## Concept
A deep archive maze with branching paths and mixed formats. Players automate extraction, follow continue branches, and decode periodic passwords. The continue folder name contains the token used as the password when needed.

## Structure (as generated)
- Depth: 320 layers (configurable in `build_maze.py`)
- Branching: 1 continue branch (`k33p_g01ng_<token>`) + (BRANCH_FANOUT-1) decoy branches (`wr0ng_w4y_*`)
- Formats: rotation of `.zip`, `.7z`, `.tar.gz`
- Passworded layers: at interval (default every 37). `note.txt` and the continue folder name carry the token.
- Breadcrumbs: `progress.txt` every 25 layers shows `depth: X/320`.
- OS noise: `__MACOSX/`, `.DS_Store`, `Thumbs.db`.
- Terminal: `READ_ME.txt` contains the flag and a congrats line.

## Expected Player Approach
1. Extract current archive to a temp folder.
2. Find the inner archive by prioritizing the continue folder `k33p_g01ng_*`.
3. If extraction errors with “Wrong password”, list the archive (`7z l`) and parse the continue folder name to get `<token>`; retry with `-p<token>`.
4. Repeat until a `READ_ME.txt` is found; print flag and stop.

## Organizer Files
- `solution_files/build_maze.py` — generator used to produce `damaze_start.zip`.
- `solution_files/solver.py` — reference solver (lists contents to infer password tokens, retries with `-p<token>`, handles `.tar.gz`).

## Build/Regenerate
```bash
python3 solution_files/build_maze.py
# Output: Forensics/challenge8_damaze/media_files/damaze_start.zip
```

## Verify
```bash
python3 solution_files/solver.py --input media_files/damaze_start.zip
# Should eventually print READ_ME.txt containing the flag.
```

## Notes
- We avoid filesystem path-length issues by nesting archives rather than deep directory paths.
- Password hints are embedded both in `note.txt` and the continue folder name to allow robust solver inference.
- Decoys are lightweight to keep archive sizes reasonable.
