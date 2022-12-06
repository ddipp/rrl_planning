from lib import GeoPoint, RadioPath


def test_radio_path1():
    p1 = GeoPoint(57.366543, 60.524290, name='Point1')
    p2 = GeoPoint(57.271203, 60.499945, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=20, stoppoint=p2, stopheight=20, frequency=7)
    assert radiopath1.startpoint == p1
    assert radiopath1.stoppoint == p2
    assert radiopath1.frequency == 7
    assert int(radiopath1.length) == 10702
    assert radiopath1.startpoint.elevation == 232
    assert radiopath1.stoppoint.elevation == 232
    assert radiopath1.arc_height(0) == 0
    assert radiopath1.arc_height(radiopath1.length) == 0
    assert int(radiopath1.arc_height(radiopath1.length / 2)) == 2
    assert int(radiopath1.arc_height(radiopath1.length / 4)) == 1
    assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
    assert radiopath1.line_equation_b == 252
    assert radiopath1.line_equation_k == 0
    assert int(radiopath1.los_height(0)) == 252
    assert int(radiopath1.los_height(radiopath1.length)) == 252
    assert int(radiopath1.los_height(radiopath1.length / 2)) == 252


def test_radio_path2():
    p1 = GeoPoint(56.827275, 60.004317, name='Point1')
    p2 = GeoPoint(56.763559, 60.189839, name='Point2')
    radiopath1 = RadioPath(startpoint=p1, startheight=20, stoppoint=p2, stopheight=20, frequency=7)
    assert radiopath1.startpoint == p1
    assert radiopath1.stoppoint == p2
    assert radiopath1.frequency == 7
    assert int(radiopath1.length) == 13337
    assert radiopath1.startpoint.elevation == 509
    assert radiopath1.stoppoint.elevation == 298
    assert radiopath1.arc_height(0) == 0
    assert radiopath1.arc_height(radiopath1.length) == 0
    assert int(radiopath1.arc_height(radiopath1.length / 2)) == 3
    assert int(radiopath1.arc_height(radiopath1.length / 4)) == 2
    assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
    assert radiopath1.line_equation_b == 529
    assert radiopath1.line_equation_k == -0.01582009779681836
    assert int(radiopath1.los_height(0)) == 529
    assert int(radiopath1.los_height(radiopath1.length)) == 318
    assert int(radiopath1.los_height(radiopath1.length / 2)) == 423