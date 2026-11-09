import numpy as np, csv, datetime, sys
def load(csvp):
    R = list(csv.DictReader(open(csvp)))
    fr = np.array([int(r['frame']) for r in R]); C = np.array([[float(r[f'{k}{i}']) for i in range(4) for k in 'xy'] for r in R]).reshape(-1, 4, 2)
    side = np.mean([np.linalg.norm(C[:, i] - C[:, (i + 1) % 4], axis=1) for i in range(4)], axis=0)
    return fr, side, np.array([int(r['id']) for r in R]), C
def unix(hms): return datetime.datetime(2026, 11, 1, *hms, tzinfo=datetime.timezone(datetime.timedelta(hours=1))).timestamp()
for name, csvp, t0, logs in [('s065', 's065.csv', unix((12, 16, 29)), ['log63']), ('s066', 's066.csv', unix((12, 52, 21)), ['log63', 'log64'])]:
    fr, side, ids, C = load(csvp)
    tv = t0 + fr / 30.0
    for lg in logs:
        L = np.load(lg + '.npz'); off = float(L['off']); rf = L['RFND']
        trf = rf[:, 0] + off; d = rf[:, 1]
        sel = (tv > trf[0] + 15) & (tv < trf[-1] - 15)
        if sel.sum() < 50: continue
        best = []
        for dt in np.arange(-15, 15.01, 0.1):
            h = np.interp(tv[sel] + dt, trf, d)
            ok = (h > 0.5) & (h < 4.5)
            p = side[sel][ok] * h[ok]
            best.append((np.std(p) / np.mean(p), dt, np.mean(p), ok.sum()))
        best.sort()
        cv, dt, pm, n = best[0]
        print(f'{name} vs {lg}: n={sel.sum()} best dt={dt:+.1f} s (log time = video name time + frame/30 + dt), CV={cv:.3f}, side*h={pm:.1f} px*m -> fx~{pm/0.22:.0f}; next best: ' + ', '.join(f'{b[1]:+.1f}/{b[0]:.3f}' for b in best[1:4]))
