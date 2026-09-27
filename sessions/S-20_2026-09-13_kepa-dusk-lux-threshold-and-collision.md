# S-20: 13 Sep 2026 evening, the same meadow, LUX series down to the sensor threshold; collision with a tree in flight 4

Logs: `log_35_2026-9-13-19-09-16.bin` (pack 1, flights 1–3; log start 18:55:28) · `log_36_2026-9-13-19-18-50.bin` (pack 2, flight 4, collision; log start 19:11:26). Configuration `ariadne_v2_13sep2026_1100.params` (unchanged since S-19). Plan `missions/E1_grass_T1_3m_LAND.plan`, take-off from the path as in S-18. Sunset 18:55. Photos and screenshots: `build-log/photos/2026-09-13/session-2-dusk/`. DroneTower forecast 19–20 (`IMG_0429.PNG`): 1.6 m/s from 282°, gusts 2.9, 16.2 °C, 1018.6 hPa, 1/8.

## Conditions (per flight)

| Time | Moment | Lux GM1010 | Wind GM816 | Temp. GM816 | Infrared thermometer |
|---|---|---|---|---|---|
| 18:41–18:46 | before 1 | 42.0 | 0.0 | 20.7 °C | grass 17.2 °C (avg 17.3) |
| 18:54 | before 1 | 21.0 | 0.0 | 24.2 °C | grass 13.8 °C (avg 13.8) |
| 18:57 | before 1 | 14.7 | | | |
| 19:01 | after 1 / before 2 | 9.2, 9.0 | 0.0 | 24.6 °C | |
| 19:05 | after 2 / before 3 | 5.7 | 0.0 | 22.5 °C | |
| 19:09–19:10 | after 3, pack change | 3.0 | 0.0 | 20.2 °C | pack 1 after flights 25.9 °C (avg 25.3) / 25.0 °C (avg 25.1) |
| 19:11–19:13 | before 4 | 1.9, 1.7, 1.5 | | | |

Anemometer 0.0 at every measurement. From the log (`wind_from_log.py --wysokosc 1.5`, 5 windows): tilt 0.4–0.8°, resultant 0.60° from 182° (S), i.e. as on the evening of 12 Sep: a weak flow of about 0.4 m/s below the anemometer threshold, direction S/SSE. Lux fell 42 → 1.5 in 27 min.

## Flights

| Flight | Run | SRC2 (local time) | Lux before → after | OF.Qual in SRC2 | Path ratio outbound / return | Drift 30 / 60 s / final [m] | Notes |
|---|---|---|---|---|---|---|---|
| 1 | **E1-017** | 18:58:36–19:00:10 | 14.7 → 9.1 (~11.6) | 255 throughout | 0.975 / 0.884 | 0.4 / 1.2 / 4.3 | |
| 2 | **E1-018** | 19:02:34–19:04:11 | 9.0 → 5.7 (~7.2) | 255 throughout | 0.958 / 0.887 | 0.6 / 1.4 / 3.4 | |
| 3 | **E1-019** | 19:06:22–19:07:55 | 5.7 → 3.0 (~4.1) | mean 238, min 0, 17 % of samples < 255; on the return leg 40 % < 255 | 0.927 / 0.899 | 0.9 / 2.7 / 2.5 | first signalled degradation; navigation still correct |
| 4 | threshold test (outside the dataset) | 19:13:52–19:14:09 | 1.9 → (1.5) | **0 from take-off** | — | — | EKF failsafe after 8 s; collision with a tree at 19:14:42, see below |

SRC2 windows in log seconds: 188.8–282.5; 426.5–523.5; 654.5–747.3 (log 35); 146.3–162.7 (log 36). CSV: `data/ARIADNE_E1_017…019_20260913_LUXd-SURF1-ALT3-VEL15.csv`. Altitude reference drift `CTUN.Alt` after landing −0.36 / −0.66 / −0.68 m (cooling, as in S-18).

## Findings

1. **The illuminance threshold of the PMW3901 over grass lies between 4 and 2 lx.** At ~4 lx (E1-019) the image quality starts to fall (17 % of samples below 255, momentarily 0), but the estimate still holds the track (path ratio 0.91, final drift 2.5 m). At 1.5–1.9 lx (flight 4) `OF.Qual` = 0 from take-off; after switching to SRC2 the EKF loses position after 8 s. The nominal minimum of the sensor from the datasheet is 60 lx; the measured value is 15–30 times lower. Together with S-18: a series from 279 to 4 lx without degradation of navigation.
2. **The first run in which the degradation is signalled before the error.** In E1-019 `OF.Qual` drops in the 70th second of the run (detector v0.2 warns at the hard threshold of 50), and the position error does not exceed 5 m. In the detector table this is a "false alarm"; in substance it is a forewarning: 6 minutes later, at half the illuminance, the sensor does not work at all. Detection lead time counted between flights: about 6 min / 2 lx.
3. **Leg asymmetry in a wind of ~0.4 m/s from S:** the return lower in all three (0.88–0.90 versus 0.93–0.98). Track 140°, the wind blows towards 0°, so the return leg (course 320°) flies downwind. Consistent with the rule from S-19 (the downwind leg has the lower ratio), even in wind below the anemometer threshold. Note: DroneTower gives W 282°, the log S 182°; the direction from the log is consistent with the asymmetry, the forecast is not.
4. Detector v0.2 on E1-017/018: no warnings, indicators at baseline.

## Flight 4: course of the collision (log 36, log seconds, local time)

