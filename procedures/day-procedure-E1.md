# Day procedure: first E1 measurement run

*v0.1, 5 Sep 2026. A step-by-step compilation of the binding documents: `protocol/ARIADNE_PROTOCOL_E1-E3.md` (§4.3, §5.1, §6, §7, §8, §9.1, annexes A and B), `procedures/preflight.md` v0.2, `missions/S-15_Drift3_README.md`, `ANNEX_C` §7.1 and session card S-16. It introduces nothing new; where the documents differ, it indicates which one is binding.*

The difference between today's flight and all previous ones: the log enters the dataset. From the moment of the first arming in an E1 run, protocol §0 applies: every parameter change divides the data into "before" and "after". That is why steps 0 and 1 are done at the desk, before departure, and are not revisited in the field.

---

## 0. Decisions at the desk (without them there is no E1)

**0.1 FlowCal, the last open item of the §5.1 freeze.** The calibrator of 29 Aug refused to write (`no better scalar`, candidates x 1.106 / y 1.082), `FLOW_FXSCALER` = `FLOW_FYSCALER` = 0. Three resolutions are admissible, and each must be recorded in the log with a date:

| Variant | When | Consequence |
|---|---|---|
| A. Repeat the calibration today before E1 | wind AVG < 2 m/s | if the calibrator writes the scalers: parameter snapshot after the calibration and only then E1; if it refuses again: variant B or C |
| B. Manually `FLOW_FXSCALER` = 106, `FLOW_FYSCALER` = 82 | after a failed repeat | requires one validation run (outside the dataset) before E1; the size of the underestimate is unresolved (S-15: ~13% in X with a weak R²), so the entry is an assumption, not a measurement |
| C. Leave 0 and freeze | when A gives no result and B cannot be validated | the ~8–11% underestimate becomes a known property of the frozen configuration; the path ratio remains a measured quantity, not a corrected one. Record in README §method |

One thing is ruled out: starting E1 without a resolution and changing the scalers after the first log.

**Resolution of 5 Sep 2026: variant C.** The calibration rejected the result twice; `FLOW_FXSCALER` = `FLOW_FYSCALER` = 0 remain frozen for the duration of the campaign. The ~8–11% flow underestimate is a known property of the configuration and enters the description of the method. Parameter snapshot and weighing done before the session.

**0.2 Factor levels 2^4** (§3.2). The protocol gives ALT 1 / 2 / 4 m and VEL 0 / 0.5 / 1.5 m/s as a proposal, and `S-15_Dryf3_README` fixes 3.0 m unconditionally. Before the first log, the two extreme levels of each factor that apply in E1 and the cell name of today's run must be recorded. Constraints known from measurements:

- the upper ALT level must not exceed 3.0 m (rangefinder threshold of 4.2 m in gusts, S-15/S-16),
- the "low + fast" cell lies close to the 2.1 rad/s limit from S-11 (1.0 m × 1.5 m/s = 1.5 rad/s; 0.7 m gives 2.14 rad/s, outside the limit),
- LUX axis: today only the "bright" level exists (§12: bright cells first).

A reasonable starting point: ALT {1.5; 3.0}, VEL {0; 1.5}, SURF {grass; asphalt or concrete after the reconnaissance from §12}, LUX {bright; threshold to be determined}. The choice is the author's decision, not this procedure's.

**0.3 Run order** drawn at random and printed (§3.5). With one run today the draw is trivial, but the entry "order: 1 of 1, no draw" must be in the session card.

**0.4 GNSS criterion.** `preflight.md` says ≥ 8 satellites and HDOP ≤ 1.5; protocol §8 says ≥ 10 satellites and PDOP < 2.0. For the E1 run the protocol is binding (the §8 rejection is applied before seeing the result). Enter both in the card.

## 1. Configuration freeze (§5.1), before departure or on site before the first arming

1. Parameter snapshot to `firmware/ariadne_v2_05sep2026_HHMM.params`. The last snapshot is from 28 Aug 15:35; the state after 29 Aug (RC8_OPTION = 158 for the calibration, possible scalers) has no snapshot.
2. Compare with the snapshot of 28 Aug (`diff`) and list the differences in the log. Check in particular: `RC8_OPTION` (158 = flow calibration started from a switch; if it is to stay, switch RC8 must be protected against accidental use during a run; if not, return to the value from 28 Aug and record that too), `FLOW_FXSCALER`, `FLOW_FYSCALER` in line with decision 0.1, and the full set from `S-15_Dryf3_README`: `WP_SPD` 1.5, `EK3_RNG_USE_HGT` 70, `EK3_RNG_USE_SPD` 3.0, `RC7_OPTION` 90, `EK3_SRC2_POSXY` 0, `EK3_SRC2_VELXY` 5, `WP_RFND_USE` 1.
3. Firmware version: exact number and hash from the ground control station start-up message, to the log.
4. Weigh in flight configuration, with the pack. Reference: 1838 g (28 Aug). Result to the run card.
5. Confirm the calibrations (accelerometer, compass, done 28 Aug with the onboard computer running; ESC). Do not repeat, only note the date performed.
6. `CHECKSUMS.sha256`: recompute after the parameter snapshot.

