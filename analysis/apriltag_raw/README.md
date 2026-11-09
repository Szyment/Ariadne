# AprilTag detection on the raw onboard stream (1 Nov 2026)

Offline analysis of the AprilTag test flights of 1 Nov 2026 (`flight-logs/INDEX.md`, section "AprilTag camera tests, outside E1"; logs 63 and 64), done on the raw H.264 segments as the Raspberry Pi records them, not on the stitched MP4: luminance plane of each decoded frame, 1296 × 972, native sensor orientation (no rotation). This is the input the onboard detector sees, so detection rates, pixel sizes and image axes found here transfer directly to the Pi. Row on the ground: ID 10–12, 0.75 m between centres (laser), track across the row, 1.5 m terrain frame.

## Scripts

| Script | What it does |
|---|---|
| `raw_detect.py` | detection on a range of raw segments of one session directory (`pupil-apriltags`, tag36h11, ID whitelist, `quad_decimate` 2 by default); one row per detection with ID, decision margin, Hamming distance, centre and four corners in pixels; the frame index is global within the session directory |
| `log_extract.py` | extracts `GPS`, `RFND`, `ATT`, `POS`, `MODE`, `XKF1` from a `.bin` log into a `.npz` with Unix time |
| `sync.py`, `sync2.py` | time offset between the video and the log (see below) |
| `common.py` | loader joining detections with the log at the frame time; holds the session start times, offsets and the camera model |
| `mount.py` | which image axis is body forward: least squares of tag motion in the image against body velocity from GPS course, speed and yaw |
| `world.py`, `scale.py` | tag positions on the ground from image, attitude and rangefinder height; distance between neighbouring tags seen in the same frame |
| `fx.py`, `dist.py` | fits of the focal length and radial distortion to flight data (provisional model, superseded) |
| `cb_scan.py`, `cb_calib.py` | chessboard calibration, described in `hardware/calibration/README.md` |

```
python3 raw_detect.py out.csv ~/nagrania/sesja_066_20261101-1252 0 8 --dec 2 --ids 10,11,12
python3 log_extract.py flight-logs/platform-2-ardupilot/log_64_2026-11-1-13-00-44.bin log64.npz
```

The scripts after `raw_detect.py` were run from one working directory holding the detection CSVs under the names `s065.csv`, `s066.csv` and the extracted logs `log63.npz`, `log64.npz`; they read these relative names.

`common.py` still carries the provisional camera model (fx 1258 px, principal point at the image centre, k1 −0.2986). It was fitted to flight data before the chessboard calibration and is wrong; results computed with it (`fx.py`, `dist.py`, and `scale.py` / `world.py` as written) are superseded. The calibrated model is in `hardware/calibration/`.

## Detections

`analysis/results/apriltag/20261101/`:

| File | Source | Detections | Frames with a tag | ID 10 / 11 / 12 | Median margin |
|---|---|---|---|---|---|
| `raw_kam0_sesja_065_flights3-5.csv` | kam0, `sesja_065`, flights 3 to 5 | 506 | 357 | 148 / 226 / 132 | 47.6 |
| `raw_kam0_sesja_066_flights6-7.csv` | kam0, `sesja_066`, flights 6 and 7 | 5023 | 3422 | 1171 / 2357 / 1495 | 54.3 |
| `raw_kam1_sesja_066_segments5-8.csv` | kam1, `sesja_066`, segments 5 to 8 | 3315 | 2562 | 943 / 1592 / 780 | 53.0 |

Flight 7 (Loiter, flown by hand over the row) gives 3300 of the 3422 kam0 frames with a tag in `sesja_066`; on the Auto passes at 1.5 m/s the row stays in view for a few frames per pass.

## Findings

**Time alignment.** The session directory name is stamped before the first frame and is not the time of frame 0. The offset was found from two independent quantities: tag side in pixels × rangefinder height (constant for a fixed tag size, so it locks the video to `RFND`) and the spread of GPS position during the passes. Frame time = time in the directory name + frame / 30 + offset, with offset +12.5 s for `sesja_065` (name 12:16:29) and +3.1 s for `sesja_066` (name 12:52:21), local time (CET) from GPS.

**Camera axes.** In the raw image (native orientation) +y is body forward and −x is body right. The onboard detector works in this frame; the 180° rotation of kam0 exists only in the stitched MP4.

**Scale.** With the provisional model the distance between neighbouring tags computed from the image and the rangefinder height came out 10 % off. With the chessboard calibration of kam0 the same-frame distance is 0.755 to 0.756 m against 0.75 m measured with a laser. The rangefinder and the attitude are consistent with the image; the error was in the provisional model.

**Tag size against the rangefinder.** With the calibrated model and the rangefinder height, the tag side in pixels implies a black square of 209 to 215 mm on 1 Nov and 210 to 219 mm in the hovers of 2 Nov, while the tags measure 220 mm with a ruler (one 221 mm). The rangefinder is not the cause: checked on 8 Nov 2026 against a laser distance meter at 0.5, 1.0, 1.5 and 2.0 m (`DISTANCE_SENSOR` in QGC), it reads the same. The shortfall grows as the tag gets smaller in the image (0.5 % at 350 px, 4.5 % at 77 px), which is a constant inward bias of the detected corners of about 2 to 3 full-resolution pixels per side, consistent with the onboard detector working on the 640 × 480 stream with `quad_decimate` 2 (one detector pixel is four sensor pixels). It does not affect the row spacing from the image (a ratio) or the position over a tag (the centre); it affects only a height computed from the tag size, which the system does not use.
