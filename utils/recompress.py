#!/usr/bin/env python

import zipfile
from pathlib import Path


this_dir = Path()
# Folder for hdt.zip files
target_dir = this_dir / 'srtm3'
# Folder with original data
zip_dir = this_dir / 'zip'
# temp folder
temp_dir = this_dir / '.tmp'

if not target_dir.exists():
    target_dir.mkdir()
if not temp_dir.exists():
    temp_dir.mkdir()

p = zip_dir.glob('*.zip')
files = [x for x in p if x.is_file()]

for file in files:
    with zipfile.ZipFile(file, mode="r") as archive:
        for filename in archive.namelist():
            if filename.endswith(".hgt"):
                temp_filename = Path(filename).name.upper()
                temp_fullname = temp_dir / temp_filename
                temp_fullname = temp_fullname.with_suffix('.hgt')
                open(temp_fullname, 'wb').write(archive.open(filename).read())

                zip_file_dir = target_dir / temp_filename[0:3].upper()
                if not zip_file_dir.exists():
                    zip_file_dir.mkdir()
                full_zip_filename = zip_file_dir / temp_filename
                with zipfile.ZipFile(full_zip_filename.with_suffix('.zip'), 'w', zipfile.ZIP_LZMA, compresslevel=9) as zipf:
                    zipf.write(temp_fullname, arcname=temp_fullname.name)
                temp_fullname.unlink()
                print(filename, temp_fullname, full_zip_filename)
