#!/usr/bin/env python3
"""
Optical-flow degradation detector, version 0.2 (RQ1), offline work on the CSV from cut_runs.py.

Principle: the detector sees only the signals available on board without GNSS
(of_qual, the xkf4_* measurement residuals, flow scatter after subtracting rotation, rangefinder).
GNSS serves only as the reference measurement for judging whether and when the position
error really grew. The difference between these two moments is the detection lead time.

Usage:
  python3 degradation_detector.py analysis/data/E1/ARIADNE_E1_*.csv
  python3 degradation_detector.py analysis/data/E1/ARIADNE_E1_*.csv --plots analysis/results/detector
  python3 degradation_detector.py ... --qual-min 150 --sv-max 0.5 --scatter-max 0.15 --error-m 2.0
"""
import argparse, math, os, sys
import numpy as np
import pandas as pd

FS = 10.0  # Hz in the CSV

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = p2 - p1
    dl = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2
    return 2*R*np.arcsin(np.sqrt(a))

def indicators(d, window_s):
    """Onboard indicators computed in a rolling window. Returns a DataFrame with w_* columns."""
    n = max(1, int(window_s*FS))
    w = pd.DataFrame(index=d.index)
    w['w_qual'] = d.of_qual.rolling(n, min_periods=1).mean()
    w['w_sv'] = d.xkf4_SV.rolling(n, min_periods=1).mean()
    w['w_sh'] = d.xkf4_SH.rolling(n, min_periods=1).mean()
    # ground-relative flow = measured flow minus airframe rotation (rad/s)
    gx = d.of_flowX - d.of_bodyX
    gy = d.of_flowY - d.of_bodyY
    w['w_scatter'] = np.sqrt(gx.rolling(n, min_periods=2).var().fillna(0) +
                             gy.rolling(n, min_periods=2).var().fillna(0))
    # rangefinder: jumps between samples (lost return, grass, edge)
    w['w_rfnd_jump'] = d.rfnd_dist.diff().abs().rolling(n, min_periods=1).max().fillna(0)
    # v0.2: XKF5 signals (require a CSV from cut_runs.py v0.2)
    if 'xkf5_ePos' in d:
        w['w_epos'] = d.xkf5_ePos.rolling(n, min_periods=1).mean()          # EKF's own position uncertainty; baseline <= 0.11
        w['w_fi'] = (d.xkf5_FIX.abs() + d.xkf5_FIY.abs()).rolling(n, min_periods=1).mean()  # optical-flow measurement residuals; baseline <= 870
    else:
        w['w_epos'] = 0.0; w['w_fi'] = 0.0
    # wind proxy: airframe tilt in hover (ground-relative flow < 0.08 rad/s),
    # minus a constant trim offset of ~0.8 deg measured at zero wind (S-18). Informative only, does not vote.
    g = np.hypot(gx, gy).rolling(int(FS), min_periods=1).mean()   # smoothed over 1 s: hover ~0.07, flight ~0.45 rad/s
    tilt = np.hypot(d.roll, d.pitch)
    # hover counts only when it lasts 2 s without interruption (cuts off the tilt when starting and braking)
    hover = (g < 0.15).astype(int).rolling(2*int(FS), min_periods=2*int(FS)).min().fillna(0).astype(bool)
    hover = hover & hover.shift(-2*int(FS), fill_value=False)   # and for another 2 s after this moment (cuts off the start of a move)
    w['w_wind'] = (tilt.where(hover).rolling(5*int(FS), min_periods=5).median() - 0.8).clip(lower=0)
    return w

def detect(w, a):
    """Returns the warning mask. Rule: at least `a.votes` indicators beyond their threshold
    continuously for `a.hold` s, or of_qual alone below the hard threshold."""
    votes = (
        (w.w_qual < a.qual_min).astype(int) +
        (w.w_sv > a.sv_max).astype(int) +
        (w.w_scatter > a.scatter_max).astype(int) +
        (w.w_rfnd_jump > a.rfnd_jump_max).astype(int) +
        (w.w_epos > a.epos_max).astype(int) +
        (w.w_fi > a.fi_max).astype(int)
    )
    cand = (votes >= a.votes) | (w.w_qual < a.qual_hard)
    n = max(1, int(a.hold*FS))
    return cand.rolling(n, min_periods=n).min().fillna(0).astype(bool), votes

def analyse(path, a):
    d = pd.read_csv(path)
    name = os.path.basename(path)[:-4]
    b = d[d.phase == 'flow_only'].reset_index(drop=True)
    if b.empty:
        return dict(run=name, note='no flow_only phase')
    w = indicators(b, a.window)
    warn, votes = detect(w, a)
    # reference: EKF position error relative to GNSS, relative to the moment of the cut-off
    e = haversine_m(b.ekf_lat, b.ekf_lon, b.gps_lat, b.gps_lon)
    e0 = e.iloc[:max(1, int(2*FS))].mean()          # initial error (GNSS offset)
    e_rel = (e - e0).abs()
    err = e_rel > a.error_m
    t = b.t_since_src2_s
    t_warn = float(t[warn].iloc[0]) if warn.any() else None
    t_err = float(t[err].iloc[0]) if err.any() else None
    if t_warn is not None and t_err is not None:
        outcome, lead = 'hit', round(t_err - t_warn, 1)
    elif t_warn is not None:
        outcome, lead = 'false_alarm', None
    elif t_err is not None:
        outcome, lead = 'miss', None
    else:
        outcome, lead = 'no_event', None
    r = dict(run=name, outcome=outcome, t_warning_s=t_warn, t_error_s=t_err,
             lead_time_s=lead, error_max_m=round(float(e_rel.max()), 2),
             qual_min=int(w.w_qual.min()), sv_max=round(float(w.w_sv.max()), 3),
             scatter_max=round(float(w.w_scatter.max()), 3),
             rfnd_jump_max=round(float(w.w_rfnd_jump.max()), 2),
             epos_max=round(float(w.w_epos.max()), 3), fi_max=int(w.w_fi.max()),
             wind_tilt_deg=round(float(w.w_wind.dropna().median()), 2) if w.w_wind.notna().any() else None,
             votes_max=int(votes.max()))
    if a.plots:
        plot(name, t, w, votes, warn, e_rel, a)
    return r

