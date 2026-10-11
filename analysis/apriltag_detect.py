#!/usr/bin/env python3
"""AprilTag detection in the onboard recordings (v0.1, 11 Oct 2026).

For every N-th frame of an MP4 from stitch_recording.sh: detect tag36h11 markers, estimate the
camera pose relative to each tag (tag_size in metres, camera intrinsics from --fx/--fy/--cx/--cy
or a pinhole guess from --hfov), and write one row per detection.

Usage:
  python3 apriltag_detect.py movies/kam0_20261011_185254.mp4 --tag-size 0.16 --step 3 --csv out.csv
"""
import argparse, csv, math, sys
import cv2, numpy as np
from pupil_apriltags import Detector

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('--tag-size', type=float, default=0.16)
ap.add_argument('--step', type=int, default=3, help='process every N-th frame')
ap.add_argument('--hfov', type=float, default=54.0, help='horizontal field of view [deg] for the pinhole guess')
ap.add_argument('--fx', type=float); ap.add_argument('--fy', type=float); ap.add_argument('--cx', type=float); ap.add_argument('--cy', type=float)
ap.add_argument('--rotate180', action='store_true', help='apply the kam0 rotation if the player does not')
ap.add_argument('--csv'); ap.add_argument('--t0', type=float, default=0.0, help='offset added to the video time [s]')
a = ap.parse_args()

cap = cv2.VideoCapture(a.video)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fx = a.fx or (W / 2) / math.tan(math.radians(a.hfov / 2)); fy = a.fy or fx
cx = a.cx or W / 2; cy = a.cy or H / 2
det = Detector(families='tag36h11', nthreads=4, quad_decimate=1.0, refine_edges=True, decode_sharpening=0.25)
rows = []; n = 0; nframes = 0; frames_with = 0
while True:
    ok, frame = cap.read()
    if not ok: break
    if n % a.step: n += 1; continue
    nframes += 1
    if a.rotate180: frame = cv2.rotate(frame, cv2.ROTATE_180)
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    r = det.detect(g, estimate_tag_pose=True, camera_params=(fx, fy, cx, cy), tag_size=a.tag_size)
    if r: frames_with += 1
    for d in r:
        t = d.pose_t.ravel(); R = d.pose_R
        # camera position in the tag frame: C = -R^T t ; distance along the tag normal = height above the tag plane
        C = -R.T @ t
        side = float(np.mean([np.linalg.norm(d.corners[i] - d.corners[(i + 1) % 4]) for i in range(4)]))
        rows.append(dict(t_s=round(a.t0 + n / fps, 3), frame=n, id=d.tag_id, margin=round(float(d.decision_margin), 1),
                         side_px=round(side, 1), cx_px=round(float(d.center[0]), 1), cy_px=round(float(d.center[1]), 1),
                         x_m=round(float(C[0]), 3), y_m=round(float(C[1]), 3), z_m=round(float(C[2]), 3),
                         dist_m=round(float(np.linalg.norm(t)), 3), err=round(float(d.pose_err), 6)))
    n += 1
cap.release()
print(f'{a.video}: {W}x{H} @ {fps:.1f} fps, {nframes} frames checked (step {a.step}), {frames_with} with a tag, {len(rows)} detections; fx={fx:.1f}')
ids = sorted(set(r['id'] for r in rows))
for i in ids:
    z = [r['z_m'] for r in rows if r['id'] == i]; s = [r['side_px'] for r in rows if r['id'] == i]
    print(f'  ID {i}: {len(z)} detections, height above tag median {np.median(z):.3f} m (min {min(z):.2f} max {max(z):.2f}), side {np.median(s):.0f} px')
if a.csv and rows:
    with open(a.csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
