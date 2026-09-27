# S-14: 28 Aug 2026, evening, balance and tuning check after the computer installation

Log: `log_23_2026-8-28-20-22-42.bin` (both flights on one pack) · `log_22`: false start without the motors running

## Conditions

| | |
|---|---|
| Wind | about 2 m/s, intermittent, from 120° |
| Surface | field, the same as in the previous sessions |
| Start of flight 1 | 20:23 (balance), flight 2: 20:28 (`Test1`) |

## Finding 1: balance accepted: the computer did not shift the centre of gravity

`S-06_Balance1.plan`, four heading hovers of 30 s each:

| Heading | (CCW−CW)/2 | `YawOut` median |
|---|---|---|
| 2° | −5.6 µs | −0.012 |
| 90° | +29.2 µs | +0.029 |
| 181° | +5.8 µs | +0.001 |
| 269° | +35.0 µs | +0.039 |

Constant component of `YawOut` for the whole: **+0.017** against the criterion ≤ 0.098 from the mount correction of 22 Aug. The variation between headings corresponds to the 2 m/s wind, not to mass. Nothing needs to be moved.

## Finding 2: tuning holds despite +140 g: autotune unnecessary

`S-04_Test1.plan`, full 26 commands:

| Quantity | Result | Criterion |
|---|---|---|
| Roll error, p95 | **1.15°** | ≤ 1.86° |
| Pitch error, p95 | **1.26°** | ≤ 2.11° |
| Altitude error, p95 | **0.35 m** | ≤ 0.38 m |
| `VibeY` mean / p95 | 28.4 / 39.9 | target 20 / 30; baseline before the filter 30.3 / 44.8 |

Angle tracking is better than the thresholds, so the increase in moment of inertia fits within the tuning margin of 23 Aug. Vibration above target, but below the old baseline and without effect on tracking; to be observed, not acted on.

## Finding 3: external compass clean after disabling the internal one

Length of the `MAG` vector over the whole flight: 503 mGs below 5 A, 504 mGs above 12 A, difference **+1 mGs**. The decision `COMPASS_USE2` = 0 from card S-13 confirmed in flight.

## Incident: onboard recording again failed in the field

Recording directory empty despite two arming cycles. Decision taken independently of the diagnosis: **return to recording from power-up**; the arming-gated start made recording depend on the chain daemon → MAVLink → systemd, while a start with the system depends only on systemd. Session directories, 60 s segments and clean shutdown via SE remain.

**Diagnosis closed on the evening of 28 Aug: it was not the software; the Raspberry was not running at all during the flights.** There is no journal from the session, because journald was working in volatile mode, but the rotation of `.xsession-errors` settles it: the file from 19:26 survived untouched until the boot at 20:42, so there was no boot between those times, and the flights took place 20:23–20:32. The computer received power but did not start. **Correction of the diagnosis, 29 Aug:** the fuse, contacts and voltage converter are sound; a test reproduced the symptom at home: after power is applied to the X500 the Raspberry waits, and starts only after the button is pressed. The cause is too slow a rise of the 5 V rail (soft start of the converter plus capacitances and wiring): the Pi 5 power controller refuses to start by itself on a slow edge, a behaviour known and described on Raspberry forums. All earlier home tests were done with the Pi already running, so the defect only showed up in the field. Fix: a button brought out from the J2 pads to the airframe, or a disconnect on the 5 V line plugged in after the converter has started; whichever is chosen, the `RPi: REC active` gate in QGC before take-off applies. This failure is also the only one without a software safeguard in the failure matrix (`RPi5_onboard_computer.md`, "Recording architecture, final decision") and is caught by the field rule: no `RPi: REC active` in QGC before take-off = we do not fly. The journal is persistent from now on (`/var/log/journal`).

## Conclusions

Aircraft cleared for `Dryf3`: balance within limits, tuning within limits, compass clean, parameters complete (snapshot `ariadne_v2_28aug2026_1735.params` + `COMPASS_USE2` = 0).

## Open

- [x] Cause of the missing recordings established: no power to the Raspberry in the field (Incident section); journal persistent from now on
- [x] Recording start with the system restored and frozen after the audit (version with `REC active`/`REC off`/`REC cam DOWN` reports in QGC)
- [x] Verification of the card's figures from the log by independent recalculation: consistent, including `MAG` to the milligauss
- [ ] `Dryf3` in the terrain frame: regenerate the plan for the day's wind (`drift_plan.py --wiatr <azimuth>`)

Photos and screenshots: `build-log/photos/2026-08-28/`.
