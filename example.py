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
fig = plt.figure()
ax = fig.add_subplot()

ax.grid(True)

ax.annotate(f'Antenna gain {r1.antenna_gain_a:.1f} dBm',
            xy=(0, r1_chart['los_height'][0]), xycoords='data',
            xytext=(0.1, 0.5), textcoords='axes fraction',
            horizontalalignment='left',
            arrowprops=dict(arrowstyle="simple",
                            fc="0.6", ec="none",
                            connectionstyle="arc3,rad=0.3"),
            bbox=dict(boxstyle="round", fc="1", alpha=0.5))

ax.annotate(f'Antenna gain {r1.antenna_gain_b:.1f} dBm',
            xy=(r1_chart['distance'][-1], r1_chart['los_height'][-1]), xycoords='data',
            xytext=(0.9, 0.5), textcoords='axes fraction',
            horizontalalignment='right',
            arrowprops=dict(arrowstyle="simple",
                            fc="0.6", ec="none",
                            connectionstyle="arc3,rad=0.3"),
            bbox=dict(boxstyle="round", fc="1", alpha=0.5))

ax.annotate(f'TX power {r1.tx_power} dBm\nExpected RX Level {r1.expected_signal_strength():.1f} dBm',
            xy=(0.5, 0.5), xycoords='axes fraction',
            horizontalalignment='center',
            bbox=dict(boxstyle="round", fc="1", alpha=0.5))

ax.plot(r1_chart['distance'], r1_chart['relief'], label="Elevation", linestyle='solid', linewidth=0.5)
ax.plot(r1_chart['distance'], r1_chart['relief_arc'], label="Surface with curvature of the earth", color='darkgreen', linewidth=0.5)

ax.plot(r1_chart['distance'], r1_chart['los_height'], color='darkred', label="Line of sight", linewidth=0.5)

ax.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_60_top'], label="60% 1 Frenzel zone", color='red', linewidth=0.15, alpha=.15)
ax.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_60_bottom'], color='red', linewidth=0.15, alpha=.15)

ax.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_top'], label="1 Frenzel zone", color='lightcoral', linewidth=0.5)
ax.plot(r1_chart['distance'], r1_chart['frenzel_zone_1_bottom'], color='lightcoral', linewidth=0.5)

ax.fill_between(r1_chart['distance'], r1_chart['frenzel_zone_1_60_top'],
                r1_chart['frenzel_zone_1_60_bottom'], color='red', alpha=.15, linewidth=0)

ax.fill_between(r1_chart['distance'], r1_chart['relief_arc'], min(r1_chart['relief']), color='darkgreen', alpha=.4)

ax.set_xlabel('Distance (m)')
ax.set_ylabel('Elevation (m)')

plt.legend()
plt.title(
    f'Profile from "{r1.startpoint.name}" {r1.startpoint.latitude} {r1.startpoint.longitude} H={r1.startheight} '
    f'to "{r1.stoppoint.name}" {r1.stoppoint.latitude} {r1.stoppoint.longitude}  H={r1.stopheight}\n'
    f'Distance {r1.length / 1000:.2f} km, Frequency {r1.frequency}GHz')
plt.savefig(f"{r1.startpoint.name}-{r1.stoppoint.name}.png", dpi=300)
plt.close()
