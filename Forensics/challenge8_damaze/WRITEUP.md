# Challenge 8: DAMAZE — Writeup

## Summary
You’re given `damaze_start.zip`, which actually opens as a 7z archive. Every layer contains multiple branches; only one continues. Periodically, archives are passworded. The continue folder is named `k33p_g01ng_<token>`; that `<token>` is the password to use for that layer’s archive.

- Start: `damaze_start.zip`
- Goal: Extract until you find `READ_ME.txt` with the flag:
  - `SecurinetsENIT{F33L1NG_W4RM3D_UP_Y3T?}`

## Key Signals
- Continue folder: `k33p_g01ng_<token>` (leetspeak).
- Decoys: `wr0ng_w4y_*` with `readme.txt` only.
- Hints: `note.txt` with `password hint: <token>`, and `progress.txt` showing depth.
- Formats: zip/7z/tar.gz.

## Strategy
1. Iteratively extract the current archive into a temp folder.
2. If extraction fails with “Wrong password”, list the archive contents first:
   - `7z l -ba archive.7z` (or `.zip`) to see paths. Look for `k33p_g01ng_<token>`.
   - Retry extraction with `7z x -p<token> ...`.
3. From the extracted files, choose the inner archive under the `k33p_g01ng_*` path.
4. Repeat until `READ_ME.txt` is found; print and stop.

## Reference Skeleton (Python)
```python
import re, shutil, subprocess, tempfile
from pathlib import Path

EXTS = ['.zip','.7z','.tar.gz']

def list_token(archive: Path):
    if archive.suffixes[-2:] == ['.tar','.gz']:
        return None
    out = subprocess.check_output(['7z','l','-ba',str(archive)], text=True)
    m = re.search(r'k33p_g01ng_([A-Za-z0-9]+)\b', out)
    return m.group(1) if m else None

def extract(arc: Path, out: Path, pwd: str|None):
    out.mkdir(parents=True, exist_ok=True)
    n = ''.join(arc.suffixes)
    if n.endswith('.tar.gz'):
        subprocess.run(['tar','-xzf',str(arc),'-C',str(out)], check=True)
    else:
        cmd = ['7z','x','-y',str(arc),f'-o{out}']
        if pwd: cmd.insert(3,'-p'+pwd)
        subprocess.run(cmd, check=True)
```

## Tips
- If multiple archives are present, prioritize those under `k33p_g01ng_*`.
- `.tar.gz` layers are plain (no password) by design; use `tar -xzf`.
- Use a temp directory and clean up per-iteration to avoid disk bloat.

## Final
When you reach the terminal layer, open `READ_ME.txt`:
```
SecurinetsENIT{F33L1NG_W4RM3D_UP_Y3T?}
```
