import numpy as np, cv2, collections
exec(open('sync.py').read().split('for name, csvp')[0])
from scipy.optimize import least_squares
FX = 1260.0
fr, side, ids, C = load('s066.csv')
fr2, side2, ids2, C2 = load('s065.csv')
fr = np.r_[fr, fr2 + 10**6]; ids = np.r_[ids, ids2]; C = np.r_[C, C2]
by = collections.defaultdict(dict)
for k in range(len(fr)): by[fr[k]][ids[k]] = C[k]
pairs = [(f[a], f[b]) for f in by.values() for a, b in [(10, 11), (11, 12)] if a in f and b in f]
P = np.array([np.r_[p[0], p[1]] for p in pairs])  # (n, 8, 2)
print('two-tag frames (pairs):', len(P))
TARGET = 0.75 / 0.22
def ratios(k, cx=648, cy=486):
    K = np.array([[FX, 0, cx], [0, FX, cy], [0, 0, 1.]])
    D = np.array([k[0], k[1] if len(k) > 1 else 0, 0, 0, 0])
    U = cv2.undistortPoints(P.reshape(-1, 1, 2).astype(np.float64), K, D, P=K).reshape(-1, 8, 2)
    A, B = U[:, :4], U[:, 4:]
    sa = np.mean([np.linalg.norm(A[:, i] - A[:, (i + 1) % 4], axis=1) for i in range(4)], 0)
    sb = np.mean([np.linalg.norm(B[:, i] - B[:, (i + 1) % 4], axis=1) for i in range(4)], 0)
    d = np.linalg.norm(A.mean(1) - B.mean(1), axis=1)
    return d / ((sa + sb) / 2), U
r0, _ = ratios([0])
print('raw: spacing %.4f m (median), p5 %.4f p95 %.4f' % (np.median(r0) * 0.22, np.percentile(r0, 5) * 0.22, np.percentile(r0, 95) * 0.22))
for npar in (1, 2):
    s = least_squares(lambda k: ratios(k)[0] - TARGET, [0.0] * npar)
    r, U = ratios(s.x)
    print(f'k ({npar} param, normalised with fx={FX:.0f}):', np.round(s.x, 4), ' spacing after %.4f m, p5 %.4f p95 %.4f' % (np.median(r) * 0.22, np.percentile(r, 5) * 0.22, np.percentile(r, 95) * 0.22))
# position dependence: midpoint radius
mid = P.mean(1); rad = np.hypot(mid[:, 0] - 648, mid[:, 1] - 486)
sep = np.linalg.norm(P[:, :4].mean(1) - P[:, 4:].mean(1), axis=1)
for lo, hi in [(0, 100), (100, 200), (200, 350), (350, 600)]:
    m = (rad >= lo) & (rad < hi)
    if m.sum(): print(f'  pair midpoint radius {lo}-{hi} px: n={m.sum()}, raw spacing {np.median(r0[m])*0.22:.4f}, after {np.median(r[m])*0.22:.4f}')
