# S-09: Session card, 25 Aug 2026

**Type:** check flight after tuning + GNSS-denied run attempts · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Log:** `log_14_2026-8-25-12-20-40.bin`
**Configuration:** `ariadne_v2_23aug2026_2036.params` (first flight on the gains from autotune)
**In the E1–E3 dataset:** no

---

## Conditions

| | Before the flight | After the flight |
|---|---|---|
| Wind | **4.6 m/s**, direction 124° (SE) | 2.9 m/s |
| Air temperature (transmitter) | 19.6 °C | 19.8 °C |
| Ground temperature (AX-7510) | 26.3 °C | 25.3 °C |
| Grass temperature (AX-7510) | 21.7 °C | 20.8 °C |
| Illuminance (GM1010) | 3095 lx | 3441 lx |
| Cloud cover | complete | complete |

Flight 12:14:05 – 12:20:26. GM1010 range multiplier not recorded, [TO BE COMPLETED].

**The wind of 4.6 m/s exceeded the criterion of 4.0 m/s AVG at 2.0 m** established on 23 Aug (`ANNEX_C` §7.1). The session would not have qualified as a measurement session.

Illuminance rose from 3095 to 3441 lx under complete overcast, a stable cell, unlike the dusk of S-08, where the rate was −7.27 %/min.

The ground was 6.7 K warmer than the air, the grass 4.6 K cooler than the ground. In S-08 in the evening the grass–ground difference was 1.6–2.3 K.

---

## Course of the session

Two armings. The first 12:13:04 – 12:13:53, brief. The second 12:14:05 – 12:20:26.

Three attempts to switch to source set 2, all in AltHold mode. Then the mission `S-04_Test1.plan` in AUTO mode, 12:16:43 – 12:20:23.

| Window | Log time | Duration | Ended by |
|---|---|---|---|
| 1 | 310.0 → 330.8 s | 20.8 s | EKF failsafe, then pilot's return |
| 2 | 380.4 → 386.9 s | 6.5 s | aborted by the pilot |
| 3 | 417.9 → 421.5 s | 3.6 s | aborted by the pilot |

---

## Finding 1: the 6 m ceiling confirmed in flight

Window 1 took place at an altitude of **9.9 – 11.0 m**. The rangefinder returned a distance of 9.6 – 11.8 m, but ArduPilot marked these samples with the status **`OutOfRangeHigh`**, because `RNGFND1_MAX` = 6 m. The reading existed but was not used.

Without altitude, optical flow cannot be converted into velocity. The estimator was left without horizontal aiding.

```
310.0 s   Using EKF Source Set 2
320.0 s   XKF4.TS 48 → 49, bit 0 = position timeout
320.9 s   EKF variance → EKF Failsafe
          ERR subsystem 16 code 2 (EKFCHECK), subsystem 17 code 1 (FAILSAFE_EKFNAV)
330.8 s   return to set 1
331.9 s   EKF Failsafe Cleared
```

**Exactly 10.0 s from the switch to the position timeout.** `README` §4.4 describes the 6 m ceiling as a limitation resulting from the configuration; this is the first measurement confirming it in flight, together with the mechanism and the timing.

**The wind was not the cause of the abort.** The 4.6 m/s wind was pushing the aircraft, but the failsafe triggered because of the flight altitude.

---

## Finding 2: the failure did not come from the variances

The `XKF4` ratios at the moment the failsafe triggered, both cores:

| SV | SP | SH | SM | Threshold `FS_EKF_THRESH` |
|---|---|---|---|---|
| 0.08 | 0.03 | 0.21 | 0.00 | 0.80 |

None came close to the threshold. Maximum in the whole window: SH 0.21, SM 0.56.

The failsafe triggered from the **timeout flag** (`XKF4.TS` bit 0), not from a variance exceedance.

**Consequence for RQ1:** the degradation detector cannot rely solely on the innovation ratios. When aiding is cut off the ratios do not grow, because there is no measurement against which the estimate could diverge. The signal is a bit in `XKF4.TS`, a binary quantity, not a continuous one.

This narrows the feature list of question RQ1-b and is a result, not a technical problem.

---

## Finding 3: the divergence did not build up before the signal

The divergence between the estimate and the recorded GNSS in window 1, **also after the failsafe triggered**, did not exceed **0.58 m** over 14.5 m of distance travelled.

The aircraft reported the loss of reliability **before** the estimate diverged. The detection lead time was positive.

Caveat: this is a single observation from a window in which aiding was cut off sharply and in a known way, not degraded gradually. It settles nothing about the behaviour under a gradual loss of texture, which is the scenario RQ1 asks about.

