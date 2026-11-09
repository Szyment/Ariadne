# Intrinsic calibration of the onboard cameras

Calibration of both OV5647 cameras of the Raspberry Pi 5 (kam0 standard lens, kam1 NoIR with the longer lens) at the recording resolution 1296 × 972, in the native sensor orientation (the raw stream, before the 180° rotation of kam0 that is applied only at output). Done on 1 Nov 2026 indoors at home, cameras mounted on the aircraft, the aircraft standing still on a support with the lenses about 1 m above the floor.

## Setup and recordings

Chessboard printed on A4 (`apriltag/ariadne_kam0_calibration_chessboard_9x6_25mm_A4.pdf`): 9 × 6 inner corners, 25 mm squares. The board was placed in a series of still poses across the field of view, flat on the floor and tilted or raised on boxes (20 and 30 cm). Both cameras recorded the raw stream with `rpicam-vid` (H.264, 30 fps) while the board was moved; the recordings are `movies/calib_20261101/kam0_calib.h264` (53 354 frames) and `kam1_calib.h264` (26 521 frames). The first part of the kam0 recording was taken at other heights (lens 1.37 to 1.39 m above the floor) and is not used; the calibration frames come from the part with the lens at 0.96 m.

Photos: `build-log/photos/2026-11-01/` (EXIF local time), IMG_2370 to IMG_2380 at 15:03 to 15:32: the aircraft resting on a bar clamped between two tables, the board on the floor below it, lit by a studio lamp with an umbrella. Illuminance at the floor next to the board, Benetech GM1010 in foot-candles: 29.2 fc (IMG_2371, 15:04) and 40.8 fc (IMG_2373, 15:09).

Reference distances measured with a laser distance meter, lens to floor: kam0 0.96 m, kam1 0.94 m; rangefinder 0.96 m (laser), the same rangefinder in QGC `DISTANCE_SENSOR` 0.93 m.

## Method

Scripts: `analysis/apriltag_raw/cb_scan.py` and `cb_calib.py` (OpenCV).

1. `cb_scan.py` decodes every 15th frame at half resolution and records where the board is found (square size in pixels, board centre). Output: `analysis/results/apriltag/20261101/chessboard_scan_kam0.csv`, `chessboard_scan_kam1.csv`.
2. `cb_calib.py` keeps only frames in which the board stood still (the next scanned frame, 15 frames later, has the board centre within 1 px and the square size within 0.2 px), then one frame per cell of a grid over board position (120 px) and square size (2 px), so that the views are diverse and not dominated by one pose.
3. On the selected frames: full-resolution luminance, `findChessboardCorners`, `cornerSubPix`, then `calibrateCameraExtended`. Views with a reprojection error above 2.5 × the median are dropped and the calibration is repeated without them.
4. Two models are computed: the full five-coefficient model (k1, k2, p1, p2, k3) and the same without tangential terms. The full model is adopted for both cameras.

## Results (adopted model: k1 k2 p1 p2 k3)

| | kam0 | kam1 |
|---|---|---|
| fx, fy [px] | 1293.0, 1294.5 | 1544.2, 1544.5 |
| cx, cy [px] | 651.2, 469.2 | 630.2, 499.1 |
| k1, k2, p1, p2, k3 | 0.0978, −0.4655, −0.0019, −0.0019, 0.4234 | −0.5250, 0.3663, −0.0052, 0.0018, −0.1941 |
| RMS reprojection error | 0.211 px | 0.219 px |
| views with corners found / used | 32 / 31 | 24 / 19 |
| horizontal × vertical field of view | 53.2° × 41.2° | 45.5° |
| radial distortion at r = 648 px (image edge) | +0.2 % | −8.2 % |
| radial distortion in the image corners | −0.8 % | −12.1 % |

Check against the laser: the depth of the board centre in the near-flat views (tilt below 3°) is 0.968 m for kam0 (laser 0.96 m) and 0.954 m for kam1 (laser 0.94 m).

The files `kam0_20261101.json` and `kam1_20261101.json` hold the frame numbers with corners found and both models; use the entry `k1k2p1p2k3`.

## What it changes

kam0 is close to a distortion-free pinhole across most of the frame; kam1 has strong barrel distortion, so any geometry from kam1 near the edge of the frame needs the distortion model.

Before this calibration the analysis of the 1 Nov flights used a provisional kam0 model fitted to flight data (fx 1258 px, k1 −0.30). That model gave a 10 % scale error in the distance between tags computed from the image and the rangefinder height. With the calibrated model the same quantity is 0.755 to 0.756 m against 0.75 m laid out and measured with a laser, so the error came from the provisional model and not from the rangefinder or the camera. Details in `analysis/apriltag_raw/README.md`.
