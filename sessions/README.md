# sessions

One card per flight session: conditions, configuration, flights, readings, findings and incidents. S-01…S-16 are platform bring-up and tuning (August); S-17 onwards is the E1 campaign. Every number in a card is reproducible from the logs with the scripts in `analysis/`.

## Two different documents that must not be confused

**A session card** (karty `S-*.md`) describes an outing: conditions, equipment, course of events, flights performed and anomalies observed. It is part of the build log and evidence of how the project was conducted.

**A run card** (`TEMPLATE_run_card.md`, annex B of the E1–E3 protocol) describes one measurement in the matrix: run number, cell, lux, wind, PDOP, log file and the decision to accept or reject. It is part of the dataset.

The sessions of 15–20 August 2026 were platform tuning, not a measurement campaign. They have session cards and deliberately have no run cards:

> Entering tuning flights into run cards would contaminate the dataset. A measurement run has a frozen configuration (protocol §2.3), and these flights served precisely to change the configuration: between them the motor mounts, `INS_GYRO_FILTER`, the harmonic notch filter and `MOT_HOVER_LEARN` changed. The protocol warns against such an inconsistency in its closing remarks.

The E1–E3 campaign begins only after the configuration freeze (protocol §5.1). Only then will the `przebieg-cards/` directory begin to fill.

## Where the data in the cards comes from

Three levels of reliability are marked in the cards:

- **From the log**: data extracted programmatically from the `.bin` files by `pymavlink` (arming times, voltages, satellites, HDOP, modes, messages, vibration, angle tracking errors). They are repeatable and verifiable.
- **From documentation**: data copied from `build-log/0*_*.md`.
- **`[TO BE COMPLETED]`**: data that is not in the log and that nobody wrote down: location, wind from the anemometer, lux, temperature, presence of an observer, DroneTower. The consolidated list is in `MISSING_DATA.md`.

## Note on time

Times in the cards are given in log seconds (`TimeUS`, counted from controller start-up), because this is a verifiable value. Clock times calculated from the file name are approximate. The tuning document uses yet another reference (Filter Review, absolute time, the log starts at 90.2 s), so the same events have different timestamps in different documents. When comparing, always state which reference is being used.

## Note on vibration

`VIBE` is logged separately for the three IMU instances. The cards give the IMU0 values, following the convention of the tuning document. IMU2 consistently shows about 2× lower values; the difference results from the use of a different sensor, not from different behaviour of the drone, and the values of the two instances must not be mixed.

## Files

| File | Title |
|---|---|
| [`S-01_2026-08-15_commissioning.md`](S-01_2026-08-15_commissioning.md) | S-01: Session card, 15 Aug 2026 |
| [`S-02_2026-08-18_first-flights.md`](S-02_2026-08-18_first-flights.md) | S-02: Session card, 18 Aug 2026 |
| [`S-03_2026-08-19_after-correction.md`](S-03_2026-08-19_after-correction.md) | S-03: Session card, 19 Aug 2026 |
| [`S-04_2026-08-20_auto-missions.md`](S-04_2026-08-20_auto-missions.md) | S-04: Session card, 20 Aug 2026 |
| [`S-05_2026-08-21_filter-verification.md`](S-05_2026-08-21_filter-verification.md) | S-05: Session card, 21 Aug 2026 |
| [`S-06_2026-08-22_balance-check.md`](S-06_2026-08-22_balance-check.md) | S-06: Session card, 22 Aug 2026 |
| [`S-07_2026-08-23_first-gnss-denied-run.md`](S-07_2026-08-23_first-gnss-denied-run.md) | S-07: Session card, 23 Aug 2026 |
| [`S-08_2026-08-23_autotune.md`](S-08_2026-08-23_autotune.md) | S-08: Session card, 23 Aug 2026, evening |
| [`S-09_2026-08-25_first-estimator-failure.md`](S-09_2026-08-25_first-estimator-failure.md) | S-09: Session card, 25 Aug 2026 |
| [`S-10_2026-08-25_crash-in-auto-run.md`](S-10_2026-08-25_crash-in-auto-run.md) | S-10: 25 Aug 2026, crash in an automatic run |
| [`S-11_2026-08-26_flow-limit-and-flip-over.md`](S-11_2026-08-26_flow-limit-and-flip-over.md) | S-11: 26 Aug 2026, optical-flow limit and tip-over after landing |
| [`S-12_2026-08-26_first-full-gnss-denied-runs.md`](S-12_2026-08-26_first-full-gnss-denied-runs.md) | S-12: 26 Aug 2026, two full GNSS-denied runs |
| [`S-13_2026-08-28_onboard-computer-and-hover-throttle.md`](S-13_2026-08-28_onboard-computer-and-hover-throttle.md) | S-13: 28 Aug 2026, onboard computer integration and hover throttle |
| [`S-14_2026-08-28_balance-and-post-install-check.md`](S-14_2026-08-28_balance-and-post-install-check.md) | S-14: 28 Aug 2026, evening, balance and tuning check after the computer installation |
| [`S-15_2026-08-29_drift3-terrain-frame.md`](S-15_2026-08-29_drift3-terrain-frame.md) | S-15: 29 Aug 2026, first Dryf3 run in the terrain frame |
| [`S-16_2026-08-29_flow-calibration-and-three-runs.md`](S-16_2026-08-29_flow-calibration-and-three-runs.md) | S-16: 29 Aug 2026, afternoon, flow calibration and three Dryf3 runs at 3.0 m |
| [`S-17_2026-09-12_kepa-first-E1-run.md`](S-17_2026-09-12_kepa-first-E1-run.md) | S-17: 12 Sep 2026 (day), Vistula meadow (Kępa), first E1 measurement runs |
| [`S-18_2026-09-12_kepa-dusk-lux-series.md`](S-18_2026-09-12_kepa-dusk-lux-series.md) | S-18: 12 Sep 2026 evening, the same meadow, illuminance descent series (dusk) |
| [`S-19_2026-09-13_kepa-field-SURF2.md`](S-19_2026-09-13_kepa-field-SURF2.md) | S-19: 13 Sep 2026, the same meadow, SURF2 cell (ploughed field), two directions relative to the wind |
| [`S-20_2026-09-13_kepa-dusk-lux-threshold-and-collision.md`](S-20_2026-09-13_kepa-dusk-lux-threshold-and-collision.md) | S-20: 13 Sep 2026 evening, the same meadow, LUX series down to the sensor threshold; collision with a tree in flight 4 |
| [`S-21_2026-09-17_kepa-dusk-new-props-alt15-and-failsafe.md`](S-21_2026-09-17_kepa-dusk-new-props-alt15-and-failsafe.md) | S-21: 17 Sep 2026 evening, the same meadow: grass at 3 m and 1.5 m, field at 3 m at dusk; second EKF failsafe with a climb to 37 m |
| [`S-22_2026-09-20_kepa-overcast-vel075-and-field.md`](S-22_2026-09-20_kepa-overcast-vel075-and-field.md) | S-22: 20 Sep 2026 afternoon, Kępa Okrzewska: first overcast (LUX2) session, first speed level 0.75 m/s, field at 3 m; battery failsafe on a VEL075 run |
| [`TEMPLATE_run_card.md`](TEMPLATE_run_card.md) | Run card: template |
