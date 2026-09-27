# S-12: 26 Aug 2026, two full GNSS-denied runs

Log: `log_19_2026-8-26-16-45-12.bin` · Ground telemetry: `2026-08-26 16-46-37.tlog` · Parameters: `ariadne_v2_26aug2026_1756.params`

## Conditions

| | |
|---|---|
| Wind | 3.0 m/s, gusts up to 4.0 m/s, from 80° (anemometer) |
| Air temperature | 24 °C |
| Illuminance, sensor horizontal facing up | 6500 lx |
| Illuminance, sensor perpendicular to the sun | 27 700 lx |
| Surface | field, low grass, mixed dry and green, sandy bald patches and clods of earth; the same as in the previous sessions |
| Mission | `S-12_Drift2.plan`, leg 40 m, azimuth 80°, altitude 3.5 m |

The wind is within the 4.0 m/s threshold of `ANNEX_C` §7.1.

The direction was checked independently by the method of `ANNEX_C` §8.1, from the aircraft tilt in hover: 5337 `ATT` samples at a ground speed below 0.4 m/s give a mean tilt of 2.9° directed towards **109°**, i.e. a horizontal acceleration of 0.50 m/s² balancing the wind load. The anemometer indicated 80°. The 29° difference fits within one 45° sector, so both measurements agree at the resolution adopted in the protocol. The leg azimuth of 80° stands.

Parameters: `WP_SPD` = 1.5 · `EK3_RNG_USE_HGT` = 70 · `EK3_RNG_USE_SPD` = 3.0 · `LOIT_SPEED_MS` = 2.0 · `FS_EKF_ACTION` = 2.

## Course of the session

| | Run 1 | Run 2 |
|---|---|---|
| Arming | 16:25:16 | 16:40:56 |
| Switch to `EK3_SRC2` | 16:28:25 | 16:42:38 |
| Return to `EK3_SRC1` | — | — |
| GNSS-denied time | **151.9 s** | **112.6 s** |
| AUTO phase | 67.6 s | 68.2 s |
| Disarming | 16:31:22 | 16:44:58 |

**Both runs completed without an EKF failsafe, without pilot intervention and without incidents in the log.** The first such runs in the project.

## Finding 1: velocity as commanded

| | Median | 90th percentile | Maximum |
|---|---|---|---|
| Run 1 | 1.54 m/s | 1.99 m/s | 2.16 m/s |
| Run 2 | 1.59 m/s | 2.16 m/s | 2.42 m/s |

1.5 m/s was commanded through `WP_SPD`. In AUTO mode the parameter applies, unlike in LOITER (card S-11, finding 2).

## Finding 2: the first measured drift

Divergence between the position from the estimate and the recorded GNSS, counted from the moment of the source switch:

| Time since cut-off | Run 1 | Run 2 |
|---|---|---|
| 10% | 0.23 m | 0.33 m |
| 25% | 4.10 m | 0.30 m |
| 50% | 0.85 m | 1.74 m |
| 75% | 1.17 m | 4.20 m |
| end | 1.77 m | 4.14 m |
| **maximum** | **4.40 m** | **4.51 m** |

Distance travelled per GNSS: 98.4 m and 95.7 m.

These are **the first real drift figures** in the project. The earlier values of 0.45 m (S-07) and 0.58 m (S-09) were upper bounds from runs in which the aircraft barely moved.

## Finding 3: the distance underestimate fell from 19–21% to 7–9%

| | Distance per estimate | Distance per GNSS | Ratio |
|---|---|---|---|
| Run 1 | 91.5 m | 98.4 m | **0.930** |
| Run 2 | 86.8 m | 95.7 m | **0.908** |

Card S-09 reported a ratio of 0.79–0.81 with the altitude taken from the barometer. After moving the altitude to the rangefinder (`EK3_RNG_USE_HGT` = 70) the underestimate fell from 19–21% to 7–9%.

This supports the hypothesis of `MISSING_DATA` §E5n about an **underestimated height-above-terrain estimate**, rather than a lag in the velocity estimate. Flow rate is converted into linear velocity through height, so an underestimated height gives an underestimated velocity and an underestimated distance.

This also settles the second hypothesis: at **constant velocity** a lag in the estimate does not shorten the distance, it only shifts it in time. The remaining 7–9% is therefore a scale error, not a lag.

## Finding 4: altitude reference drift

