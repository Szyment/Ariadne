# Glossary and writing rules

*Binding terminology and writing rules for every document in this repository, so that the same thing is always called by the same name.*

## Guiding rule

The work will be read by an international jury (EUCYS, ISEF) and by a reviewer with a research background. Vocabulary follows the ArduPilot documentation and the estimation literature where it exists, and is defined once where it does not. A term is chosen once and used everywhere; synonyms in the same document are a defect.

## Terms

| Term | Notes |
|---|---|
| dataset |  |
| run | one A → B → A measurement; a session contains several runs |
| session, session card | one field outing; card S-NN |
| run card | protocol annex B |
| flight | one arm-to-disarm cycle |
| calibration flight | protocol §7.3, first flight of a session |
| test flight | outside the dataset |
| estimator, extended Kalman filter (EKF3) | "EKF3" for the ArduPilot instance, "estimator" in prose |
| GNSS-denied, without GNSS | not "GPS-denied" (the receiver is multi-constellation) |
| source-set switch, EKF source set 2 | `EK3_SRC2_*`, RC7 |
| optical flow |  |
| optical-flow sensor | PMW3901 |
| image quality (`OF.Qual`) | 0–255 |
| measurement residual (innovation) | "innovation" only in parentheses at first use |
| optical-flow measurement residual | `XKF5.FIX`, `XKF5.FIY` |
| velocity test ratio | `XKF4.SV` |
| estimator position uncertainty | `XKF5.ePos` |
| silent failure | RQ1 term; "unsignalled failure" is not used |
| silent drift |  |
| detection lead time | seconds between warning and reference error > 5 m |
| proxy | e.g. hover tilt as a wind proxy |
| confound |  |
| covariate |  |
| experimental design |  |
| matrix cell | LUX-SURF-ALT-VEL code |
| surface | SURF1 grass, SURF2 ploughed field |
| grass, meadow |  |
| ploughed field |  |
| illuminance | lx, Benetech GM1010 |
| full daylight / overcast / dusk | LUX1 / LUX2 / LUXd |
| altitude above ground (AGL) | from the rangefinder |
| terrain frame | mission altitude relative to the rangefinder |
| rangefinder | TFmini-S |
| barometer, barometric altitude | `CTUN.Alt` |
| hover |  |
| reference hover at A | 30 s |
| path ratio | estimator path length / GNSS path length per leg |
| outbound leg / return leg |  |
| drift | estimator-vs-GNSS distance |
| position error relative to GNSS | reference error |
| reference measurement, reference trajectory | not "ground truth" |
| geofence | `FENCE_*` |
| failsafe | EKF failsafe, battery failsafe |
| parameter snapshot | `.params` file |
| configuration freeze (protocol §0) |  |
| tuning, autotune |  |
| balance (centre-of-gravity check) |  |
| yaw asymmetry |  |
| harmonic notch filter |  |
| battery pack | P1–P4 |
| endurance per pack |  |
| transmitter | RadioMaster Pocket |
| ground control station (GCS) | QGroundControl |
| onboard computer | Raspberry Pi 5 |
| onboard camera recording |  |
| advisor | Szymon |
| pilot in command | Filip |
| observer | VLOS |
| incident | collision, failsafe |
| collision |  |
| post-incident check | preflight §F |
| dusk rules | preflight §G |
| preflight checklist |  |
| day procedure |  |
| DroneTower check-in | keep the product name |
| zone | RPA55 |
| dyke | Vistula dyke at Kępa Okrzewska |
| path (take-off point) | home on the path |
| track (A/B pair) | T1, T2, T3 |
| course | degrees, A → B |
| wind from log | `wind_from_log.py`, hover tilt |
| airframe tilt | hypot(roll, pitch) |
| anemometer | Benetech GM816, AVG at 2.0 m |
| infrared thermometer | pack and surface temperature |
| Kp index | geomagnetic |
| E1–E3 protocol | frozen 7 Aug 2026 |
| annex | annex C (wind), annex D (illuminance) |
| glossary | this file |
| documentation rules |  |
| build log |  |
| arming, disarming |  |
| propeller | 1045 |
| flip-over |  |
| crash |  |
| climb |  |
| land in place | `FS_EKF_ACTION` 1 |
| abort |  |
| flag (flagged run) | protocol rejection or caveat |
| accepted | run status |
| miss / false alarm / hit | detector outcomes |
| vote (voting indicator) | detector rule |

**Proper names, parameters and commands stay unchanged:** `EK3_SRC2_VELXY`, `INS_HNTCH_FREQ`, `RNGFND1_MAX`, `WP_SPD`, `FS_EKF_ACTION`, `Loiter`, `AltHold`, `Auto`, `RTL`, `Land`, ArduPilot, ArduCopter 4.7.0, QGroundControl, MAVLink, Betaflight, ExpressLRS, EUCYS, ISEF, Kępa Okrzewska, DroneTower.

## Numbers, units and dates

Decimal point (0.73, not 0,73). Thin space or plain space between value and unit (3 m, 1.5 m/s, 480 lx, 16.8 V). Dates as "17 Sep 2026" in prose and ISO `2026-09-17` in file names and tables. Times local (CEST) unless stated. Coordinates as decimal degrees with 7 decimals, comma separated: 52.1375457, 21.1603449.

## Style

Technical documents: plain declarative sentences; passive or impersonal voice where the agent does not matter ("the calibration was performed", "the log contains"), first person plural for team decisions ("we adopted a 5 m/s limit"). No rhetorical contrast ("this is not X, it is Y"), no intensifiers ("crucially", "importantly"), no addressing the reader except in checklists and procedures, where the imperative is correct. Bold only for a value the reader must not miss. No em-dash asides; use a comma, parentheses or a separate sentence. One term per concept, from the table above.

Narrative documents (competition summary, jury preparation): first person singular in the author's voice.
