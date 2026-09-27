# S-02: Session card, 18 Aug 2026

**Type:** first flights of platform 2, detection of yaw torque imbalance · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Logs:** `log_2` … `log_5` in `flight-logs/platform-2-ardupilot/`
**Parameter snapshots:** `ariadne_v2_18aug2026_1734.params`, `ariadne_v2_18aug2026_1740.params`
**In the E1–E3 dataset:** no (tuning session)

---

## Conditions

| | |
|---|---|
| Location | Field at Kuźnica Kiedrzyńska, 50.914028 N / 19.086457 E, terrain about 224 m above sea level. Confirmed 21 Aug: all three sessions of 18–20 Aug took place at the same site |
| Pilot in command | Filip Pepliński |
| Observer (VLOS role) and telemetry operator | Szymon P. Pepliński |
| Wind (GM816 anemometer) | 2.5 m/s; according to a second reading 3–4 m/s with gusts to 5 m/s, i.e. at the limit of the rejection threshold from protocol §8 |
| Illuminance (GM1010) | 1330 lx |
| Air and pack temperature | [TO BE COMPLETED] |
| Kp index | [TO BE COMPLETED] |
| Surface | Grass. This follows from the description of the tip-over after landing in the tuning document; to be confirmed |
| DroneTower check-in | yes, done |
| GNSS quality criterion | Met with margin in log 5: 23–25 satellites, HDOP 0.54–0.64, against the requirement of ≥8 satellites and HDOP ≤1.5 |

## Course of the flights according to the log

### `log_2` (16:21): work on the ground

The record lasts 6.0 min, Stabilize mode, no arming. Pack voltage 16.77 → 16.73 V, 44 mAh drawn, maximum current 1.2 A. At 313 s the message "GPS Glitch or Compass error" appeared. The session was of a configuration nature.

### `log_3` (16:58 – 17:08): six short lift-offs

The record lasts 10.3 min. Six arming events were recorded, flights from 9 to 24 s, altitude 2.2–5.0 m.

| Flight | Time [log s] | Duration | Max. altitude | Mean throttle | VibeY IMU0 mean/p95 | Roll/pitch tracking error p95 |
|---|---|---|---|---|---|---|
| 1 | 2297 → 2307 | 10 s | 2.2 m | 0.062 | 1.0 / 5.0 | 0.29° / 1.04° |
| 2 | 2317 → 2336 | 20 s | 3.2 m | 0.108 | 0.5 / 1.2 | 0.54° / 1.05° |
| 3 | 2779 → 2790 | 11 s | 5.0 m | 0.127 | 0.5 / 1.5 | 0.10° / 0.96° |
| 4 | 2798 → 2821 | 24 s | 3.0 m | 0.032 | 1.7 / 6.4 | 0.97° / 2.37° |
| 5 | 2826 → 2835 | 9 s | 3.6 m | 0.051 | 1.1 / 4.6 | 1.44° / 1.92° |
| 6 | 2841 → 2856 | 15 s | 4.6 m | 0.041 | 0.8 / 3.7 | 0.50° / 1.40° |

GNSS reception remained poor throughout the record: 5–8 satellites, HDOP 1.24–4.71, i.e. below the quality criterion from the checklist. An estimator core change was recorded (`EKF3 lane switch 1`, `EKF primary changed:1` at 2326 s) and a return to core 0 at 2331 s, then `Glitch cleared` at 2414 s and a repeated "GPS Glitch or Compass error" message at 2418 s. Pack voltage 16.62 → 16.57 V, 262 mAh drawn, maximum current 7.0 A.

### `log_4` (17:57 – 17:58): two short lift-offs

The record lasts 14.5 min, two arming events of 6 and 9 s. The first attempt did not end in a lift-off (maximum altitude −1.8 m). The second reached 3.9 m, with a pitch tracking error (p95) of 6.36°, the highest in the whole session. GNSS reception: 7–10 satellites, HDOP 1.34–2.25. Messages recorded: `PreArm: Hardware safety switch`, `PreArm: High GPS HDOP`, `EKF3 IMU0/IMU1 MAG0 in-flight yaw alignment complete`, `GPS Glitch or Compass error` (1125 s) and `Glitch cleared` (1135 s).

