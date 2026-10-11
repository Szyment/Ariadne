# analysis

Analysis scripts (Python: pymavlink, pandas, numpy): run extraction, drift analysis, the degradation detector, wind-from-log, flow orientation. `reproduce.sh` regenerates the detector results in `results/` from `data/`. Script documentation follows.

## `session_extract.py`

Extracts from an ArduPilot log (`.bin`) the facts needed to fill in a session card: arming periods, flight duration, maximum altitude, mean throttle, vibration broken down by IMU instance, attitude tracking error, battery balance, GNSS reception quality, mode sequence, EKF3 source switches and diagnostic messages.

```bash
pip install pymavlink
python3 session_extract.py ../../flight-logs/platform-2-ardupilot/log_6_2026-8-19-19-33-42.bin
```

Session cards S-01 … S-04 in the `sessions/` directory were filled in with data from this script. Every number in those cards can be reproduced with a single command, which is a condition of the reproducibility declared in the README.

## `flight_times.py`

Converts the GPS timestamps from the log (week and milliseconds) to civil time. Needed because the log file name contains the moment the session **ended**, not when it started; a mistake in that direction corrupted several cards before it came to light.

## `session_weather.py`

Builds a ready "Atmospheric conditions" block for the session card. From the log it takes the coordinates of the flying site, the absolute time of the session window and the pressure from the onboard barometer. The rest it fetches from the ERA5 reanalysis through the Open-Meteo Archive API. It computes air density.

```bash
python3 session_weather.py ../../flight-logs/platform-2-ardupilot/log_8_2026-8-21-19-56-38.bin \
    --wind "1–2 m/s" \
    --lux "58 lx at start → 21 lx at end" \
    --card ../../sessions/S-05_2026-08-21_filter-verification.md \
    --append \
    --archive ../pogoda-era5
```

Without `--append` the script only prints the block to the screen, so it can be inspected before saving. If the card already has an "Atmospheric conditions" section (or the earlier Polish heading "Warunki atmosferyczne"), the script refuses and overwrites nothing.

`--archive DIRECTORY` saves the raw server response as JSON next to the log. It is worth using always: it allows every number in the card to be reproduced without connecting to the network again, and protects against the provider changing the format or withdrawing the date range.

### What people supply and what the script supplies

In the field, two readings remain: **wind speed from the GM816 anemometer** and **illuminance from the GM1010 lux meter**. The rest fills itself in.

This separation is deliberate. The wind over the field differs from the modelled wind, and illuminance at ground level is an axis of the experiment matrix; neither may be taken from a model. The rejection criteria of protocol §8 rest on the anemometer, and the ERA5 wind serves only as background and as a source of direction.

### Why one source and why ERA5

ERA5 is the ECMWF reanalysis: the same model and the same assimilation procedure for every date since 1940. An August session and a November session are therefore described in the same way, and sessions already flown can be filled in retrospectively. An ordinary weather service does not give this, because it changes model and resolution over time, so a difference between sessions could come from a provider update.

The price: ERA5 enters the archive with a delay of about five days. The script will not build a block for a session flown yesterday. It says so explicitly and gives the date from which the data should be available. It does not then reach for another source, because swapping the source for one session would destroy the comparability of the whole series.

The ERA5 grid resolution is about 25 km. The data describe the situation over the area, not the conditions at the take-off point. The block gives the distance to the nearest grid point, so that this is visible in the card rather than hidden.

### Pressure and air density

Pressure is taken from the aircraft (`BARO.Press`, instance 0, median over the flight window), because it is a measurement at the same place and time as the flight. The ERA5 pressure serves as a check: a discrepancy greater than 2 hPa means a fault on one side or the other and requires checking before the data are used.

**The temperature from the log must not be used.** The fields `BARO.Temp` and `BARO.GndTemp` describe the inside of the controller housing, not the air: in the log of 18 August `BARO.Temp` is 39.3 °C at an air temperature of the order of 20 °C. The barometer heats itself. The ERA5 temperature enters the density calculation, and eventually the reading from the GM816 anemometer, which has its own sensor.

