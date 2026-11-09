import sys, subprocess, numpy as np, cv2, csv, json
src, scan, start, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
R = np.array([[float(x) for x in r] for r in list(csv.reader(open(scan)))[1:]])
R = R[R[:, 0] >= start]
# stillness: next scan sample (15 frames later) with nearly the same board centre and size
still = []
for i in range(len(R) - 1):
    if R[i + 1, 0] - R[i, 0] == 15 and np.hypot(*(R[i + 1, 2:4] - R[i, 2:4])) < 1.0 and abs(R[i + 1, 1] - R[i, 1]) < 0.2:
        still.append(R[i])
still = np.array(still)
# diversity: one frame per cell of (cx, cy, square size) grid
pick = {}
for r in still:
    key = (int(r[2] // 120), int(r[3] // 120), int(r[1] // 2))
    pick.setdefault(key, int(r[0]))
frames = sorted(pick.values())
print('still samples', len(still), 'distinct poses', len(frames))
W, H = 1296, 972; FS = W * H * 3 // 2
want = set(frames); got = {}
ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-r', '30', '-f', 'h264', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'], stdout=subprocess.PIPE, bufsize=FS * 4)
n = 0; last = max(frames)
while n <= last:
    b = ff.stdout.read(FS)
    if len(b) < FS: break
    if n in want: got[n] = np.frombuffer(b, np.uint8, W * H).reshape(H, W).copy()
    n += 1
ff.kill()
objp = np.zeros((54, 3), np.float32); objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2) * 0.025
O, I, F = [], [], []
for fr in frames:
    g = got.get(fr)
    if g is None: continue
    ok, c = cv2.findChessboardCorners(g, (9, 6), cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)
    if not ok: continue
    c = cv2.cornerSubPix(g, c, (7, 7), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.01))
    O.append(objp); I.append(c); F.append(fr)
print('frames used', len(F))
res = {}
for name, flags in [('k1k2p1p2k3', 0), ('k1k2k3 no tangential', cv2.CALIB_ZERO_TANGENT_DIST)]:
    rms, K, D, rv, tv, _, _, pve = cv2.calibrateCameraExtended(O, I, (W, H), None, None, flags=flags)
    bad = [F[k] for k in range(len(F)) if pve[k, 0] > 2.5 * np.median(pve)]
    if bad:
        keep = [k for k in range(len(F)) if pve[k, 0] <= 2.5 * np.median(pve)]
        print(f'  {name}: dropping {len(bad)} views with error > 2.5x median: frames {bad}')
        O2 = [O[k] for k in keep]; I2 = [I[k] for k in keep]
        rms, K, D, rv, tv, _, _, pve = cv2.calibrateCameraExtended(O2, I2, (W, H), None, None, flags=flags)
    else:
        keep = list(range(len(F)))
    # per-view errors
    errs = pve[:, 0].tolist()
    # tilt of each view (angle between board normal and optical axis) and distance
    tilt = [np.degrees(np.arccos(abs(cv2.Rodrigues(r)[0][2, 2]))) for r in rv]
    dist = [float(np.linalg.norm(t)) for t in tv]
    zc = [float((cv2.Rodrigues(rv[k])[0] @ np.array([0.1, 0.0625, 0]) + tv[k].ravel())[2]) for k in range(len(rv))]
    print(f'\n{name}: RMS {rms:.3f} px; fx {K[0,0]:.1f} fy {K[1,1]:.1f} cx {K[0,2]:.1f} cy {K[1,2]:.1f}; dist {np.round(D.ravel(), 4).tolist()}')
    print(f'  per-view error median {np.median(errs):.3f} max {max(errs):.3f}; tilt range {min(tilt):.0f}-{max(tilt):.0f} deg; board centre depth range {min(zc):.3f}-{max(zc):.3f} m')
    flat = [zc[k] for k in range(len(rv)) if tilt[k] < 3]
    if flat: print(f'  near-flat views (tilt<3 deg): n={len(flat)}, board-centre depth median {np.median(flat):.3f} m, p10 {np.percentile(flat,10):.3f} p90 {np.percentile(flat,90):.3f}')
    res[name] = dict(rms=rms, K=K.tolist(), D=D.ravel().tolist(), n=len(rv))
json.dump(dict(frames=F, results=res), open(out, 'w'), indent=1)
