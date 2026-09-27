# S-21: 17 Sep 2026 evening, the same meadow: grass at 3 m and 1.5 m, field at 3 m at dusk; second EKF failsafe with a climb to 37 m

Logs: `log_38_2026-9-17-18-53-30.bin` (pack 1, flights 1–3; log start 18:36:06) · `log_39_2026-9-17-19-11-58.bin` (pack 2, flights 4–7; start 18:55:17). Configuration `ariadne_v2_17sep2026_1705.params`: `FENCE_RADIUS` 90 → 120 (geofence, not estimator; §0 preserved). New Holybro 1045 propellers (full set), check hover `log_37` (see S-20). Sunset 18:46. Photos: `build-log/photos/2026-09-17/session-1-dusk/` (file times in UTC, +2 h). DroneTower forecast (`IMG_0528.PNG`): 1.7 m/s from 260° at the surface, gusts 5.2; 15.7 °C, 1014.2 hPa, 0/8.

Plans: `E1_grass_T2_3m_LAND.plan` (new A/B: A 52.1376277 / 21.1604128, B 52.1373418 / 21.1608037, course 140°, 41.5 m; home from the path 52.1381317 / 21.1612820, A 82 m from home), `E1_grass_T2_1.5m_LAND.plan` (the same points, 1.5 m), `E1_field_T1_3m_LAND.plan` (A/B from 13 Sep), all with take-off on grass.

The session was planned as a daytime one (wind 3.7 / 8.4 m/s in Warsaw at 14:00), flown after 18:35, so in practice another illuminance descent series, with zero wind on the anemometer.

## Conditions (per flight; local times)

| Time | Moment | Lux GM1010 | Wind GM816 | Temp. GM816 | Infrared thermometer |
|---|---|---|---|---|---|
| 18:35–18:38 | before 1 | 138.0 · 120.2 | 0.0 | 19.6 °C | grass 12.6 °C; pack 1 before flights 18.4 °C |
| 18:43 | after 1 / before 2 | 78.1 | 0.0 | 16.9 °C | |
| 18:48 | after 2 / before 3 | 46.4 | 0.0 | 15.6 °C | |
| 18:53–18:55 | after 3, pack change | 26.4 · 21.3 | 0.0 | 14.7 °C | grass 13.3 °C; pack 1 after 3 flights 29.9 °C; pack 2 before flights 17.4 °C |
| 19:01–19:04 | after 4 / before 6 | 8.6 · 6.1 · 5.0 | | | |
| 19:07 | after 6 / before 7 (field) | 3.0 | | | |
| 19:11 | after 7 | 1.1 | | | |
| 19:13 | after the session | | | | pack 2 after 4 flights 27.1 °C |

Anemometer 0.0 at every measurement. From the log (`wind_from_log.py --wysokosc 1.2`): tilt 0.3–1.0° (log 38), 0.8–1.5° (log 39), direction **170–200° (S/SSW)**, i.e. a weak wind of about 0.5 m/s from the south, not from the west as in the forecast. At 30 m (flight 7) 4.0° from 204°. Lux fell 138 → 1.1 in 36 min. Packs after Storage charging (Neo, 20:38): P1 3.782 / 3.779 / 3.773 / 3.773 V (Δ 9 mV), P2 3.797 / 3.797 / 3.792 / 3.792 V (Δ 6 mV).

## Flights