Density is computed for moist air: the partial pressure of water vapour from relative humidity by Buck's formula, then Dalton's law for the mixture of dry air and vapour. The result is referred to 1.225 kg/m³ (15 °C, 1013.25 hPa).

Why compute this at all: the thrust needed to hover varies inversely with air density. Cooling from 25 to 5 °C raises the density by about 7%, which corresponds to about a 3.5% difference in `MOT_THST_HOVER`. That is the same order of magnitude as the differences currently being examined in tuning (0.267 against the measured 0.253–0.261). Without the density correction, autumn flights would look detuned even though only the weather had changed.

### Verification status

Log parsing, time conversion, session window selection, density calculation and block construction were checked on `log_4_2026-8-18-17-58-36.bin`. The connection to the archive itself has not yet been run; the first call will take place on the computer where the logs are stored. The address, variable names, units and delay come from the provider's documentation.

At the first run, check: that the values are not empty, that the ERA5 pressure agrees with the onboard pressure within 2 hPa, and that the distance to the grid point is sensible for Kuźnica Kiedrzyńska.

## `wind_from_log.py`

Computes from the log the wind direction and an indicator of its strength. Basis: an aircraft holding position tilts towards the direction the wind blows from, by an angle that grows with the wind.

```bash
python3 wind_from_log.py ../../flight-logs/platform-2-ardupilot/log_8_2026-8-21-19-56-38.bin
```

The script searches for hover windows (horizontal speed below 0.7 m/s, altitude above 2 m, duration at least 15 s), averages roll and pitch within them, combines them into a tilt vector, rotates it by the aircraft heading and gives the direction the wind blew **from**. The thresholds can be changed with the `--speed`, `--height` and `--min-window` options (also `--throttle` and `--yaw-rate`; the same options apply to `balance.py`, which additionally takes `--spacing`).

Why a separate tool when there is an anemometer: the anemometer gives no direction, measures for one minute at hand height, and depends on who held it. The flight log gives the direction, covers the whole run and applies to the run altitude. These two measurements check each other, and the third independent one is the ERA5 direction from `session_weather.py`. Agreement within one sector means all three work; a discrepancy points to a measurement in the lee or to a miscalibrated compass.

What the script does not give: speed in metres per second. Converting tilt to speed requires the product of the drag coefficient and the frontal area of the aircraft, and that has not been determined. Instead of speed, it gives the horizontal acceleration needed to hold position, g·tan(tilt), a quantity proportional to the wind force and independent of mass, hence comparable also after changes of equipment.

The same arming and throttle condition applies in `wind_from_log.py`; its first version also computed the tilt of an aircraft standing on the ground.

Values of this type have already entered cards S-03, S-04 and S-05 as a "proxy from the log"; the script systematises them, together with the direction, which was not computed before.

The anemometer measurement procedure that this serves as a check on: `protocol/ANNEX_C_wind_measurement.md`.

## `balance.py`

Checks two things at once: whether the battery went back to the same place after charging, and whether the frame is symmetrical.

```bash
python3 balance.py ../../flight-logs/platform-2-ardupilot/log_8_2026-8-21-19-56-38.bin
```

Basis: an aircraft with a shifted centre of gravity **does not tilt**. The controller balances the moment with a thrust difference and the aircraft hovers level; the only trace is uneven motor loading. That is why a pack offset is visible neither on the aircraft nor in telemetry; it is visible only in the flight log.

### Three conditions without which the result is fiction

**The aircraft must be armed and actually flying.** The first version of the script did not check this and took the ground tests of 18 August for a hover: the propellers were turning at idle (throttle 0.03–0.13, output 1080–1260 µs), the aircraft stood on the ground, and the altitude from the estimator had drifted away by several metres. The result, 18.5 mm of offset, described a drone standing in the grass. The current version requires arming and a mean throttle of at least 0.10.

