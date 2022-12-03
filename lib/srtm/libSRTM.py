import math as m
from zipfile import ZipFile
from pathlib import Path

cache_dir = Path.cwd() / 'data' / 'cache'
srtm3_dir = Path.cwd() / 'data' / 'srtm3'


def file_name_for_point(latitude: float, longitude: float) -> str:
    """
    For the specified coordinates, returns the name of the SRTM3 file
    """
    north_south = 'N' if latitude >= 0 else 'S'
    east_west = 'E' if longitude >= 0 else 'W'
    file_name = '{0}{1}{2}{3}.hgt'.format(north_south, str(int(abs(m.floor(latitude)))).zfill(2),
                                          east_west, str(int(abs(m.floor(longitude)))).zfill(3))  # TODO: Разве тут нужны str(int?
    return file_name


def hgt_file(latitude: float, longitude: float) -> str:
    """
    For the specified coordinates, returns the name of the SRTM3 file.
    If this file is not in the cache folder, then we look for the packed file in the strm3 folder, unpack it and return the name.
    If no file exists for the given coordinates, then return None.
    """

    hgt_file_name = file_name_for_point(latitude, longitude)

    # Checking if the file is in the cache.
    cache_hgt_file_name = cache_dir / hgt_file_name
    if not cache_hgt_file_name.exists():
        # Checking if the zip file exists
        zip_hgt_file_name = srtm3_dir / hgt_file_name[0:3] / hgt_file_name
        zip_hgt_file_name = zip_hgt_file_name.with_suffix('.zip')
        # If no file exists for the given coordinates, then return None.
        if not zip_hgt_file_name.exists():
            return None
        # Else unpack and return filename
        else:
            with ZipFile(zip_hgt_file_name, mode='r') as archive:
                open(cache_hgt_file_name, 'wb').write(archive.open(hgt_file_name).read())
            return cache_hgt_file_name
    else:
        return cache_hgt_file_name


def get_elevation_point(latitude: float, longitude: float) -> int:
    """
    For the given coordinates, returns the height of the ground level above sea level (or None if there is no data)
    """
    srtm_file = hgt_file(latitude, longitude)
    if srtm_file is None:
        return None

    # For the northern hemisphere
    if latitude > 0:
        i = 1200 - int(round((abs(latitude) - abs(int(latitude))) * (1201 - 1), 0))
    # For the southern hemisphere
    else:
        i = int(round((abs(latitude) - abs(int(latitude))) * (1201 - 1), 0))

    # For the Eastern Hemisphere
    if longitude > 0:
        j = int(round((abs(longitude) - abs(int(longitude))) * (1201 - 1), 0))
    # For the Western Hemisphere
    else:
        j = 1200 - int(round((abs(longitude) - abs(int(longitude))) * (1201 - 1), 0))

    pos = (i * 1201) + j

    with open(srtm_file, "rb") as f:
        f.seek(pos * 2)
        val = int.from_bytes(f.read(2), byteorder="big", signed="True")
        if not val == -32768:
            return val
        else:
            return None
