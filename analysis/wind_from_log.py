#!/usr/bin/env python3
"""
Wind read from the flight log, a check on the anemometer measurement.

A multirotor holding position tilts towards the direction the wind blows
from, by an angle that grows with the wind. The flight log therefore
contains an independent trace of the wind: the direction and an indicator
of its strength, measured throughout the run, at the run altitude and
without human involvement.

The script searches the log for hover windows, computes the averaged tilt
within them and converts it into the direction the wind blew from.

    python3 wind_from_log.py ../../flight-logs/platform-2-ardupilot/log_8_*.bin

Requires: pymavlink.

--- What this is for, and what it is not for -------------------------------

It serves three purposes:

1. Wind direction. Computed from the record, not from the pilot's memory.
   The GM816 anemometer gives no direction at all; it has to be found by
   turning the instrument, which is a subjective reading.
2. Comparing sessions with each other. The indicator is computed from the
   same record by the same method, so the comparison "today was calmer than
   yesterday" no longer depends on who held the anemometer.
3. Catching a situation in which the anemometer reading disagrees with the
   behaviour of the aircraft, for example when the measurement was made in
   the lee of a car or at a different moment than the flight.

It does not replace the anemometer. Converting tilt to metres per second
requires the product of the drag coefficient and the frontal area, which has
not been determined for this aircraft. Until it is, the result is the
horizontal acceleration needed to hold position [m/s2], a quantity
proportional to the wind force but not expressed as its speed.

--- Limitations to keep in mind ----------------------------------------------

The heading comes from the magnetometer. The wind direction is therefore
affected by the compass calibration error. Agreement with the direction from
the ERA5 reanalysis (given by `session_weather.py`) is the simplest check of both
at once.

The averaged tilt makes sense only in hover. In transit along the track the
aircraft tilts to accelerate, and the tilt from the wind is lost in the tilt
from the manoeuvre. That is why the script computes only within windows in
which the horizontal speed is near zero.
"""
import argparse
import math
import os
import statistics
import sys

from pymavlink import mavutil

EV_ARM, EV_DISARM = 10, 11

SPEED_THRESHOLD = 0.7    # m/s; above this the aircraft is moving
HEIGHT_THRESHOLD = 2.0   # m; lower than this the ground effect counts
MIN_THROTTLE = 0.10      # fraction; below this the aircraft is not flying, only spinning the propellers
MIN_WINDOW = 15.0        # s; a shorter window does not average out gusts
YAW_RATE_THRESHOLD = 1.0 # deg/s of commanded yaw; above this the window ends
G = 9.80665


def fmt(x, places=2):
    """Number with a decimal point, or a placeholder when there is no value."""
    if x is None:
        return 'n/a'
    return f'{x:.{places}f}'


def percentile(values, p):
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * p / 100.0
    d, g = math.floor(k), math.ceil(k)
    return s[int(k)] if d == g else s[d] + (s[g] - s[d]) * (k - d)


def compass_point(degrees):
    rose = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return rose[int((degrees % 360) / 22.5 + 0.5) % 16]


def load(path):
    m = mavutil.mavlink_connection(path)
    d = {'att': [], 'speed': [], 'altitude': [], 'throttle': [],
         'events': []}
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
        if typ == 'ATT':
            d['att'].append((ts, msg.Roll, msg.Pitch, msg.Yaw,
                             getattr(msg, 'DesYaw', msg.Yaw)))
        elif typ == 'GPS' and getattr(msg, 'Status', 0) >= 3:
            d['speed'].append((ts, msg.Spd))
        elif typ == 'CTUN':
            d['altitude'].append((ts, msg.Alt))
            d['throttle'].append((ts, getattr(msg, 'ThO', 0)))
        elif typ == 'EV' and msg.Id in (EV_ARM, EV_DISARM):
            d['events'].append((ts, msg.Id))
    return d


def value_at(series, ts):
    """Sample of the series nearest to the moment ts."""
    if not series:
        return None
    return min(series, key=lambda x: abs(x[0] - ts))[1]


def unwrap(angles):
    out = [angles[0]]
    for k in angles[1:]:
        out.append(out[-1] + ((k - out[-1] + 180) % 360 - 180))
    return out


