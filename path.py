#!/usr/bin/env python
import logging
import matplotlib.pyplot as plt
from lib import GeoPoint, RadioPath


logging.basicConfig(
    # filename='application.log',
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logging.info('start')

p1 = GeoPoint(58.59152, 125.30347, name='Point1')
p1.h = 75
p2 = GeoPoint(58.92182, 125.98498, name='Point2')
p2.h = 50

r1 = RadioPath(p1, p1.h, p2, p2.h, 7)
r1.get_relief()
print(r1.relief)
print(len(r1.relief))
print(r1.line_of_sight())


r1_chart = r1.get_chart_data()

plt.rcParams["figure.figsize"] = (14, 9)
plt.grid(False)
plt.plot(r1_chart['distance'], r1_chart['relief'], label="Elevation", linestyle='solid', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['relief_arc'], label="Surface with curvature of the earth", color='darkgreen', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['los_height'], color='darkred', label="Line of sight", linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_top'], label="1 Frenzel zone", color='red', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_bottom'], color='red', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_2_top'], label="2 Frenzel zone", color='lightcoral', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_2_bottom'], color='lightcoral', linewidth=0.5)

plt.fill_between(r1_chart['distance'], r1_chart['frenzel_zone_1_top'], r1_chart['frenzel_zone_1_bottom'], color='red', alpha=.05)
plt.fill_between(r1_chart['distance'], r1_chart['relief_arc'], min(r1_chart['relief']), color='darkgreen', alpha=.4)

plt.xlabel('Distance (km)')
plt.ylabel('Elevation (m)')
plt.legend()
plt.title(
    f'Profile from "{r1.startpoint.name}" {r1.startpoint.latitude} {r1.startpoint.longitude} H={r1.startheight} '
    f'to "{r1.stoppoint.name}" {r1.stoppoint.latitude} {r1.stoppoint.longitude}  H={r1.stopheight}\n'
    f'Distance {r1.length / 1000:.2f} km, Frequency {r1.frequency}GHz')
plt.savefig(f"{r1.startpoint.name} - {r1.stoppoint.name}.png", dpi=300)
plt.close()


print(r1.line_of_sight())
print(r1.visibility_in_fresnel_zone(1))
print(r1.visibility_in_fresnel_zone(2))
