#!/usr/bin/env python3
"""AprilTag detector benchmark for the Raspberry Pi 5, on 300 raw kam0 frames from flight 7 (1 Nov 2026).
Run with the recording services ACTIVE, so that the load is the same as in flight.
Usage: python3 bench_rpi.py [frames.npy] [expected.csv]"""
import sys, time, os, csv, subprocess, numpy as np
from pupil_apriltags import Detector
fp = sys.argv[1] if len(sys.argv) > 1 else 'kam0_f7_frames12150-12449_Y1296x972.npy'
ep = sys.argv[2] if len(sys.argv) > 2 else 'expected_mac_dec2.csv'
Y = np.load(fp); n = len(Y)
exp = {}
for r in csv.DictReader(open(ep)): exp.setdefault(int(r['frame']) - 12150, set()).add(int(r['id']))
def sh(c):
    try: return subprocess.check_output(c, shell=True, text=True).strip()
    except Exception as e: return f'n/a ({e.__class__.__name__})'
print('host', sh('hostname'), '| cpu', sh('nproc'), 'cores |', sh('vcgencmd measure_temp'), '|', sh('vcgencmd get_throttled'))
print('recording services:', sh('systemctl is-active ariadne-nagrywanie@0 ariadne-nagrywanie@1 | tr "\\n" " "'))
print('load before:', sh('cat /proc/loadavg'))
VARIANTS = [('full 1296x972, decimate 2, 4 threads', False, 2.0, 4), ('full 1296x972, decimate 2, 2 threads', False, 2.0, 2),
            ('lores 648x486, decimate 1, 2 threads', True, 1.0, 2), ('lores 648x486, decimate 1, 1 thread', True, 1.0, 1),
            ('lores 648x486, decimate 2, 1 thread', True, 2.0, 1)]
print(f'\n{"variant":42s} {"ms med":>7s} {"ms p95":>7s} {"max fps":>8s} {"frames ok":>10s} {"missed":>7s} {"extra":>6s}')
for name, lores, dec, th in VARIANTS:
    det = Detector(families='tag36h11', nthreads=th, quad_decimate=dec, refine_edges=True, decode_sharpening=0.25)
    t = []; ok = miss = extra = 0
    for i in range(n):
        g = np.ascontiguousarray(Y[i, ::2, ::2]) if lores else Y[i]
        t0 = time.perf_counter(); r = det.detect(g); t.append(time.perf_counter() - t0)
        got = {d.tag_id for d in r if d.tag_id in (10, 11, 12)}; want = exp.get(i, set())
        miss += len(want - got); extra += len(got - want); ok += (got == want)
    t = np.array(t) * 1000
    print(f'{name:42s} {np.median(t):7.1f} {np.percentile(t, 95):7.1f} {1000/np.median(t):8.1f} {ok:>6d}/{n:<3d} {miss:7d} {extra:6d}')
print('\nload after:', sh('cat /proc/loadavg'), '|', sh('vcgencmd measure_temp'), '|', sh('vcgencmd get_throttled'))
