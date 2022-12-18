#!/usr/bin/env python

import zipfile
import bz2
from pathlib import Path


this_dir = Path()
# Folder for hdt.zip files
target_dir = this_dir / 'srtm3'
# Folder with original data
zip_dir = this_dir / 'zip'

if not target_dir.exists():
    target_dir.mkdir()

p = zip_dir.glob('*.zip')
files = [x for x in p if x.is_file()]

for file in files:
    with zipfile.ZipFile(file, mode="r") as archive:
        for filename in archive.namelist():
            if filename.endswith(".hgt"):
                hgt_filename = Path(filename).name.upper()

                zip_file_dir = target_dir / hgt_filename[0:3].upper()

                if not zip_file_dir.exists():
                    zip_file_dir.mkdir()

                bz2_file_dir = target_dir / hgt_filename[0:3].upper()
                full_zip_filename = zip_file_dir / hgt_filename
                full_zip_filename = full_zip_filename.with_suffix('.hgt.bz2')
                with bz2.open(full_zip_filename, "wb") as f:
                    print(f'write {full_zip_filename}')
                    f.write(archive.open(filename).read())
