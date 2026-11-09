import numpy as np, collections
from common import *
from world import tagworld
for s in ['s065', 's066']:
    d = load(s)
    tn, te, f, rt = tagworld(d, True)
    idx = collections.defaultdict(dict)
    for k in range(len(d['fr'])): idx[d['fr'][k]][d['id'][k]] = k
    D = []; side = []
    for fr_, m in idx.items():
        for a, b in [(10, 11), (11, 12)]:
            if a in m and b in m:
                i, j = m[a], m[b]
                D.append(np.hypot(f[i] - f[j], rt[i] - rt[j]))
                # height implied by tag size (undistorted side in normalised units)
                for k in (i, j):
                    U = d['U'][k]; sn = np.mean([np.linalg.norm(U[q] - U[(q + 1) % 4]) for q in range(4)])
                    side.append((0.22 / sn, d['h'][k] * np.cos(np.radians(d['roll'][k])) * np.cos(np.radians(d['pitch'][k]))))
    D = np.array(D); side = np.array(side)
    print(f'{s}: same-frame tag distance from image+rangefinder: n={len(D)}, median {np.median(D):.3f} m (p5 {np.percentile(D,5):.3f}, p95 {np.percentile(D,95):.3f}); '
          f'height from tag size {np.median(side[:,0]):.3f} m vs rangefinder vertical {np.median(side[:,1]):.3f} m')