| Flight | Run | Plan | SRC2 (local time) | Lux before → after (~geom. mean) | OF.Qual in SRC2 | Path ratio outbound / return | Drift 30 / 60 s / final [m] | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | calibration (§7.3, new propellers and A/B) | grass 3 m | 18:40:25–18:41:55 | 120 → 78 (~97) | 255 | 0.956 / 0.917 | 0.8 / 1.2 / 2.1 | |
| 2 | **E1-020** | grass 3 m | 18:45:17–18:46:55 | 78 → 46 (~60) | 255 | 0.998 / 0.894 | 0.2 / 1.0 / 4.9 | |
| 3 | **E1-021** | grass 3 m | 18:50:01–18:51:37 | 46 → 26 (~35) | 255 | 0.972 / 0.892 | 1.0 / 1.5 / 3.7 | |
| 4 | **E1-022** | grass **1.5 m** | 18:58:01–18:59:25 | 21 → 8.6 (~13) | 255 | 0.958 / **0.732** | 1.0 / 2.7 / **14.2** | return: GNSS 57.9 m with an estimate of 42.4 m |
| 5 | aborted | grass 1.5 m | — (Auto 19:02:06, Loiter 19:02:08, landing 19:02:39) | 8.6 → 6.1 | | | | advisor's decision: 1.5 m in falling light too risky (14 m drift in flight 4); change to 3 m and the field |
| 6 | **E1-023** | field 3 m | 19:05:42–19:07:15 | 5.0 → 3.0 (~3.9) | mean 197, min 0, 45 % < 255 | 0.923 / 0.837 | 0.8 / 3.3 / 4.2 | first signalled degradation over the field |
| 7 | test (outside the dataset) | field 3 m | 19:09:18–19:10:10 | 3.0 → 1.1 (~1.8) | mean 29, at A 50–90, in motion 0 | — | — | EKF failsafe 32 s after the switch (9 s after leaving A); see below |

SRC2 windows in log seconds: 259.1–348.8; 550.5–649.1; 835.0–930.7 (log 38); 164.0–247.8; 624.9–717.9; 840.5–892.3 (log 39). CSV v0.2: `data/ARIADNE_E1_020…023_20260917_*.csv`, `ARIADNE_KAL_20260917_38.csv`, `ARIADNE_TEST_20260917_39_LUXd-SURF2-ALT3-VEL15.csv`. Altitude reference drift `CTUN.Alt` after landing −0.5 / −0.8 / −1.6 m (log 38), +0.2 / −0.1 / −0.9 / −1.4 m (log 39): cooling, as in S-18/S-20.

## Findings

1. **Altitude 1.5 m (E1-022): the first measured ALT level.** Outbound leg as at 3 m (0.958), return leg 0.732: the aircraft flew 57.9 m per GNSS, the estimate 42.4 m, final drift 14.2 m, `OF.Qual` 255, residuals within norm. Flow scatter 0.4–0.5 rad/s (twice as much as at 3 m, consistent with 1/h). Candidates: (a) at 1.5 m the flow at 1.5 m/s is 1.0 rad/s plus airframe rotation, close to the useful range of the PMW3901 in weak light (13 lx); (b) coupling with the wind on the return leg (downwind, see 3). Run accepted with a flag: the ALT15 cell mixed with LUXd ~13 lx, i.e. two variables at once; to be repeated in daylight.
2. **LUX series over grass at 3 m, a repeat of S-18 with a different A/B: 97 / 60 / 35 lx without degradation** (ratio 0.89–1.00, `OF.Qual` 255). Consistent with S-18 (65 / 47 / 30 lx: 0.935–0.964). New propellers without effect.
3. **Leg asymmetry consistent with the rule for the fifth time.** Wind from S (log), track 140°: the return leg (320°) flies downwind and has the lower ratio in all flights (0.89–0.92 versus 0.96–1.00 outbound). The DroneTower forecast (W 260°) was wrong for this site; the direction from the log (S/SSW) agrees with the behaviour of the aircraft.
4. **Field at ~4 lx (E1-023): the first signalled degradation over SURF2**, 45 % of `OF.Qual` samples < 255, navigation still correct (0.88 whole, drift 4.2 m); at ~2 lx (flight 7) `OF.Qual` in hover 50–90, in motion 0 → failsafe. The threshold over the field is similar to grass (2–4 lx), so the light threshold depends weakly on the surface; the surface acts on accuracy, the light on availability.
5. Detector v0.2: E1-023 warning in the 87th s (error < 5 m, a "forewarning" as in E1-019); flight 7 warning 12.9 s after the switch, 19 s before the failsafe: **the first detection lead time measured within a single flight**. E1-022 a miss: 14 m error without any signal (as SURF2 in S-19).

