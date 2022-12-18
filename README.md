# rrl_planning
[![Testing status](https://github.com/ddipp/rrl_planning/actions/workflows/pytest.yml/badge.svg)](https://github.com/ddipp/rrl_planning/actions) [![codecov](https://codecov.io/gh/ddipp/rrl_planning/branch/main/graph/badge.svg?token=CK8LLFQU39)](https://codecov.io/gh/ddipp/rrl_planning)
## Usage example
To use, you need to prepare SRTM data (see below).

For example, in the example.py file, the radio channel parameters (coordinates, antenna heights, frequency) are defined.
The presence of a line of sight is displayed, taking into account the first and second Fresnel zones.
Using mathplotlib, a radio channel profile is created.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install --no-cache-dir -r requirements.txt

./example.py
````

![graph](Point1-Point2.png?raw=true)

## RadioPath class
Radio path. Start and end points, antenna heights and operating frequency are set.
- the height of the planet's arc at a given distance (in meters) from the start of the path
- radio channel length in meters
- calculates the height (in meters above sea level) of the line of sight above the line at a given distance (in meters) between the start and end points of the path (taking into account the height of the antenna suspension). Height in meters above ... above a straight line (not on the arc of the ball) between the points if the points were at sea level.
- having a direct line of sight.
- visibility with Fresnel Zone

```python3
from lib import GeoPoint, RadioPath

p1 = GeoPoint(56.827275, 60.004317, name='Point1')
p2 = GeoPoint(56.763559, 60.189839, name='Point2')
radiopath1 = RadioPath(startpoint=p1, startheight=20, stoppoint=p2, stopheight=20, frequency=7)
assert int(radiopath1.length) == 13337
assert radiopath1.startpoint.elevation == 509
assert radiopath1.stoppoint.elevation == 298
assert radiopath1.arc_height(0) == 0
assert radiopath1.arc_height(radiopath1.length) == 0
assert int(radiopath1.arc_height(radiopath1.length / 2)) == 3
assert int(radiopath1.arc_height(radiopath1.length / 4)) == 2
assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
assert int(radiopath1.los_height(0)) == 252
assert int(radiopath1.los_height(radiopath1.length)) == 252
assert int(radiopath1.los_height(radiopath1.length / 2)) == 252
assert radiopath1.line_of_sight() is True
assert radiopath1.visibility_in_fresnel_zone(1) is True
assert radiopath1.visibility_in_fresnel_zone(2) is True

p1 = GeoPoint(57.366543, 60.524290, name='Point1')
p2 = GeoPoint(57.271203, 60.499945, name='Point2')
radiopath1 = RadioPath(startpoint=p1, startheight=20, stoppoint=p2, stopheight=20, frequency=17)
assert int(radiopath1.length) == 10702
assert radiopath1.startpoint.elevation == 232
assert radiopath1.stoppoint.elevation == 232
assert radiopath1.arc_height(0) == 0
assert radiopath1.arc_height(radiopath1.length) == 0
assert int(radiopath1.arc_height(radiopath1.length / 2)) == 2
assert int(radiopath1.arc_height(radiopath1.length / 4)) == 1
assert radiopath1.arc_height(radiopath1.length / 4) == radiopath1.arc_height(radiopath1.length / 4 * 3)
assert int(radiopath1.los_height(0)) == 252
assert int(radiopath1.los_height(radiopath1.length)) == 252
assert int(radiopath1.los_height(radiopath1.length / 2)) == 252
assert radiopath1.line_of_sight() is True
assert radiopath1.visibility_in_fresnel_zone(1) is True
assert radiopath1.visibility_in_fresnel_zone(2) is False

```


## GeoPoint class
The essence of a geographic point.
The coordinates of the point and optionally the height above sea level are set. If the height is not specified, then the height is taken from the SRTM3 data.
Geographic point methods:
- calculation of azimuth between two points
- calculates the coordinates of the next point in the given azimuth and distance.
- calculation of the distance between two points in meters in a straight line.
- calculation of the distance between two points in meters on the surface of the planet.
- each point has properties - coordinates in the x, y, z format with the origin at the center of the planet.

```python3
from lib import GeoPoint

p1 = GeoPoint(43.350183, 42.451874, name='Elbrus')
p2 = GeoPoint(43.350183, 42.451874, name='Elbrus sea level', elevation=0)
assert p1.distance_to(p2) == 5518.999999999588
assert p1.arc_distance_to(p2) == 0.0

p1 = GeoPoint(90, 0, name='N')
p2 = GeoPoint(-90, 0, name='S')
assert p1.distance_to(p2) == 12744717.0
assert p1.arc_distance_to(p2) == 20015115.070354454

p3 = GeoPoint(0, 0, name='00')
assert p3.elevation is None  # This point is in the ocean
assert p3.x == 6371009
assert p3.y == 0
assert p3.z == 0

p4 = GeoPoint(0, 0)
p5 = GeoPoint(1, 1)
assert p4.azimuth(p5) == 44.99563645534485
assert p5.azimuth(p4) == 225.00436354465515

p6 = GeoPoint(54.9132538, 34.3426619)
p7 = p6.nextpoint(azimuth=90, distance=500)
assert (p7.latitude, p7.longitude) == (54.913253548816705, 34.350484580324036)
```

## SRTM data
To work with terrain data, you need SRTM data.
Typically SRTM archives include areas between 60 degrees north latitude and 56 degrees south latitude. But on the Internet there is data for the relief of the entire planet (apparently compiled from various sources).
From this [link](http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm) I downloaded all the data, then using the "utils/recompress.py" script, the data was reformatted into the form:
- folders with the name of the latitude in the format N00, N05, N34, S01, S45, etc.
- inside latitude folders there are files for this latitude, each file is packed in bz2. For example, folder N08 contains files N08E000.hgt.bz2, N08E019.hgt.bz2, N08E038.hgt.bz2, N08E081.hgt.bz2, N08E134.hgt.bz2, N08W003.hgt.bz2, etc.

Next, to work with SRTM3 files, you need to create a “data” folder in the root folder.
In the "data" folder, create a "cache" and "srtm3" folder.
In the folder "srtm3" you need to add the prepared SRTM3 data

```python3
from lib.srtm import srtm

assert srtm.get_elevation_point(54.999999, 41.999999) == 158
assert srtm.get_elevation_point(54.238421, 57.995044) == 605
assert srtm.get_elevation_point(55.013505, 48.862878) == 202
assert srtm.get_elevation_point(55.841989, -41.038896) is None  # No data for open ocean, returns None
assert srtm.get_elevation_point(2.238345, 118.071729) == 0  # For coastal waters, returns 0

points = ((-4.003640, -79.058322), (-3.991163, -79.092340),
		  (-3.957352, -79.023306), (-3.991068, -79.015972))
elevations = ((-4.003640, -79.058322, 3132), (-3.991163, -79.092340, 2005),
              (-3.957352, -79.023306, 1553), (-3.991068, -79.015972, 1507))
assert srtm.get_all_elevations_points(points) == elevations
```
