from lib import GeoPoint


def test_geo_point():
    p1 = GeoPoint(56.86358, 60.62379, name='Point1', elevation=765)
    assert p1.longitude == 60.62379
    assert p1.latitude == 56.86358
    assert p1.elevation == 765
    assert p1.rlongitude == 1.0580847405376133
    assert p1.rlatitude == 0.9924566954711972
    assert p1.name == 'Point1'
    assert p1.x == 1708572.6529589149
    assert p1.y == 3035173.9704191233
    assert p1.z == 5335541.431375747
    p2 = GeoPoint(56.86358, 60.62379, name='Point1')
    assert p2.elevation == 275
    p3 = GeoPoint(44.332845, 47.673761, name='Point1')
    assert p3.elevation == -29
    p4 = GeoPoint(37.514828, 49.990733, name='Point1')
    assert p4.elevation == -29
    p5 = GeoPoint(43.350183, 42.451874, name='Point1')
    assert p5.elevation == 5519
    p6 = GeoPoint(0, 0, name='00')
    assert p6.elevation is None
    assert p6.x == 6371009
    assert p6.y == 0
    assert p6.z == 0


def test_geo_diatsnce():
    p1 = GeoPoint(90, 0, name='N')
    p2 = GeoPoint(-90, 0, name='S')
    assert p1.distance_to(p2) == 12744717.0
    assert p1.arc_distance_to(p2) == 20015115.070354454
    p3 = GeoPoint(0, 0, name='G')
    p4 = GeoPoint(0, 180, name='g')
    assert p3.distance_to(p4) == 12742018
    assert p3.arc_distance_to(p4) == 20015115.070354454
    p5 = GeoPoint(58, 125, name='Y')
    p6 = GeoPoint(36, -9, name='S')
    assert p5.distance_to(p6) == 8055902.777931563
    assert p5.arc_distance_to(p6) == 8720408.57008249
    p7 = GeoPoint(43.350183, 42.451874, name='Elbrus')
    p8 = GeoPoint(43.350183, 42.451874, name='Elbrus sea level', elevation=0)
    assert p7.distance_to(p8) == 5518.999999999588
    assert p7.arc_distance_to(p8) == 0.0


def test_geo_azimuth():
    p1 = GeoPoint(54.9132538, 34.3426619)
    p2 = GeoPoint(54.9132538, 35.3426619)
    assert p1.azimuth(p2) == 89.5908552147599
    assert p2.azimuth(p1) == 270.4091447852401
    p3 = GeoPoint(0, 0)
    p4 = GeoPoint(0, 20)
    assert p3.azimuth(p4) == 90
    assert p4.azimuth(p3) == 270
    p5 = GeoPoint(54.9132538, 34.3426619)
    p6 = GeoPoint(55.9132538, 34.3426619)
    assert p5.azimuth(p6) == 0.0
    assert p6.azimuth(p5) == 180


def test_geo_nextpoint():
    p1 = GeoPoint(54.9132538, 34.3426619)
    p2 = p1.nextpoint(azimuth=90, distance=500)
    assert (p2.latitude, p2.longitude) == (54.913253548816705, 34.350484580324036)
    assert int(p1.distance_to(p2)) == 500
    p3 = GeoPoint(0, 0, name='N')
    p4 = p3.nextpoint(azimuth=-90, distance=20015115.070354454)
    assert (p4.latitude, p4.longitude) == (4.296495291499103e-31, -180)
    p5 = GeoPoint(0, 0, name='N')
    p6 = p5.nextpoint(azimuth=90, distance=20015115.070354454 / 2)
    assert (p6.latitude, p6.longitude) == (3.508354649267438e-15, 90)
