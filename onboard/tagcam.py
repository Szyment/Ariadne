#!/usr/bin/env python3
"""tagcam.py, stage A (bench test): one process for camera 0 that

1. records exactly as record.sh does: 1296x972, 30 fps, H.264 with the SPS/PPS headers
   repeated in every keyframe, 60 s segments named kamN_HHMMSS_%05d.h264, no transform
   (native sensor orientation, kam0 upside down as in every raw recording);
2. in parallel takes the ISP's low-resolution stream (640x480, same field of view) and runs
   AprilTag detection (tag36h11) on its Y plane, every N-th frame;
3. writes three CSV files next to the segments: frames.csv (one row per encoded frame:
   frame number, segment, keyframe flag, encoder timestamp), detections.csv (one row per
   detected tag, corners in full-resolution pixels) and processed.csv (one row per frame
   given to the detector: sensor timestamp, clocks, exposure, gain, detector time);
   clock steps of the wall clock against the monotonic clock go to clock.csv.

No serial port, no MAVLink, no commands to the flight controller.
Stage A runs on the bench with the recording service of the same camera stopped.

Usage (in the venv that has pupil-apriltags and sees the system picamera2):
  ~/venvs/tags/bin/python tagcam.py [--camera 0] [--minutes 10] [--every 2] [--decimate 2] [--exposure-us 8000]
"""
import argparse, csv, inspect, json, os, resource, signal, sys, threading, time
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import LibavH264Encoder
from picamera2.outputs import Output
from pupil_apriltags import Detector

MAIN = (1296, 972)
LORES = (640, 480)
FPS = 30
# principal point of kam0 from the chessboard calibration of 1 Nov 2026 (native orientation),
# used only for the offset column in tag-side units; the raw corners are logged as well
PP = {0: (651.2, 469.2), 1: (630.2, 499.1)}