**The window must not contain a commanded turn.** A controller executing a heading turn by design loads one pair of motors more heavily, and that looks identical to a frame asymmetry. The script reads the commanded heading (`ATT.DesYaw`) and skips windows in which it changed faster than 1°/s. Without this filter, the mission `S-04_Test1.plan`, in which the aircraft turns at the corners of the square, gave an inflated asymmetry.

**The payload must be separated from the wind.** Air drag acts at a different height from the centre of gravity, so tilt in wind by itself produces a loading asymmetry. The payload offset is fixed in the aircraft axes, whereas the moment from the wind is fixed relative to the ground. Given at least two hover windows with different headings, the script separates one from the other by least squares. With a single heading this cannot be done, and the script does not pretend to; it then gives the raw values with a note that they contain both causes.

### Torque asymmetry

This quantity is robust to wind, because wind produces no steady moment about the vertical axis. If the pair of motors turning in one direction works persistently harder than the other, the cause is mechanical.

History for Platform 2, resolved on 22 Aug by correcting the seating of the arms in the clamps:

| Session | Log | Windows with settled heading | Asymmetry | Yaw output | Yaw headroom |
|---|---|---|---|---|---|
| 18 Aug evening | 5 | rough estimate | +69% | — | — |
| 19 Aug | 6 | 1 | +16.8% | +60 µs | 30% |
| 20 Aug | 7 | 4 | about +14% | about +60 µs | about 30% |
| 21 Aug | 8 | 4 | about +15% | about +48 µs | about 24% |
| **22 Aug, after the correction** | **9** | **5** | **−2.3%** | **−8 µs** | **4%** |

**Reference value for the battery position, established 22 Aug: 4.1 mm.** A discrepancy above roughly 5 mm means the pack sits differently than it did then.

### Three methods of determining the wind direction agree

On 22 August all three could be compared for the first time:

| Method | Direction |
|---|---|
| GM816 anemometer | 270° |
| Airframe tilt (`wind_from_log.py`) | 283° |
| Motor loading distribution (`balance.py`) | 278° |

The two methods from the log use entirely different signals, the first the roll and pitch angles, the second the outputs of the four motors. Agreement within thirteen degrees confirms at once the compass calibration, the arithmetic and the soundness of separating payload from wind.

### Two corrections introduced on 22 Aug after the first runs

**The hover window ends at the moment a heading turn is commanded.** The first version looked only at horizontal speed, which is zero during a turn on the spot; the four hovers of the mission `S-06_Balance1.plan` thereby merged into one window with an averaged heading, together with the turns between them. Averaging over headings cancelled the tilt from the wind: the window showed 0.31° where the neighbouring ones showed 4.6–4.9°.

**Thrust computed from the ArduPilot curve, not from the square of the output.** AP_Motors linearises the propeller characteristic with the formula `(1 − expo)·t + expo·t²`, where `expo` is `MOT_THST_EXPO`, 0.65 in our case. The approximation by the square alone overstated the relative differences between motors by roughly half. The yaw output in microseconds does not depend on the model and did not change; the numbers in millimetres and percent changed.

## Two pitfalls the scripts account for

**Time reference.** All timestamps are in log seconds (the `TimeUS` field, counted from controller start-up). The Filter Review tool in Mission Planner uses absolute time, so the same events have different timestamps in the two places. The tuning documentation, for example, locates the tip-over after landing of 18 Aug at t = 502.9 s, while the script gives `Crash: Disarming` at 561 s. In every comparison, state which reference is used.

**IMU instances.** The `VIBE` message is logged separately for each instance. The project documentation uses the IMU0 values. IMU2 consistently shows values about half as large, because it is a different sensor; instances must not be mixed in one table.

