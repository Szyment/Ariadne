# Measurement session sheet (template v0.2, 18 Sep 2026)

Session no. S-__  Date: ____  Location: ____________  Home (from the path, from QGC): ____________
Pilot in command: ________  Observer / VLOS role: ________  Advisor present: Y/N
DroneTower check-in: from ____ to ____, altitude ____ m, radius ____ m (screenshot: ____)
Configuration: `ariadne_v2_<date>_<time>.params` (before): ________  (after): ________  Changes relative to §0: ______ (allowed: only `FENCE_*`)
Mission plans (from `missions/`): ____________________  Propellers: set no. ____  Last VIBE check hover: log ____

## Conditions per measurement (before each flight and after the last; local times)
| Time | Moment (before flight n / after session) | Lux GM1010 (without multiplier) | Wind GM816 AVG / MAX at 2.0 m | Direction (from which) | Air temp. | Infrared thermometer: surface / pack |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

DroneTower forecast (screenshot): wind ____ m/s from ____°, gusts ____, temp. ____, pressure ____ hPa, cloud cover ____. Sunset: ____
Kp index: ____  Satellites at take-off: ____  HDOP: ____   THRESHOLD: sat ≥8, HDOP ≤1.5, Kp ≤5 → OK / FLAG: ____
Wind from log (`wind_from_log.py`, after the session): tilt ____° / direction ____°

## Surface (photo mandatory)
Type: short grass / tall grass / ploughed field / asphalt / bare soil / concrete  Damp: Y/N  Track (A/B per `missions/README.md`): ____

## Packs (3 flights per pack)
| Pack | V before (per cell) | Temp. before | Flights | V after | Temp. after |
|---|---|---|---|---|---|
| P_ |   |   |   |   |   |

## Flights (one row per flight; reference: GNSS track; altitude in the terrain frame ≤ 6 m)
| Flight | Run (E1-NNN / calibration / test) | Cell (LUX-SURF-ALT-VEL) | Plan | Altitude [m, rangefinder] | OF.Qual in hover at A | SRC2 from–to [log s / time] | .bin file | Notes / anomalies |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

Rule §G (`preflight.md`) applied at OF.Qual < 255: Y/N, decision: ____
After returning to GNSS, waited for a fix (satellites, HDOP within threshold) before the next measurement: Y/N
Safety incidents / aborts / post-incident check (§F): ____________  Propellers damaged: ____
After the session: parameter snapshot → `firmware/`, logs → `flight-logs/`, photos → `build-log/photos/<date>/`, `REC` copied from the RPi: Y/N, `tools/update.sh` run: Y/N
