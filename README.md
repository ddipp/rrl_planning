# rrl_planning
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
```

## SRTM data
To work with SRTM3 files, you need to create a "data" folder in the root folder.
In the "data" folder, create a "cache" and "srtm3" folder.
In the "srtm3" folder, you need to prepare and put the SRTM3 data in the following format:
- folders with the name of the latitude in the format N00, N05, N34, S01, S45, etc.
- inside latitude folders are files for that latitude, each file is zip packed. For example, the N08 folder contains the files N08E000.zip N08E019.zip N08E038.zip N08E081.zip N08E134.zip N08W003.zip, etc.

```python3
from lib.srtm import srtm

assert srtm.get_elevation_point(54.999999, 41.999999) == 158
assert srtm.get_elevation_point(54.238421, 57.995044) == 605
assert srtm.get_elevation_point(55.013505, 48.862878) == 202
```
