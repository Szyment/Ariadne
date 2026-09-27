# S-01: Session card, 15 Aug 2026

**Type:** bench commissioning check (no flights) · **Platform:** 2 (Holybro X500 V2 + Pixhawk 6X) · **Firmware:** ArduCopter 4.7.0
**Data source:** `build-log/01_init.md`, 44 screenshots in `build-log/photos/`
**In the E1–E3 dataset:** no

---

## Course of the session

This was the first power-up of platform 2. The working window derived from the screenshot timestamps: 17:26 – 18:39 (about 1 h 13 min).

Location: **[TO BE COMPLETED]** (the document implies "indoors")
Present: **[TO BE COMPLETED]**

## Completed

| Item | Result |
|---|---|
| Top plate assembly | Pixhawk 6X in the centre, GPS M10 on the mast at the rear, 433 telemetry at M2 |
| Platform Board assembly | TFmini-S at the front, further from the centre, PMW3901 at the front, closer to the centre, both ahead of the battery-pack edge |
| Soldering TFmini-S → TELEM3 | TX/RX crossed, pins 1/2/3/6 |
| Sensor geometry | `FLOW_POS_*`, `RNGFND1_POS_*`, `RNGFND1_GNDCLR = 0.17` |
| Accelerometer calibration | OK (full, not Simple) |
| Compass calibration | both compasses in the green range; `COMPASS_ORIENT = 6` set automatically |
| 433 telemetry | wireless link works |
| GPS fix | 16 sat, 3D DGPS Lock, HDOP 0.9, VDOP 1.1 |
| Optical flow | `quality = 255`, `flow_comp_m_x/y` respond to motion |
| Rangefinder | `current_distance` 54 → 15 cm, responds correctly |

## Decisions with rationale

- The telemetry radio was placed at M2, not at M1. At M1 the antenna protruded beyond the outline of the plate, which risked mechanical damage during transport.
- The ARF kit does not include an RC receiver. Holybro leaves it out deliberately, because the receiver must match the user's transmitter. The two 433 modules in the box are an air/ground pair, not two onboard radios.
- Placing the optical-flow sensor next to the rangefinder is safe. Manufacturers integrate both on a single board (CubePilot HereFlow, MicoAir MTF-01) and both operate at 940 nm.

## Anomalies

| Symptom | Status |
|---|---|
| "GPS Glitch or Compass error" | appears indoors; probably no fix and metal in the surroundings. **Open**, will recur on 18 Aug and 20 Aug |
| `COMPASS_ORIENT = 6` (270° rotation) | ArduPilot compensated on its own. To be verified physically: whether the GPS module on the mast is rotated, or the IST8310 board inside the M10 housing |

## Blocker closing the session

No RC receiver. The RadioMaster RP1 V2 was lost together with platform 1, and the model has been discontinued. The session ends in the state "ready for everything except flight".

## Conditions

Wind / illuminance / temperature / Kp: **not applicable** (bench session)

## Parameter snapshot

None. The first parameter snapshot dates from 18 Aug (`ariadne_v2_18aug2026_1734.params`). The lesson from platform 1 was not implemented in this session: a copy of the configuration should be made at the end of every session, including bench sessions.
