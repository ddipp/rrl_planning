from lib.srtm import srtm


def test_file_name_for_point():
    assert srtm.file_name_for_point(56.86358, 60.62379) == 'N56E060.hgt'
    assert srtm.file_name_for_point(-56.86358, 60.62379) == 'S57E060.hgt'
    assert srtm.file_name_for_point(-56.86358, -60.62379) == 'S57W061.hgt'
    assert srtm.file_name_for_point(56.86358, -60.62379) == 'N56W061.hgt'


def test_get_elevation_point_NW():
    assert srtm.get_elevation_point(54.0, 41.0) == 157
    assert srtm.get_elevation_point(54.999999, 41.999999) == 158
    assert srtm.get_elevation_point(54.238421, 57.995044) == 605
    assert srtm.get_elevation_point(55.013505, 48.862878) == 202
    assert srtm.get_elevation_point(41.647916, 41.586085) == 0
    assert srtm.get_elevation_point(43.352347, 42.438384) == 5623
    assert srtm.get_elevation_point(43.281865, 41.713529) == 3225
    assert srtm.get_elevation_point(45.768722, 13.622579) == 0
    assert srtm.get_elevation_point(45.789651, 13.611512) == 269
    assert srtm.get_elevation_point(10.117540, 77.402218) == 1791
    assert srtm.get_elevation_point(2.238345, 118.071729) == 0
    assert srtm.get_elevation_point(0.508258, 117.654982) == 0
    assert srtm.get_elevation_point(0.567686, 117.513862) == 249
    assert srtm.get_elevation_point(67.579852, 10.776552) is None


def test_get_elevation_point_SW():
    assert srtm.get_elevation_point(-1.586075, 9.049527) == 0
    assert srtm.get_elevation_point(-1.406886, 10.512137) == 811
    assert srtm.get_elevation_point(-0.640121, 29.490220) == 912
    assert srtm.get_elevation_point(-0.482565, 29.227155) == 2440
    assert srtm.get_elevation_point(-1.571237, 121.413484) == 1989
    assert srtm.get_elevation_point(-1.577306, 121.416234) == 2231


def test_get_elevation_point_NE():
    assert srtm.get_elevation_point(52.966951, -6.465526) == 919
    assert srtm.get_elevation_point(52.959848, -6.336204) == 449
    assert srtm.get_elevation_point(52.968336, -6.183284) == 203
    assert srtm.get_elevation_point(55.841989, -41.038896) is None
    assert srtm.get_elevation_point(54.742000, -8.539797) == 178
    assert srtm.get_elevation_point(54.747656, -8.524792) == 176
    assert srtm.get_elevation_point(37.185165, -118.582057) == 3540


def test_get_elevation_point_SE():
    assert srtm.get_elevation_point(-4.003640, -79.058322) == 3132
    assert srtm.get_elevation_point(-3.991163, -79.092340) == 2005
    assert srtm.get_elevation_point(-3.957352, -79.023306) == 1553
    assert srtm.get_elevation_point(-3.991068, -79.015972) == 1507
    assert srtm.get_elevation_point(-46.431256, -73.741309) == 0
    assert srtm.get_elevation_point(-47.194529, -73.468960) == 3370
    assert srtm.get_elevation_point(-54.446149, -70.842950) == 1941


def test_get_all_points():
    points = ((-4.003640, -79.058322), (-3.991163, -79.092340), (-3.957352, -79.023306), (-3.991068, -79.015972))
    elevations = ((-4.003640, -79.058322, 3132), (-3.991163, -79.092340, 2005),
                  (-3.957352, -79.023306, 1553), (-3.991068, -79.015972, 1507))
    assert srtm.get_all_elevations_points(points) == elevations
