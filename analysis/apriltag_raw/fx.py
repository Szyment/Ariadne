import numpy as np
exec(open('sync.py').read().split('for name, csvp')[0])
from scipy.optimize import least_squares
for name, csvp, t0, lg, dt in [('s065', 's065.csv', unix((12, 16, 29)), 'log63', 12.5), ('s066', 's066.csv', unix((12, 52, 21)), 'log64', 3.15)]:
    fr, side, ids, C = load(csvp)
    cx = C[:, :, 0].mean(1); cy = C[:, :, 1].mean(1)
    L = np.load(lg + '.npz'); off = float(L['off']); rf = L['RFND']; A = L['ATT']
    tv = t0 + fr / 30.0 + dt
    h = np.interp(tv, rf[:, 0] + off, rf[:, 1])
    roll = np.interp(tv, A[:, 0] + off, A[:, 1]); pitch = np.interp(tv, A[:, 0] + off, A[:, 2])
    # vertical height from slant rangefinder reading
    hv = h * np.cos(np.radians(roll)) * np.cos(np.radians(pitch))
    r = np.hypot(cx - 648, cy - 486)
    ok = (hv > 0.6) & (hv < 4) & (r < 200) & (np.abs(roll) < 4) & (np.abs(pitch) < 4)
    f = lambda p: side[ok] - p[0] * 0.22 / (hv[ok] + p[1])
    s = least_squares(f, [1270, 0.0])
    res = f(s.x)
    print(f'{name}: n={ok.sum()}, h range {hv[ok].min():.2f}-{hv[ok].max():.2f} m, fx={s.x[0]:.0f} px, delta={s.x[1]:+.3f} m (camera height above tag minus rangefinder vertical reading), rms {np.sqrt(np.mean(res**2)):.1f} px')
    for lo, hi in [(0.6, 1.2), (1.2, 1.8), (1.8, 2.5), (2.5, 4)]:
        m = ok & (hv >= lo) & (hv < hi)
        if m.sum(): print(f'   h {lo}-{hi}: n={m.sum()}, fx(delta=0)={np.median(side[m]*hv[m]/0.22):.0f}')
