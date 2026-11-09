#!/usr/bin/env python3
"""RQ2 counterfactual: what the E1 drift would have been with printed anchors every S metres.

For every run CSV, in the flow-only phase: the estimator error vector (EKF minus GNSS, in metres, the
offset of the first 2 s after the switch removed) along the true path (GNSS). Anchors are met every
S metres of true travelled distance. At an anchor the position error is reset to zero and the drift
between anchors is the increment of the measured error vector, which is what a position correction
leaves untouched (the flow scale error is not corrected). An anchor counts only if a row of three tags
(centres 0.75 m apart, 1.5 m wide) falls inside the camera swath at the true position: lateral error
below 0.75 m plus half the swath (kam0 53 deg: 1.5 m wide at 1.5 m, 3.0 m at 3 m).

  python3 analysis/scripts/anchor_counterfactual.py analysis/data/E1/ARIADNE_E1_*.csv --csv analysis/results/anchor_counterfactual.csv --plot analysis/results/anchor_counterfactual.png
"""
import argparse, os, math
import numpy as np, pandas as pd
R = 6371000.0
ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--csv'); ap.add_argument('--plot')
ap.add_argument('--spacings', default='5,10,20'); ap.add_argument('--hfov-deg', type=float, default=53.2); ap.add_argument('--row-width', type=float, default=1.5)
a = ap.parse_args(); S_LIST = [float(x) for x in a.spacings.split(',')]
rows = []; curves = {}
for f in a.files:
    d = pd.read_csv(f); d = d[d.phase == 'flow_only'].copy()
    if len(d) < 10: continue
    name = os.path.basename(f).replace('.csv', ''); cell = name.split('_')[-1]
    surf = 'field' if 'SURF2' in cell else 'grass'; vel = '0.75' if 'VEL075' in cell else '1.5'; alt = 1.5 if 'ALT15' in cell else 3.0
    lat0, lon0 = d.gps_lat.values[0], d.gps_lon.values[0]
    def ne(lat, lon): return np.radians(lat - lat0) * R, np.radians(lon - lon0) * R * math.cos(math.radians(lat0))
    gn, ge = ne(d.gps_lat.values, d.gps_lon.values); en, ee = ne(d.ekf_lat.values, d.ekf_lon.values)
    t = d.t_since_src2_s.values
    err = np.c_[en - gn, ee - ge]
    m0 = t < 2.0
    if m0.any(): err = err - np.median(err[m0], axis=0)
    step = np.hypot(np.diff(gn), np.diff(ge)); dist = np.r_[0, np.cumsum(step)]
    # true track direction (unit), smoothed over ~1 s
    k = max(1, int(round(1.0 / max(np.median(np.diff(t)), 1e-3))))
    vn = np.gradient(pd.Series(gn).rolling(k, center=True, min_periods=1).mean().values, t)
    ve = np.gradient(pd.Series(ge).rolling(k, center=True, min_periods=1).mean().values, t)
    sp = np.hypot(vn, ve); ok = sp > 0.3
    un = np.where(ok, vn / np.where(sp > 0, sp, 1), np.nan); ue = np.where(ok, ve / np.where(sp > 0, sp, 1), np.nan)
    def lateral_of(v, i):                                   # component of v across the true track at sample i
        return abs(v[0] * (-ue[i]) + v[1] * un[i]) if not np.isnan(ue[i]) else float(np.hypot(*v))
    swath = 2 * alt * math.tan(math.radians(a.hfov_deg / 2)); capture = a.row_width / 2 + swath / 2
    e_free = np.hypot(err[:, 0], err[:, 1])
    r = {'run': name, 'surface': surf, 'speed_m_s': vel, 'alt_m': alt, 'flow_only_s': round(t.max(), 1), 'dist_m': round(dist[-1], 1),
         'err_end_free_m': round(float(e_free[-1]), 2), 'err_max_free_m': round(float(e_free.max()), 2)}
    curves[name] = {'dist': dist, 'free': e_free, 'surf': surf, 'alt': alt, 'vel': vel}
    for S in S_LIST:
        ref = np.zeros(2); e_anch = np.zeros(len(t)); n_anch = 0; n_missed = 0; next_a = S; anchors = []
        for i in range(len(t)):
            if dist[i] >= next_a:
                if lateral_of(err[i] - ref, i) <= capture: ref = err[i].copy(); n_anch += 1; anchors.append(dist[i])
                else: n_missed += 1
                next_a += S
            e_anch[i] = np.hypot(*(err[i] - ref))
        tag = f'{S:g}m'
        r[f'err_end_{tag}'] = round(float(e_anch[-1]), 2); r[f'err_max_{tag}'] = round(float(e_anch.max()), 2)
        r[f'anchors_{tag}'] = n_anch; r[f'missed_{tag}'] = n_missed
        curves[name][tag] = e_anch; curves[name][f'anchors_{tag}'] = anchors
    rows.append(r)
df = pd.DataFrame(rows)
if a.csv: df.to_csv(a.csv, index=False)
print('n =', len(df))
for (surf, alt, vel), g in df.groupby(['surface', 'alt_m', 'speed_m_s']):
    line = f'{surf:5s} {alt:3.1f} m {vel} m/s  n={len(g):2d}  dist med {g.dist_m.median():5.0f} m  free: end med {g.err_end_free_m.median():5.2f} max med {g.err_max_free_m.median():5.2f}'
    for S in S_LIST:
        tag = f'{S:g}m'; line += f' | {tag}: end {g[f"err_end_{tag}"].median():4.2f} max {g[f"err_max_{tag}"].median():4.2f} (p90 {g[f"err_max_{tag}"].quantile(0.9):4.2f}) missed {int(g[f"missed_{tag}"].sum())}/{int(g[f"anchors_{tag}"].sum() + g[f"missed_{tag}"].sum())}'
    print(line)
print('all runs: free end med %.2f, max med %.2f' % (df.err_end_free_m.median(), df.err_max_free_m.median()))
for S in S_LIST:
    tag = f'{S:g}m'; print(f'  {tag}: end med {df[f"err_end_{tag}"].median():.2f}, max med {df[f"err_max_{tag}"].median():.2f}, max p90 {df[f"err_max_{tag}"].quantile(0.9):.2f}, max of max {df[f"err_max_{tag}"].max():.2f}, missed {int(df[f"missed_{tag}"].sum())}')
if a.plot:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    groups = [('grass', 3.0), ('field', 3.0), ('grass', 1.5), ('field', 1.5)]
    for ax, (surf, alt) in zip(axes.ravel(), groups):
        for name, c in curves.items():
            if c['surf'] != surf or c['alt'] != alt: continue
            ax.plot(c['dist'], c['free'], color='0.75', lw=0.8)
            ax.plot(c['dist'], c['10m'], color='C0', lw=0.8, alpha=0.8)
            ax.plot(c['dist'], c['5m'], color='C2', lw=0.8, alpha=0.8)
        ax.set_title(f'{surf}, {alt:g} m: no anchor (grey), every 10 m (blue), every 5 m (green)'); ax.set_ylabel('error vs GNSS [m]'); ax.grid(alpha=0.3)
    for ax in axes[1]: ax.set_xlabel('true distance flown without GNSS [m]')
    fig.tight_layout(); fig.savefig(a.plot, dpi=130)
