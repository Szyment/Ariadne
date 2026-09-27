# data

The E1 dataset (CC BY 4.0): one CSV per run, cut from the ArduPilot dataflash log by `analysis/cut_runs.py` (window from the switch to source set 2 until the return to GNSS, with a margin on both sides). File name: `ARIADNE_E1_<run>_<date>_<cell>.csv`; `KAL` = calibration flight, `TEST` = test flight outside the dataset. Cell code: LUX (1 daylight, d dusk), SURF (1 grass, 2 ploughed field), ALT (3 = 3 m, 15 = 1.5 m), VEL (15 = 1.5 m/s).


## Data dictionary

One row per estimator position sample (POS message, ~10 Hz); other messages are matched to the nearest earlier sample. Column names keep the ArduPilot message and field they come from.

| Column | Unit | Meaning |
|---|---|---|
| `t_log_s` | s | log time (TimeUS/1e6) |
| `phase` |  | phase: before (before the switch), flow_only (source set 2, no GNSS), after (after the return to GNSS) |
| `t_since_src2_s` | s | time since the switch to source set 2 |
| `ekf_lat` | deg | estimator position (POS.Lat) |
| `ekf_lon` | deg | estimator position (POS.Lng) |
| `ekf_alt` | m | estimator altitude (POS.Alt) |
| `gps_lat` | deg | GNSS position, reference only (GPS.Lat) |
| `gps_lon` | deg | GNSS position (GPS.Lng) |
| `gps_nsats` |  | satellites (GPS.NSats) |
| `gps_hdop` |  | HDOP (GPS.HDop) |
| `gps_spd` | m/s | GNSS ground speed (GPS.Spd) |
| `of_qual` | 0–255 | optical-flow image quality (OF.Qual) |
| `of_flowX` | rad/s | raw flow rate X (OF.flowX) |
| `of_flowY` | rad/s | raw flow rate Y (OF.flowY) |
| `of_bodyX` | rad/s | body rotation rate X (OF.bodyX) |
| `of_bodyY` | rad/s | body rotation rate Y (OF.bodyY) |
| `rfnd_dist` | m | rangefinder distance (RFND.Dist) |
| `ctun_alt` | m | barometric altitude above home (CTUN.Alt) |
| `roll` | deg | ATT.Roll |
| `pitch` | deg | ATT.Pitch |
| `yaw` | deg | ATT.Yaw |
| `xkf4_SV` |  | velocity test ratio (XKF4.SV) |
| `xkf4_SP` |  | position test ratio (XKF4.SP) |
| `xkf4_SH` |  | height test ratio (XKF4.SH) |
| `xkf4_SM` |  | magnetometer test ratio (XKF4.SM) |
| `xkf4_SS` | bitmask | solution status (XKF4.SS) |
| `rc7` | PWM | RC channel 7 = EKF source-set switch (RCIN.C7) |
| `mode` |  | flight mode number (MODE.Mode) |
| `gpa_hacc` | m | GNSS horizontal accuracy (GPA.HAcc) |
| `gpa_sacc` | m/s | GNSS speed accuracy (GPA.SAcc) |
| `xkf3_IVN` | m/s | velocity innovation N (XKF3.IVN) |
| `xkf3_IVE` | m/s | velocity innovation E (XKF3.IVE) |
| `xkf4_TS` | bitmask | timeout status (XKF4.TS) |
| `xkf5_FIX` |  | optical-flow measurement residual X (XKF5.FIX) |
| `xkf5_FIY` |  | optical-flow measurement residual Y (XKF5.FIY) |
| `xkf5_AFI` |  | auxiliary flow innovation (XKF5.AFI) |
| `xkf5_HAGL` | m | height above ground estimate (XKF5.HAGL) |
| `xkf5_RI` | m | range innovation (XKF5.RI) |
| `xkf5_eVel` | m/s | estimator velocity uncertainty (XKF5.eVel) |
| `xkf5_ePos` | m | estimator position uncertainty (XKF5.ePos) |
| `vibe_x` | m/s² | vibration X (VIBE.VibeX) |
| `vibe_y` | m/s² | vibration Y (VIBE.VibeY) |
| `vibe_z` | m/s² | vibration Z (VIBE.VibeZ) |