## Flight 7: course of the incident (log 39, local time)

| log s | time | Event |
|---|---|---|
| 810 | 19:08:47 | Auto, flight to A over the field (72 m from home); `OF.Qual` 50–90 in hover at A (lux ~2), rule B: full flight with observation |
| 840.5 | 19:09:18 | RC7 Mid (SRC2) |
| 863 | 19:09:40 | departure towards B; `OF.Qual` drops to 0 in motion |
| 872.6 | 19:09:50 | `EKF variance` → **EKF Failsafe → AltHold**, 9.6 m from A on course 140°, 2.0 m altitude |
| 872–903 | | **throttle stick at 1805 (about 80 %)**, as throughout the flight in Auto, where it does not matter; in AltHold it is a climb command: the aircraft climbs at 1.3 m/s **from 2 to 37.5 m** in 30 s, at the same time carried by the wind to the NE (course 36–50° from A) at a speed rising to 3.5 m/s, 60 m from A; pitch and roll sticks neutral |
| 892.3 | 19:10:10 | RC7 Low (20 s after the failsafe), GNSS returns, `EKF Failsafe Cleared` 19:10:11 |
| 902.9–903.3 | 19:10:20 | Stabilize for 0.4 s, then **Loiter**: the aircraft stops at 37.5 m, 60 m from A (over the dyke / trees on the NE side of the path) |
| 916–943 | | Loiter, return with the pitch stick (pitch to 2011) towards the path, 35 m from A on course 73° (near point 4) |
| 943–985 | 19:11:00–19:11:43 | descent in Loiter from 37 m to landing, 34 m from A; disarming 19:11:43 |

Interpretation: compared with S-20 the procedure worked (RC7 Low, then Loiter, return in Loiter, landing without damage), but with two weaknesses: 20 s to RC7 Low (8.5 s in S-20) and **throttle at 80 % during AUTO**, which after the failsafe turned into a 35 m climb. Up to 37.5 m over the field, in the dark, over the dyke; that evening's check-in was up to 50 m AGL, so no exceedance, with a 12 m margin. Wind played no part in the loss of position (cause: `OF.Qual` 0 at ~2 lx), but it did in the displacement at 37 m (at 30 m from the log 4.0° of tilt).

## Operational conclusions (for `preflight.md` §G)

1. In AUTO keep the throttle stick near the centre; on a failsafe to AltHold the aircraft reads it immediately (80 % = climb at 1.3 m/s). A climb after a failsafe is to be a decision, not a consequence of the stick position.
2. RC7 Low within 5 s of the failsafe message; you read the message aloud.
3. **Advisor's decision of 18 Sep: `FS_EKF_ACTION` stays at 2 (AltHold).** The meadow and the field are private; landing in place would mean walking in to retrieve the aircraft, after dusk without visibility. Procedure after a failsafe: controlled climb to 10–15 m (throttle about 60 %, not 80 %), RC7 Low, Loiter, return over the path in Loiter, landing on the path.
4. Tests at `OF.Qual` < 100 in hover: do not send to B (rule B to be corrected: at 1–100 hover only). The result is known: in motion the quality drops to 0.
5. Lux at 1.5 m only in daylight, until the ALT level is measured without the LUX factor.

## §8 decision (preliminary)

E1-020, E1-021 accepted: LUXd (~60, ~35 lx)-SURF1-ALT3-VEL15. E1-022 accepted with the ALT15 flag at LUXd ~13 lx (two factors). E1-023 accepted with the flag `OF.Qual` < 255: LUXd (~3.9 lx)-SURF2-ALT3-VEL15. Flight 5 and flight 7 outside the dataset. Wind 0 on the anemometer, ~0.5 m/s from S from the log.