---

## Finding 4: distance travelled underestimated by 20%, cause undetermined

Windows 2 and 3 took place at about 2 m, where the rangefinder worked within range. Comparison of the **distance travelled**, integrated along the trajectory, not the net displacement:

| Window | Duration | Distance per estimate | Distance per GNSS | Ratio |
|---|---|---|---|---|
| 2 | 6.5 s | 12.22 m | 15.51 m | **0.788** |
| 3 | 3.6 s | 5.89 m | 7.27 m | **0.810** |

The estimate underestimates the distance travelled by **19–21%** in two independent windows.

**Sensor rotational scale ruled out.** Slope of the regression of `OF.flow` on `OF.body` at rotation rates above 0.15 rad/s:

| Log | X axis | Y axis |
|---|---|---|
| 9 (22 Aug) | 1.009 | 1.107 |
| 10 (23 Aug) | 0.972 | 0.942 |
| 13 (23 Aug) | 0.908 | 0.889 |
| 14 (25 Aug) | 0.981 | 1.182 |

On average 0.97 in X and 1.03 in Y. No systematic deficit. **`FLOW_FXSCALER` and `FLOW_FYSCALER` do not require a change; flow calibration is not indicated.**

Note on the tool: `flow_orientation.py` computes correlations, which are insensitive to scale. It checked the orientation correctly and by design could not detect a scale error.

**Two hypotheses remain.**

Underestimated terrain height estimator: velocity is flow times height. In window 2 the rangefinder indicated 1.99 m, `CTUN.Alt` 1.22 m.

Lag of the velocity estimate during acceleration: **both windows were a monotonic acceleration from zero** under the push of the wind. A lagging estimate underestimates the integrated distance without any scale error. At a final velocity of 2.4 m/s, a lag of 0.7 s gives a 1.7 m deficit against the observed 3.3 m.

Caveat: two windows of 6.5 and 3.6 s, in a 4.6 m/s wind, in AltHold under manual control. An indication, not a measurement.

This is settled by **a run at constant velocity**, not an accelerating one, comparing the path ratio separately in the steady phase and in the acceleration phase. Details: `MISSING_DATA.md` §E5n.

---

## Facts from the log

| | Whole flight 2 | AUTO mission |
|---|---|---|
| Duration | 373 s | 220 s |
| Roll tracking error p95 | 1.17° | 1.25° |
| Pitch tracking error p95 | 1.34° | 1.40° |
| Mean resultant tilt | 6.00° | 6.61° |
| Mean / max. altitude | 9.0 / 23.3 m | 12.3 / 23.3 m |
| Mean throttle | 0.250 | 0.254 |
| VibeZ mean / max. | 18.0 / 47.6 | 18.0 / 47.6 |
| Satellites / HDOP | 22–27 / 0.54–0.66 | 23–27 / 0.54–0.62 |

Battery: 16.76 → 15.64 V, minimum 15.29 V, consumption 1578 mAh, mean current 12.22 A.

`OF.Qual` was 255 for the whole flight, in all windows. Over grass in daylight the indicator remains saturated and carries no information.

---

## Tracking error after tuning

First flight on the gains from S-08. The mission `S-04_Test1.plan` was also flown on 20, 21 and 22 August, so the profile is the same.

| Session | Wind | Roll p95 | Pitch p95 |
|---|---|---|---|
| S-05, 21 Aug | 1–2 m/s | 1.43 / 1.46° | 2.05 / 2.22° |
| S-06, 22 Aug | 2 m/s, gusts 3.2 | 2.25 / 1.98° | 2.46 / 2.58° |
| **S-09, 25 Aug, after tuning** | **4.6 m/s** | **1.25°** | **1.40°** |

The tracking error is the lowest in the series despite the strongest wind. **The comparison is not conclusive, however**, because the wind differs from both reference sessions in the opposite direction to what the result would suggest. To settle it, a flight of `S-04_Test1.plan` at 1–2 m/s is needed, i.e. in the conditions of S-05.

The resultant tilt in the mission was 6.61°, against 5.4° in S-06 at 2 m/s with gusts of 3.2, a data point for the tilt–wind comparison.

---

## Open

- [ ] **A 60 s run at constant velocity**, which settles the cause of the 20% distance underestimate
- [ ] Repeat `S-04_Test1.plan` in a 1–2 m/s wind to settle the effect of tuning
- [ ] Fly GNSS-denied runs **below 6 m**, in accordance with `README` §4.4
- [ ] Add `XKF4.TS` to the list of diagnostic features considered in RQ1-b
- [ ] Complete the GM1010 range multiplier for the two illuminance readings
