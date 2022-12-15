import math as m
from lib.srtm import srtm
from lib import GeoPoint

EARTH_RADIUS = 6371009


class RadioPath():
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

    def frenzel_zone_size(self, zone_number: int, distance: int) -> float:
        # Fresnel zone size
        d1 = distance / 1000
        d2 = int(self.length - distance) / 1000
        r1 = 17.3 * m.sqrt((d1 * d2) / (self.frequency * (d1 + d2)))
        return r1 * m.sqrt(zone_number)

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
            if self.relief[-1][1] != elevation or distance - self.relief[-1][0] > 100:
                self.relief.append((distance, elevation))

        nextpoint = self.stoppoint
        self.relief.append((self.length, srtm.get_elevation_point(nextpoint.latitude, nextpoint.longitude)))

    def visibility_in_fresnel_zone(self, zone_number) -> bool:
        """ the presence of visibility in the fresnel zones.
            If there are obstacles on the way between points (considering antenna heights),
            then False is returned, otherwise True.
        """
        # checking the availability of terrain data. If not, then we calculate.
        if len(self.relief) == 0:
            self.get_relief()

        for point in self.relief:
            distance = point[0]
            elevation = point[1]
            los_height = self.los_height(distance)
            arc_height = self.arc_height(distance)
            frenzel_zone = self.frenzel_zone_size(zone_number, distance)
            # Compare line of sight height and surface height + planet curvature
            if los_height - frenzel_zone < elevation + arc_height:
                return False

        return True

    def line_of_sight(self) -> bool:
        """ having a direct line of sight.
            If there are obstacles on the way between points (considering antenna heights),
            then False is returned, otherwise True.
        """
        # checking the availability of terrain data. If not, then we calculate.
        if len(self.relief) == 0:
            self.get_relief()

        # Iterate over the heights and compare with the height of the line of sight at that point.
        for point in self.relief:
            distance = point[0]
            elevation = point[1]
            los_height = self.los_height(distance)
            arc_height = self.arc_height(distance)
            # Compare line of sight height and surface height + planet curvature
            if los_height < elevation + arc_height:
                return False

        return True

    def get_chart_data(self):
        """ Chart data.
            Returns a list of data points:
            - distance from starting point
            - relief height
            - the height of the relief, taking into account the curvature of the planet
            - line of sight height
            - height of the first fresnel zone
            - height of the second fresnel zone
        """
        chart_data = {'distance': [], 'relief': [], 'relief_arc': [], 'los_height': [], 'frenzel_zone_1_top': [],
                      'frenzel_zone_1_bottom': [], 'frenzel_zone_2_top': [], 'frenzel_zone_2_bottom': []}
        # checking the availability of terrain data. If not, then we calculate.
        if len(self.relief) == 0:
            self.get_relief()

        for point in self.relief:
            distance = point[0]
            elevation = point[1]
            arc_height = self.arc_height(distance)
            los_height = self.los_height(distance)
            chart_data['distance'].append(distance)
            chart_data['relief'].append(elevation)
            chart_data['relief_arc'].append(elevation + arc_height)
            chart_data['los_height'].append(los_height)
            chart_data['frenzel_zone_1_top'].append(los_height + self.frenzel_zone_size(1, distance))
            chart_data['frenzel_zone_1_bottom'].append(los_height - self.frenzel_zone_size(1, distance))
            chart_data['frenzel_zone_2_top'].append(los_height + self.frenzel_zone_size(2, distance))
            chart_data['frenzel_zone_2_bottom'].append(los_height - self.frenzel_zone_size(2, distance))
        return chart_data