The aircraft flew lower than the estimate indicated, and the difference grew with time. This is settled by comparing three readings at moments when the aircraft **stands on the ground** at the same spot:

| | EKF altitude | Barometer | Rangefinder | Terrain `XKF5.TOfs` |
|---|---|---|---|---|
| Run 1, arming | 0.00 m | −0.18 m | 0.15 m | +0.49 m |
| Run 1, disarming | **1.72 m** | 0.00 m | 0.15 m | −1.27 m |
| Run 2, arming | 0.73 m | −0.19 m | 0.14 m | −0.27 m |
| Run 2, disarming | **2.00 m** | 0.31 m | 0.14 m | −1.55 m |

The altitude estimate departed from the truth by 1.72 m in run 1 and by 1.27 m in run 2. The barometer stayed within ±0.31 m of zero throughout, so **this is not barometer drift**.

The terrain state shifted by the same amount in the opposite direction: −1.76 m and −1.28 m. The difference altitude minus terrain, i.e. `XKF5.HAGL`, on the ground was 0.22–0.25 m against a rangefinder reading of 0.14–0.15 m; it remained correct. What drifts is the **common component**, not the difference.

Mechanism: with `EK3_RNG_USE_HGT` = 70 the altitude source below the threshold is the rangefinder, and the barometer is no longer fused. Altitude above the take-off point then ceases to be observed; only the distance from the ground is observed. The pair (altitude, terrain) drifts together. Control in AUTO mode holds the target altitude in the estimate's frame, so the drift of the reference lowers the actual flight:

| | Time airborne | Drift | Rate |
|---|---|---|---|
| Run 1 | 365 s | 1.72 m | 0.28 m/min |
| Run 2 | 242 s | 1.27 m | 0.32 m/min |

This is visible directly in the record: `CTUN.DAlt` held 3.49 m to within a centimetre, while the rangefinder fell from about 4.0 m at the start of the leg to 2.4–3.0 m towards the end, with a minimum of 0.72 m.

**Correction of an earlier entry in this card.** The 4.2 m threshold concerns height above terrain, not altitude above the take-off point, and the return to the rangefinder requires descending below 0.7 × 4.2 = 2.94 m (`selectHeightForFusion` in `AP_NavEKF3_PosVelFusion.cpp`: `belowLowerSwHgt = (terrainState - stateStruct.position.z) < 0.7f * rangeMaxUse`). The sentence stating that in run 2 the altitude source was the barometer, because the median of the estimate was 4.22 m, was wrong. Both runs flew on the rangefinder, and the divergence from the barometer is precisely the proof.

**The slope of the field does not explain the drift.** Terrain computed as `GPS.Alt − RFND.Dist` in 5 m bins along the leg gives 225.6 m at the 5th metre and 224.2 m at the 40th metre, i.e. a spread of 1.3 m with GNSS altitude noise of the same order; an inconclusive measurement. Independently of it, the error grows with **time**, not with position along the leg, and persists after landing at the take-off point.

## Finding 5: optical flow beyond reproach

`OF.Qual` = 255 in both runs, median and minimum. Zero samples below 100.

The angular rate of the image at 1.5 m/s and 2.8 m altitude is 0.54 rad/s, i.e. four times below the 2.1 rad/s threshold measured in card S-11.

## Changes before the next session

| | |
|---|---|
| Waypoints | terrain frame (`frame` = 10, `MAV_FRAME_GLOBAL_TERRAIN_ALT`) instead of relative (`frame` = 3) |
| Run altitude | unchanged, 3.5 m above ground |

In the terrain frame the target altitude is the distance from the ground, and `WP_RFND_USE` = 1 (already set) makes it be measured by the rangefinder. The target is then recomputed continuously, so the reference drift of finding 4 does not lower the flight.

Lowering the run to 3.0 m, recorded here earlier, does not address the cause: the drift would simply start from 3.0 m.

## Open

- [x] Why the altitude estimate does not follow the rangefinder below the switching threshold: it does follow; the reference drifts, finding 4
- [x] Whether the field slopes along the leg: measurement inconclusive and irrelevant to the drift, finding 4
- [ ] Repeat both runs in the terrain frame and check whether the rangefinder holds 3.5 m along the whole leg
- [ ] Whether the path ratio rises above 0.93 at a constant actual altitude
- [ ] Where the rate of 0.28–0.32 m/min comes from: check `XKF2.AZ` (accelerometer bias in the vertical axis) and the process noise of the terrain state
