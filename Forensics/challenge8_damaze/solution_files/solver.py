#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ARCH_EXTS = ['.zip', '.7z', '.tar.gz']


def find_note_password(root: Path):
    for p in root.rglob('note.txt'):
        m = re.search(r'password hint:\s*(\S+)', p.read_text(errors='ignore'))
        if m:
            return m.group(1)
    # also infer from continue-folder name if present
    for d in root.glob('k33p_g01ng_*'):
        m = re.search(r'k33p_g01ng_([A-Za-z0-9]+)$', d.name)
        if m:
            return m.group(1)
    return None


def find_inner_archive(root: Path):
    keep = sorted(root.glob('k33p_g01ng_*'))
    search_dirs = keep if keep else [root]
    for base in search_dirs:
        for ext in ARCH_EXTS:
            hits = list(base.rglob(f'*{ext}'))
            if hits:
                return hits[0]
    for ext in ARCH_EXTS:
        hits = list(root.rglob(f'*{ext}'))
        if hits:
            return hits[0]
    return None


def extract(archive: Path, outdir: Path, password: str | None):
    outdir.mkdir(parents=True, exist_ok=True)
    name = archive.name
    if name.endswith('.tar.gz'):
        subprocess.run(['tar', '-xzf', str(archive), '-C', str(outdir)], check=True)
    elif name.endswith('.zip') or name.endswith('.7z'):
        cmd = ['7z', 'x', '-y', str(archive), f'-o{outdir}']
        if password:
            cmd.insert(3, '-p' + password)
        subprocess.run(cmd, check=True)
    else:
        raise SystemExit('Unknown format: ' + name)


def infer_pwd_from_listing(archive: Path) -> str | None:
    """For 7z/zip, list contents and try to extract password token from
    the continue folder name k33p_g01ng_<token>."""
    name = archive.name
    if name.endswith('.tar.gz'):
        # tar.gz not passworded
        return None
    try:
        # -ba: bare output for easier parsing
        out = subprocess.check_output(['7z', 'l', '-ba', str(archive)], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return None
    # Look for paths like k33p_g01ng_<token>/
    m = re.search(r'k33p_g01ng_([A-Za-z0-9]+)\b', out)
    if m:
        return m.group(1)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    args = ap.parse_args()

    cur = Path(args.input).resolve()
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        for step in range(1, 2000):
            out = work / f'layer_{step:04d}'
            out.mkdir()
            # Prefer inferring password from the archive listing itself
            pwd = infer_pwd_from_listing(cur)
            try:
                extract(cur, out, pwd)
            except subprocess.CalledProcessError:
                # fallback: try without password
                shutil.rmtree(out)
                out.mkdir()
                extract(cur, out, None)
            # check for note hints post-extraction; if mismatch, re-extract
            hint = find_note_password(out)
            if hint:
                # re-extract with hinted password to be safe
                shutil.rmtree(out)
                out.mkdir()
                extract(cur, out, hint)
            if pwd:
                pass
            # check for flag
            for f in out.rglob('READ_ME.txt'):
                txt = f.read_text(errors='ignore')
                print(txt.strip())
                return
            nxt = find_inner_archive(out)
            if not nxt:
                raise SystemExit('No inner archive found; stuck at step %d' % step)
            cur = nxt


if __name__ == '__main__':
    main()