class SegmentedOutput(Output):
    """Writes the H.264 stream into segments of about seg_s seconds, switching only at a
    keyframe, so every segment starts with SPS/PPS and an IDR frame and plays on its own."""

    def __init__(self, pattern, seg_s, index_path):
        super().__init__()
        self.pattern, self.seg_s = pattern, seg_s
        self.n_seg, self.f, self.t_open = -1, None, None
        self.frame = self.frame_in_seg = self.bytes = 0
        self.lock = threading.Lock()
        self.stopped = False
        self.closing = []                               # closer threads for finished segments
        self.idx_f = open(index_path, 'w', newline='')
        self.idx = csv.writer(self.idx_f)
        self.idx.writerow(['frame', 'segment', 'frame_in_segment', 'keyframe', 'encoder_ts_us', 'mono_ns'])

    @staticmethod
    def _close(f):
        f.flush(); os.fsync(f.fileno()); f.close()

    def _open(self):
        if self.f:
            # flush + fsync + close in a separate thread: done inline it blocked the encoder
            # thread for about 250 ms at every segment switch and the camera dropped frames
            t = threading.Thread(target=self._close, args=(self.f,), daemon=True); t.start()
            self.closing = [c for c in self.closing if c.is_alive()] + [t]
        self.n_seg += 1
        self.f = open(self.pattern % self.n_seg, 'wb')
        self.t_open, self.frame_in_seg = time.monotonic(), 0

    def outputframe(self, frame, keyframe=True, timestamp=None, *args, **kwargs):
        with self.lock:
            if self.f is None:
                if not keyframe:
                    return                      # wait for the first keyframe
                self._open()
            elif keyframe and time.monotonic() - self.t_open >= self.seg_s:
                self._open()
            self.f.write(frame)
            self.bytes += len(frame)
            self.idx.writerow([self.frame, self.n_seg, self.frame_in_seg, int(bool(keyframe)), timestamp, time.monotonic_ns()])
            self.frame += 1; self.frame_in_seg += 1

    def stop(self):
        with self.lock:
            if self.stopped:                            # stop_recording() already called it
                return
            self.stopped = True
            if self.f:
                self._close(self.f); self.f = None
            for t in self.closing:
                t.join(timeout=10)
            self.idx_f.flush(); self.idx_f.close()
        try:
            super().stop()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--camera', type=int, default=0)
    ap.add_argument('--outdir', default=None, help='default ~/nagrania/tagcam_YYYYMMDD-HHMM')
    ap.add_argument('--minutes', type=float, default=10.0, help='stop by itself after this time (0 = run until SIGINT)')
    ap.add_argument('--segment', type=float, default=60.0, help='segment length [s]')
    ap.add_argument('--bitrate', type=int, default=6_000_000)
    ap.add_argument('--intra', type=int, default=30, help='keyframe period [frames]')
    ap.add_argument('--every', type=int, default=2, help='run the detector on every N-th low-resolution frame')
    ap.add_argument('--decimate', type=float, default=2.0)
    ap.add_argument('--threads', type=int, default=1)
    ap.add_argument('--ids', default='0-24', help='accepted tag IDs, e.g. 0-24 or 10,11,12')
    ap.add_argument('--stats', type=float, default=10.0, help='print statistics every N seconds')
    ap.add_argument('--exposure-us', type=int, default=0, help='fixed exposure time [us], analogue gain stays automatic (0 = full auto exposure)')
    a = ap.parse_args()

    ids = set()
    for part in a.ids.split(','):
        lo, _, hi = part.partition('-'); ids.update(range(int(lo), int(hi or lo) + 1))
    cam = a.camera
    outdir = os.path.expanduser(a.outdir or time.strftime('~/nagrania/tagcam_%Y%m%d-%H%M'))
    os.makedirs(outdir, exist_ok=True)
    stamp = time.strftime('%H%M%S')
    pattern = os.path.join(outdir, f'kam{cam}_{stamp}_%05d.h264')

    picam2 = Picamera2(cam)
    modes = [m for m in picam2.sensor_modes if tuple(m['size']) == MAIN]
    bit_depth = modes[0].get('bit_depth', 10) if modes else 10
    kw = dict(main={'size': MAIN, 'format': 'YUV420'}, lores={'size': LORES, 'format': 'YUV420'},
              controls={'FrameDurationLimits': (int(1e6 / FPS), int(1e6 / FPS))}, buffer_count=8, encode='main')
    if a.exposure_us > 0:
        # fixed shutter, gain left to the AGC: over grass at 1.5 m/s the automatic 33 ms shutter blurs
        # the tag over almost two cells (2 Nov 2026); with 8 ms the blur is 1.2 cm, under half a cell
        kw['controls']['ExposureTime'] = a.exposure_us
    try:
        cfg = picam2.create_video_configuration(sensor={'output_size': MAIN, 'bit_depth': bit_depth}, **kw)
    except TypeError:                                   # older picamera2 without the sensor argument
        cfg = picam2.create_video_configuration(raw={'size': MAIN}, **kw)
    picam2.configure(cfg)
    used = picam2.camera_configuration()
    lw, lh = used['lores']['size']
    mw, mh = used['main']['size']
    sx, sy = mw / lw, mh / lh

    ekw = dict(bitrate=a.bitrate, repeat=True, iperiod=a.intra, framerate=FPS)
    eparams = inspect.signature(LibavH264Encoder.__init__).parameters
    if 'profile' in eparams:
        ekw['profile'] = 'baseline'
    enc = LibavH264Encoder(**ekw)
    out = SegmentedOutput(pattern, a.segment, os.path.join(outdir, f'kam{cam}_{stamp}_frames.csv'))

    import picamera2 as p2
    info = dict(started_wall=time.strftime('%Y-%m-%dT%H:%M:%S%z'), camera=cam, picamera2=getattr(p2, '__version__', 'unknown'),
                sensor_mode_bit_depth=bit_depth, main=list(used['main']['size']), lores=[lw, lh],
                main_format=used['main']['format'], lores_format=used['lores']['format'],
                sensor=str(used.get('sensor')), raw=str(used.get('raw', {}).get('size')),
                encoder=dict((k, v) for k, v in ekw.items()), encoder_profile_supported='profile' in eparams,
                detector=dict(decimate=a.decimate, threads=a.threads, every=a.every, ids=a.ids), exposure_us=a.exposure_us,
                segment_s=a.segment, principal_point=PP.get(cam))
    with open(os.path.join(outdir, f'kam{cam}_{stamp}_run.json'), 'w') as f:
        json.dump(info, f, indent=1)
    print(json.dumps(info, indent=1), flush=True)

    det = Detector(families='tag36h11', nthreads=a.threads, quad_decimate=a.decimate, refine_edges=True, decode_sharpening=0.25)
    df = open(os.path.join(outdir, f'kam{cam}_{stamp}_detections.csv'), 'w', newline='')
    pf = open(os.path.join(outdir, f'kam{cam}_{stamp}_processed.csv'), 'w', newline='')
    cf = open(os.path.join(outdir, f'kam{cam}_{stamp}_clock.csv'), 'w', newline='')
    dw, pw, cw = csv.writer(df), csv.writer(pf), csv.writer(cf)
    dw.writerow(['req', 'sensor_ts_ns', 'id', 'hamming', 'margin'] + [f'{k}{i}' for i in range(4) for k in 'xy'] +
                ['cx', 'cy', 'side_px', 'dx_side', 'dy_side'])
    pw.writerow(['req', 'sensor_ts_ns', 'mono_ns', 'boot_ns', 'wall_ns', 'exposure_us', 'analogue_gain', 'lux', 'det_ms', 'n_tags', 'gap_frames'])
    cw.writerow(['mono_ns', 'wall_ns', 'step_ms'])
    ppx, ppy = PP.get(cam, (mw / 2, mh / 2))

    running = [True]
    def stop(*_):
        running[0] = False
    signal.signal(signal.SIGINT, stop); signal.signal(signal.SIGTERM, stop)

    picam2.start_recording(enc, out)
    t_start = time.monotonic(); t_stat = t_start
    ru0 = resource.getrusage(resource.RUSAGE_SELF); frames0 = 0
    nreq = nproc = ntags = gaps = 0; tags_int = frames_tag_int = 0; last_ts = None; last_off = None; dms = []; lat = []
    try:
        while running[0]:
            if a.minutes and time.monotonic() - t_start > a.minutes * 60:
                break
            req = picam2.capture_request()
            try:
                md = req.get_metadata()
                ts = md.get('SensorTimestamp')
                mono, boot, wall = time.monotonic_ns(), time.clock_gettime_ns(time.CLOCK_BOOTTIME), time.time_ns()
                gap = 0
                if ts is not None and last_ts is not None:
                    gap = int(round((ts - last_ts) / (1e9 / FPS))) - 1
                    gaps += max(gap, 0)
                last_ts = ts
                nreq += 1
                if nreq % a.every:
                    continue
                arr = req.make_array('lores')
            finally:
                req.release()
            off = wall - mono
            if last_off is not None and abs(off - last_off) > 20_000_000:
                cw.writerow([mono, wall, round((off - last_off) / 1e6, 1)]); cf.flush()
            last_off = off
            y = np.ascontiguousarray(arr[:lh, :lw])
            t0 = time.perf_counter(); r = det.detect(y); dt = (time.perf_counter() - t0) * 1000
            dms.append(dt); nproc += 1
            if ts is not None:
                lat.append((time.monotonic_ns() - ts) / 1e6)
            n = 0
            for d in r:
                if d.tag_id not in ids:
                    continue
                c = (d.corners + 0.5) * (sx, sy) - 0.5           # to full-resolution pixels
                cx, cy = c.mean(0)
                side = float(np.mean([np.linalg.norm(c[i] - c[(i + 1) % 4]) for i in range(4)]))
                dw.writerow([nreq, ts, d.tag_id, d.hamming, round(float(d.decision_margin), 1)] +
                            [round(float(v), 2) for v in c.ravel()] +
                            [round(float(cx), 2), round(float(cy), 2), round(side, 2),
                             round((cx - ppx) / side, 4), round((cy - ppy) / side, 4)])
                n += 1
            ntags += n; tags_int += n; frames_tag_int += (n > 0)
            pw.writerow([nreq, ts, mono, boot, wall, md.get('ExposureTime'), round(md.get('AnalogueGain', 0) or 0, 3),
                         round(md.get('Lux', 0) or 0, 1), round(dt, 2), n, gap])
            now = time.monotonic()
            if now - t_stat >= a.stats:
                ru = resource.getrusage(resource.RUSAGE_SELF)
                cpu = (ru.ru_utime + ru.ru_stime - ru0.ru_utime - ru0.ru_stime) / (now - t_stat) * 100
                enc_fps = (out.frame - frames0) / (now - t_stat)
                print(f'[{now - t_start:6.0f} s] encoded {out.frame} frames ({enc_fps:.1f}/s, segment {out.n_seg}), '
                      f'detector {nproc} frames ({len(dms) / (now - t_stat):.1f}/s), det ms med {np.median(dms):.1f} '
                      f'p95 {np.percentile(dms, 95):.1f}, tags/s {tags_int / (now - t_stat):.1f} '
                      f'(frames with a tag {100 * frames_tag_int / max(len(dms), 1):.0f} %), '
                      f'sensor-to-result ms med {np.median(lat) if lat else float("nan"):.0f}, '
                      f'gaps {gaps}, process CPU {cpu:.0f} % of one core', flush=True)
                for fh in (df, pf): fh.flush()
                t_stat, ru0, frames0, dms, lat, tags_int, frames_tag_int = now, ru, out.frame, [], [], 0, 0
    finally:
        for step in (picam2.stop_recording, out.stop, df.close, pf.close, cf.close, picam2.close):
            try:
                step()
            except Exception as e:
                print(f'shutdown step {getattr(step, "__name__", step)} failed: {e!r}', flush=True)
        print(f'stopped: {out.frame} frames in {out.n_seg + 1} segments, {nproc} frames to the detector, {ntags} tag detections, '
              f'{gaps} missed sensor frames on the detector side; output in {outdir}', flush=True)


if __name__ == '__main__':
    main()
