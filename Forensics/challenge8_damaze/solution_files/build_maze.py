#!/usr/bin/env python3
"""
Builds the DAMAZE nested-archives challenge with branching paths, mixed formats,
passworded layers, and decoys. Produces media_files/damaze_start.zip.

Requirements:
  - python3, 7z (p7zip-full), zip, tar/gzip
"""

import os
import random
import shutil
import string
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'media_files'
BUILD = ROOT / 'build_tmp'

FINAL_FLAG = 'SecurinetsENIT{F33L1NG_W4RM3D_UP_Y3T?}'

DEPTH = 320
BRANCH_FANOUT = 3
PASSWORD_INTERVAL = 37
NOTE_INTERVAL = 25

FORMATS = ['zip', '7z', 'targz']


def rand_name(n=10):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(n))


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def enc_leet(s: str) -> str:
    table = str.maketrans({'a':'4','e':'3','i':'1','o':'0','t':'7','s':'5'})
    return s.translate(table)


def pack_folder(src: Path, dst_archive: Path, fmt: str, password: str | None = None):
    dst_archive.parent.mkdir(parents=True, exist_ok=True)
    if dst_archive.exists():
        dst_archive.unlink()
    if fmt == 'zip':
        if password:
            subprocess.run(['7z','a','-p'+password,'-y',str(dst_archive),'.'], cwd=src, check=True)
        else:
            subprocess.run(['7z','a','-y',str(dst_archive),'.'], cwd=src, check=True)
    elif fmt == '7z':
        args = ['7z','a','-y']
        if password:
            args.append('-p'+password)
        args += [str(dst_archive), '.']
        subprocess.run(args, cwd=src, check=True)
    elif fmt == 'targz':
        # tar.gz cannot be passworded simply; use as plain
        tmp_tar = dst_archive.with_suffix('.tar')
        if tmp_tar.exists(): tmp_tar.unlink()
        subprocess.run(['tar','-cf',str(tmp_tar),'.'], cwd=src, check=True)
        subprocess.run(['gzip','-f',str(tmp_tar)], cwd=dst_archive.parent, check=True)
        tmp_tar_gz = tmp_tar.with_suffix('.tar.gz')
        tmp_tar_gz.rename(dst_archive)
    else:
        raise ValueError('unknown fmt')


def main():
    random.seed(1337)
    if BUILD.exists(): shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)

    # Terminal folder with flag (packed as child archive)
    terminal = BUILD / 'terminal'
    terminal.mkdir(exist_ok=True)
    write_text(terminal / 'READ_ME.txt', 'Congrats!\n\n' + FINAL_FLAG + '\n')
    child_archive = BUILD / 'layer_0000.zip'
    pack_folder(terminal, child_archive, 'zip', password=None)

    # Build main path upwards using archive-in-archive to avoid long paths
    published_entry = child_archive

    for depth in reversed(range(1, DEPTH+1)):
        layer_dir = BUILD / f'layer_{depth:04d}_dir'
        if layer_dir.exists(): shutil.rmtree(layer_dir)
        layer_dir.mkdir()

        # OS noise
        if depth % 11 == 0:
            (layer_dir / '__MACOSX').mkdir(exist_ok=True)
            write_text(layer_dir / '__MACOSX' / '.DS_Store', '0')
        if depth % 17 == 0:
            write_text(layer_dir / 'Thumbs.db', '0')

        # Format
        fmt = FORMATS[depth % len(FORMATS)]

        # Password usage
        password = None
        if depth % PASSWORD_INTERVAL == 0:
            password = enc_leet(rand_name(6))
            write_text(layer_dir / 'note.txt', f"password hint: {password}\n")

        # Progress note
        if depth % NOTE_INTERVAL == 0:
            write_text(layer_dir / 'progress.txt', f"depth: {depth}/{DEPTH}\n")

        # Continue branch containing the previous archive
        # Include password token in continue folder name when present so solvers can infer it from filenames
        cont_token = rand_name(4)
        if password:
            cont_token = password
        cont_dir = layer_dir / enc_leet('keep_going_' + cont_token)
        cont_dir.mkdir()
        shutil.copy2(published_entry, cont_dir / published_entry.name)

        # Decoy branches
        for b in range(BRANCH_FANOUT - 1):
            decoy = layer_dir / enc_leet('wrong_way_' + rand_name(4))
            decoy.mkdir()
            write_text(decoy / 'readme.txt', 'Nothing here. Turn back.\n')
            (decoy / 'empty').mkdir()

        # Pack this layer directory into next archive
        out_name = f"layer_{depth:04d}.{ 'zip' if fmt=='zip' else ('7z' if fmt=='7z' else 'tar.gz') }"
        out_path = BUILD / out_name
        pack_folder(layer_dir, out_path, fmt, password=password)
        published_entry = out_path

    # Final start archive for players
    start_zip = MEDIA / 'damaze_start.zip'
    if start_zip.exists(): start_zip.unlink()
    shutil.copy2(published_entry, start_zip)

    print('[+] Wrote', start_zip)


if __name__ == '__main__':
    main()