Files are UTF-8 CSV with a header row, decimal point, comma separator. Runs listed with session, cell and acceptance flags in `../flight-logs/INDEX.md`.

## Files

| File | Title |
|---|---|
| [`ARIADNE_E1_001_20260912_LUX1-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_001_20260912_LUX1-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_002_20260912_LUX1-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_002_20260912_LUX1-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_003_20260912_LUX1-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_003_20260912_LUX1-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_004_20260912_LUX1-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_004_20260912_LUX1-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_005_20260912_LUX1-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_005_20260912_LUX1-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_006_20260912_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_006_20260912_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_007_20260912_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_007_20260912_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_008_20260912_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_008_20260912_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_009_20260912_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_009_20260912_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_010_20260912_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_010_20260912_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_011_20260912_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_011_20260912_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_012_20260913_LUX1-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_012_20260913_LUX1-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_013_20260913_LUX1-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_013_20260913_LUX1-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_014_20260913_LUX1-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_014_20260913_LUX1-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_015_20260913_LUX1-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_015_20260913_LUX1-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_016_20260913_LUX1-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_016_20260913_LUX1-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_017_20260913_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_017_20260913_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_018_20260913_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_018_20260913_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_019_20260913_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_019_20260913_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_020_20260917_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_020_20260917_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_021_20260917_LUXd-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_021_20260917_LUXd-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_022_20260917_LUXd-SURF1-ALT15-VEL15.csv`](ARIADNE_E1_022_20260917_LUXd-SURF1-ALT15-VEL15.csv) |  |
| [`ARIADNE_E1_023_20260917_LUXd-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_023_20260917_LUXd-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_024_20260920_LUX2-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_024_20260920_LUX2-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_025_20260920_LUX2-SURF1-ALT3-VEL15.csv`](ARIADNE_E1_025_20260920_LUX2-SURF1-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_026_20260920_LUX2-SURF1-ALT3-VEL075.csv`](ARIADNE_E1_026_20260920_LUX2-SURF1-ALT3-VEL075.csv) |  |
| [`ARIADNE_E1_027_20260920_LUX2-SURF1-ALT3-VEL075.csv`](ARIADNE_E1_027_20260920_LUX2-SURF1-ALT3-VEL075.csv) |  |
| [`ARIADNE_E1_028_20260920_LUX2-SURF1-ALT3-VEL075.csv`](ARIADNE_E1_028_20260920_LUX2-SURF1-ALT3-VEL075.csv) |  |
| [`ARIADNE_E1_029_20260920_LUX2-SURF1-ALT3-VEL075.csv`](ARIADNE_E1_029_20260920_LUX2-SURF1-ALT3-VEL075.csv) |  |
| [`ARIADNE_E1_030_20260920_LUX2-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_030_20260920_LUX2-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_031_20260920_LUX2-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_031_20260920_LUX2-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_E1_032_20260920_LUX2-SURF2-ALT3-VEL15.csv`](ARIADNE_E1_032_20260920_LUX2-SURF2-ALT3-VEL15.csv) |  |
| [`ARIADNE_KAL_20260912_29.csv`](ARIADNE_KAL_20260912_29.csv) |  |
| [`ARIADNE_KAL_20260913_33.csv`](ARIADNE_KAL_20260913_33.csv) |  |
| [`ARIADNE_KAL_20260917_38.csv`](ARIADNE_KAL_20260917_38.csv) |  |
| [`ARIADNE_KAL_20260920_40.csv`](ARIADNE_KAL_20260920_40.csv) |  |
| [`ARIADNE_TEST_20260917_39_LUXd-SURF2-ALT3-VEL15.csv`](ARIADNE_TEST_20260917_39_LUXd-SURF2-ALT3-VEL15.csv) |  |