### `log_5` (18:41 – 18:46): diagnostic session, described in the tuning document as LOG 5

The record lasts 10.7 min, two arming periods.

| | Flight 1 | Flight 2 |
|---|---|---|
| Time [log s] | 231 → 279 (48 s) | 493 → 561 (68 s) |
| **Real time (GPS)** | **18:41:15 → 18:42:03** | **18:45:37 → 18:46:44** |
| Max. altitude | 3.8 m | 3.8 m |
| Mean throttle | 0.226 | 0.241 |
| VibeY IMU0 mean / p95 / max. | 23.2 / 46.7 / 59.9 | 48.3 / 111.5 / 164.6 |
| Clipping events | 0 | 21 |
| Roll tracking error p95 | 2.62° | 4.90° |
| Pitch tracking error p95 | 4.30° | 8.63° |
| Pack voltage | 16.41 → 16.13 V | 16.31 → 15.83 V (min. 15.59) |
| GNSS reception | 23–24 sat., HDOP 0.59–0.64 | 24–25 sat., HDOP 0.54–0.59 |

Mode sequence: Stabilize → Land → Stabilize → … → AltHold → Land.

## Significant events in `log_5`

| Time [log s] | Event |
|---|---|
| 264 | `Yaw Imbalance 38%` |
| 274 | `Yaw Imbalance 41%` |
| 347 | `PreArm: Compasses inconsistent` |
| 541 | `Yaw Imbalance 45%` |
| 551 | `Yaw Imbalance 47%` |
| 561 | `Crash: Disarming: AngErr=80>30, Accel=0.0<3.0` |
| 585 | `Radio Failsafe - Disarming` |
| 586 | `PreArm: Radio failsafe on` |

## Diagnosis according to the tuning document

**Yaw torque imbalance.** Outputs C1 and C2 ran 370 µs higher than C3 and C4 (C3 at 1260 µs, C1 at 1639 µs). About 45% of the yaw control range was permanently taken up by holding the heading. The phenomenon was present from the first flight of the session and grew between flights: +334, +362, +407 µs.

The cause was the motor mounts being seated at an angle. The source of the misalignment was not established.

**Tip-over after landing.** After touchdown in the grass the aircraft tipped over before disarming: the pitch angle changed from −3° to −68°, the roll angle from −0.5° to −10.2°, after which it settled at −4.6°. The motors were running throughout the tip-over and only went down to 1000 on disarming. The event has no causal link to the yaw torque imbalance, which was present earlier.

## Discrepancies between the log and the documentation

1. The tuning document lists three flights in LOG 5, whereas the record contains two arming periods. Lift-offs within one arming were probably counted. To be confirmed.
2. ~~`Radio Failsafe - Disarming` at 585 s~~, explained 21 Aug on the basis of the record: the transmitter was switched off after the completed flight. The aircraft had been disarmed 24 s earlier, the channel values remained frozen until the end of the record, and the failsafe state did not clear. The event does not belong to the same category as the loss of control on platform 1. Details in `sessions/MISSING_DATA.md` §C2.
3. The message `PreArm: Compasses inconsistent` (347 s) does not appear in the documentation. It relates to the open item concerning `COMPASS_ORIENT` from 15 Aug.
4. The whole of `log_3` was recorded below the GNSS quality criterion (5–8 satellites, HDOP up to 4.71). For tuning flights this does not matter, whereas a measurement run in such conditions would be rejected under protocol §8.
5. The tuning document places the tip-over at t = 502.9–504.1 s and the crash check at 505.6 s; the log gives `Crash: Disarming` at 561 s. This results from the use of different time references (Filter Review versus `TimeUS`). The references must be unified before the thesis is written up.

## Parameter snapshots

The files `ariadne_v2_18aug2026_1734.params` and `ariadne_v2_18aug2026_1740.params` were made before the flights of this session (17:34 and 17:40, flights until 18:49). There is no snapshot made after the session.
