# S-10: 25 Aug 2026, crash in an automatic run

Logs: `log_14_2026-8-25-12-20-40.bin`, `log_15_2026-8-25-19-01-14.bin`, `log_16_2026-8-25-19-05-34.bin`.

## Conditions

| | |
|---|---|
| Wind | 1.7 m/s, from **113°** (the reading recorded in the field as 293° was reversed by 180°, confirmed by the drift from the log) |
| Illuminance | 326 lx |
| Surface | grass |
| Mission | `S-10_Drift1.plan`, altitude 3 m |
| Target altitude | 2.65 m above the take-off point |

## Course of the session

Log 15, first flight. Take-off in AUTO at 162.4 s. At 169.6 s the pilot interrupted the mission by switching to AltHold, at 175.0 s returned to AUTO. Mission resumed from item 3 (hold above the take-off point).

At 201.6 s item 3 reached, `DO_AUX_FUNCTION` executed: message `Using EKF Source Set 2`, `EV 86`, after 60 ms `EKF3 IMU0/IMU1 fusing optical flow`. **Command 218 works.**

The aircraft set off towards the turn point. Ground impact at 209.9 s. Crash detected at 212.4 s: `Crash: Disarming: AngErr=149>30, Accel=0.1<3.0`.

Second flight of the same day: arming 349.5 s, disarming 843.1 s, 493.6 s airborne, no incidents.

## Finding 1: the aircraft flew at 5.0 m/s instead of 1.5 m/s

Velocity commanded by the position controller at the moment of acceleration: `DVN` = −2.80 m/s, `DVE` = +4.15 m/s, i.e. **exactly 5.00 m/s**. GNSS velocity reached 6.4 m/s. Parameter `WP_SPD` = 5.0.

Mission item 2 (`DO_CHANGE_SPEED`, 1.5 m/s) was executed at 163.3 s, before the mission was interrupted.

Cause in the code, `ArduCopter/mode_auto.cpp`, `ModeAuto::init()`:

```cpp
wp_nav->wp_and_spline_init_m();
// initialise desired speed overrides
desired_speed_override_ms = {0, 0, 0};
```

**Every re-entry into AUTO mode clears the speed set by `DO_CHANGE_SPEED`.** A mission resumed from item 3 does not execute item 2 again, so `WP_SPD` applies.

## Finding 2: the barometer overestimates altitude by 1.40 m at 5.6 m/s

| Phase | Velocity | BARO | Rangefinder | BARO − rangefinder | EKF altitude − rangefinder |
|---|---|---|---|---|---|
| Hover above the take-off point, 193–201 s | 0.08 m/s | 2.73 m | 2.38 m | 0.35 m | 0.28 m |
| Transit, 205.0–207.5 s | 5.58 m/s | 3.92 m | 2.17 m | **1.75 m** | **0.76 m** |

The growth of the barometer error is **1.40 m**, and the growth of the altitude error in the estimate **0.48 m**.

Card S-07 predicted 1.6 m at 5.6 m/s from the dynamic pressure `q = ½·1.19·5.6² = 18.7 Pa` divided by 11.7 Pa/m. The measurement from this flight confirms the calculation.

`EK3_SRC1_POSZ` = 1 and `EK3_SRC2_POSZ` = 1, i.e. the barometer. `EK3_RNG_USE_HGT` = −1, i.e. the rangefinder never enters the altitude estimate.

## Finding 3: the descent was a controller command, not a loss of thrust

The altitude error of 0.48 m multiplied by `PSC_D_POS_P` = 1.0 gives a commanded vertical velocity of −0.48 m/s. The recorded `DCRt` in the window 206–209 s is from −0.3 to −0.5 m/s.

The aircraft descended from 2.5 m to zero in 5 s, executing a descent command, in the belief that it was 0.5 m too high.

GNSS altitude fell by 2.7 m in the same window, and the difference `GPS.Alt − rangefinder` changed by 0.45 m, so the terrain relief accounts for at most 0.45 m of this descent.

Thrust was available: `ThO` at the moment of the descent was 0.19–0.22 against 0.25 in hover.

## Finding 4: the drift in AltHold is consistent with the wind

Six windows in log 15 and six in log 16, all with the sticks in the neutral position and a tilt angle below 0.5°:

| Log | Drift direction | Acceleration |
|---|---|---|
| 15 | 282–303° | 0.14–0.37 m/s² |
| 16 | 280–290° | 0.14–0.23 m/s² |
| 14 (noon) | 281–335° | 0.18–0.72 m/s² |

The aircraft heading in all windows of 25 Aug lay within 121–134°, so within a single day it is not possible to separate an airframe-bound force from an earth-bound force.

The comparison with earlier sessions at the same aircraft heading settles it:

| Session | Aircraft heading | Drift direction | Acceleration in the first 3 s |
|---|---|---|---|
| 18 Aug (log 5) | 117–128° | 56°, 235°, 253° | 0.00–0.15 m/s² |
| 19 Aug (log 6) | 106–163° | 27°, 87°, 204°, 260° | 0.00–0.33 m/s² |
| 25 Aug (logs 14, 15, 16) | 121–133° | **278–317°** | **0.18–0.91 m/s²** |