def commanded_yaw_rate(att, window=0.5):
    """Commanded heading rate, sample by sample.

    The hover window must end at the moment the controller receives a yaw
    command. Otherwise several hovers on different headings merge into one
    window, and averaging over headings cancels the tilt from the wind,
    which is exactly the quantity being measured.
    """
    if not att:
        return []
    t = [x[0] for x in att]
    z = unwrap([x[4] for x in att])
    out, j = [], 0
    for i in range(len(t)):
        while j < len(t) - 1 and t[j] - t[i] < window:
            j += 1
        dt = t[j] - t[i]
        out.append((t[i], (z[j] - z[i]) / dt if dt > 1e-6 else 0.0))
    return out


def armed_periods(d):
    arm = sorted(t for t, i in d['events'] if i == EV_ARM)
    disarm = sorted(t for t, i in d['events'] if i == EV_DISARM)
    periods = []
    for a in arm:
        b = next((x for x in disarm if x > a), None)
        if b is not None:
            periods.append((a, b))
    return periods


def hover_windows(d, speed_threshold, height_threshold, min_window, min_throttle=MIN_THROTTLE,
                  yaw_rate_threshold=YAW_RATE_THRESHOLD):
    """Segments in which the aircraft really stands in the air.

    The throttle and arming conditions filter out ground tests: the propellers
    turn at idle, the aircraft stands still, and the altitude from the estimator
    has time to drift away by several metres. Without this the result would
    describe an aircraft standing on the ground.
    """
    periods = armed_periods(d)
    if not d['speed'] or not periods:
        return []
    rate = commanded_yaw_rate(d['att'])
    windows, start, prev = [], None, None
    for ts, v in d['speed']:
        h = value_at(d['altitude'], ts)
        g = value_at(d['throttle'], ts)
        o = value_at(rate, ts)
        hover = (any(a <= ts <= b for a, b in periods)
                 and v < speed_threshold and h is not None and h > height_threshold
                 and g is not None and g >= min_throttle
                 and (o is None or abs(o) < yaw_rate_threshold))
        if hover and start is None:
            start = ts
        elif not hover and start is not None:
            if prev - start >= min_window:
                windows.append((start, prev))
            start = None
        prev = ts
    if start is not None and prev - start >= min_window:
        windows.append((start, prev))
    return windows


def analyse_window(d, a, b):
    samples = [x for x in d['att'] if a <= x[0] <= b]
    if len(samples) < 10:
        return None
    roll = [x[1] for x in samples]
    pitch = [x[2] for x in samples]
    yaw = [x[3] for x in samples]

    mean_roll = statistics.fmean(roll)
    mean_pitch = statistics.fmean(pitch)

    # heading averaged as a vector, otherwise 350 and 10 deg give 180
    sy = statistics.fmean([math.sin(math.radians(k)) for k in yaw])
    cy = statistics.fmean([math.cos(math.radians(k)) for k in yaw])
    mean_yaw = math.degrees(math.atan2(sy, cy)) % 360

    # resultant tilt: hypotenuse of the averaged components.
    # Averaged before combining, so that gusts in both directions cancel
    # and only the constant component, the one from the wind, remains.
    theta = math.hypot(mean_roll, mean_pitch)

    # instantaneous tilt, a measure of air turbulence
    instantaneous = [math.hypot(r, p) for r, p in zip(roll, pitch)]

    # tilt vector in the aircraft axes: forward and right.
    # Forward tilt is negative Pitch (positive Pitch is nose up).
    forward, right = -mean_pitch, mean_roll
    fi = math.radians(mean_yaw)
    north = forward * math.cos(fi) - right * math.sin(fi)
    east = forward * math.sin(fi) + right * math.cos(fi)
    direction = math.degrees(math.atan2(east, north)) % 360

    return {
        'from': a, 'to': b, 'duration': b - a,
        'mean_roll': mean_roll, 'mean_pitch': mean_pitch,
        'mean_yaw': mean_yaw,
        'theta': theta,
        'theta_p95': percentile(instantaneous, 95),
        'direction': direction,
        'acceleration': G * math.tan(math.radians(theta)),
        'altitude': statistics.fmean(
            [h for ts, h in d['altitude'] if a <= ts <= b] or [float('nan')]),
    }


