# S-15: 29 Aug 2026, first Dryf3 run in the terrain frame

Log: `log_24_2026-8-29-12-09-54.bin` · flight 12:09–12:13 · onboard camera recording: `movies/kam0_20260829_111535.mp4` and `kam1_20260829_111535.mp4` from 16:50 to 20:04 (recording start 11:53:04, measured from the segment mtime)

## Conditions

| | |
|---|---|
| Wind | 3.5 m/s, gusts 4, from 279° |
| Illuminance | 3000 lx, up to 30 000 lx in bright spells, clouds after rain |
| Temperature | 23.4 °C at the ground |
| Surface | field, the same as in the previous sessions |
| Plan | `S-15_Drift3.plan`, take-off 50.9140935/19.0866297, turn point 40 m on azimuth 99° |

Leg reversed with the `--z-wiatrem` switch, because a road runs on the windward side: the outbound half flies downwind, the upwind return ends at the take-off point. Comparisons with S-12 by halves only.

## Course of the session

| Log time [s] | Event |
|---|---|
| 1038 | in-flight heading alignment (both IMUs) |
| 1046 | source set 2, optical-flow fusion, start of the GNSS-denied phase |
| 1048 | AUTO |
| 1081 | turn point reached after 32 s |
| 1117 | return to the take-off point after 33 s |
| 1134 | source set 1, end of the GNSS-denied phase (87 s) |
| 1147 | LOITER |
| 1204 | disarming |

The return to set 1 took place while still in AUTO, before the switch to LOITER, the reverse of the procedure (steps 7 and 8). No consequences: the physical position of the switch matched the state, GNSS came back cleanly.

## Finding 1: the terrain frame removed the altitude reference drift

Check from `S-15_Dryf3_README` after the flight:

| Quantity | Dryf2 (S-12) | Dryf3 |
|---|---|---|
| `CTUN.Alt` at disarming against the rangefinder | 1.72–2.00 m | **−0.16 m** against 0.12 m |
| `XKF5.TOfs` start → end | drift 0.28–0.32 m/min | 0.74 → 0.85 (**0.11 m** over 190 s) |

The difference at disarming fits within the 0.3 m criterion. Finding 4 of S-12 is closed: the target altitude in the terrain frame (`frame` 10, `WP_RFND_USE` 1) does not let the altitude reference drift lower the flight, because the target is the distance from the ground measured by the rangefinder.

## Finding 2: path ratio 0.935; the first session with the halves separated

| Phase | GNSS distance | Estimate distance | Ratio | Final drift |
|---|---|---|---|---|
| outbound, downwind, 32 s | 44.1 m | 40.1 m | **0.907** | 5.26 m |
| return, upwind, 33 s | 42.3 m | 39.9 m | **0.942** | 2.79 m |
| whole GNSS-denied phase, 87 s | 90.4 m | 84.5 m | **0.935** | 2.91 m |

The question from S-12, whether the ratio would exceed 0.93, has an affirmative answer. Leg asymmetry: worse downwind (0.907) than upwind (0.942), with a larger final drift on the downwind half. The airflow direction in both halves is the same as in S-12, only the order changed.

## Finding 3: the margin to the altitude switching threshold too small in this wind

`RFND` on the legs: median 3.59 m, p95 4.34 m, maximum **4.49 m**. The threshold above which the rangefinder ceases to be the altitude source lies at 4.2 m (70% of `RNGFND1_MAX` 6 m), and the return requires descending below 2.94 m. Above the threshold were 180 of 3792 samples (4.7%). Gusts of 4 m/s pushed the aircraft nearly a metre above the commanded 3.5 m. There were no consequences (finding 1), but in a wind of about 3 m/s and above the run altitude should be lowered to 3.0 m, which increases the margin to the threshold from 0.7 to 1.2 m.

## Finding 4: optical flow without a single quality drop

`OF.Qual` = 255 for all 8347 samples of the GNSS-denied phase. `XKF4`: no faults (`FS` 0), the only timeout is position, expected, because set 2 has no position source. Barometer against rangefinder on the legs: a range of 4.36 m at 1.3–1.4 m/s over the ground, a further confirmation of the barometer's dynamic error from S-10 and of the need for the terrain frame.

## To do

- [ ] Further Dryf3 runs for repeatability of the path ratio; this is not yet E1: the E1 campaign is a 2^4 design with about 30 runs after the configuration freeze (protocol §3.2 and §5.1), and the freeze requires, among other things, FlowCal, which has not been done
- [ ] In a wind ≥ 3 m/s: run altitude 3.0 m instead of 3.5 m (decision before the next session, not in the field)
- [ ] Separation of the downwind/upwind halves as a standing item of the analysis

Photos and screenshots: `build-log/photos/2026-08-29/` (Mac screenshots `2026-08-29_mac-screenshot_*`: MAVLink Inspector GLOBAL_POSITION_INT 11:56, 12:00, 14:22; image from both RPi cameras 17:04).
