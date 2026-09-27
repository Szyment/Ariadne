#!/usr/bin/env python3
"""Generates a GNSS-denied run plan for a given take-off point and wind direction.

Usage:
    python3 drift_plan.py --lat 50.9139925 --lon 19.0863896 --wind 116
    python3 drift_plan.py --lat ... --lon ... --wind 116 --length 40 --height 4

Output goes by default to missions/E1_nowy.plan (assign the final name according to missions/README.md; historically: S-15_Drift3.plan).

Waypoints are written in the terrain frame (frame 10, MAV_FRAME_GLOBAL_TERRAIN_ALT).
The commanded altitude is then the distance from the ground measured by the
rangefinder (WP_RFND_USE = 1), not the altitude above the take-off point, which
drifts when the altitude source is set to the rangefinder (card S-12, finding 4).

The take-off point coordinates are read after arming from the position shown
by the ground control station. The wind direction is given as the azimuth
FROM WHICH it blows (annex C, paragraph 5). The leg is flown into the wind.
"""
import argparse, json, math, os

def offset(lat, lon, azimuth_deg, metres):
    dlat = metres * math.cos(math.radians(azimuth_deg)) / 111320.0
    dlon = metres * math.sin(math.radians(azimuth_deg)) / (111320.0 * math.cos(math.radians(lat)))
    return lat + dlat, lon + dlon

def wp(idx, lat, lon, alt, hold):
    return {
        "AMSLAltAboveTerrain": None, "Altitude": alt, "AltitudeMode": 4,
        "autoContinue": True, "command": 16, "doJumpId": idx, "frame": 10,
        "params": [hold, 0, 0, None, lat, lon, alt], "type": "SimpleItem",
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lat", type=float, required=True, help="latitude of the take-off point")
    p.add_argument("--lon", type=float, required=True, help="longitude of the take-off point")
    p.add_argument("--wind", type=float, required=True, help="azimuth the wind blows from [deg]")
    p.add_argument("--length", type=float, default=40.0, help="leg length [m]")
    p.add_argument("--height", type=float, default=3.0, help="height [m]")
    p.add_argument("--downwind", dest="downwind", action="store_true",
                   help="leg in the other direction: 40 m turn point downwind instead of into the wind")
    p.add_argument("--out", default=None)
    a = p.parse_args()

    # The condition concerns the AXIS, not the direction: drift should go along the track, not across it
    # (S-10_Drift1_README.md line 67). Both directions of the same axis satisfy it equally.
    azimuth = (a.wind + 180.0) % 360.0 if a.downwind else a.wind
    tlat, tlon = offset(a.lat, a.lon, azimuth, a.length)

    plan = {
        "fileType": "Plan",
        "geoFence": {"circles": [], "polygons": [], "version": 2},
        "groundStation": "QGroundControl",
        "mission": {
            "cruiseSpeed": 15, "firmwareType": 3, "globalPlanAltitudeMode": 4,
            "hoverSpeed": 5,
            "items": [
                wp(1, tlat, tlon, a.height, 3),
                wp(2, a.lat, a.lon, a.height, 5),
            ],
            "plannedHomePosition": [a.lat, a.lon, 224],
            "vehicleType": 2, "version": 2,
        },
        "rallyPoints": {"points": [], "version": 2},
        "version": 1,
    }

    out = a.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "missions", "E1_nowy.plan")
    out = os.path.normpath(out)
    with open(out, "w") as f:
        json.dump(plan, f, indent=4)

    print("take-off point   %.7f  %.7f" % (a.lat, a.lon))
    print("turn point       %.7f  %.7f" % (tlat, tlon))
    print("leg              %.0f m, azimuth %.0f deg (%s, wind from %.0f)"
          % (a.length, azimuth, "downwind" if a.downwind else "into the wind", a.wind))
    print("height           %.1f m above ground (terrain frame)" % a.height)
    print("written          %s" % out)

if __name__ == "__main__":
    main()
