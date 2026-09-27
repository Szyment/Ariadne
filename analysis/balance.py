#!/usr/bin/env python3
"""
Aircraft balance and torque asymmetry, from motor loading.

Answers two questions:

1. Whether the battery went back to the same place after charging.
2. Whether the frame is symmetrical, that is, whether the aircraft does not
   have to fight a constant moment about the vertical axis.

A multirotor with a shifted centre of gravity **does not tilt**: the
controller balances the moment with a thrust difference and the aircraft
hovers level. The only trace is uneven motor loading. That is why a payload
offset is visible neither on the aircraft nor in telemetry; it is visible
only in the flight log.

    python3 balance.py ../../flight-logs/platform-2-ardupilot/log_8_*.bin

Requires: pymavlink.

--- Two things that must be separated ---------------------------------------

Uneven motor loading along the fore-aft and left-right axes has two causes
at once:

- **centre-of-gravity offset**: fixed in the aircraft axes, rotates with it;
- **moment from air drag**: drag acts at a different height than the centre
  of gravity, so tilt in wind by itself produces an asymmetry; this one is
  fixed relative to the ground, because the wind blows from one side
  regardless of how the aircraft is turned.

The script separates them when the record contains at least two hover
windows with clearly different headings. The quantity constant in the
aircraft axes is the payload, the quantity constant relative to the ground
is the wind. With a single heading they cannot be separated and the script
does not pretend to.

Torque asymmetry is free of this confusion: wind produces no steady moment
about the vertical axis. If the motors turning in one direction work
persistently harder than the other pair, the cause is mechanical.

--- ArduCopter Quad X motor layout ------------------------------------------

    3 (front left, CW)     1 (front right, CCW)
                  \\       /
                   \\     /
                    \\   /
                     ---
                    /   \\
                   /     \\
    2 (rear left, CCW)      4 (rear right, CW)
"""
import argparse
import math
import os
import statistics

from pymavlink import mavutil

EV_ARM, EV_DISARM = 10, 11

SPEED_THRESHOLD = 0.7     # m/s
HEIGHT_THRESHOLD = 2.0    # m
MIN_WINDOW = 15.0         # s
MIN_THROTTLE = 0.10       # fraction; below this the aircraft is not flying, only spinning the propellers
YAW_RATE_THRESHOLD = 1.0  # deg/s of commanded yaw; above this the window ends

FRONT, REAR = (1, 3), (2, 4)
RIGHT, LEFT = (1, 4), (2, 3)
CCW, CW = (1, 2), (3, 4)

DEFAULT_SPACING = 354.0   # mm; the X500 V2 has 500 mm diagonally -> 500*cos45

DESCRIPTION = {1: ('front right', 'CCW'), 2: ('rear left', 'CCW'),
               3: ('front left', 'CW'), 4: ('rear right', 'CW')}


def fmt(x, places=1):
    if x is None:
        return 'n/a'
    return f'{x:.{places}f}'


def signed(x, places=1):
    return ('+' if x >= 0 else '') + fmt(x, places)


def compass_point(degrees):
    rose = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return rose[int((degrees % 360) / 22.5 + 0.5) % 16]


def unwrap(angles):
    """Sequence of angles without the jump through 360 deg."""
    out = [angles[0]]
    for k in angles[1:]:
        out.append(out[-1] + ((k - out[-1] + 180) % 360 - 180))
    return out


def solve(A, b):
    """Least squares through the normal equations. No dependencies."""
    n = len(A[0])
    M = [[sum(A[k][i] * A[k][j] for k in range(len(A))) for j in range(n)]
         + [sum(A[k][i] * b[k] for k in range(len(A)))] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[p][i]) < 1e-12:
            return None
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r == i:
                continue
            f = M[r][i] / M[i][i]
            for c in range(i, n + 1):
                M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]


# --- log reading ------------------------------------------------------------

