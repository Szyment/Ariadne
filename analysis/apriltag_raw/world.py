import numpy as np
from common import *
def tagworld(d, att=True, delta=0.0):
    xn, yn = d['uc'][:, 0], d['uc'][:, 1]
    vb = np.stack([yn, -xn, np.ones_like(xn)], 1)          # body F, R, D
    r = np.radians(d['roll']) if att else 0 * xn; p = np.radians(d['pitch']) if att else 0 * xn
    cr, sr, cp, sp = np.cos(r), np.sin(r), np.cos(p), np.sin(p)
    # v_l = Ry(p) Rx(r) vb
    x1 = vb[:, 0]; y1 = cr * vb[:, 1] - sr * vb[:, 2]; z1 = sr * vb[:, 1] + cr * vb[:, 2]
    f = cp * x1 + sp * z1; rt = y1; z = -sp * x1 + cp * z1
    H = d['h'] * np.cos(np.radians(d['roll'])) * np.cos(np.radians(d['pitch'])) + delta
    s = H / z; f *= s; rt *= s
    y = np.radians(d['yaw'])
    return d['N'] + np.cos(y) * f - np.sin(y) * rt, d['E'] + np.sin(y) * f + np.cos(y) * rt, f, rt
FL = {'s065': [('flight 3', unix((12, 32, 37)), unix((12, 34, 25))), ('flight 4', unix((12, 42, 16)), unix((12, 44, 44))), ('flight 5', unix((12, 47, 37)), unix((12, 50, 21)))],
      's066': [('flight 6', unix((12, 53, 21)), unix((12, 55, 49))), ('flight 7', unix((12, 56, 13)), unix((13, 0, 29)))]}
out = {}
for s in ['s065', 's066']:
    d = load(s)
    for att in (False, True):
        tn, te, f, rt = tagworld(d, att)
        for fl, a, b in FL[s]:
            m = (d['t'] >= a) & (d['t'] <= b) & (d['h'] > 0.8)
            line = f'{fl} att={int(att)}:'
            for tid in (10, 11, 12):
                k = m & (d['id'] == tid)
                if k.sum() < 5: continue
                n0, e0 = np.median(tn[k]), np.median(te[k])
                sp = np.sqrt(np.median((tn[k] - n0)**2 + (te[k] - e0)**2))
                line += f'  ID{tid} n={k.sum()} N={n0:+.2f} E={e0:+.2f} spread(med)={sp:.2f} m;'
                if att: out[(fl, tid)] = (n0, e0, k.sum())
            print(line)
import pickle; pickle.dump(out, open('tagpos.pkl', 'wb'))
print()
for fl in ['flight 3', 'flight 4', 'flight 5', 'flight 6', 'flight 7']:
    P = {tid: out[(fl, tid)] for tid in (10, 11, 12) if (fl, tid) in out}
    s = fl + ':'
    for a, b in [(10, 11), (11, 12), (10, 12)]:
        if a in P and b in P: s += f'  d{a}-{b}={np.hypot(P[a][0]-P[b][0], P[a][1]-P[b][1]):.3f} m'
    if 10 in P and 12 in P: s += f'  row bearing {np.degrees(np.arctan2(P[12][1]-P[10][1], P[12][0]-P[10][0]))%360:.0f} deg'
    print(s)
