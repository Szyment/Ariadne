#!/usr/bin/env python3
"""AprilTag detection on raw kam0 .h264 segments, as the RPi will see the stream:
Y plane of each decoded frame, native sensor orientation (no rotation), 1296x972.
Writes one row per detection with the 4 corners (pixels, native orientation).
Frame index is global within the session directory (sum of earlier segments).
Usage: raw_detect.py out.csv session_dir first_seg last_seg [--dec 2] [--ids 10,11,12]"""
import sys, os, glob, subprocess, time, argparse, csv, numpy as np
from pupil_apriltags import Detector
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('sdir'); ap.add_argument('s0', type=int); ap.add_argument('s1', type=int)
ap.add_argument('--dec', type=float, default=2.0); ap.add_argument('--ids', default='10,11,12'); ap.add_argument('--cam', default='kam0')
a = ap.parse_args()
ids = set(int(x) for x in a.ids.split(','))
segs = sorted(glob.glob(os.path.join(a.sdir, f'{a.cam}_*_[0-9][0-9][0-9][0-9][0-9].h264')))
def nframes(p):
    return int(subprocess.check_output(['ffprobe', '-v', 'error', '-f', 'h264', '-count_packets', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p]).strip())
cache = os.path.join(a.sdir, f'.{a.cam}_framecounts.txt')
counts = {}
if os.path.exists(cache):
    for l in open(cache): k, v = l.split(); counts[k] = int(v)
for p in segs:
    b = os.path.basename(p)
    if b not in counts: counts[b] = nframes(p)
try:
    with open(cache, 'w') as f: f.writelines(f'{k} {v}\n' for k, v in counts.items())
except OSError: pass
f0 = sum(counts[os.path.basename(p)] for p in segs[:a.s0])
use = segs[a.s0:a.s1 + 1]
W, H = 1296, 972; FS = W * H * 3 // 2
det = Detector(families='tag36h11', nthreads=4, quad_decimate=a.dec, refine_edges=True, decode_sharpening=0.25)
cat = subprocess.Popen(['cat'] + use, stdout=subprocess.PIPE)
ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-r', '30', '-f', 'h264', '-i', '-', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'], stdin=cat.stdout, stdout=subprocess.PIPE, bufsize=FS * 4)
rows = []; n = f0; td = []; rej = 0
while True:
    buf = ff.stdout.read(FS)
    if len(buf) < FS: break
    y = np.frombuffer(buf, np.uint8, W * H).reshape(H, W)
    t0 = time.perf_counter(); r = det.detect(y); td.append(time.perf_counter() - t0)
    for d in r:
        if d.tag_id not in ids: rej += 1; continue
        c = d.corners
        row = dict(frame=n, id=d.tag_id, margin=round(float(d.decision_margin), 1), ham=d.hamming,
                   cx=round(float(d.center[0]), 2), cy=round(float(d.center[1]), 2))
        for i in range(4): row[f'x{i}'] = round(float(c[i, 0]), 2); row[f'y{i}'] = round(float(c[i, 1]), 2)
        rows.append(row)
    n += 1
new = not os.path.exists(a.out)
with open(a.out, 'a', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['frame', 'id', 'margin', 'ham', 'cx', 'cy'] + [f'{k}{i}' for i in range(4) for k in 'xy'])
    if new: w.writeheader()
    w.writerows(rows)
td = np.array(td) * 1000
print(f'{os.path.basename(a.sdir)} seg {a.s0}-{a.s1}: frames {f0}-{n - 1}, det {len(rows)} (rejected IDs {rej}), frames with tag {len(set(r["frame"] for r in rows))}, ms median {np.median(td):.1f} p95 {np.percentile(td, 95):.1f}')