A third, added on the occasion of the weather work: **the clock change**. The last Sunday of October moves civil time from UTC+2 to UTC+1. Autumn and winter flights converted with a fixed +2 offset would get an hour too much, and with it a wrong reference hour in the weather archive. `session_weather.py` uses the `Europe/Warsaw` time zone.

## What is still missing here

According to `DATA_AUDIT.md`, still missing are a dictionary of the logger fields (description of units and sampling rates) and the actual processing pipeline for the E1–E3 campaign: computation of drift relative to the GNSS trajectory, the failure probability model and the plots. These elements will be created before the first measurement run, not after the campaign.

Also missing is the retrieval of the Kp index. The source (GFZ Potsdam or NOAA SWPC) has not yet been chosen and checked; no address that nobody has called goes into the documentation.

## `drift_analysis.py` and `cut_runs.py` (from 12 Sep 2026)

Data structure from E1 onwards: **the master `.bin` in `flight-logs/` remains untouched** (one log covers several flights), `flight-logs/INDEX.md` maps run → log → time window, and `data/` holds per-run excerpts as CSV for analysis and training.

`drift_analysis.py LOG.bin …`: for each window without GNSS (from `Using EKF Source Set 2` to `Set 1`) it computes the estimator/GNSS path ratio separately for the outbound and return halves (split at the point of maximum distance according to GNSS), the drift of the estimate relative to GNSS at 15/30/60 s and at the end, `OF.Qual`, rangefinder, satellites; at each disarming it compares `CTUN.Alt` with the rangefinder (reference frame drift).

`cut_runs.py LOG.bin --names calibration,E1-001,E1-002 --cell LUX1-SURF1-ALT3-VEL15 --date 20260912 --out data`: cuts the windows with a 25 s margin (`--margin`, to capture the reference hover; `--min-window` sets the shortest accepted SRC2 window, 20 s) into CSV at ~10 Hz: EKF and GNSS position, flow (`OF`), rangefinder, `CTUN.Alt`, attitude angles, `XKF4` residuals, RC7, mode. Column `phase` = `before` / `flow_only` / `after`; column `t_since_src2_s` is the time since the switch to source set 2. A name that does not start with `E1` is written as the calibration flight (`ARIADNE_KAL_...`).

Note of 12 Sep: `CTUN.Alt` (above the take-off point) was ~1.3 m higher than the rangefinder over the field, because take-off was on the dyke and the field lies lower. The terrain frame worked correctly; for altitude above ground use `rfnd_dist`, not `ctun_alt`.

## degradation_detector.py: detector prototype (RQ1), v0.1 of 12 Sep 2026

Works offline on the CSV from `cut_runs.py`, phase `flow_only` only. The detector sees only the onboard signals available without GNSS: `of_qual`, the `xkf4_SV/SH` residuals, the flow scatter after subtracting rotation (`flow − body`, variance in a 1 s window), rangefinder jumps. GNSS is only the reference: error = EKF–GNSS distance minus the offset from the first 2 s after the cut-off.

Rule v0.1: warning when at least 2 indicators (`--votes`) are beyond their threshold continuously for 1 s (`--hold`), or `of_qual` < 50 (`--qual-hard`). Result per run in column `outcome`: `hit` (warning before error > 5 m; lead time in column `lead_time_s`), `false_alarm`, `miss`, `no_event`.

```
python3 analysis/degradation_detector.py data/ARIADNE_E1_*.csv \
    --plots analysis/results/detector --csv analysis/results/detector_v0.1_20260912.csv
```

Thresholds: `--qual-min 150`, `--sv-max 0.5`, `--scatter-max 1.0`, `--rfnd-jump-max 0.5`, `--epos-max 0.3`, `--fi-max 1500`, `--error-m 5.0` (reference error relative to GNSS); `--window 1.0` sets the rolling window.

