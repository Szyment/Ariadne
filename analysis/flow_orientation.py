#!/usr/bin/env python3
"""
Optical-flow sensor orientation, checked from the flight log.

The parameter FLOW_ORIENT_YAW says how the sensor is rotated relative to the
nose of the aircraft. An error of 90 or 180 deg shows no symptom as long as the
aircraft flies on GNSS, because optical flow does not then enter the estimator
as a velocity source. It shows up only in the first second of the first
GNSS-denied run, that is, at the worst possible moment.

    python3 flow_orientation.py ../../flight-logs/platform-2-ardupilot/*.bin

Requires: pymavlink.

--- What the check consists of ---------------------------------------------

While the aircraft rotates, the flow sensor sees the image moving and measures
an angular rate, the same one the gyroscope measures. ArduPilot logs both in
the `OF` message: `flowX` and `flowY` are the sensor reading, `bodyX` and
`bodyY` the angular rate from the gyroscope, both brought to the same frame
by `FLOW_ORIENT_YAW`.

If the parameter is set correctly, `flowX` follows `bodyX` and `flowY` follows
`bodyY`. The script computes the correlation coefficients for both matching
pairs and for the crossed pairs and decides on that basis:

- matching pairs high and positive, crossed pairs near zero: orientation correct;
- matching pairs near zero and crossed pairs high: rotation by 90 or 270 deg;
- matching pairs high and **negative**: rotation by 180 deg.

The method comes from the ArduPilot documentation, where it is described as
a comparison of traces on a plot. The script replaces looking at the plot
with a number.

--- Why from a flight and not from a bench test ------------------------------

A test held in the hands above the floor works too, but the flight record is
better for three reasons: there are more rotations and they are faster, the
surface under the aircraft is the one the measurements will be made over, and
the material already exists, so nothing extra has to be done.

Condition: the record must contain enough segments with clear rotation. A calm
hover from start to end is not enough.
"""
import argparse
import math
import os
import statistics

from pymavlink import mavutil

ROTATION_THRESHOLD = 0.15   # rad/s; below this the rotation is lost in noise
MIN_SAMPLES = 500
AGREEMENT_THRESHOLD = 0.4   # correlation regarded as clear


def fmt(x, places=3):
    if x is None:
        return 'n/a'
    return f'{x:+.{places}f}'


def correlation(a, b):
    n = len(a)
    if n < 2:
        return None
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((x - mb) ** 2 for x in b))
    if sa == 0 or sb == 0:
        return None
    return sum((a[i] - ma) * (b[i] - mb) for i in range(n)) / (sa * sb)


def load(path):
    m = mavutil.mavlink_connection(path)
    of, parm = [], {}
    while True:
        try:
            msg = m.recv_match(blocking=False)
        except Exception:
            continue
        if msg is None:
            break
        typ = msg.get_type()
        if typ == 'PARM':
            if msg.Name in ('FLOW_ORIENT_YAW', 'FLOW_TYPE', 'EK3_SRC2_VELXY'):
                parm[msg.Name] = msg.Value
        elif typ == 'OF':
            of.append((msg.TimeUS / 1e6, msg.Qual, msg.flowX, msg.flowY,
                       msg.bodyX, msg.bodyY))
    return of, parm


def report(path, args):
    of, parm = load(path)
    L = [f'### {os.path.basename(path)}']

    if not of:
        L.append('No `OF` messages: the flow sensor was not logged.')
        return '\n'.join(L)

    sel = [x for x in of if math.hypot(x[4], x[5]) > args.threshold]
    L.append(f'`OF` samples: {len(of)}, of which with rotation above '
             f'{fmt(args.threshold, 2)[1:]} rad/s: {len(sel)}.')

    if len(sel) < MIN_SAMPLES:
        L.append(f'Too few segments with clear rotation to decide anything '
                 f'(at least {MIN_SAMPLES} needed). '
                 f'A record with manoeuvring is required, not just hover.')
        return '\n'.join(L)

    fx = [x[2] for x in sel]
    fy = [x[3] for x in sel]
    bx = [x[4] for x in sel]
    by = [x[5] for x in sel]

    matching = [correlation(fx, bx), correlation(fy, by)]
    crossed = [correlation(fx, by), correlation(fy, bx)]

    L.append('')
    L.append('| Pair | Correlation |')
    L.append('|---|---|')
    L.append(f'| flowX <-> bodyX | **{fmt(matching[0])}** |')
    L.append(f'| flowY <-> bodyY | **{fmt(matching[1])}** |')
    L.append(f'| flowX <-> bodyY | {fmt(crossed[0])} |')
    L.append(f'| flowY <-> bodyX | {fmt(crossed[1])} |')

    if parm:
        L.append('')
        L.append('Parameters in the log: ' + ', '.join(
            f'`{k}` = {v:g}' for k, v in sorted(parm.items())))

    z = [c for c in matching if c is not None]
    s = [c for c in crossed if c is not None]
    L.append('')
    if not z or not s:
        L.append('The correlations could not be computed.')
    elif min(z) > AGREEMENT_THRESHOLD and max(abs(c) for c in s) < AGREEMENT_THRESHOLD:
        L.append('**Orientation correct.** The matching pairs are clearly positive '
                 'and the crossed pairs near zero: the sensor is rotated as '
                 '`FLOW_ORIENT_YAW` declares.')
    elif max(z) < -AGREEMENT_THRESHOLD or (max(z) < AGREEMENT_THRESHOLD
                                           and min(z) < -AGREEMENT_THRESHOLD):
        L.append('**Rotation by 180 deg.** The matching pairs have a high but '
                 'negative correlation. Add 180 to `FLOW_ORIENT_YAW`.')
    elif max(abs(c) for c in s) > AGREEMENT_THRESHOLD:
        L.append('**Rotation by 90 or 270 deg.** The axes are swapped: flow '
                 'in one axis follows rotation in the other. The sign of the '
                 'crossed correlation says which way.')
    else:
        L.append('**No decision.** No pair shows clear agreement. '
                 'Possible causes: the sensor does not see the surface '
                 '(check `OF.Qual` and the illuminance), it is not pointed '
                 'downwards, or the record contains too few rotations.')

    quality = [x[1] for x in sel]
    lo, hi = min(quality), max(quality)
    L.append('')
    L.append(f'Image quality `OF.Qual`: {lo}-{hi}, median '
             f'{statistics.median(quality):.0f}.')
    if lo == hi == 255:
        L.append('The value stays at the maximum, so the sensor sees the '
                 'ground with a large margin. Over grass in daylight this is '
                 'expected. A drop in this number at dusk will be the first '
                 'sign of approaching the operating limit.')
    elif hi - lo < 5:
        L.append('The value is practically constant. Check whether the driver '
                 'reports a real quality before treating it as a measure of visibility.')
    return '\n'.join(L)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Check of FLOW_ORIENT_YAW from the flight log.')
    p.add_argument('logs', nargs='+')
    p.add_argument('--threshold', type=float, default=ROTATION_THRESHOLD,
                   help='angular-rate threshold [rad/s] regarded as rotation')
    a = p.parse_args()
    for path in sorted(a.logs):
        print(report(path, a), '\n')
