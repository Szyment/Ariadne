import numpy as np, csv, datetime
exec(open('sync.py').read().split('for name, csvp')[0])
def ne(lat, lon, lat0, lon0):
    R = 6371008.8
    return np.radians(lat - lat0) * R, np.radians(lon - lon0) * R * np.cos(np.radians(lat0))
for name, csvp, t0, lg in [('s065', 's065.csv', unix((12, 16, 29)), 'log63'), ('s066', 's066.csv', unix((12, 52, 21)), 'log64')]:
    fr, side, ids, C = load(csvp)
    cx = C[:, :, 0].mean(1); cy = C[:, :, 1].mean(1)
    L = np.load(lg + '.npz'); off = float(L['off']); P = L['POS']
    tp = P[:, 0] + off; n, e = ne(P[:, 1], P[:, 2], P[0, 1], P[0, 2])
    tv = t0 + fr / 30.0
    sel = (ids == 11) & (np.hypot(cx - 648, cy - 486) < 250) & (tv > tp[0]) & (tv < tp[-1])
    res = []
    for dt in np.arange(-20, 20.01, 0.1):
        N = np.interp(tv[sel] + dt, tp, n); E = np.interp(tv[sel] + dt, tp, e)
        res.append((np.sqrt(np.var(N) + np.var(E)), dt))
    res.sort()
    print(name, lg, 'n', sel.sum(), 'best dt %+.1f spread %.2f m' % (res[0][1], res[0][0]), ' | spread at other dt:', ', '.join('%+.0f:%.2f' % (d, s) for s, d in sorted(res, key=lambda x: x[1])[::25]))