Baseline from 11 runs of 12 Sep (bright and dusk down to 258 lx): `of_qual` 255 throughout, `SV` ≤ 0.05, scatter ≤ 0.78 rad/s (peaks when starting to move), rangefinder jumps ≤ 0.07 m. The default thresholds (150 / 0.5 / 1.0 / 0.5) lie above this baseline, hence 0 false alarms. E1-005 exceeds 5 m of error with all indicators within norms: the first recorded case of silent drift (with the caveat K1: part of it is GNSS wander). Thresholds to be revised after the first runs with real degradation (below 258 lx, different surface).

**Wind indicator (12 Sep, evening).** Airframe tilt in hover (median `hypot(roll, pitch)` at ground-relative flow < 0.08 rad/s) over 11 runs: without wind 0.79–1.00°, in wind of 1.2–2.1 m/s 1.07–2.47°. Trim offset of ~0.8° subtracted. The ordering within the windy runs does not agree with the block anemometer, so calibration requires wind per flight. In the detector as `w_wind` (column `wind_tilt_deg`, green line on panel 3), without a threshold.

**v0.2 (12 Sep evening).** `cut_runs.py` v0.2 adds to the CSV: `gpa_hacc/sacc` (GNSS accuracy per sample, the answer to K1 at the data level), `xkf3_IVN/IVE`, `xkf4_TS`, `xkf5_FIX/FIY/AFI` (optical-flow measurement residuals), `xkf5_HAGL/RI`, `xkf5_eVel/ePos` (estimator uncertainty), `vibe_x/y/z`. All 12 CSVs of 12 Sep recomputed. Detector v0.2 received two new voting indicators: `w_epos` (threshold 0.3; baseline ≤ 0.11) and `w_fi` = |FIX|+|FIY| mean over 1 s (threshold 1500; baseline ≤ 870). Observation: `ePos` grows ~3× after the GNSS cut-off (0.012 → 0.035) in every run, that is, the EKF itself signals lower confidence, though far from the threshold. Still 0 false alarms on 11 runs.

**v0.3 (4 Oct 2026).** `cut_runs.py` v0.3 adds `imu_accX/Y/Z`, `imu_gyrX/Y/Z` (IMU instance 0, nearest sample), `xkf2_AX/AY/AZ` (accelerometer bias states, cm/s² as logged) and `xkf1_VN/VE/VD` (EKF velocity); `--names` accepts `name:cell` per run and `skip` for a window to leave out. All 56 CSVs (49 runs, 6 calibration, 1 test) were recomputed with unchanged file names; the first 43 columns are identical to v0.2.

**Detector v0.2 after 60 runs: 0 hits, 2 early warnings, 23 misses (S-25 added seven: grass plain, field ×3, 1.5 m ×3).** Every miss is a scale error of the flow-derived velocity (field, 1.5 m, downwind leg) with image quality 255 and all residuals nominal. In source set 2 such an error is unobservable by construction: flow is the only horizontal velocity measurement and the terrain state is frozen, so the velocity state follows k·v and the innovation stays at zero. The six indicators of v0.2 measure noise, consistency and image quality, none of them scale. Mechanism, literature and the two candidate observables tested on 4 Oct (IMU Δv against EKF Δv over acceleration phases, `scale_observable.py`, correlation 0.34–0.42 with the reference; accelerometer-bias sawtooth, amplitude 0.001 m/s², unusable) are in `docs/research/SCALE_ERROR_HYPOTHESES.md`. Proposed next step: a scale self-test manoeuvre at the start of each run (three accelerate-and-stop cycles after the switch) to give the IMU-based observable enough excitation.

## scale_observable.py (4 Oct 2026)

Per run and per acceleration phase (EKF horizontal speed changing by more than `--a-min` 0.3 m/s² for at least 0.8 s): the velocity change from the IMU (specific force rotated with the EKF attitude, gravity removed, trapezoidal integral) against the change of `xkf1_VN/VE`; `r_pair` = Σ|Δv_ekf| / Σ|Δv_imu| over all phases of the run (a constant accelerometer bias cancels between acceleration and deceleration). The reference path ratio (estimator / GNSS) is printed for validation only. Output `analysis/results/scale_observable.csv`. Status: at the current excitation (one acceleration and one deceleration per leg) the observable is at the noise level (gravity leakage from a 1° attitude error is 17 % of a 1.5 m/s velocity change); see the research note.

