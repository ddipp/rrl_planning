import math as m
from lib.srtm import srtm
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
        # List for relief
        self.relief = list()

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

    def get_relief(self, incremental: int = 10):
        """ Calculate elevation points on a straight line between start and end.
        """
        distance = 0

        nextpoint = self.startpoint
        self.relief.append((0, srtm.get_elevation_point(nextpoint.latitude, nextpoint.longitude)))

        for i in range(int(self.length // incremental)):
            distance += incremental
            nextpoint = self.startpoint.nextpoint(self.startpoint.azimuth(self.stoppoint), distance)
            elevation = srtm.get_elevation_point(nextpoint.latitude, nextpoint.longitude)
            # To save memory, if the previous point is at the same height and
            # the distance to it is not too large, then I do not add a new one
            if self.relief[-1][1] != elevation or distance - self.relief[-1][0] > 200:
                self.relief.append((distance, elevation))

        nextpoint = self.stoppoint
        self.relief.append((self.length, srtm.get_elevation_point(nextpoint.latitude, nextpoint.longitude)))

    @property
    def line_of_sight(self) -> bool:
        """ having a direct line of sight.
            If there are obstacles on the way between points (considering antenna heights),
            then False is returned, otherwise True.
        """
        # checking the availability of terrain data. If not, then we calculate.
        if len(self.relief) == 0:
            self.get_relief()

        # Iterate over the heights and compare with the height of the line of sight at that point.
        for i in self.relief:
            distance = i[0]
            elevation = i[1]
            los_height = self.los_height(distance)
            arc_height = self.arc_height(distance)
            # Compare line of sight height and surface height + planet curvature
            if los_height < elevation + arc_height:
                return False

        return True
