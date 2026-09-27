#!/usr/bin/env python3
"""
Extraction of facts from ArduPilot logs (.bin) for the Ariadne project session cards.

For each arming period it prints: duration, maximum altitude, mean throttle,
vibration broken down by IMU instance, attitude tracking error, battery
balance and GNSS reception quality. In addition: the list of flight modes,
EKF3 source-set switches and diagnostically relevant messages.

Requires: pymavlink  (pip install pymavlink)

Usage:
    python3 session_extract.py log_6_2026-8-19-19-33-42.bin
    python3 session_extract.py ../flight-logs/platform-2-ardupilot/*.bin

Note on time: all timestamps are given in log seconds (the TimeUS field,
counted from controller start-up). The Filter Review tool in Mission Planner
uses absolute time, so the same events have different timestamps there.
In every comparison, state which reference is used.

Note on vibration: the VIBE message is logged separately for each IMU
instance. The project documentation uses the IMU0 values. IMU2 consistently
shows values about half as large; it is a different sensor, not a different
aircraft. Do not mix them.
"""
import sys, os, math
from pymavlink import mavutil

MODES = {0: 'Stabilize', 1: 'Acro', 2: 'AltHold', 3: 'Auto', 4: 'Guided',
         5: 'Loiter', 6: 'RTL', 7: 'Circle', 9: 'Land', 11: 'Drift',
         13: 'Sport', 14: 'Flip', 15: 'AutoTune', 16: 'PosHold', 17: 'Brake',
         18: 'Throw', 19: 'Avoid_ADSB', 20: 'Guided_NoGPS', 21: 'Smart_RTL',
         22: 'FlowHold', 23: 'Follow', 24: 'ZigZag', 25: 'SystemID',
         26: 'Heli_Autorotate', 27: 'AutoRTL'}

# EV: 10 = arming, 11 = disarming
EV_ARM, EV_DISARM = 10, 11

KEYWORDS = ('Error', 'error', 'Glitch', 'EKF', 'Failsafe', 'failsafe',
            'Crash', 'Land', 'Yaw', 'yaw', 'Vibration', 'PreArm', 'Arm')


def percentile(values, p):
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * p / 100.0
    d, g = math.floor(k), math.ceil(k)
    return s[int(k)] if d == g else s[d] + (s[g] - s[d]) * (k - d)


def load(path):
    m = mavutil.mavlink_connection(path)
    d = {'modes': [], 'events': [], 'messages': [], 'gnss': [], 'battery': [],
         'altitude': [], 'vibration': {}, 'attitude': [], 't0': None, 't1': None}
    while True:
        try:
            msg = m.recv_match(blocking=False)
        except Exception:
            continue
        if msg is None:
            break
        t = getattr(msg, 'TimeUS', None)
        if t is None:
            continue
        ts, typ = t / 1e6, msg.get_type()
        if d['t0'] is None:
            d['t0'] = ts
        d['t1'] = ts
        if typ == 'MODE':
            d['modes'].append((ts, MODES.get(msg.Mode, str(msg.Mode))))
        elif typ == 'EV' and msg.Id in (EV_ARM, EV_DISARM):
            d['events'].append((ts, msg.Id))
        elif typ == 'MSG':
            d['messages'].append((ts, msg.Message))
        elif typ == 'GPS':
            d['gnss'].append((ts, msg.NSats, msg.HDop))
        elif typ == 'BAT':
            d['battery'].append((ts, msg.Volt, getattr(msg, 'Curr', 0),
                                 getattr(msg, 'CurrTot', 0)))
        elif typ == 'CTUN':
            d['altitude'].append((ts, msg.Alt, getattr(msg, 'ThO', 0)))
        elif typ == 'VIBE':
            i = getattr(msg, 'IMU', getattr(msg, 'I', 0))
            d['vibration'].setdefault(i, []).append(
                (ts, msg.VibeY, getattr(msg, 'Clip0', getattr(msg, 'Clip', 0))))
        elif typ == 'ATT':
            d['attitude'].append((ts, msg.Roll, msg.DesRoll, msg.Pitch, msg.DesPitch))
    return d