def load(path):
    m = mavutil.mavlink_connection(path)
    d = {'rcou': [], 'speed': [], 'ctun': [], 'att': [], 'events': [],
         'parm': {}}
    while True:
        try:
            msg = m.recv_match(blocking=False)
        except Exception:
            continue
        if msg is None:
            break
        typ = msg.get_type()
        if typ == 'PARM':
            if msg.Name in ('MOT_PWM_MIN', 'MOT_PWM_MAX', 'FRAME_CLASS',
                            'FRAME_TYPE', 'MOT_THST_HOVER', 'MOT_THST_EXPO',
                            'MOT_YAW_HEADROOM'):
                d['parm'][msg.Name] = msg.Value
            continue
        t = getattr(msg, 'TimeUS', None)
        if t is None:
            continue
        ts = t / 1e6
        if typ == 'RCOU':
            d['rcou'].append((ts, msg.C1, msg.C2, msg.C3, msg.C4))
        elif typ == 'GPS' and getattr(msg, 'Status', 0) >= 3:
            d['speed'].append((ts, msg.Spd))
        elif typ == 'CTUN':
            d['ctun'].append((ts, msg.Alt, getattr(msg, 'ThO', 0)))
        elif typ == 'ATT':
            d['att'].append((ts, msg.Roll, msg.Pitch, msg.Yaw,
                             getattr(msg, 'DesYaw', msg.Yaw)))
        elif typ == 'EV' and msg.Id in (EV_ARM, EV_DISARM):
            d['events'].append((ts, msg.Id))
    return d


def armed_periods(d):
    arm = sorted(t for t, i in d['events'] if i == EV_ARM)
    disarm = sorted(t for t, i in d['events'] if i == EV_DISARM)
    periods = []
    for a in arm:
        b = next((x for x in disarm if x > a), None)
        if b is not None:
            periods.append((a, b))
    return periods


def value_at(series, ts, column=1):
    return min(series, key=lambda x: abs(x[0] - ts))[column] if series else None