| log s | time | Event |
|---|---|---|
| 111.2 | 19:13:17 | Auto, flight to A; `OF.Qual` = 0 from arming (lux 1.5–1.9) |
| 146.3 | 19:13:52 | RC7 Mid (SRC2), hover at A, according to procedure C (hover only, no leg to B) |
| 154.2 | 19:14:00 | `EKF variance` → **EKF Failsafe → AltHold** (`FS_EKF_ACTION` 2), 8 s after the switch |
| 155–166 | | AltHold, sticks neutral, the drone creeps NNW at 0.1 → 0.9 m/s, 6 m from A |
| 162.7 | 19:14:09 | **RC7 Low**, `EKF Failsafe Cleared`, GNSS returns (8.5 s reaction) |
| 166–170 | | throttle to 1829: **climb from 3 to 7 m** (rangefinder), still AltHold, no Loiter |
| 172–178 | | roll to the left, return towards A (3.5 m from A) |
| 179–183 | 19:14:26 | pitch −8° for 4 s, 2.9 m/s; the drone flies over A and onward to the **WSW (237–259°)** |
| 186–190 | | 9 → 13.6 m from A on course 255°, 6 m altitude; rangefinder 6.6 → 4.1 → 2.1 m: tree crowns under the drone (`OF.Qual` jumps to 255: leaves at close range) |
| 190.6 | 19:14:36 | **Land mode from the auxiliary switch** (reason AUX_FUNCTION), the drone descends into the crown |
| 194.0 | | roll 49° → 75° → 100°: caught on branches |
| 195.7 | 19:14:42 | `Crash: Disarming: AngErr=103>30`, automatic disarming; 14.8 m from A on course 259°, 52.1379877 / 21.1605638 |
| 195–203 | | Loiter/Land with full throttle (2011) with motors disarmed, no effect |

Interpretation: the procedure up to the failsafe worked as intended (test hover, failsafe after 8 s, RC7 Low within 8.5 s). What failed was what came next: after GNSS was recovered the drone **was not switched to Loiter** and for 28 s was piloted manually in AltHold, in the dark (1.5 lx), 40 m from the pilot. The climb to 7 m and the 14 m flight to the WSW look like a loss of the drone's orientation relative to the pilot (symmetrical frame, LEDs in the dark). Land engaged over the tree crowns ended the flight in the branches. Wind played no part (0.0 on the anemometer, 0.6° from the log).

The aircraft flew into the crown of a large bush / small tree and hung between the branches, without falling to the ground. The motors were disarmed automatically by the crash detector (195.7 s); the electronics remained powered until the aircraft was recovered (the log runs to 436 s, `Radio Failsafe - Disarming` after the transmitter was switched off, as in LOG 5 of 18 Aug). Damage: one propeller cracked. Post-incident check (`preflight.md` §F), performed on 15 Sep: motors OK (even rotation, no play); arms OK; screws tightened, practically no play; sensor board OK (lenses clean, no scratches, plugs pressed in); GPS mast, 433 MHz antenna and ELRS OK; landing gear OK. Pack 2 (from flight 4) undamaged, connected through the smoke stopper: no shorts, idle draw 0.5 A after switch-on (as on 29 Aug), 0.8 A while downloading recordings from the RPi 5; voltage 16.3 V. Bench test in QGC on 15 Sep: compass and horizon consistent with reality; `DISTANCE_SENSOR.current_distance` changes correctly; `OPTICAL_FLOW.quality` 255, 0 when covered, `flow_x/flow_y` respond to displacement and return to zero. Aircraft serviceable apart from the propeller. New propellers fitted on 17 Sep; check hover on 17 Sep (`log_37_2026-9-17-16-38-28.bin`, Loiter, 80 s, 1.7–2.5 m): `VIBE` X 18–22 / Y 20–23 / Z 14–17 (baseline 12 Sep: 17–21 / 19–23 / 11–15), clipping 0, hover throttle 0.28–0.29 (baseline 0.282), current 15.4 A (baseline 15.65); wind from the anemometer 3.7 m/s, gusts 8.4, from the log tilt 1.75° from about 270° at 2 m (compare 3.2° at 6.9 m in S-19: the indicator depends on altitude). Aircraft serviceable, configuration unchanged, cleared for runs.

## Onboard recordings

`movies/kam0_20260913_190936.mp4`, `movies/kam1_20260913_190936.mp4` (483 s): pack 2 only, i.e. flight 4 with the collision; kam1 (NoIR + IR) shows the branches at close range and the recovery of the aircraft. Frames: `build-log/photos/2026-09-13/session-2-dusk/_klatki_kolizja.jpg`. **Flights 1–3 (pack 1) without recording**: no RPi session from 18:55–19:08, most likely the computer did not start after the pack was plugged in (a known case, `RPi: REC active` was not checked). For the procedure: check `REC active` before the first arming of each pack.

## Operational conclusions (for `preflight.md` and the day procedure)

1. After `RC7 Low` following a failsafe, **Loiter immediately**, before any stick movement. AltHold in the dark is prohibited.
2. Perform the threshold test (`OF.Qual` = 0) over the middle of the field, with A moved at least 30 m from the tree line, or not at all: the result of the test is already known (failsafe after ~8 s).
3. For sessions after dusk consider `FS_EKF_ACTION` = 1 (land in place): when hovering over grass, landing in place is safer than manual piloting in the dark. The parameter change does not affect the estimator; Filip's decision.
4. Land from the switch only over known, open ground; over trees, Loiter and return.
5. A full set of spare propellers in the bag for every session.
6. `RPi: REC active` in QGC before every arming, also after a pack change.

## §8 decision (preliminary)

E1-017…019 accepted, cell LUXd-SURF1-ALT3-VEL15 (lux ~11.6 / 7.2 / 4.1, geometric mean of before and after). E1-019 with the flag "image quality below 255", stays in the dataset as a borderline run. Flight 4 outside the dataset (test, no run).
