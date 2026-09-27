# S-06: Session card, 22 Aug 2026

**Type:** balance and symmetry check flight, after the motor alignment correction · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Log:** `log_9_2026-8-22-16-05-38.bin` (123 MB) · **Ground telemetry:** `2026-08-22 16-05-42.tlog`
**Configuration:** `ariadne_v2_22aug2026_1519.params`, no changes for the flight
**In the E1–E3 dataset:** no (technical session)

---

## Conditions

| | |
|---|---|
| Location | Field at Kuźnica Kiedrzyńska, 50.914028 N / 19.086457 E |
| Pilot in command | Filip Pepliński |
| Observer (VLOS role) and telemetry operator | Szymon P. Pepliński |
| Wind (GM816 anemometer) | **2 m/s on average, gusts 3.2 m/s, from the west (270°)** |
| Illuminance (GM1010) | **70 000 lx** (reading 7000 on the ×10 range) |
| Weather | after rain, cloudless, full sun |
| Surface condition | **wet grass.** On 22 Aug intermittent showers all day, heavy towards the end of the day; session at 16:05. Confirmed 23 Aug: the next day there were puddles in the forest. Difference between the first and second flight not recorded |
| Session start | 16:05 |
| Air and pack temperature, Kp index | [TO BE COMPLETED] |

> **Correction 23 Aug.** The reading was recorded without the range multiplier. Solar elevation at 16:01 was 34.3°, upper bound for a cloudless sky 62 100 lx. The recorded weather is *after rain, cloudless, full sun*, in which 7 000 lx would correspond to dense overcast. A reading of 7000 on the ×10 range gives 70 000 lx, i.e. 13% above the model. Verification: `protocol/ANNEX_D_illuminance_measurement.md` §6.

**70 000 lx is the upper point of the illuminance axis.** The previous maximum was 2450 lx (20 Aug). The range covered in August spans 21 – 70 000 lx, i.e. three and a half orders of magnitude.

**First session after rain.** Surface condition is a covariate introduced into the run card on 22 Aug precisely because of this factor; this session is the first opportunity to record it.

---

## Course of the session

Two flights, both on one battery pack:

1. **Mission `S-06_Balance1.plan`**: four hovers of 30 s each at absolute headings 0°, 90°, 180° and 270°, altitude 15 m. Purpose: to check the effect of the motor alignment correction and to collect material for separating the payload offset from the wind-induced moment.

   The mission was flown **without changing `WP_YAW_BEHAVIOR`**, which remained at 2. The recommendation from the mission description to set it to 0 for the flight turned out to be unnecessary: `CONDITION_YAW` worked correctly, and the autopilot did not try to point the nose at the next waypoint, because all the mission waypoints are at the same location. The configuration was therefore left untouched, which matters given the requirement to freeze parameters for the duration of the campaign (protocol §2.3).

   Of the four hovers, three entered the analysis, at headings 90°, 182° and 269°. The hover at heading 0° dropped out, most likely because the aircraft was still flying to the waypoint and the horizontal velocity filter rejected it. The heading spread was 0.897 anyway, so the material was sufficient. When repeating the mission it is worth adding a ten-second hold before the first `CONDITION_YAW`.
2. **Mission `S-04_Test1.plan`**: repetition of the track of 20 and 21 August.

---

## Result: torque asymmetry removed

On 22 August the alignment of the arms in the clamps was corrected. The propellers were inspected visually: a uniform set, undamaged, not swapped between motors.

| Session | Log | Windows with settled heading | Asymmetry | Yaw output | Yaw margin |
|---|---|---|---|---|---|
| 18 Aug evening | 5 | rough estimate | +69% | — | — |
| 19 Aug | 6 | 1 | +16.8% | +60 µs | 30% |
| 20 Aug | 7 | 4 | about +14% | about +60 µs | about 30% |
| 21 Aug | 8 | 4 | about +15% | about +48 µs | about 24% |
| **22 Aug, after correction** | **9** | **5** | **−2.3%** | **−8 µs** | **4%** |

Motor outputs in the first window: 1524 / 1424 / 1515 / 1453 µs. For comparison, 21 August: 1531 / 1624 / 1483 / 1459 µs. The spread between the heaviest and lightest fell from 165 to 100 µs, and the difference **between the counter-rotating pairs**, i.e. the one that creates the yaw moment, from 141 to 8 µs.

The cause was the arm alignment. The matter is closed, autotune is unblocked.

---

## Result: reference value for the battery position

Five hover windows with headings spread over the range 33–271°, spread measure 0.897. For the first time the material is sufficient to separate the payload offset from the wind-induced moment.

| | |
|---|---|
| Payload offset, fore–aft | +1.5 mm |
| Payload offset, left–right | −3.8 mm |
| **Payload offset, resultant** | **4.1 mm** |
| Wind component, resultant | 22.5 mm |

**The figure of 4.1 mm is the reference value for subsequent sessions.** The battery sits practically level. A deviation of more than roughly 5 mm from this value in a subsequent session will mean that the pack went back into a different position after charging.

---

## Result: three independent methods agree on the wind direction

| Method | Direction the wind blew from |
|---|---|
| GM816 anemometer, field reading | 270° (W) |
| Aircraft tilt in hover (`wind_from_log.py`) | 283° (WNW) |
| Motor load distribution (`balance.py`) | 278° (W) |

A spread of thirteen degrees, i.e. less than the width of a sector. The two methods from the log use entirely different signals: the first the roll and pitch angles, the second the outputs of the four motors. Their agreement, and the agreement of both with the instrument, confirms at the same time the compass calibration, the correctness of the computation and the soundness of separating payload from wind.

