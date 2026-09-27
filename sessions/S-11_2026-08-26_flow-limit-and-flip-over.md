# S-11: 26 Aug 2026, optical-flow limit and tip-over after landing

Log: `log_18_2026-8-26-11-30-22.bin`.

## Conditions

| | |
|---|---|
| Wind | **5.0 m/s, gusts 5.5 m/s**, from 69° |
| Air temperature | 22.7 °C |
| Ground temperature | 32.3 °C |
| Illuminance | 15 370 lx |
| Surface | grass |
| Mode | LOITER throughout the flight |

**The wind exceeded the threshold of `ANNEX_C` §7.1, which is 4.0 m/s.** The session does not meet the protocol conditions.

## Course of the session

Arming 182.8 s, climb to about 3.5 m. At 268.5 s the pilot switched `RC7` to `EK3_SRC2`: message `Using EKF Source Set 2`, after 10 ms `fusing optical flow`.

From 358 s the pilot deflected the pitch stick, velocity rose over 11 s to **7.45 m/s**. At 369.59 s `OF.Qual` dropped to zero. At 371.62 s the EKF failsafe triggered and the mode changed to LAND. Ground contact at 386.5 s at a velocity of 4.5 m/s, the aircraft tipped over onto its side. Crash detected at 389.37 s: `Crash: Disarming: AngErr=64>30`.

## Finding 1: the altitude fix works

Parameters in the log: `WP_SPD` = 1.5, `EK3_RNG_USE_HGT` = 70, `EK3_RNG_USE_SPD` = 3.0, `RC_OPTIONS` = 8480.

The difference between the altitude in the estimate and the rangefinder reading throughout the flight below the 4.2 m threshold lies within **−0.9 to +0.3 m** and **does not grow with velocity**. The phenomenon from card S-10, in which the aircraft descended as it accelerated, is absent.

Above 4.2 m the difference grows to +1.7 m, as expected: above the threshold the altitude source is the barometer again.

## Finding 2: `WP_SPD` does not apply in LOITER mode

`WP_SPD` = 1.5 applies exclusively to navigation in AUTO mode. In LOITER the velocity is commanded by the stick, and its ceiling is set by **`LOIT_SPEED_MS` = 12.5 m/s**.

The pitch stick record (`RCIN.C2`) rises from 1500 to 1778 in the window 358–369 s. Velocity reached 7.45 m/s against the intended 1.5 m/s.

## Finding 3: optical flow loses the image at 2.1 rad/s

The quantity that decides the loss of flow is the angular rate of the image, i.e. velocity relative to the ground divided by altitude.

| Time | Velocity | Altitude | v/h | `OF.Qual` |
|---|---|---|---|---|
| 366.0 s | 4.96 m/s | 3.76 m | 1.32 rad/s | 255 |
| 368.0 s | 6.37 m/s | 3.76 m | 1.69 rad/s | 255 |
| 369.0 s | 7.15 m/s | 3.58 m | 1.99 rad/s | 255 |
| **369.6 s** | ~7.4 m/s | ~3.5 m | **≈2.1 rad/s** | **0** |
| 370.0 s | 7.45 m/s | 3.45 m | 2.16 rad/s | 0 |

Flow quality held at 255 up to 1.99 rad/s and dropped to zero between 2.0 and 2.1 rad/s. **This is the first measured point of the failure envelope for RQ3**, not merely "too fast" but a threshold value expressed in a quantity that has physical meaning at every altitude.

At the run altitude of 3.5 m this corresponds to a velocity of about 7.4 m/s. At 1.5 m it would correspond to 3.2 m/s.

## Finding 4: `OF.Qual` warned 2.03 s before the failsafe

| | |
|---|---|
| `OF.Qual` dropped to zero | 369.59 s |
| EKF failsafe | 371.62 s |
| **Lead time** | **2.03 s** |

The variances in `XKF4` remained low throughout this time: `SV` ≤ 0.02, `SP` = 0.00, `SH` ≤ 0.13, `SM` ≤ 0.14, against the threshold `FS_EKF_THRESH` = 0.8. The failsafe did not come from the variances but from the loss of aiding: `XKF4.TS` = 49, i.e. bit 0 (position timeout) was set throughout the GNSS-denied run.

**This is a result for RQ1-b.** The sensor telemetry announced the estimator failure with a lead time of 2.03 s, while the EKF variance ratios did not move. Exactly this thesis is the subject of the work.

## Finding 5: the tip-over resulted from the failsafe response

`FS_EKF_ACTION` = 1 means a change to LAND mode. The aircraft began to descend with 4.3 m/s of velocity relative to the ground and touched the ground while still moving. At 386.5 s the roll reached 147°.

Descent rate and altitude were under control; what brought it down was the horizontal motion, which in LAND mode nothing was braking, because position was not available.

## Parameter changes before the next flight

| Parameter | Was | To be | Purpose |
|---|---|---|---|
| `LOIT_SPEED_MS` | 12.5 | **2.0** | the stick cannot accelerate the aircraft beyond the flow range |
| `FS_EKF_ACTION` | 1 (Land) | **2 (AltHold)** | the pilot retains control instead of landing while moving |

`FS_EKF_ACTION` = 2 is, in the ArduPilot description, "Switch to AltHold mode if current mode requires position". In AltHold position is not needed, so the aircraft stays in the air and the pilot brings it down manually.

## Open

- [x] Condition of the aircraft after the tip-over: propellers and motor mounts intact, mounts tightened. Ground contact was on sand.
- [x] PMW3901 and TFmini-S lenses checked after the landing on sand: `OPTICAL_FLOW.quality` = 255, the rangefinder reports the correct distance. Sensors undamaged.
- [ ] Repeat the envelope point at a different altitude, to check whether the 2.1 rad/s threshold is constant
- [ ] A session in a wind below 4.0 m/s, compliant with the protocol
- [ ] A run according to `S-12_Drift2_README.md`, in AUTO, where `WP_SPD` = 1.5 actually applies