def plot(name, t, w, votes, warn, e_rel, a):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    os.makedirs(a.plots, exist_ok=True)
    panels = [
        ('Optical-flow sensor image quality (OF.Qual, 0-255)', w.w_qual, a.qual_min, 'threshold %g' % a.qual_min, (0, 260)),
        ('Optical-flow measurement residual |FIX|+|FIY| (measurement minus estimator prediction)', w.w_fi, a.fi_max, 'threshold %g' % a.fi_max, None),
        ('Estimator position uncertainty (XKF5.ePos)', w.w_epos, a.epos_max, 'threshold %g' % a.epos_max, None),
        ('Velocity test ratio (XKF4.SV; > 1 = measurement rejected)', w.w_sv, a.sv_max, 'threshold %g' % a.sv_max, None),
        ('Flow scatter after subtracting rotation [rad/s] (peaks = starting and braking)', w.w_scatter, a.scatter_max, 'threshold %g' % a.scatter_max, None),
        ('Airframe tilt in hover [deg] (wind proxy, not converted to m/s)', w.w_wind, None, None, None),
        ('Estimator position error relative to GNSS [m] (reference, not visible to the aircraft)', e_rel, a.error_m, 'reference error %g m' % a.error_m, None),
    ]
    fig, axs = plt.subplots(len(panels), 1, figsize=(11, 2.0*len(panels)), sharex=True)
    for ax, (title, y, thr, label, ylim) in zip(axs, panels):
        ax.plot(t, y, color='#1f4e79', lw=1.2)
        if thr is not None:
            ax.axhline(thr, ls='--', color='#c0392b', lw=1)
            ax.text(t.iloc[-1], thr, ' ' + label, color='#c0392b', va='bottom', ha='right', fontsize=8)
        if warn.any():
            ax.fill_between(t, *ax.get_ylim(), where=warn, color='#c0392b', alpha=0.12, step='post')
        ax.set_title(title, loc='left', fontsize=9.5, fontweight='bold')
        if ylim: ax.set_ylim(*ylim)
        ax.grid(alpha=0.25); ax.spines[['top', 'right']].set_visible(False)
    axs[-1].set_xlabel('seconds since GNSS cut-off (RC7 Mid)')
    for x, lab in ((0, 'GNSS cut-off'),):
        axs[0].axvline(x, color='grey', lw=0.8, ls=':')
    n_warn = int(warn.sum())
    fig.suptitle('%s\ndetector warnings: %s' % (name, 'none' if n_warn == 0 else 'from %.1f s' % float(t[warn].iloc[0])),
                 fontsize=11, x=0.01, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(os.path.join(a.plots, name + '_detector.png'), dpi=110); plt.close(fig)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='+')
    p.add_argument('--window', type=float, default=1.0, help='rolling window [s]')
    p.add_argument('--hold', type=float, default=1.0, help='how many seconds the condition must hold')
    p.add_argument('--votes', type=int, default=2, help='how many indicators beyond threshold at once')
    p.add_argument('--qual-min', type=float, default=150)
    p.add_argument('--qual-hard', type=float, default=50, help='this threshold alone is enough for a warning')
    p.add_argument('--sv-max', type=float, default=0.5)
    p.add_argument('--scatter-max', type=float, default=1.0)
    p.add_argument('--rfnd-jump-max', type=float, default=0.5)
    p.add_argument('--epos-max', type=float, default=0.3, help='XKF5.ePos, baseline of 12 Sep <= 0.11')
    p.add_argument('--fi-max', type=float, default=1500, help='|XKF5.FIX|+|FIY| mean over 1 s, baseline of 12 Sep <= 870')
    p.add_argument('--error-m', type=float, default=5.0, help='threshold of the reference position error relative to GNSS')
    p.add_argument('--plots', default=None, help='directory for PNG files')
    p.add_argument('--csv', default=None, help='write the results table')
    a = p.parse_args()
    res = pd.DataFrame([analyse(f, a) for f in a.files])
    pd.set_option('display.width', 200); pd.set_option('display.max_columns', 20)
    print(res.to_string(index=False))
    if a.csv:
        res.to_csv(a.csv, index=False)
    n = len(res);
    for k in ['hit', 'false_alarm', 'miss', 'no_event']:
        print(f'{k}: {(res.outcome == k).sum()}/{n}')

if __name__ == '__main__':
    main()