**Self-test runs, 11 Oct 2026 (S-25, E1-050…053 grass, E1-055…056 field; cell suffix `-SELFTEST`).** The outbound leg split into four 10 m segments with 3 s stops gives 10–13 phases per run. `r_pair` on the four grass runs: 0.944, 0.928, 1.003, 0.943 against reference 0.956, 0.960, 0.929, 0.957; field 0.974, 0.912 against 0.903, 0.885; rms error 0.05 over the 11 runs of the day, correlation 0.87 (0.52 over all 60 runs). The per-phase estimates are asymmetric in every run (acceleration 1.00–1.13, braking 0.83–0.91: Δv_IMU 1.2–1.3 m/s when accelerating, 1.6–1.7 m/s when braking, for the same change in the estimator), which is a gravity leak through an attitude error that follows the direction of acceleration; a joint fit of scale and a constant along-track bias does not reduce the error. The error is per run, not per phase, so more phases do not average it down. The observable separates the 1.5 m regime (0.73–0.81 read, 0.81–0.84 reference) from 3 m grass, and nothing finer. The campaign CSV `scale_observable.csv` covers 60 runs.

### CSV columns (v0.2)

Run CSV from `cut_runs.py`: `t_log_s`, `phase` (`before` / `flow_only` / `after`), `t_since_src2_s`, `ekf_lat`, `ekf_lon`, `ekf_alt`, `gps_lat`, `gps_lon`, `gps_nsats`, `gps_hdop`, `gps_spd`, `of_qual`, `of_flowX`, `of_flowY`, `of_bodyX`, `of_bodyY`, `rfnd_dist`, `ctun_alt`, `roll`, `pitch`, `yaw`, `xkf4_SV`, `xkf4_SP`, `xkf4_SH`, `xkf4_SM`, `xkf4_SS`, `rc7`, `mode`, `gpa_hacc`, `gpa_sacc`, `xkf3_IVN`, `xkf3_IVE`, `xkf4_TS`, `xkf5_FIX`, `xkf5_FIY`, `xkf5_AFI`, `xkf5_HAGL`, `xkf5_RI`, `xkf5_eVel`, `xkf5_ePos`, `vibe_x`, `vibe_y`, `vibe_z`. Column names after the first two follow the ArduPilot message and field names.

Detector results CSV (`detector_v0.2_*.csv`): `run`, `outcome` (`hit` / `false_alarm` / `miss` / `no_event`), `t_warning_s`, `t_error_s`, `lead_time_s`, `error_max_m`, `qual_min`, `sv_max`, `scatter_max`, `rfnd_jump_max`, `epos_max`, `fi_max`, `wind_tilt_deg`, `votes_max`.

CSV files produced before 20 Sep 2026 were renamed in place (column `faza` → `phase` with values `przed` → `before`, `bez_gnss` → `flow_only`, `po` → `after`; `t_od_src2_s` → `t_since_src2_s`; detector columns `przebieg` → `run`, `wynik` → `outcome` with translated values, `t_ostrzezenia_s` → `t_warning_s`, `t_bledu_s` → `t_error_s`, `wyprzedzenie_s` → `lead_time_s`, `blad_max_m` → `error_max_m`, `rozrzut_max` → `scatter_max`, `rfnd_skok_max` → `rfnd_jump_max`, `wiatr_przechyl_deg` → `wind_tilt_deg`, `glosy_max` → `votes_max`) without recomputation.


`wind_from_log.py`: in gusty conditions (S-22) use `--speed 1.0`, the default 0.7 m/s hover threshold finds no window.


