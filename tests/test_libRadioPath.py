from lib import GeoPoint, RadioPath


def test_radio_path1():
    p1 = GeoPoint(1.594837, 31.158936, name='Point1')
    p2 = GeoPoint(1.870223, 30.878149, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=20, stoppoint=p2, stopheight=20, frequency=17)
    radiopath1.set_radio_parameters(tx_power=18, receiver_sensitivity=-65, antenna_gain_a=38.1, antenna_gain_b=38.1)
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
    assert len(radiopath1.relief) == 107
    assert round(radiopath1.free_space_loss(), 2) == 149.86
    assert round(radiopath1.expected_signal_strength(), 2) == -55.66


def test_radio_path2():
    p1 = GeoPoint(1.594837, 31.158936, name='Point1')
    p2 = GeoPoint(1.870223, 30.878149, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=40, stoppoint=p2, stopheight=40, frequency=13)
    radiopath1.set_radio_parameters(tx_power=18, receiver_sensitivity=-65, antenna_gain_a=38.1, antenna_gain_b=38.1)
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
    assert len(radiopath1.relief) == 107
    assert round(radiopath1.free_space_loss(), 2) == 147.53
    assert round(radiopath1.expected_signal_strength(), 2) == -53.33


def test_radio_path3():
    p1 = GeoPoint(1.594837, 31.158936, name='Point1')
    p2 = GeoPoint(1.870223, 30.878149, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=1, stoppoint=p2, stopheight=1, frequency=13)
    radiopath1.set_radio_parameters(tx_power=18, receiver_sensitivity=-65, antenna_gain_a=38.1, antenna_gain_b=38.1)
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
    assert len(radiopath1.relief) == 107
    assert round(radiopath1.free_space_loss(), 2) == 147.53
    assert round(radiopath1.expected_signal_strength(), 2) == -53.33


def test_radio_path_chart_data():
    p1 = GeoPoint(1.594748, 31.158804, name='Point1')
    p2 = GeoPoint(1.595744, 31.160749, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=40, stoppoint=p2, stopheight=40, frequency=13)
    radiopath1.set_radio_parameters(tx_power=18, receiver_sensitivity=-65, antenna_gain_a=38.1, antenna_gain_b=38.1)
    assert round(radiopath1.free_space_loss(), 2) == 102.45
    assert round(radiopath1.expected_signal_strength(), 2) == -8.25

    assert radiopath1.get_chart_data() == {
        'distance': [0, 10, 90, 100, 160, 170, 200, 210, 240, 243.5269906724964],
        'relief': [660, 660, 660, 690, 690, 641, 641, 677, 677, 677],
        'relief_arc': [660.0, 660.0001832726225, 660.0010843985596, 690.0011264065372, 690.0010488385484, 641.0009809736314,
                       641.0006832036295, 677.0005525552118, 677.0000664318784, 677.0],
        'los_height': [700.0, 700.6980745728863, 706.2826711559771, 706.9807457288634, 711.1691931661816, 711.8672677390679,
                       713.9614914577269, 714.6595660306133, 716.7537897492723, 717.0],
        'frenzel_zone_1_top': [700.0, 701.1679137754085, 707.4248609107453, 708.1447090872165, 712.2908766565142, 712.9515870215793,
                               714.8641438049195, 715.469851232417, 717.0149683184817, 717.0],
        'frenzel_zone_1_bottom': [700.0, 700.2282353703641, 705.140481401209, 705.8167823705104, 710.0475096758489, 710.7829484565565,
                                  713.0588391105342, 713.8492808288096, 716.4926111800629, 717.0],
        'frenzel_zone_1_60_bottom': [700.0, 700.416171051373, 705.5973573031163, 706.2823677138516, 710.4961830719819, 711.216676169561,
                                     713.4199000494114, 714.173394909531, 716.5970826077466, 717.0],
        'frenzel_zone_1_60_top': [700.0, 700.9799780943996, 706.967985008838, 707.6791237438753, 711.8422032603812, 712.5178593085748,
                                  714.5030828660424, 715.1457371516956, 716.910496890798, 717.0]}
