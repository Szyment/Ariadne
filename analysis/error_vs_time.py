#!/usr/bin/env python3
"""Position error relative to GNSS as a function of time since the switch to source set 2, for all run CSVs.

Tests whether the estimator error grows with time without GNSS regardless of heading and wind (S-22 finding 5).
For each run: error(t) = distance estimator-GNSS minus the offset in the first 2 s after the switch (as in the detector),
sampled every 10 s of the flow-only phase; also the error at the GNSS turn (outbound end) and at the end of the phase.
Outputs a table (CSV) and a plot: one line per run, coloured by surface, dashed for 0.75 m/s.

  python3 analysis/scripts/error_vs_time.py analysis/data/E1/ARIADNE_E1_*.csv --csv analysis/results/error_vs_time.csv --plot analysis/results/error_vs_time.png
"""
import sys, argparse, math, os
import numpy as np, pandas as pd
def hav(lat1, lon1, lat2, lon2):
    R = 6371000.0; p1, p2 = np.radians(lat1), np.radians(lat2); dl = np.radians(lon2 - lon1)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))
ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--csv'); ap.add_argument('--plot'); ap.add_argument('--step', type=float, default=10.0)
a = ap.parse_args()
rows = []; curves = {}
for f in a.files:
    d = pd.read_csv(f); d = d[d.phase == 'flow_only'].copy()
    if len(d) < 10: continue
    t = d.t_since_src2_s.values
    e = hav(d.ekf_lat.values, d.ekf_lon.values, d.gps_lat.values, d.gps_lon.values)
    e = e - np.median(e[t < 2.0]) if (t < 2.0).any() else e
    # GNSS turn = max distance from the start point (GNSS)
    dist0 = hav(d.gps_lat.values, d.gps_lon.values, d.gps_lat.values[0], d.gps_lon.values[0]); iturn = int(np.argmax(dist0))
    name = os.path.basename(f).replace('.csv', ''); cell = name.split('_')[-1]
    surf = 'field' if 'SURF2' in cell else 'grass'; vel = '0.75' if 'VEL075' in cell else '1.5'; alt = '1.5' if 'ALT15' in cell else '3'
    grid = np.arange(0, t.max() + 1e-9, a.step); ei = np.interp(grid, t, e)
    curves[name] = (grid, ei, surf, vel, alt)
    r = {'run': name, 'surface': surf, 'speed_m_s': vel, 'alt_m': alt, 'flow_only_s': round(t.max(), 1), 't_turn_s': round(t[iturn], 1),
         'err_turn_m': round(float(e[iturn]), 2), 'err_end_m': round(float(e[-1]), 2), 'err_max_m': round(float(e.max()), 2)}
    for g, v in zip(grid, ei):
        if g <= 150: r[f'err_{int(g)}s'] = round(float(v), 2)
    rows.append(r)
df = pd.DataFrame(rows)
if a.csv: df.to_csv(a.csv, index=False)
# summary: mean error at fixed times, by group
print('n =', len(df))
for grp, g in df.groupby(['surface', 'speed_m_s']):
    cols = [c for c in ['err_30s', 'err_60s', 'err_90s', 'err_120s'] if c in g]
    print(f"{grp[0]:5s} {grp[1]} m/s  n={len(g):2d}  " + '  '.join(f"{c}: {g[c].mean():.1f}±{g[c].std():.1f}" for c in cols) + f"  turn: {g.err_turn_m.mean():.1f}  end: {g.err_end_m.mean():.1f}")
# growth rate: median slope error vs time over the flow-only phase (m per 10 s)
sl = []
for name, (grid, ei, surf, vel, alt) in curves.items():
    if len(grid) > 3: sl.append((name, surf, vel, np.polyfit(grid, ei, 1)[0] * 10))
sd = pd.DataFrame(sl, columns=['run', 'surface', 'speed', 'slope_m_per_10s'])
print(sd.groupby(['surface', 'speed']).slope_m_per_10s.describe()[['count', 'mean', '50%', 'min', 'max']].round(2))
# error at the same elapsed time, outbound vs return at equal distance from the switch
if a.plot:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 6))
    col = {'grass': 'tab:green', 'field': 'tab:brown'}
    for name, (grid, ei, surf, vel, alt) in curves.items():
        ax.plot(grid, ei, color=col[surf], ls='--' if vel == '0.75' else '-', lw=1.6 if alt == '1.5' else 1.0, alpha=0.8)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color='tab:green', label='grass, 1.5 m/s'), Line2D([], [], color='tab:green', ls='--', label='grass, 0.75 m/s'),
         Line2D([], [], color='tab:brown', label='ploughed field, 1.5 m/s'), Line2D([], [], color='tab:green', lw=1.6, label='thick: 1.5 m altitude')]
    ax.legend(handles=h); ax.set_xlabel('time since the switch to source set 2 [s]'); ax.set_ylabel('estimator error relative to GNSS [m]')
    ax.set_title(f'Position error against time without GNSS, {len(curves)} E1 runs'); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(a.plot, dpi=130)