## 2. Before departure (annex A, `preflight.md` A and B)

- [ ] DroneRadar / PANSA UTM: zones, ≥ 150 m from buildings (A3)
- [ ] Forecast: wind up to 4.0 m/s AVG at 2.0 m (`ANNEX_C` §7.1; the protocol's 5 m/s threshold applies to the run altitude), Kp ≤ 5, no thunderstorm
- [ ] Phone ≥ 50%, power bank; pilot certificates on the phone
- [ ] Two packs measured: 16.7–16.8 V full, not less than 15.2 V (`BATT_ARM_VOLT`); pack numbers
- [ ] Transmitter charged; **transmitter first, then the drone** (the ELRS receiver enters Wi-Fi after 60 s without a transmitter, S-13)
- [ ] Dataflash with spare space; RPi card with spare space for recordings
- [ ] GM1010 lux meter, GM816 anemometer, AX-7510 infrared thermometer (ε = 0.95), ribbon and stake, tape, scale
- [ ] Printout: session card S-17, run cards (annex B), this procedure, `S-15_Dryf3_README` run table
- [ ] Laptop with the ground control station and `drift_plan.py`; smoke stopper
- [ ] Roles recorded: pilot in command, VLOS observer, advisor present Y/N
- [ ] VEL075 (0.75 m/s) runs: two per pack, start only above 90 %; abort before switching to SRC2 if the pack is below 50 % (S-22: battery failsafe on the home leg of the second VEL075 run). Set `WP_SPD` 0.75 before the block and restore 1.5 after it; check the value in QGC (shown in m/s).
- [ ] Heading test (from S-23): on one pack alternate the forward and the reversed plan of the same track (`E1_grass_T3_3m_LAND` / `E1_grass_T3R_3m_LAND`, then the field pair); the reversed plan starts its reference hover at B. Purpose: separate leg order from heading in the return-leg scale error. Field runs in wind ≤ 2 m/s when possible, to separate surface from wind.



## 3. On site, before the first arming

1. DroneTower check-in; confirm that the flight is active.
2. Photo of the site and the surface (file name to the card). Surface condition: dry / damp / wet.
3. Ribbon on the stake at 2.0 m, fixed measuring point ≥ 10 m from the aircraft.
4. Baseline conditions to the session card: wind 60 s (AVG, MAX, sector it blows from; below 1 m/s: "variable"), air temperature from the GM816, pack and surface temperature with the infrared thermometer, illuminance (three readings, median, multiplier, sensor placement, time), cloud cover.
5. `preflight.md` list C: propellers, motors, frame, PMW3901 and TFmini-S lenses clean, downward field of view clear; pack connector to the rear, within the outline, in the same place (reference 4.1 mm).
6. First power-up through the smoke stopper. Then plug in the pack as late as possible (idle draw 0.54 A).
7. Check `RPi: REC active` in QGC. If absent, press the RPi power button (decision of 29 Aug: part of the procedure, not a fault).
8. GNSS: ≥ 10 satellites, PDOP < 2.0 (protocol); numbers to the card. Compass without warnings, no pre-arm errors.
9. Failsafe test on the ground (transmitter switched off, response matches the configuration), RTL altitude for the terrain, mode assignment checked: Stabilize / AltHold / Loiter / Auto / RTL on CH6, `RC7` = EK3 source set, `RC8` as in 1.2, SE = RPi switch.
10. Yaapu: altitude on the ground **0.15 m** (the rangefinder reaches the transmitter). Rangefinder test with a hand. `FLOW_QUAL` non-zero after lifting the aircraft.
11. Short tap of SE (< 3 s): `RPi: SE wykryty` and `RPi: SE puszczony` in QGC.
12. Arm at the take-off point, read the coordinates from the ground control station, disarm.
13. Mission plan:
    ```
    python3 analysis/drift_plan.py --lat <lat> --lon <lon> --wiatr <azimuth it blows from> [--z-wiatrem]
    ```
    Upload `missions/S-15_Drift3.plan`; in the ground control station the waypoints must show terrain altitude (frame 10). Record the leg direction (upwind / downwind) in the session card. Confirm the wind direction by drift in AltHold (`ANNEX_C` §8.1); this may be the first short flight of the day.

## 4. Session calibration flight (§7 item 3), not part of the dataset

One run under reference conditions, with the same procedure as in step 5, named `log_NN` without a protocol name, described in the session card as a quality check. It serves to detect systematic drift between sessions. If variant A was chosen in step 0.1, the flow calibration repeat takes place **before** the calibration flight (LOITER ~5 m, rocking to 100% on both axes), followed by a parameter snapshot and a repeat of step 1.2.

Note on altitude: the flow calibration takes place at ~5 m, that is, above the 4.2 m threshold; after it the altitude in the estimate returns to the rangefinder only below 2.94 m. Before the calibration flight and the run, land and arm anew.

## 5. E1 run (protocol §6 as implemented by `S-15_Dryf3_README`)

Before arming:

1. Run card (annex B) filled in the "before" part: run number (E1-001), LUX/SURF/ALT/VEL cell, time, pack number, starting voltage, mass, pack temperature, satellites / PDOP.
2. Wind 60 s (AVG, MAX) and illuminance (median of 3) just before arming.
3. Pilot: thumb at `RC7` for the whole run; observer: VLOS and bystanders.

Flight:

| | Action | Check |
|---|---|---|
| 1 | Arm, climb in LOITER to 3.0 m (or the cell's ALT) | rangefinder shows the commanded altitude; never above 4.2 m |
| 2 | `RC7` Low | `Using EKF Source Set 1` |
| 3 | Hover 20 s without stick movement | zero-point window (§4.3) |
| 4 | `RC7` Mid | `Using EKF Source Set 2`, then `fusing optical flow`; record the second from the watch |
| 5 | AUTO mode | the aircraft moves to the turn-around point |
| 6 | Touch nothing | 27 s out, 3 s pause, 27 s back, 5 s pause (62 s) |
| 7 | LOITER mode | end of the run, **LOITER first** |
| 8 | `RC7` Low | `Using EKF Source Set 1`; record the second, only now, not before step 7 (S-15 and S-16 had it the other way round) |
| 9 | Land, disarm | |

Abort: AltHold mode (needs no position), then `RC7` Low. Mark the run FAILURE and record the cause; do not correct drift with the sticks, every intervention ends the run.

Immediately after landing:

4. `CTUN.Alt` on the ground against the rangefinder's 0.15 m; a difference > 0.3 m is reference frame drift (S-12 item 4); enter in the card.
5. Wind 60 s after the run; illuminance after the run (change > 30% = rejection under §8).
6. Pack temperature, motor temperature by hand.
7. Decision accepted / rejected **solely** on the §8 criteria, before viewing the result. Pilot's signature.

Next run of the same session: from the "before arming" point, without parameter changes. A pack change marks the boundary of the onboard camera recordings (recording on power-up, log on arming).

## 6. After the session

1. Close the flight in DroneTower.
2. Shut down the RPi with the SE button (≥ 3 s), confirmation in QGC; packs to 15.2–15.4 V.
3. Parameter snapshot after the last run (`INDEX.md`: before the first and after the last, in every session).
4. Logs: an unchanged copy of `log_NN_….bin` to `flight-logs/platform-2-ardupilot/`, and a copy of the measurement run under the §9.1 name: `ARIADNE_E1_001_20260905_LUX?-SURF?-ALT?-VEL?.bin`. Both entries to `INDEX.md` with the link log ↔ parameter snapshot ↔ card S-17 ↔ run card E1-001. The session calibration flight stays under its original name.
5. Onboard camera recordings: `stitch_recording.sh`, names `kamN_20260905_HHMMSS.mp4`; assignment to runs from viewing the content, not from mtime.
6. Session card S-17 and run card to `sessions/`; draw order, leg direction, decisions from step 0 in the log.
7. Copy to a second medium, sync T9, `shasum -a 256 -c CHECKSUMS.sha256`, recompute the sums.
8. Preliminary review: path ratio by halves, drift at t = 15/30/60 s, `OF.Qual`, `XKF4` flags TS/FS, `XKF5.TOfs` start/end, `BARO.Alt` − `RFND.Dist`.
9. `wind_from_log.py` as an independent check of the wind direction.

## Time

The sequence of steps 3–5 with one E1 run and one calibration flight takes about 60–75 minutes from arrival, without a flow calibration repeat (a further ~15 min with the parameter snapshot). A run in a bright cell requires stable illuminance in the run window; at dusk the illuminance falls by ~7 %/min (S-08), so a 60 s run and the two measurements around it fit within the 30% limit only in full daylight.

## Session site near Warsaw (added 6 Sep 2026)

Kępa Okrzewska (Konstancin municipality), meadows behind the dyke east of the 239 bus loop. Zone WA RPA55: check-in without a mission up to 100 m AGL. Getting there: bus 239 from Os. Kabaty (zone 2, ticket 1+2). On site: 150 m from the houses on the SW side, take-off closer to the dyke, ≥50 m from trees and power lines. Generate the mission plan after reading the position from QGC (`drift_plan.py`, axis along the dyke), save the result as `missions/E1_<surface>_T<n>_<altitude>_<LAND|RTL>.plan` (placeholders: surface, track number, altitude; track descriptions in `missions/README.md`). Warsaw within the city limits (RPA06 and neighbouring): closed for Platform 2, see `docs/legal/legal.md`.
