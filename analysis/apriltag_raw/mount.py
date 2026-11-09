import numpy as np
from common import *
# image motion of a tag vs body velocity: find which image axis is body-forward
rows = []
for s in ['s065', 's066']:
    d = load(s)
    for tid in (10, 11, 12):
        m = np.where(d['id'] == tid)[0]
        for a, b in zip(m[:-1], m[1:]):
            if d['fr'][b] - d['fr'][a] != 1: continue
            if d['spd'][a] < 0.8: continue
            du = (d['uc'][b] - d['uc'][a]) * 30   # normalised units per s
            # body velocity: ground course relative to yaw
            rel = np.radians(d['crs'][a] - d['yaw'][a]); v = d['spd'][a]
            vf, vr = v * np.cos(rel), v * np.sin(rel)
            rows.append((du[0] * d['h'][a], du[1] * d['h'][a], vf, vr, s))
R = np.array([r[:4] for r in rows], float)
print('samples', len(R))
# least squares: [du*h, dv*h] = M @ [vf, vr]
M, *_ = np.linalg.lstsq(R[:, 2:4], R[:, 0:2], rcond=None)
print('M (rows: vf, vr -> cols: image x, image y):\n', np.round(M, 3))
res = R[:, 0:2] - R[:, 2:4] @ M
print('residual rms (m/s equiv):', np.round(np.sqrt((res**2).mean(0)), 3))
