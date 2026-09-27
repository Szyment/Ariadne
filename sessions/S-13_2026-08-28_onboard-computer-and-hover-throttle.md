# S-13: 28 Aug 2026, onboard computer integration and hover throttle

Parameters: `ariadne_v2_28aug2026_1143.params` · Flight log: `log_20_2026-8-28-11-57-20.bin`

## Conditions

| | |
|---|---|
| Wind | 3 m/s on average, gusts above 4 m/s |
| Illuminance | 14 000 lx |
| Air temperature | 25 °C |
| Surface | field, the same as in the previous sessions |

The wind ruled out the balance measurement (`S-06_Balance1.plan` compares motor loading on four headings, and the wind by itself differentiates the diagonals). Only a hover for throttle learning was performed.

## Finding 1: take-off mass after the computer installation

| | 21 Aug | 28 Aug |
|---|---|---|
| With pack | 1698 g | **1838 g** |
| Without pack | 1263 g | 1404 g |
| Pack | 435 g | 434 g |

Increase of 140 g, i.e. 8.2%, entirely in the equipment: Raspberry Pi 5 with cooling, two OV5647 cameras, voltage converter, fuse, harnesses. Flight time recalculated in `BOM.md` §6: an estimated 760 s and 6 runs per pack, to be replaced by a run-down measurement.

## Finding 2: hover throttle 0.282, harmonic notch filter unchanged

A hover in Loiter with `MOT_HOVER_LEARN` = 2 gave `MOT_THST_HOVER` = **0.282** against 0.2667 before the installation (log: 0.2667 → 0.2818, median throttle in flight 0.284). Prediction from linear scaling with mass: 0.289; difference 2.4%. Large margin to the abort threshold of 0.32 and the limit of 0.45.

Current in flight: median **15.65 A** against 13.45 A before the installation. Endurance per pack recalculated from the measurement: **~735 s**, still 6 runs. Vibration `VibeY` median 31, p95 46, the level of the old baseline, but measured in hover in gusts; `S-04_Test1.plan` will settle it.

`INS_HNTCH_REF` remains 0.267. The `FREQ`/`REF` pair is the calibration point of the motor vibration, not a function of mass; the filter in throttle-scaling mode will itself recompute the frequency to 210 × √(0.282/0.267) = 215.8 Hz. The original version of the procedure required the new value to be entered and has been corrected.

## Finding 3: compass calibration after the installation

Calibration in the field, with the onboard computer running and the cameras on, both compasses in the green fit range.

| Offsets | X | Y | Z | Length | Before installation |
|---|---|---|---|---|---|
| Compass 1, external on the mast | −29.9 | 14.6 | 18.1 | **37.9** | 45.7 |
| Compass 2, internal in the Pixhawk | −59.5 | 31.4 | 73.4 | **99.6** | 39.6 |

The external one came out better than before the installation; the mast is far from the new wiring. The internal one grew two and a half times: it sits closest to the voltage converter and the power harnesses.

**Dependence on current, from the hover log (`MAG` against `BAT.Curr`):**

| | Correlation | Slope | Field <5 A | Field >12 A |
|---|---|---|---|---|
| Compass 1, external | −0.30 | −0.23 mGs/A | 498 mGs | 496 mGs |
| Compass 2, internal | **0.94** | **6.6 mGs/A** | 489 mGs | **599 mGs** |

The field of the internal compass rises by 110 mGs (22%) between standstill and hover, a current-induced disturbance that the static calibration does not compensate. Decision: **`COMPASS_USE2` = 0**. The external one is clean, so CompassMot is not needed; disabling the internal one also removes the source of `Compasses inconsistent`.

## Finding 4: onboard computer operational

Full description in `hardware/RPi5_onboard_computer.md`. Summary of the state: MAVLink on GPS2 confirmed by frames, clock set from GNSS time, recording of both cameras controlled by arming with a separate directory for each cycle (verified with two cycles: 323 frames, correct timestamp in the name), kill switch from the transmitter on channel 9 with STATUSTEXT reports in QGC. Software in version 3, after a code audit that found and closed 12 defects, including a session directory without write permission for the cameras and a kill switch deaf after a Pixhawk restart, the cause of that day's field failure.

## Incident: ELRS receiver in Wi-Fi mode

The drone was powered with the transmitter off for more than 60 s: the receiver went into Wi-Fi mode and stopped listening to the radio, which required a power cycle. Operational rule: **transmitter first, then the drone**; a receiver that sees the transmitter from the first second never counts down to Wi-Fi.

The payload plate with the optical-flow sensor, rangefinder and cameras was moved 1 cm forward; new values `FLOW_POS_X` = 0.098 and `RNGFND1_POS_X` = 0.122 (`SENSOR_GEOMETRY.md`, update of 28 Aug).

## Open

- [ ] Enter `FLOW_POS_X` = 0.098, `RNGFND1_POS_X` = 0.122, `COMPASS_USE2` = 0 into the aircraft and dump the parameters
- [x] Dependence of `MAG` on `BAT.Curr` checked, finding 3; internal compass to be disabled
- [x] Kill switch tested; onboard software frozen after the final audit (S-14)
- [x] Balance flight: accepted, `YawOut` +0.017 (card S-14)
- [x] Check flight `S-04_Test1.plan`: tracking below thresholds, autotune unnecessary (card S-14)

Photos and screenshots: `build-log/photos/2026-08-28/` (Mac screenshots `2026-08-28_mac-screenshot_*`: compass calibration 11:37–11:41, QGC without the parameter list 16:05, onboard log list 18:37, IR camera 20:01).
