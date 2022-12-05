# rrl_planning
## GeoPoint class
The essence of a geographic point.
The coordinates of the point and optionally the height above sea level are set. If the height is not specified, then the height is taken from the SRTM3 data.
Geographic point methods:
- calculation of azimuth between two points
- calculates the coordinates of the next point in the given azimuth and distance.
- calculation of the distance between two points in meters in a straight line.
- calculation of the distance between two points in meters on the surface of the planet.

## SRTM data
To work with SRTM3 files, you need to create a "data" folder in the root folder.
In the "data" folder, create a "cache" and "srtm3" folder.
In the "srtm3" folder, you need to prepare and put the SRTM3 data in the following format:
- folders with the name of the latitude in the format N00, N05, N34, S01, S45, etc.
- inside latitude folders are files for that latitude, each file is zip packed. For example, the N08 folder contains the files N08E000.zip N08E019.zip N08E038.zip N08E081.zip N08E134.zip N08W003.zip, etc.
