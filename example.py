#!/usr/bin/env python
import logging
import matplotlib.pyplot as plt
from lib import GeoPoint, RadioPath

logging.basicConfig(level=logging.INFO, format='[%(asctime)s: %(levelname)s] %(message)s')

p1 = GeoPoint(34.105719, -118.362051, name='Point1')
p1.h = 15
p2 = GeoPoint(34.054077, -118.156900, name='Point2')
p2.h = 15

r1 = RadioPath(p1, p1.h, p2, p2.h, 7)
r1.set_radio_parameters(tx_power=18, receiver_sensitivity=-65, antenna_gain_a=38.1, antenna_gain_b=38.1)

logging.info(f'Having a line of sight - {r1.line_of_sight()}')
logging.info(f'Visibility in 1 fresnel zone - {r1.visibility_in_fresnel_zone(1)}')
logging.info(f'Visibility in 2 fresnel zone - {r1.visibility_in_fresnel_zone(2)}')
logging.info(f'Points: {len(r1.relief)}')
logging.info(f'FSL: {r1.free_space_loss():.1f} dB')
logging.info(f'Length: {r1.length / 1000:.2f} km')
logging.info(f'Expected RX level: {r1.expected_signal_strength():.1f} dBm')

r1_chart = r1.get_chart_data()

plt.rcParams["figure.figsize"] = (14, 9)
plt.grid(False)
plt.plot(r1_chart['distance'], r1_chart['relief'], label="Elevation", linestyle='solid', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['relief_arc'], label="Surface with curvature of the earth", color='darkgreen', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['los_height'], color='darkred', label="Line of sight", linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_top'], label="1 Frenzel zone", color='red', linewidth=0.15)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_bottom'], color='red', linewidth=0.15)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_2_top'], label="2 Frenzel zone", color='lightcoral', linewidth=0.5)
plt.plot(r1_chart['distance'], r1_chart['frenzel_zone_2_bottom'], color='lightcoral', linewidth=0.5)

plt.fill_between(r1_chart['distance'], r1_chart['frenzel_zone_1_top'],
                 r1_chart['frenzel_zone_1_bottom'], color='red', alpha=.15, linewidth=0)
plt.fill_between(r1_chart['distance'], r1_chart['relief_arc'], min(r1_chart['relief']), color='darkgreen', alpha=.4)

plt.xlabel('Distance (m)')
plt.ylabel('Elevation (m)')
plt.legend()
plt.title(
    f'Profile from "{r1.startpoint.name}" {r1.startpoint.latitude} {r1.startpoint.longitude} H={r1.startheight} '
    f'to "{r1.stoppoint.name}" {r1.stoppoint.latitude} {r1.stoppoint.longitude}  H={r1.stopheight}\n'
    f'Distance {r1.length / 1000:.2f} km, Frequency {r1.frequency}GHz')
plt.savefig(f"{r1.startpoint.name}-{r1.stoppoint.name}.png", dpi=300)
plt.close()
