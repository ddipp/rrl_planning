import bz2
import math as m
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
                                          east_west, str(int(abs(m.floor(longitude)))).zfill(3))
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
        bz2_hgt_file_name = srtm3_dir / hgt_file_name[0:3] / hgt_file_name
        bz2_hgt_file_name = bz2_hgt_file_name.with_suffix('.hgt.bz2')
        # If no file exists for the given coordinates, then return None.
        if not bz2_hgt_file_name.exists():
            return None
        # Else unpack and return filename
        else:
            with bz2.open(bz2_hgt_file_name, "rb") as f:
                open(cache_hgt_file_name, 'wb').write(f.read())
            return cache_hgt_file_name
    else:
        return cache_hgt_file_name


def get_elevation_point(latitude: float, longitude: float) -> int:
    """ For the given coordinates, returns the height of the ground level above sea level
        (or None if there is no data).
        To get the height of one point, we read only one byte from the file.
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


def get_all_elevations_points(points: tuple) -> tuple:
    """ For all points returns the height of the ground level above sea level
        (or None if there is no data).
        To get the height of one point, we read only one byte from the file.
    """
    elevations = []
    for point in points:
        elevations.append((*point, get_elevation_point(*point)))
    return tuple(elevations)

# def get_elevation_point(latitude: float, longitude: float) -> int:
#     SAMPLES = 1201
#     srtm_file = hgt_file(latitude, longitude)
#     if srtm_file is None:
#         return None
#     with open(srtm_file, 'rb') as hgt_data:
#         elevations = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES * SAMPLES).reshape((SAMPLES, SAMPLES))
#         # For the northern hemisphere
#         if latitude > 0:
#             i = 1200 - int(round((abs(latitude) - abs(int(latitude))) * (1201 - 1), 0))
#         # For the southern hemisphere
#         else:
#             i = int(round((abs(latitude) - abs(int(latitude))) * (1201 - 1), 0))

#         # For the Eastern Hemisphere
#         if longitude > 0:
#             j = int(round((abs(longitude) - abs(int(longitude))) * (1201 - 1), 0))
#         # For the Western Hemisphere
#         else:
#             j = 1200 - int(round((abs(longitude) - abs(int(longitude))) * (1201 - 1), 0))

#     return elevations[i, j].astype(int)