def report(path):
    d = load(path)
    L = [f"### {os.path.basename(path)}",
         f"record: {d['t0']:.1f} - {d['t1']:.1f} s ({(d['t1']-d['t0'])/60:.1f} min)"]

    arms = [t for t, i in d['events'] if i == EV_ARM]
    disarms = [t for t, i in d['events'] if i == EV_DISARM]
    L.append(f"armings: {len(arms)}, disarmings: {len(disarms)}")

    for nr, a in enumerate(arms, 1):
        b = next((x for x in disarms if x > a), None)
        if b is None:
            continue
        L.append(f"\n  flight {nr}: {a:.1f} -> {b:.1f} s  ({b-a:.0f} s = {(b-a)/60:.1f} min)")
        w = [x for x in d['altitude'] if a <= x[0] <= b]
        if w:
            L.append(f"     max altitude {max(x[1] for x in w):.1f} m, "
                     f"mean throttle {sum(x[2] for x in w)/len(w):.3f}")
        for imu in sorted(d['vibration']):
            v = [x for x in d['vibration'][imu] if a <= x[0] <= b]
            if v:
                vy = [x[1] for x in v]
                L.append(f"     IMU{imu}: VibeY mean {sum(vy)/len(vy):.1f}, "
                         f"p95 {percentile(vy,95):.1f}, max {max(vy):.1f}, "
                         f"clipping events {max(x[2] for x in v)}")
        k = [x for x in d['attitude'] if a <= x[0] <= b]
        if k:
            er = [abs(x[1]-x[2]) for x in k]
            ep = [abs(x[3]-x[4]) for x in k]
            L.append(f"     tracking error: roll p95 {percentile(er,95):.2f} deg, "
                     f"pitch p95 {percentile(ep,95):.2f} deg")
        bt = [x for x in d['battery'] if a <= x[0] <= b]
        if bt:
            L.append(f"     battery {bt[0][1]:.2f} -> {bt[-1][1]:.2f} V "
                     f"(min {min(x[1] for x in bt):.2f}), "
                     f"cumulative consumption {bt[-1][3]:.0f} mAh")
        g = [x for x in d['gnss'] if a <= x[0] <= b]
        if g:
            L.append(f"     GNSS: {min(x[1] for x in g)}-{max(x[1] for x in g)} sat., "
                     f"HDOP {min(x[2] for x in g):.2f}-{max(x[2] for x in g):.2f}")

    seq, prev = [], None
    for t, name in d['modes']:
        if name != prev:
            seq.append(f"{t:.0f}s:{name}")
            prev = name
    if seq:
        L.append("\nmodes: " + " -> ".join(seq))

    sources = [(t, m) for t, m in d['messages'] if 'Source Set' in m]
    if sources:
        L.append("EKF3 sources: " + " | ".join(f"{t:.0f}s {m}" for t, m in sources))

    seen, lines = set(), []
    for t, m in d['messages']:
        if any(s in m for s in KEYWORDS) and 'Source Set' not in m and m not in seen:
            seen.add(m)
            lines.append(f"   {t:.0f}s {m}")
    if lines:
        L.append("messages (first occurrence of each):")
        L.extend(lines[:30])

    if d['battery']:
        b = d['battery']
        L.append(f"\nbattery, whole record: {b[0][1]:.2f} -> {b[-1][1]:.2f} V, "
                 f"min {min(x[1] for x in b):.2f} V, "
                 f"consumption {b[-1][3]:.0f} mAh, max current {max(x[2] for x in b):.1f} A")
    return "\n".join(L)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for p in sorted(sys.argv[1:]):
        try:
            print(report(p), "\n")
        except Exception as e:
            print(f"### {os.path.basename(p)}\nERROR: {e}\n")