def commanded_yaw_rate(att, window=0.5):
    """Commanded heading rate, sample by sample.

    Needed so that the hover window ends at the moment the controller
    receives a yaw command. Otherwise four hovers on four headings merge
    into one window with an averaged heading, and together with the heading
    the tilt from the wind is averaged too, so exactly what is being
    measured disappears.
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


def hover_windows(d, args):
    """Flight segments in hover: armed, in the air, almost motionless."""
    periods = armed_periods(d)
    if not periods or not d['speed']:
        return []
    rate = commanded_yaw_rate(d['att'])
    windows, start, prev = [], None, None
    for ts, v in d['speed']:
        in_flight = any(a <= ts <= b for a, b in periods)
        h = value_at(d['ctun'], ts, 1)
        throttle = value_at(d['ctun'], ts, 2)
        yaw_rate = value_at(rate, ts, 1)
        hover = (in_flight and v < args.speed and h is not None
                 and h > args.height and throttle is not None and throttle >= args.throttle
                 and (yaw_rate is None or abs(yaw_rate) < args.yaw_rate))
        if hover and start is None:
            start = ts
        elif not hover and start is not None:
            if prev - start >= args.min_window:
                windows.append((start, prev))
            start = None
        prev = ts
    if start is not None and prev - start >= args.min_window:
        windows.append((start, prev))
    return windows


# --- computation ------------------------------------------------------------

def thrust_from_output(t, expo):
    """Thrust from the output, according to the ArduPilot curve.

    AP_Motors linearises the propeller characteristic with the formula
    thrust = (1 - expo)*t + expo*t^2, where t is the output normalised to
    the range 0-1 and expo is `MOT_THST_EXPO`. The approximation by the
    square alone overstates the relative differences between motors by
    roughly half, so at this expo value it gave offsets larger than the
    physics implies.
    """
    t = max(0.0, min(1.0, t))
    return (1.0 - expo) * t + expo * t * t


def analyse_window(d, a, b, args, pwm_min, span, expo):
    r = [x for x in d['rcou'] if a <= x[0] <= b]
    at = [x for x in d['att'] if a <= x[0] <= b]
    if len(r) < 30 or len(at) < 10:
        return None

    mean = {i: statistics.fmean([p[i] for p in r]) for i in (1, 2, 3, 4)}
    thrust = {i: thrust_from_output((mean[i] - pwm_min) / span, expo)
              for i in mean}
    total = sum(thrust.values()) or 1e-9

    def offset(group_a, group_b):
        x = sum(thrust[i] for i in group_a)
        y = sum(thrust[i] for i in group_b)
        return args.spacing * (x - y) / (2 * (x + y))

    duration = max(1e-6, at[-1][0] - at[0][0])
    headings = unwrap([x[3] for x in at])
    commanded = unwrap([x[4] for x in at])
    heading = headings[len(headings) // 2] % 360
    rate = (headings[-1] - headings[0]) / duration
    commanded_rate = (commanded[-1] - commanded[0]) / duration

    return {
        'from': a, 'to': b, 'duration': b - a, 'samples': len(r),
        'altitude': statistics.fmean([x[1] for x in d['ctun'] if a <= x[0] <= b]),
        'throttle': statistics.fmean([x[2] for x in d['ctun'] if a <= x[0] <= b]),
        'pwm': mean, 'thrust': thrust,
        'heading': heading, 'yaw_rate': rate,
        'commanded_rate': commanded_rate,
        'commanded_turn': abs(commanded_rate) > 1.0,
        'roll': statistics.fmean([x[1] for x in at]),
        'pitch': statistics.fmean([x[2] for x in at]),
        'fore': offset(FRONT, REAR),
        'right': offset(RIGHT, LEFT),
        'torque': 100 * (sum(thrust[i] for i in CCW)
                         - sum(thrust[i] for i in CW)) / total,
        # mixer yaw output: the mixer adds +y to the CCW pair and -y to the CW pair
        'yaw_us': (sum(mean[i] for i in CCW) - sum(mean[i] for i in CW)) / 4.0,
    }


def separate(windows):
    """Separates the offset into an aircraft-fixed and a ground-fixed part.

    Model: offset seen in the aircraft axes = payload (fixed in the aircraft
    axes) + wind (fixed relative to the ground, rotated into the aircraft axes).
    """
    headings = [w['heading'] for w in windows]
    sk = statistics.fmean([math.sin(math.radians(k)) for k in headings])
    ck = statistics.fmean([math.cos(math.radians(k)) for k in headings])
    spread = 1 - math.hypot(sk, ck)     # 0 = one heading, grows with the spread
    if len(windows) < 2 or spread < 0.02:
        return None, spread

    A, bb = [], []
    for w in windows:
        f = math.radians(w['heading'])
        A.append([1.0, 0.0, math.cos(f), math.sin(f)])
        bb.append(w['fore'])
        A.append([0.0, 1.0, -math.sin(f), math.cos(f)])
        bb.append(w['right'])
    x = solve(A, bb)
    if x is None:
        return None, spread
    return {'cg_fore': x[0], 'cg_right': x[1],
            'wind_n': x[2], 'wind_e': x[3]}, spread


# --- report -----------------------------------------------------------------

def report(path, args):
    d = load(path)
    pwm_min = d['parm'].get('MOT_PWM_MIN', 1000.0)
    span = d['parm'].get('MOT_PWM_MAX', 2000.0) - pwm_min
    expo = d['parm'].get('MOT_THST_EXPO', 0.65)

    windows = [w for w in (analyse_window(d, a, b, args, pwm_min, span, expo)
                           for a, b in hover_windows(d, args)) if w]
    rough = False
    if not windows:
        # no hover: take the whole arming periods in which the aircraft
        # really flew. Motion disturbs the fore-aft and left-right axes,
        # but the torque asymmetry survives as long as the heading was steady.
        fallback = []
        for a, b in armed_periods(d):
            c = [x for x in d['ctun'] if a <= x[0] <= b]
            if b - a >= args.min_window and c and statistics.fmean(
                    [x[2] for x in c]) >= args.throttle:
                fallback.append((a, b))
        windows = [w for w in (analyse_window(d, a, b, args, pwm_min, span, expo)
                               for a, b in fallback) if w]
        rough = bool(windows)

    L = ['## Balance and symmetry: from motor loading in hover',
         '',
         f'*File: `{os.path.basename(path)}`. Computed by the script '
         f'`analysis/scripts/balance.py`.*',
         '']

    if not windows:
        L.append('No hover window found that meets the conditions: aircraft '
                 f'armed, horizontal speed below {fmt(args.speed, 1)} '
                 f'm/s, altitude above {fmt(args.height, 1)} m, throttle at '
                 f'least {fmt(args.throttle, 2)}, duration at least '
                 f'{fmt(args.min_window, 0)} s.')
        L.append('')
        L.append('The throttle condition filters out ground tests, in which the '
                 'propellers turn at idle and the altitude from the estimator '
                 'has time to drift away by several metres. Without it the result '
                 'would describe an aircraft standing on the ground.')
        return '\n'.join(L)

    if d['parm'].get('FRAME_CLASS') != 1 or d['parm'].get('FRAME_TYPE') != 1:
        L.append(f'**Note:** the computation assumes a Quad X layout, but the log has '
                 f'`FRAME_CLASS` = {d["parm"].get("FRAME_CLASS")}, '
                 f'`FRAME_TYPE` = {d["parm"].get("FRAME_TYPE")}.')
        L.append('')

    if rough:
        L.append('**No hover window: rough computation.** This record contains '
                 'no segment in which the aircraft stood still in the air '
                 'long enough, so whole flight periods were taken. '
                 'The fore-aft and left-right offsets are therefore '
                 'disturbed by acceleration and braking and **are not '
                 'suitable as a reference value**. The torque asymmetry '
                 'remains reliable as long as the heading was settled.')
        L.append('')
        L.append('### Flight periods')
    else:
        L.append('### Hover windows')
    L.append('')
    L.append('| Window [s] | Duration | Alt. | Throttle | Heading | Actual yaw rate | '
             'Commanded yaw rate | mean roll | mean pitch | M1 | M2 | M3 | M4 | '
             'fore-aft | left-right | torque |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for w in windows:
        L.append(
            f'| {fmt(w["from"], 0)}->{fmt(w["to"], 0)} | {fmt(w["duration"], 0)} s | '
            f'{fmt(w["altitude"], 1)} m | {fmt(w["throttle"], 3)} | '
            f'{fmt(w["heading"], 0)}° | {signed(w["yaw_rate"], 2)} °/s | '
            f'{signed(w["commanded_rate"], 2)} °/s | '
            f'{signed(w["roll"], 2)}° | {signed(w["pitch"], 2)}° | '
            + ' | '.join(fmt(w['pwm'][i], 0) for i in (1, 2, 3, 4)) +
            f' | {signed(w["fore"])} mm | {signed(w["right"])} mm | '
            f'{signed(w["torque"])} % |')
    L.append('')
    L.append('Signs: fore-aft positive means loading at the front, '
             'left-right positive means loading on the right side. Torque positive means '
             'that the pair of motors turning counter-clockwise '
             'works harder.')

    # --- torque symmetry: a clean signal, independent of wind ---------------
    clean = [w for w in windows if not w['commanded_turn']]
    L.append('')
    L.append('### Torque symmetry')
    L.append('')
    if not clean:
        L.append('In all windows the controller had a commanded heading turn, '
                 'so the loading difference between the motor pairs describes '
                 'the turn being executed, not a frame asymmetry. This assessment '
                 'needs a hover with a settled heading.')
        torque = yaw_rate = None
    else:
        torque = statistics.fmean([w['torque'] for w in clean])
        yaw_rate = statistics.fmean([w['yaw_rate'] for w in clean])
        skipped = len(windows) - len(clean)
        yaw_us = statistics.fmean([w['yaw_us'] for w in clean])
        headroom = d['parm'].get('MOT_YAW_HEADROOM', 200.0)
        L.append(f'Mean asymmetry: **{signed(torque)} %** of thrust share, '
                 f'corresponding to a constant mixer yaw output of '
                 f'**{signed(yaw_us, 0)} µs**. Mean yaw rate: '
                 f'{signed(yaw_rate, 2)} °/s. Computed from {len(clean)} windows '
                 f'with a settled heading'
                 + (f'; {skipped} windows skipped because the controller was '
                    f'executing a commanded turn in them.' if skipped else '.'))
        L.append('')
        L.append(f'`MOT_YAW_HEADROOM` = {fmt(headroom, 0)} µs, so the aircraft uses '
                 f'**{fmt(100 * abs(yaw_us) / headroom, 0)} % of the reserved '
                 f'yaw control headroom already in calm hover**. '
                 f'The rest remains for gusts and commanded turns.')
        L.append('')
    if torque is None:
        pass
    elif abs(torque) < 5:
        L.append('A value within the scatter of motors and ESCs. '
                 'Nothing indicates a mechanical asymmetry.')
    else:
        L.append(f'**Asymmetry exceeds 5%.** Wind produces no steady '
                 f'moment about the vertical axis, so the cause is '
                 f'mechanical: an arm twisted in its clamp, a tilted '
                 f'motor or a propeller of a different type on one of the mounts. '
                 f'The aircraft in hover constantly fights this moment, which takes '
                 f'yaw control headroom and loads one pair of motors.')
        if yaw_rate is not None and abs(yaw_rate) > 0.5:
            L.append('')
            L.append(f'In addition the aircraft in hover **rotates at '
                     f'{fmt(abs(yaw_rate), 2)} °/s**, that is, the yaw controller '
                     f'is not winning this fight. This is no longer cosmetic.')

    # --- separating payload from wind --------------------------------------
    L.append('')
    L.append('### Payload offset versus wind effect')
    L.append('')
    split, spread = (None, 0.0) if rough else separate(windows)
    if rough:
        L.append('Skipped: without hover the payload offset and the moment from '
                 'the wind cannot be separated, and the raw values themselves '
                 'describe mainly manoeuvring.')
    elif split is None:
        mean_f = statistics.fmean([w['fore'] for w in windows])
        mean_r = statistics.fmean([w['right'] for w in windows])
        L.append(f'All windows have a similar heading (spread measure '
                 f'{fmt(spread, 3)}), so the payload offset cannot be '
                 f'separated from the moment from the wind. Raw values: '
                 f'fore-aft {signed(mean_f)} mm, left-right {signed(mean_r)} mm; '
                 f'both contain both causes at once.')
        L.append('')
        L.append('For the separation to be possible, the record must contain at '
                 'least two hover windows with headings differing by several tens of '
                 'degrees. In the mission `S-04_Test1.plan` a hover at two '
                 'opposite corners of the square is enough.')
    else:
        cg = math.hypot(split['cg_fore'], split['cg_right'])
        wind = math.hypot(split['wind_n'], split['wind_e'])
        # The moment from air drag acts opposite to the tilt, so the vector
        # computed from motor loading points to the lee side. 180 deg is added
        # to give the direction in the same convention as the anemometer and
        # `wind_from_log.py`: the one the wind blows FROM.
        azimuth = (math.degrees(math.atan2(split['wind_e'],
                                           split['wind_n'])) + 180) % 360
        L.append('| | |')
        L.append('|---|---|')
        L.append(f'| Payload, fore-aft | **{signed(split["cg_fore"])} mm** |')
        L.append(f'| Payload, left-right | **{signed(split["cg_right"])} mm** |')
        L.append(f'| Payload, resultant | **{fmt(cg)} mm** |')
        L.append(f'| Wind part, resultant | {fmt(wind)} mm, '
                 f'from {fmt(azimuth, 0)}° ({compass_point(azimuth)}) |')
        L.append(f'| Heading spread between windows | {fmt(spread, 3)} |')
        L.append('')
        if spread < 0.15:
            L.append('**The separation is ill-conditioned.** A heading spread '
                     'below 0.15 corresponds to hover windows lying within a fan '
                     'narrower than roughly 60 deg. With such material the computation '
                     'has nothing to decide from how much falls on the payload and how much '
                     'on the wind, and the split between these two items is largely arbitrary. '
                     '**These two numbers should not be quoted.** The raw values in the '
                     'window table and the torque asymmetry remain reliable.')
            L.append('')
            L.append('Material that would suffice: a 30 s hover on four '
                     'headings differing by 90 deg, in light wind. '
                     'One battery, one flight.')
            L.append('')
        L.append('The separation rests on the payload offset being fixed in the '
                 'aircraft axes and the moment from the wind fixed relative to the ground. '
                 'The direction in the "wind part" row was computed from the motor loading '
                 'distribution, that is, from an entirely different signal than the '
                 'airframe tilt used by `wind_from_log.py`. Agreement of the two is an '
                 'independent check that the separation makes sense.')
        L.append('')
        if cg < 5:
            L.append('The payload sits level.')
        elif cg < 15:
            L.append('Moderate payload offset. Harmless in itself, but if it '
                     'differs from previous sessions, the pack went back to a different place.')
        else:
            L.append('**Large payload offset.** Check the pack position and '
                     'whether anything has come loose.')

    L.append('')
    L.append(f'Windows: {len(windows)}, motor-loading samples: '
             f'{sum(w["samples"] for w in windows)}. Spacing assumed in the '
             f'computation: {fmt(args.spacing, 0)} mm.')
    L.append('')
    L.append('**How to use this.** What matters is the change between sessions, '
             'not the number itself: motors and ESCs are not identical, so '
             'even a well-balanced aircraft shows a few millimetres. Establish '
             'a reference value from a flight in which the pack certainly sat '
             'correctly, and compare against it.')
    return '\n'.join(L)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Payload offset and frame symmetry from motor loading.')
    p.add_argument('logs', nargs='+')
    p.add_argument('--spacing', type=float, default=DEFAULT_SPACING,
                   help='distance between the front and rear motor axes '
                        '[mm]; default 354 for a 500 mm frame in X layout')
    p.add_argument('--speed', type=float, default=SPEED_THRESHOLD)
    p.add_argument('--height', type=float, default=HEIGHT_THRESHOLD)
    p.add_argument('--throttle', type=float, default=MIN_THROTTLE,
                   help='smallest mean throttle regarded as flight')
    p.add_argument('--min-window', type=float, default=MIN_WINDOW)
    p.add_argument('--yaw-rate', type=float, default=YAW_RATE_THRESHOLD,
                   help='commanded yaw rate [deg/s] above which the hover window '
                        'is ended')
    a = p.parse_args()
    for path in sorted(a.logs):
        print(report(path, a), '\n')