def report(path, args):
    d = load(path)
    windows = hover_windows(d, args.speed, args.height, args.min_window,
                            args.throttle, args.yaw_rate)
    results = [w for w in (analyse_window(d, a, b) for a, b in windows) if w]

    L = [f'## Wind: check from the flight log',
         '',
         f'*File: `{os.path.basename(path)}`. Computed by the script '
         f'`analysis/scripts/wind_from_log.py`.*',
         '']

    if not results:
        L.append('No hover window found that meets the conditions '
                 f'(aircraft armed, horizontal speed below '
                 f'{fmt(args.speed, 1)} m/s, altitude above '
                 f'{fmt(args.height, 1)} m, throttle at least '
                 f'{fmt(args.throttle, 2)}, duration at least '
                 f'{fmt(args.min_window, 0)} s). Without hover the tilt '
                 'describes a manoeuvre, not the wind.')
        return '\n'.join(L)

    L.append('| Window [log s] | Duration | Altitude | Heading | mean roll | mean pitch | '
             'Resultant tilt | p95 instantaneous | Wind from | '
             'Acceleration |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for w in results:
        signed = lambda v: ('+' if v >= 0 else '') + fmt(v)
        L.append(
            f'| {fmt(w["from"], 0)} -> {fmt(w["to"], 0)} | {fmt(w["duration"], 0)} s | '
            f'{fmt(w["altitude"], 1)} m | {fmt(w["mean_yaw"], 0)}° | '
            f'{signed(w["mean_roll"])}° | {signed(w["mean_pitch"])}° | '
            f'**{fmt(w["theta"])}°** | {fmt(w["theta_p95"])}° | '
            f'**{fmt(w["direction"], 0)}° ({compass_point(w["direction"])})** | '
            f'{fmt(w["acceleration"])} m/s² |')

    # agreement of direction between windows, as vectors
    sk = statistics.fmean([math.sin(math.radians(w['direction'])) for w in results])
    ck = statistics.fmean([math.cos(math.radians(w['direction'])) for w in results])
    session_direction = math.degrees(math.atan2(sk, ck)) % 360
    consistency = math.hypot(sk, ck)      # 1 = all windows agree, 0 = scatter
    session_theta = statistics.fmean([w['theta'] for w in results])

    L.append('')
    count = 'one hover window' if len(results) == 1 else f'{len(results)} hover windows'
    L.append(f'**Resultant from {count}:** wind from '
             f'**{fmt(session_direction, 0)}° '
             f'({compass_point(session_direction)})**, tilt '
             f'**{fmt(session_theta)}°**, horizontal acceleration '
             f'{fmt(G * math.tan(math.radians(session_theta)))} m/s². '
             f'Direction consistency between windows: {fmt(consistency)} '
             f'(1.00 means full agreement).')

    if consistency < 0.8:
        L.append('')
        L.append('The direction scatter between windows is large. Either the wind '
                 'was variable, or the aircraft did not stand still in the hover '
                 'windows. The result should then not be given as the session wind direction.')

    L.append('')
    L.append('**How to read this.** The resultant tilt is the averaged constant '
             'component of the tilt; gusts in both directions cancel in it, '
             'leaving the tilt needed to hold position against the wind. '
             'The p95 of the instantaneous tilt describes the turbulence of the air: '
             'the difference between these two numbers grows in gusty wind. '
             'The direction is the one the wind blows **from**. '
             'The horizontal acceleration is g*tan(tilt), a quantity '
             'proportional to the wind force and independent of the aircraft mass, '
             'hence comparable also after a change of equipment.')
    L.append('')
    L.append('**What is not here.** Speed in metres per second. Computing it '
             'requires the product of the drag coefficient and the frontal area, '
             'which has not been determined for this aircraft. The speed binding '
             'for the rejection criteria of protocol §8 comes from the anemometer; '
             'procedure in `docs/protocol/ANNEX_C_wind_measurement.md`.')
    return '\n'.join(L)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Wind direction and strength indicator from the tilt in hover.')
    p.add_argument('logs', nargs='+', help='.bin files')
    p.add_argument('--speed', type=float, default=SPEED_THRESHOLD,
                   help='horizontal-speed threshold for hover [m/s]')
    p.add_argument('--height', type=float, default=HEIGHT_THRESHOLD,
                   help='minimum altitude of a hover window [m]')
    p.add_argument('--min-window', type=float, default=MIN_WINDOW,
                   help='shortest accepted hover window [s]')
    p.add_argument('--throttle', type=float, default=MIN_THROTTLE,
                   help='smallest mean throttle regarded as flight')
    p.add_argument('--yaw-rate', type=float, default=YAW_RATE_THRESHOLD,
                   help='commanded yaw rate [deg/s] above which the hover window '
                        'is ended')
    a = p.parse_args()
    for path in sorted(a.logs):
        try:
            print(report(path, a), '\n')
        except Exception as e:
            print(f'### {os.path.basename(path)}\nERROR: {e}\n', file=sys.stderr)