Resultant hover tilt was 5.42°, horizontal acceleration 0.93 m/s².

---

## Wind indicator from the log: cumulative table

| Session | Wind from anemometer | Hover tilt | Hover altitude |
|---|---|---|---|
| 20 Aug | 2–3 m/s | 4.6° | 15 m |
| 21 Aug | 1–2 m/s | 3.3° | 15 m |
| 22 Aug | 2 m/s, gusts 3.2 | 5.4° | 15 m |

The table is the seed of a conversion from tilt to wind speed. Three points are not enough and do not yet form a monotonic sequence: 22 August gave a larger tilt than 20 August at a similar anemometer reading. Possible causes: gustiness (3.2 versus no recorded gusts on 20 August), a different altitude of the hover windows, a different moment of the anemometer measurement. The table is to be extended after every session; with a dozen or more points a curve fit will become meaningful.

---

## Facts from the log

Record 13.9 – 576.5 s (9.4 min), two arming events. **Both flights were flown on one battery pack.**

| | Flight 1 (`S-06_Balance1.plan`) | Flight 2 (`S-04_Test1.plan`) |
|---|---|---|
| Time [log s] | 49.0 → 250.2 | 309.3 → 561.6 |
| Duration | 201 s (3.4 min) | 252 s (4.2 min) |
| Max. altitude | 15.5 m | 25.8 m |
| Mean throttle | 0.220 | 0.245 |
| VibeY IMU0 mean / p95 / max. | 22.5 / 31.5 / 43.9 | 25.2 / 35.6 / 61.8 |
| Clipping events | 0 | 0 |
| Roll tracking error p95 | 2.25° | 1.98° |
| Pitch tracking error p95 | 2.46° | 2.58° |
| Pack voltage | 16.78 → 16.17 V (min. 15.95) | 16.31 → 15.53 V (min. 15.29) |
| Cumulative consumption | 655 mAh | 1582 mAh |
| GNSS reception | 23–28 sat., HDOP 0.47–0.52 | 28–30 sat., HDOP 0.45–0.49 |

Session balance: 16.78 → 15.64 V, minimum 15.29 V, 1584 mAh drawn, maximum current 29.3 A.

GNSS quality criterion met with a large margin: 23 to 30 satellites, HDOP below 0.52, the best readings in the whole August series.

---

## Three findings from this log

### 1. EKF3 source-set switching works: first trace in the project

Messages from 40–45 s:

```
40s  Using EKF Source Set 2
40s  EKF3 IMU0 fusing optical flow
40s  EKF3 IMU1 fusing optical flow
41s  Using EKF Source Set 1
41s  Using EKF Source Set 2
45s  Using EKF Source Set 1
45s  EKF3 IMU0 is using GPS
```

The switch on the transmitter (`RC7_OPTION` = 90) changes the source set, and the estimator actually accepts optical flow as the velocity source when switched to it. **The mechanism on which the whole research question RQ1 rests has been confirmed in a log for the first time.**

Caveat: this happened on the ground, before take-off, so what is confirmed is the switching and the start of fusion, not the behaviour of the aircraft in GNSS-denied flight. That remains to be checked in the first measurement run.

### 2. The flight budget is probably twice what the plan assumes

Both flights from one pack: **453 seconds airborne, 1584 mAh of 5000, final voltage 15.53 V** against the warning threshold `BATT_LOW_VOLT` = 14.8 V. Mean current 12.6 A versus 15.9 A in log 6 of 19 August.

Item B1 in `MISSING_DATA.md` bases the campaign feasibility calculation on 411 seconds of flight per pack and derives from that about 105 runs against the 160–190 needed. Today's log undermines that basis.

**To be settled with a single flight:** drain a pack in hover down to the 14.8 V threshold and record the time. This is the cheapest possible resolution of the project's largest planning constraint; it may remove the need to buy further battery packs.

### 3. Minor item to watch: `Arm: Gyros inconsistent`

Message at 23 s, cleared on its own, arming succeeded some twenty-odd seconds later. Most likely the gyroscopes had not warmed up after power-on; `BRD_HEAT_TARG` is 45 °C and reaching that temperature takes time. If the message were to recur, it would be a signal about the sensor, not about the procedure.

---

## Note on angle tracking error comparisons

The tracking error came out worse than on 21 August: roll p95 2.25 and 1.98° versus 1.43 and 1.46°, pitch 2.46 and 2.58° versus 2.05 and 2.22°. **No conclusion about tuning should be drawn from this**, because the conditions were clearly harsher: hover tilt 5.42° versus 3.3°, wind 2 m/s with gusts of 3.2 versus 1–2 m/s with no recorded gusts.

This is the same confound described in card S-05: without a repetition in the same conditions, a between-session comparison does not settle anything about tuning. The hover tilt indicator, now computed by `wind_from_log.py`, at least allows the scale of this difference to be measured rather than passed over in silence.

---

## Open after this session

- [x] Facts from the log completed 22 Aug
- [x] Surface condition completed 23 Aug: wet grass. Air and pack temperature not recorded, cannot be reconstructed
- [x] **Done 23 Aug (log 10): 855.8 s, 3207 mAh.** Item B1 closed
- [x] `INS_RAW_LOG_OPT` = 0 from 23 Aug. Log 10 is 27 MB versus 123 MB
- [ ] Autotune (`RC8_OPTION` 16 → 17), calm day, more than one pack