At an almost identical aircraft heading the drift direction changes between days by more than 150°. An airframe-bound force would give the same direction relative to the nose in every session. **The drift is earth-bound, i.e. it comes from the wind.**

The earlier sessions had no fixed drift direction and weaker accelerations, which is why the phenomenon did not draw attention earlier.

The wind speed calculated backwards from the drift acceleration, with `½·ρ·C_d·A` = 0.0714 and a mass of 1.7 kg, is **2.7 m/s at 0.3 m/s² and 4.6 m/s at 0.9 m/s²**. The anemometer held at hand height showed 1.7 m/s. The wind at run altitude is stronger than at the ground, and that is the value acting on the aircraft.

AltHold mode holds altitude and angles, it does not hold position. The behaviour is correct.

**The wind direction reading was reversed by 180°.** The recorded 293° would push the aircraft towards 113°, and the measured drift has a direction of 282–303°, which corresponds to a wind **from 110–125°**. The pilot confirmed the error in the measurement.

The noon measurement of the same day, 124°, is consistent with the drift from log 14 and with the aircraft tilt. The azimuth of the turn point in `S-10_Drift1.plan` was calculated from the noon value and **remains correct**. A check procedure has been added to `ANNEX_C` §8.1.

## Finding 5: plan geometry

| | |
|---|---|
| Take-off point in the log | 50.9139925 N / 19.0863896 E |
| "Take-off" point in `S-10_Drift1.plan` | 6.2 m away, azimuth 50° |
| Turn point | 42.2 m from the take-off point, azimuth 116° |
| Impact point | 30.7 m from the take-off point, azimuth 113°, 11.6 m short of the turn point |

The coordinates in the mission file are absolute, so after take-off the aircraft flies to the point recorded in the plan, not to the arming location. In this session that was 6.2 m. **Before every session the coordinates in the plan must be moved to the actual take-off point.**

The run leg runs on azimuth 116°, i.e. exactly upwind relative to the wind established from the drift (110–125°). The assumption from `S-10_Drift1_README.md` is met.

## Parameter changes before the next flight

| Parameter | Was | To be | Purpose |
|---|---|---|---|
| `WP_SPD` | 5.0 | **1.5** | run velocity independent of `DO_CHANGE_SPEED` |
| `EK3_RNG_USE_HGT` | −1 | **70** | altitude from the rangefinder below 4.2 m instead of from the barometer |
| `EK3_RNG_USE_SPD` | 2.0 | **3.0** | margin above the commanded 1.5 m/s, so that a gust does not switch the source in flight |

Run altitude **3.5 m**, i.e. 0.7 m below the source switching threshold.

`S-10_Drift1.plan` is withdrawn. It is replaced by `S-12_Drift2.plan` with manual switching, described in `missions/S-12_Drift2_README.md`.

## Finding 6: the fix verified in flight

Log `log_17_2026-8-25-20-28-10.bin`, check flight at 20:28, LOITER, `EK3_SRC1`. Wind 1.6 m/s from 133°. Parameters in the log: `WP_SPD` = 1.5, `EK3_RNG_USE_HGT` = 70, `EK3_RNG_USE_SPD` = 3.0.

The flight took place at a median of **4.38 m**, i.e. above the switching threshold of 4.2 m for 76% of the time. This gave a comparison of both states in a single flight.

**Below the threshold, altitude from the rangefinder:**

| Velocity | n | EKF altitude − rangefinder | barometer − rangefinder |
|---|---|---|---|
| 0.0–0.4 m/s | 1197 | +0.51 m | +0.55 m |
| 0.4–1.0 m/s | 204 | +0.42 m | +0.71 m |
| 1.0–2.0 m/s | 17 | **+0.27 m** | +0.95 m |

**Above the threshold, altitude from the barometer:**

| Velocity | n | EKF altitude − rangefinder | barometer − rangefinder |
|---|---|---|---|
| 0.0–0.4 m/s | 1922 | +0.26 m | +0.38 m |
| 0.4–1.0 m/s | 508 | +0.88 m | +0.93 m |
| 1.0–2.0 m/s | 395 | **+1.03 m** | +1.30 m |

The barometer overestimates in both states, and the faster the aircraft flies, the more it overestimates. The difference is that **below the threshold the estimate stops following it**: the altitude error does not grow with velocity but decreases. Above the threshold it grows to +1.03 m at 1–2 m/s.

The fix works. The condition is flight below 4.2 m.

The barometer error reaching a metre at 1–2 m/s relative to the ground confirms that the driving quantity is the velocity relative to the air: in a 1.6 m/s wind, upwind flight at 1.5 m/s gives more than 3 m/s of airflow.

## Open

- [ ] Condition of the aircraft after the impact, `[TO BE COMPLETED]`
- [ ] Repeat the check flight at **3.5 m**, with two legs of 15 s at 1.5 m/s; below the threshold there are so far only 17 samples in the 1–2 m/s bin
- [ ] Upload `S-12_Drift2.plan` to the aircraft; in log 17 the mission `Dryf1` was still loaded
- [ ] Research run according to `S-12_Drift2_README.md`