## error_vs_time.py (21 Sep 2026)

Estimator error relative to GNSS as a function of time since the switch to source set 2, for all run CSVs; every 10 s of the flow-only phase, plus the error at the GNSS turn and at the end. Table and plot, one line per run (surface colour, dashed for 0.75 m/s). Used for S-22 finding 5: the error grows with distance flown on the outbound leg and partly reverses on the return, so it is a scale error on the flow velocity rather than a time-driven drift.

```
python3 analysis/error_vs_time.py data/ARIADNE_E1_*.csv --csv analysis/results/error_vs_time.csv --plot analysis/results/error_vs_time.png
```

## apriltag_detect.py (11 Oct 2026)

Detects tag36h11 markers in the stitched MP4 of one camera (`pupil-apriltags`, OpenCV), every N-th frame, and writes one row per detection: time in the video, tag ID, decision margin, side length and centre in pixels, camera position in the tag frame from the pose estimate (`--tag-size` in metres, pinhole intrinsics from `--hfov` or `--fx/--fy/--cx/--cy`). The pose of a single tag viewed face-on is ambiguous (two minima), so distances between tags are taken from the image: pixel distance between centres divided by the tag side in pixels, times the tag size. This ratio is independent of the intrinsics and of the height.

```
python3 analysis/apriltag_detect.py movies/kam0_20261011_192145.mp4 --tag-size 0.16 --step 3 --csv analysis/results/apriltag/kam0_20261011_192145.csv
```

**Indoor test, 11 Oct 2026 (home, no arming, no log; rangefinder read in MAVLink Inspector 1.50 ± 0.03 m).** Three A4 tags (ID 12, 13, 14; black square 16 cm, 20 cm boards, 20 cm apart, centres 0.40 m) on the floor, aircraft held by hand at 1.5 m; passes over the centre and 0.5 m to each side (sesja_052, 19:00) and hovers (sesja_054, 19:21). Results on the hover recording, every third frame: kam0 221 frames with a tag, 62 with all three, side 138 ± 3 px, height from the tag size 1.49 m at an assumed field of view of 54° (fx 1272 px); spacing from the image 0.403 m for neighbours (n = 269, 0.396–0.428) and 0.801 m across (n = 66), against 0.40 / 0.80 m laid out. kam1 (NoIR, larger lens): 207 frames, side 154 px, spacing 0.403 / 0.836 m; its focal length is about 1.24× that of kam0 (field of view about 44°) and the second spacing shows lens distortion at the edge of the frame. On the pass recording the spacing read 0.41 / 0.83 m (motion blur). Decision margin 55–63 (detector threshold about 20). Conclusion: a 16 cm tag at 1.5 m (136 px) is detected reliably; the row geometry is recovered from the image to 1 %; kam0 is the camera for the marker work. A 30 cm tag at 3 m gives 127 px, the same regime. Absolute camera position needs an intrinsic calibration (not done); relative scale does not.

## Files

| File | Title |
|---|---|
| [`apriltag_detect.py`](apriltag_detect.py) |  |
| [`apriltag_video.py`](apriltag_video.py) |  |
| [`balance.py`](balance.py) |  |
| [`cut_runs.py`](cut_runs.py) |  |
| [`degradation_detector.py`](degradation_detector.py) |  |
| [`drift_analysis.py`](drift_analysis.py) |  |
| [`drift_plan.py`](drift_plan.py) |  |
| [`error_vs_time.py`](error_vs_time.py) |  |
| [`flight_times.py`](flight_times.py) |  |
| [`flow_orientation.py`](flow_orientation.py) |  |
| [`scale_observable.py`](scale_observable.py) |  |
| [`session_extract.py`](session_extract.py) |  |
| [`session_weather.py`](session_weather.py) |  |
| [`stitch_recording.sh`](stitch_recording.sh) |  |
| [`wind_from_log.py`](wind_from_log.py) |  |
