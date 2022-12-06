import math as m
from lib import GeoPoint

EARTH_RADIUS = 6371.009 * 1000


class RadioPath(object):
    """ Radio path. Start and end points, antenna heights and operating frequency are set.
    """

    def __init__(self, startpoint: GeoPoint, startheight: int, stoppoint: GeoPoint, stopheight: int, frequency: int):
        self.startpoint = startpoint
        self.startheight = startheight
        self.stoppoint = stoppoint
        self.stopheight = stopheight
        self.frequency = frequency
        # Radio channel length in meters
        self.length = self.startpoint.distance_to(self.stoppoint)
        # Coefficients for calculating line-of-sight height
        self.line_equation_k = ((self.startpoint.elevation + self.startheight)
                                - (self.stoppoint.elevation + self.stopheight)) / (0 - self.length)
        self.line_equation_b = (self.stoppoint.elevation + self.stopheight) - self.line_equation_k * self.length

    def arc_height(self, distance: int) -> float:
        """ The height of the planet's arc at a given distance (in meters) from the start of the path
        """
        a = (m.pi - 2 * m.acos(self.length / (2 * EARTH_RADIUS))) / 2
        t = -1 + distance / (self.length / 2)
        h = EARTH_RADIUS * (m.sqrt((1 - (t**2) * (m.sin(a)**2))) - m.cos(a))
        return h

    def los_height(self, distance: int) -> float:
        """ Calculates the height (in meters) of the line of sight
            above a straight line at a given distance (in meters)
            between the start and end points of the path
            (taking into account the height of the antenna suspension).
        """
        return self.line_equation_k * distance + self.line_equation_b
