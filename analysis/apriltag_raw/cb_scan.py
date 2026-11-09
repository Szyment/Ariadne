import sys, subprocess, numpy as np, cv2, csv
src, out, step = sys.argv[1], sys.argv[2], int(sys.argv[3])
W, H = 648, 486
ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-r', '30', '-f', 'h264', '-i', src, '-vf', f'select=not(mod(n\\,{step})),scale={W}:{H}', '-vsync', '0', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
rows = []; k = 0
while True:
    b = ff.stdout.read(W * H)
    if len(b) < W * H: break
    g = np.frombuffer(b, np.uint8).reshape(H, W)
    ok, c = cv2.findChessboardCorners(g, (9, 6), cv2.CALIB_CB_FAST_CHECK | cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ok:
        c = c.reshape(6, 9, 2) * 2
        sq = np.mean([np.linalg.norm(c[:, 1:] - c[:, :-1], axis=2).mean(), np.linalg.norm(c[1:] - c[:-1], axis=2).mean()])
        rows.append((k * step, round(float(sq), 2), round(float(c[..., 0].mean()), 1), round(float(c[..., 1].mean()), 1)))
    k += 1
csv.writer(open(out, 'w')).writerows([('frame', 'square_px', 'cx', 'cy')] + rows)
print('scanned', k, 'frames, board found in', len(rows))
