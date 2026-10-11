#!/usr/bin/env python3
"""Scale-error observable for GNSS-denied optical-flow runs (v0.1, 4 Oct 2026).

Idea: with optical flow as the only horizontal velocity source, a constant scale error k on the
flow velocity is invisible to the EKF innovations in steady flight (the velocity state follows
k * v). The only unscaled quantity on board is the IMU. During a horizontal acceleration or
deceleration the IMU gives a velocity change dv_imu that the flow-driven EKF velocity must match;
with a scale error the EKF velocity changes by k * dv_imu. The ratio dv_ekf / dv_imu over an
acceleration phase is therefore an estimate of k that needs no GNSS. A constant accelerometer bias
adds +b*dt to the acceleration phase and +b*dt to the deceleration phase while dv_ekf flips sign,
so the pair (|dv_acc| + |dv_dec|) cancels the bias.

Input: run CSV from cut_runs.py v0.3 (columns imu_acc*, xkf1_V*, xkf2_A*, roll/pitch/yaw).
Output: one row per run with the per-phase ratios and the reference path ratio (estimator / GNSS),
plus the correlation across runs. Reference uses GNSS and is for validation only.

Usage: python3 scale_observable.py analysis/data/E1/ARIADNE_E1_0*.csv --csv analysis/results/scale_observable.csv
"""
import csv, math, argparse, sys
import numpy as np
R = 6371000.0
G = 9.80665

def rot_body_to_ned(roll, pitch, yaw):
    cr, sr = math.cos(roll), math.sin(roll); cp, sp = math.cos(pitch), math.sin(pitch); cy, sy = math.cos(yaw), math.sin(yaw)
    return np.array([[cp*cy, sr*sp*cy - cr*sy, cr*sp*cy + sr*sy],
                     [cp*sy, sr*sp*sy + cr*cy, cr*sp*sy - sr*cy],
                     [-sp,   sr*cp,            cr*cp]])

def analyse(path, a_min=0.3, min_len=0.8, bias_correct=False):
    rows = [r for r in csv.DictReader(open(path)) if r['phase'] == 'flow_only']
    if len(rows) < 50 or 'imu_accX' not in rows[0]:
        return None
    t = np.array([float(r['t_log_s']) for r in rows])
    vn = np.array([float(r['xkf1_VN']) for r in rows]); ve = np.array([float(r['xkf1_VE']) for r in rows])
    acc_b = np.array([[float(r['imu_accX']), float(r['imu_accY']), float(r['imu_accZ'])] for r in rows])
    if bias_correct:
        acc_b = acc_b - np.array([[float(r['xkf2_AX']), float(r['xkf2_AY']), float(r['xkf2_AZ'])] for r in rows]) / 100.0
    att = np.radians(np.array([[float(r['roll']), float(r['pitch']), float(r['yaw'])] for r in rows]))
    # NED acceleration from IMU (specific force rotated, gravity added: a_ned = R f + g, g = +9.81 down)
    a_ned = np.array([rot_body_to_ned(*att[i]) @ acc_b[i] for i in range(len(rows))])
    a_ned[:, 2] += G
    # reference path ratio
    la = np.array([float(r['ekf_lat']) for r in rows]); lo = np.array([float(r['ekf_lon']) for r in rows])
    gla = np.array([float(r['gps_lat']) for r in rows]); glo = np.array([float(r['gps_lon']) for r in rows])
    c = math.cos(math.radians(la[0]))
    def plen(a, b):
        return float(np.sum(R * np.hypot(np.radians(np.diff(b)) * c, np.radians(np.diff(a)))))
    ratio_ref = plen(la, lo) / plen(gla, glo)
    # EKF horizontal speed and its derivative (smoothed) -> acceleration phases
    sp = np.hypot(vn, ve)
    k = 5
    sps = np.convolve(sp, np.ones(k) / k, 'same')
    dsp = np.gradient(sps, t)
    dsp = np.convolve(dsp, np.ones(k) / k, 'same')
    phases = []  # (i0, i1, sign)
    i = 0
    while i < len(t):
        if abs(dsp[i]) > a_min:
            s = np.sign(dsp[i]); j = i
            while j < len(t) and np.sign(dsp[j]) == s and abs(dsp[j]) > a_min * 0.5:
                j += 1
            if t[j - 1] - t[i] >= min_len:
                phases.append((i, j - 1, int(s)))
            i = j
        else:
            i += 1
    out = []
    for i0, i1, s in phases:
        dv_ekf = np.array([vn[i1] - vn[i0], ve[i1] - ve[i0]])
        # trapezoidal integral of the IMU horizontal acceleration
        dv_imu = np.array([np.trapz(a_ned[i0:i1 + 1, 0], t[i0:i1 + 1]), np.trapz(a_ned[i0:i1 + 1, 1], t[i0:i1 + 1])])
        n = np.linalg.norm(dv_imu)
        if n < 0.3:
            continue
        u = dv_imu / n
        out.append((s, float(dv_ekf @ u), float(n), float(t[i1] - t[i0])))
    acc = [o for o in out if o[0] > 0]; dec = [o for o in out if o[0] < 0]
    r_acc = np.mean([o[1] / o[2] for o in acc]) if acc else float('nan')
    r_dec = np.mean([o[1] / o[2] for o in dec]) if dec else float('nan')
    # pairwise: sum of |dv| over accel and decel phases (bias cancels)
    r_pair = (sum(abs(o[1]) for o in out) / sum(o[2] for o in out)) if out else float('nan')
    return dict(run=path.split('/')[-1][:-4], ratio_ref=ratio_ref, r_acc=r_acc, r_dec=r_dec, r_pair=r_pair,
                n_acc=len(acc), n_dec=len(dec), dv_sum=sum(o[2] for o in out))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--csv'); ap.add_argument('--bias-correct', action='store_true')
    ap.add_argument('--a-min', type=float, default=0.3)
    a = ap.parse_args()
    res = [x for x in (analyse(f, a.a_min, bias_correct=a.bias_correct) for f in a.files) if x]
    print('run                                              ref    r_acc  r_dec  r_pair n_acc n_dec dv_sum')
    for x in res:
        print(f"{x['run'][:48]:48s} {x['ratio_ref']:.3f}  {x['r_acc']:.3f}  {x['r_dec']:.3f}  {x['r_pair']:.3f}  {x['n_acc']:3d}  {x['n_dec']:3d}  {x['dv_sum']:.1f}")
    arr = np.array([[x['ratio_ref'], x['r_acc'], x['r_dec'], x['r_pair']] for x in res], float)
    for j, name in enumerate(['r_acc', 'r_dec', 'r_pair']):
        m = ~np.isnan(arr[:, j + 1])
        print(f"corr(ratio_ref, {name}) = {np.corrcoef(arr[m, 0], arr[m, j + 1])[0, 1]:.2f}  n = {m.sum()}")
    if a.csv:
        with open(a.csv, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
