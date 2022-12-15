from lib.srtm import srtm


def test_file_name_for_point():
    assert srtm.file_name_for_point(56.86358, 60.62379) == 'N56E060.hgt'
    assert srtm.file_name_for_point(-56.86358, 60.62379) == 'S57E060.hgt'
    assert srtm.file_name_for_point(-56.86358, -60.62379) == 'S57W061.hgt'
    assert srtm.file_name_for_point(56.86358, -60.62379) == 'N56W061.hgt'


def test_get_elevation_point_NW():
    assert srtm.get_elevation_point(2.274309, 31.358084) == 615
    assert srtm.get_elevation_point(2.115976, 31.087493) == 1753
    assert srtm.get_elevation_point(2.079952, 31.121195) == 1509
    assert srtm.get_elevation_point(1.151424, 30.447990) == 622
    assert srtm.get_elevation_point(1.018542, 30.656552) == 1202
    assert srtm.get_elevation_point(67.579852, 10.776552) is None  # Open ocean


def test_get_elevation_point_SW():
    assert srtm.get_elevation_point(-4.106989, 29.105975) == 767
    assert srtm.get_elevation_point(-4.139669, 29.411452) == 767
    assert srtm.get_elevation_point(-4.159174, 29.238954) == 1444
    assert srtm.get_elevation_point(-5.679582, 29.374339) == 767
    assert srtm.get_elevation_point(-5.592160, 29.314274) == 1481


def test_get_elevation_point_NE():
    assert srtm.get_elevation_point(52.966951, -6.465526) == 919
    assert srtm.get_elevation_point(52.959848, -6.336204) == 449
    assert srtm.get_elevation_point(52.968336, -6.183284) == 203
    assert srtm.get_elevation_point(55.841989, -41.038896) is None


def test_get_elevation_point_SE():
    assert srtm.get_elevation_point(-3.991163, -79.092340) == 2005
    assert srtm.get_elevation_point(-3.957352, -79.023306) == 1553
    assert srtm.get_elevation_point(-3.991068, -79.015972) == 1507


def test_get_all_points():
    points = ((-3.991163, -79.092340), (-3.957352, -79.023306), (-3.991068, -79.015972))
    elevations = ((-3.991163, -79.092340, 2005),
                  (-3.957352, -79.023306, 1553), (-3.991068, -79.015972, 1507))
    assert srtm.get_all_elevations_points(points) == elevations
