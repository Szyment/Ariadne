# S-03: Session card, 19 Aug 2026

**Type:** flights after the motor mount correction · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Log:** `log_6_2026-8-19-19-33-42.bin` · **Parameter snapshot:** none from this session
**In the E1–E3 dataset:** no (tuning session)

---

## Conditions

| | |
|---|---|
| Location | Field at Kuźnica Kiedrzyńska, 50.914028 N / 19.086457 E, terrain about 224 m above sea level. Confirmed 21 Aug |
| Pilot in command | Filip Pepliński |
| Observer (VLOS role) and telemetry operator | Szymon P. Pepliński |
| Wind (GM816 anemometer) | 2–3 m/s. Proxy from the log: hover tilt 1.47°, the lowest of the three sessions |
| Illuminance (GM1010) | 355 lx, consistent with the time of day (session 19:25 – 19:33) |
| Air and pack temperature, Kp index | [TO BE COMPLETED] |
| Surface | [TO BE COMPLETED] |
| DroneTower check-in | yes, done |
| GNSS quality criterion | Met with a large margin: 24–28 satellites, HDOP 0.47–0.53 |

## Aim of the session

Verification of the motor mount correction made after the diagnosis of 18 Aug.

## Course of the flights according to the log

The record lasts 14.0 min and covers two arming periods. The flights were made in manual modes (Stabilize, AltHold, Loiter).

| | Flight 1 | Flight 2 |
|---|---|---|
| Time [log s] | 494 → 785 | 841 → 961 |
| **Real time (GPS)** | **19:25:41 → 19:30:32** | **19:31:28 → 19:33:29** |
| Duration | 291 s (4.9 min) | 120 s (2.0 min) |
| Max. altitude | 5.4 m | 6.4 m |
| Mean throttle | 0.298 | 0.298 |
| VibeY IMU0 mean / p95 / max. | 23.1 / 31.7 / 57.4 | 25.0 / 38.2 / 124.2 |
| Clipping events | 0 | 0 |
| Roll tracking error p95 | 2.92° | 3.89° |
| Pitch tracking error p95 | 3.45° | 5.48° |
| Pack voltage | 15.90 → 15.19 V (min. 14.94) | 15.35 → 15.04 V (min. 14.68) |
| Cumulative consumption | 1343 mAh | 1817 mAh |
| GNSS reception | 24–28 sat., HDOP 0.47–0.53 | 27–28 sat., HDOP 0.47–0.49 |

Mode sequence: Stabilize → AltHold → Land → Stabilize → AltHold → Loiter → … → Loiter (522–778 s, the longest segment) → Land → Stabilize → Loiter → Land.

Balance for the whole session: voltage 16.04 → 15.15 V, minimum 14.68 V, 1818 mAh drawn, maximum current 38.8 A.

## Result of the correction according to the tuning document

| | LOG 5 (18 Aug) | LOG 6 (19 Aug) |
|---|---|---|
| Diagonal output difference | +370 µs | +84 µs |
| YawOut DC component | +0.449 | +0.098 |
| Clipping events | 21 | 0 |
| VibeY p95 | 94.7 | 32.1 |
| Pitch tracking error p95 | 6.26° | 4.01° |
| Number of ERR entries | 3 | 0 |

The residual of 85–95 µs is the lower limit resulting from the construction. Yaw control saturation was 0.00%.

**Methodological finding.** The measure of the imbalance is the YawOut DC component, not the diagonal output difference. The latter grows with stronger wind and faster flight even with unchanged mechanics, as seen in the change from 84 to 95 µs between 19 and 20 August.

## Significant events

| Time [log s] | Event | Interpretation |
|---|---|---|
| 161 | `EKF3 IMU0/IMU1 MAG0 in-flight yaw alignment complete` | The estimator aligned the heading only after take-off. Hence step 5 of the take-off procedure: arm in Loiter mode and wait some ten to twenty seconds away from concrete and metal |
| 963 | `PreArm: Battery 1 below minimum arming voltage` | Pack voltage dropped below `BATT_ARM_VOLT` = 15.2 V. The session ended with pack exhaustion, not by the pilot's decision |
| — | No `GPS Glitch or Compass error` message | Confirms the supposition of 15 Aug that the symptom occurs indoors, not in the field |

## Operational range on one pack

One 4S 5000 mAh pack allowed 411 s of flight (6.9 min) with a consumption of 1818 mAh and a mean current draw of about 15.9 A.

The E1–E3 protocol §3.1 assumes 4 to 6 runs per pack and three packs per session, giving about 15 runs. A single run involves about 90 s of flight, so realistically 3–4 runs fit on one pack, not 4–6.

This is a feasibility constraint on the campaign and requires a decision on the number of packs. With 150–200 runs planned and four runs per pack, 40–50 charge cycles are needed. The analysis of the options is in `sessions/MISSING_DATA.md` §B1.
