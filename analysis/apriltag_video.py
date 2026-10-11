#!/usr/bin/env python3
"""Side-by-side annotated video: kam0 (left) and kam1 (right) with AprilTag detections and live numbers."""
import cv2, numpy as np, math, sys, collections
from pupil_apriltags import Detector

K0, K1 = sys.argv[1], sys.argv[2]; OUT = sys.argv[3]
TAG = 0.16; FX0 = 1271.8; FX1 = 1444.0  # kam1: 1.50 m from the rangefinder at side 154 px
SPACING = 0.40
det = Detector(families='tag36h11', nthreads=4, quad_decimate=1.0, refine_edges=True, decode_sharpening=0.25)
c0 = cv2.VideoCapture(K0); c1 = cv2.VideoCapture(K1)
W, H = 1296, 972; fps = 30.0
# output: each view scaled to 960x720, stacked side by side, with a 90 px header -> 1920 x 810
SW, SH = 960, 720; HDR = 90
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUT, fourcc, fps, (2 * SW, SH + HDR))
FONT = cv2.FONT_HERSHEY_SIMPLEX
INK = (23, 23, 23); ACC = (27, 65, 200); WHITE = (244, 248, 250); GREEN = (80, 180, 60)

def annotate(frame, fx, name, hist):
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    r = det.detect(g, estimate_tag_pose=False)
    r = sorted(r, key=lambda d: d.tag_id)
    info = []
    for d in r:
        pts = d.corners.astype(int)
        cv2.polylines(frame, [pts.reshape(-1, 1, 2)], True, (60, 220, 60), 3)
        cx, cy = map(int, d.center)
        cv2.circle(frame, (cx, cy), 5, (60, 220, 60), -1)
        side = float(np.mean([np.linalg.norm(d.corners[i] - d.corners[(i + 1) % 4]) for i in range(4)]))
        h = TAG * fx / side
        cv2.putText(frame, f'ID {d.tag_id}', (cx - 40, cy - int(side / 2) - 14), FONT, 1.1, (60, 220, 60), 3)
        cv2.putText(frame, f'{side:.0f} px  h={h:.2f} m', (cx - 110, cy + int(side / 2) + 36), FONT, 0.8, (60, 220, 60), 2)
        info.append((d.tag_id, d.center, side, h))
    # spacing between neighbouring tags from the image
    spac = []
    for i in range(len(info)):
        for j in range(i + 1, len(info)):
            if info[j][0] - info[i][0] == 1:
                px = np.linalg.norm(info[i][1] - info[j][1]); s = px * TAG / np.mean([info[i][2], info[j][2]])
                spac.append(s)
                p1 = tuple(map(int, info[i][1])); p2 = tuple(map(int, info[j][1]))
                cv2.line(frame, p1, p2, (0, 200, 255), 2)
                mid = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2 - 12)
                cv2.putText(frame, f'{s:.3f} m', (mid[0] - 50, mid[1]), FONT, 0.9, (0, 200, 255), 2)
    if info: hist['h'].append(np.mean([x[3] for x in info]))
    for s in spac: hist['s'].append(s)
    hist['n'] += 1; hist['det'] += 1 if info else 0
    return frame, info, spac

hist0 = dict(h=collections.deque(maxlen=90), s=collections.deque(maxlen=90), n=0, det=0)
hist1 = dict(h=collections.deque(maxlen=90), s=collections.deque(maxlen=90), n=0, det=0)
n = 0
while True:
    ok0, f0 = c0.read(); ok1, f1 = c1.read()
    if not (ok0 and ok1): break
    f0, i0, s0 = annotate(f0, FX0, 'kam0', hist0)
    f1, i1, s1 = annotate(f1, FX1, 'kam1', hist1)
    canvas = np.full((SH + HDR, 2 * SW, 3), 250, np.uint8); canvas[:] = WHITE
    canvas[HDR:, :SW] = cv2.resize(f0, (SW, SH)); canvas[HDR:, SW:] = cv2.resize(f1, (SW, SH))
    t = n / fps
    cv2.putText(canvas, 'Ariadne  AprilTag 36h11, 3 x 16 cm, odstep 0,40 m, dron z reki ~1,5 m (dalmierz 1,50 m)   11.10.2026 19:21', (20, 32), FONT, 0.8, INK, 2)
    for k, (hist, x0, name, fov) in enumerate([(hist0, 0, 'kam0  OV5647 + filtr IR, FOV ~54', FX0), (hist1, SW, 'kam1  OV5647 NoIR + IR 850 nm, FOV ~48', FX1)]):
        hh = f'{np.median(hist["h"]):.2f} m' if hist['h'] else '--'
        ss = f'{np.median(hist["s"]):.3f} m' if hist['s'] else '--'
        rate = 100 * hist['det'] / max(1, hist['n'])
        cv2.putText(canvas, name, (x0 + 20, 62), FONT, 0.65, INK, 2)
        cv2.putText(canvas, f'wysokosc z tagu (mediana 3 s): {hh}   odstep z obrazu: {ss}   klatki z tagiem: {rate:.0f} %', (x0 + 20, 84), FONT, 0.6, ACC, 2)
    cv2.putText(canvas, f't = {t:6.1f} s', (2 * SW - 170, 32), FONT, 0.8, INK, 2)
    out.write(canvas); n += 1
    if n % 300 == 0: print(n, flush=True)
out.release(); print('frames', n)
