from lib import GeoPoint, RadioPath


def test_radio_path1():
    p1 = GeoPoint(1.594837, 31.158936, name='Point1')
    p2 = GeoPoint(1.870223, 30.878149, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=20, stoppoint=p2, stopheight=20, frequency=17)
    assert radiopath1.startpoint == p1
    assert radiopath1.stoppoint == p2
    assert radiopath1.frequency == 17
    assert int(radiopath1.length) == 43726
    assert radiopath1.startpoint.elevation == 660
    assert radiopath1.stoppoint.elevation == 624
    assert radiopath1.arc_height(0) == 0
    assert radiopath1.arc_height(radiopath1.length) == 0
    assert int(radiopath1.arc_height(radiopath1.length / 2)) == 37
    assert int(radiopath1.arc_height(radiopath1.length / 4)) == 28
    assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
    assert radiopath1.line_equation_b == 680
    assert radiopath1.line_equation_k == -0.0008233033589831102
    assert int(radiopath1.los_height(0)) == 680
    assert int(radiopath1.los_height(radiopath1.length)) == 644
    assert int(radiopath1.los_height(radiopath1.length / 2)) == 662
    assert radiopath1.visibility_in_fresnel_zone(1) is False
    assert radiopath1.line_of_sight() is True
    assert radiopath1.visibility_in_fresnel_zone(2) is False
    assert len(radiopath1.relief) == 403


def test_radio_path2():
    p1 = GeoPoint(1.594837, 31.158936, name='Point1')
    p2 = GeoPoint(1.870223, 30.878149, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=40, stoppoint=p2, stopheight=40, frequency=13)
    assert radiopath1.startpoint == p1
    assert radiopath1.stoppoint == p2
    assert radiopath1.frequency == 13
    assert int(radiopath1.length) == 43726
    assert radiopath1.startpoint.elevation == 660
    assert radiopath1.stoppoint.elevation == 624
    assert radiopath1.arc_height(0) == 0
    assert radiopath1.arc_height(radiopath1.length) == 0
    assert int(radiopath1.arc_height(radiopath1.length / 2)) == 37
    assert int(radiopath1.arc_height(radiopath1.length / 4)) == 28
    assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
    assert radiopath1.line_equation_b == 700
    assert radiopath1.line_equation_k == -0.0008233033589831102
    assert int(radiopath1.los_height(0)) == 700
    assert int(radiopath1.los_height(radiopath1.length)) == 664
    assert int(radiopath1.los_height(radiopath1.length / 2)) == 682
    assert radiopath1.line_of_sight() is True
    assert radiopath1.visibility_in_fresnel_zone(1) is True
    assert radiopath1.visibility_in_fresnel_zone(2) is True
    assert len(radiopath1.relief) == 403


def test_radio_path3():
    p1 = GeoPoint(1.594837, 31.158936, name='Point1')
    p2 = GeoPoint(1.870223, 30.878149, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=1, stoppoint=p2, stopheight=1, frequency=13)
    assert radiopath1.startpoint == p1
    assert radiopath1.stoppoint == p2
    assert radiopath1.frequency == 13
    assert int(radiopath1.length) == 43726
    assert radiopath1.startpoint.elevation == 660
    assert radiopath1.stoppoint.elevation == 624
    assert radiopath1.arc_height(0) == 0
    assert radiopath1.arc_height(radiopath1.length) == 0
    assert int(radiopath1.arc_height(radiopath1.length / 2)) == 37
    assert int(radiopath1.arc_height(radiopath1.length / 4)) == 28
    assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
    assert radiopath1.line_equation_b == 661
    assert radiopath1.line_equation_k == -0.0008233033589831102
    assert int(radiopath1.los_height(0)) == 661
    assert int(radiopath1.los_height(radiopath1.length)) == 625
    assert int(radiopath1.los_height(radiopath1.length / 2)) == 643
    assert radiopath1.line_of_sight() is False
    assert radiopath1.visibility_in_fresnel_zone(1) is False
    assert radiopath1.visibility_in_fresnel_zone(2) is False
    assert len(radiopath1.relief) == 403


def test_radio_path_chart_data():
    p1 = GeoPoint(1.594748, 31.158804, name='Point1')
    p2 = GeoPoint(1.595744, 31.160749, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=40, stoppoint=p2, stopheight=40, frequency=13)
    # print(radiopath1.get_chart_data())
    assert radiopath1.get_chart_data() == {
        'distance': [0, 100, 170, 210, 243.5269906724964],
        'relief': [660, 690, 641, 677, 677],
        'relief_arc': [660.0, 690.0011264065372, 641.0009809736314, 677.0005525552118, 677.0],
        'los_height': [700.0, 706.9807457288634, 711.8672677390679, 714.6595660306133, 717.0],
        'frenzel_zone_1_top': [700.0, 708.1447090872165, 712.9515870215793, 715.469851232417, 717.0],
        'frenzel_zone_1_bottom': [700.0, 705.8167823705104, 710.7829484565565, 713.8492808288096, 717.0],
        'frenzel_zone_2_top': [700.0, 708.6268384963516, 713.4007267743382, 715.8054823523944, 717.0],
        'frenzel_zone_2_bottom': [700.0, 705.3346529613752, 710.3338087037976, 713.5136497088322, 717.0]}
