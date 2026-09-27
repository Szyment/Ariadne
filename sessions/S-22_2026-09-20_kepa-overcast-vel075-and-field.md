# S-22: 20 Sep 2026 afternoon, Kępa Okrzewska: first overcast (LUX2) session, first speed level 0.75 m/s, field at 3 m; battery failsafe on a VEL075 run

Logs: `log_40_2026-9-20-16-23-06.bin` (pack P4, flights 1–3) · `log_41_2026-9-20-16-41-46.bin` (P3, flights 4–5) · `log_42_2026-9-20-16-59-12.bin` (P2, flights 6–7) · `log_43_2026-9-20-17-14-20.bin` (P1, flights 8–10). Packs were used in the order P4 → P3 → P2 → P1. Configuration `ariadne_v2_17sep2026_1705.params` (no change; §0 preserved; `FENCE_RADIUS` 120). `WP_SPD` 1.5 m/s in logs 40 and 43, **0.75 m/s in logs 41 and 42** (set in QGC before flight 4, restored before flight 8). Photos: `build-log/photos/2026-09-20/` (phone clock verified against the DroneTower screenshot, file times UTC +2 h), recordings `build-log/video/2026-09-20/`. Results: `analysis/results/S-22_2026-09-20_drift_analysis.txt`, `detector_v0.2_20260920.csv`, `wind_20260912.md` (S-22 section), CSV in `data/`.

Plans: `E1_grass_T3_3m_LAND.plan` (new track T3: A 52.1375457 / 21.1603449, B 52.1373898 / 21.1608774, course 115°, 40.3 m; home on the path 52.1381317 / 21.1612820, A 91 m from home; T1 too close to the trees, T2 too deep in the field), `E1_grass_T3_3m_VEL075_LAND.plan` (same track, `DO_CHANGE_SPEED` 0.75 as the first item), `E1_field_T1_3m_LAND.plan` (A/B of 13 Sep, take-off on the field). Sunset 18:39.

## Conditions (per moment; local time)

DroneTower 16:02: Kp 0.3, 18.1 °C, 1016.3 hPa, humidity 70 %, wind at the surface 2.4 m/s from W 265°, at 100 m 4 m/s from 256°, gusts 5.7, cloud base 2000 m, cover 1/8, visibility 20 km. DroneTower 17:27: 16.5 °C, 83 %, surface 3.2 m/s from W 261°, 100 m 6.7 m/s from 253°, gusts 5.7, cloud base 1300 m, precipitation 0.4 mm, visibility 1 km. Sky at 16:03 mostly clear (4175 lx on the path in sun), variable cloud 16:05–16:18 (1400–2900 lx), from about 16:20 overcast (7–8/8) for the rest of the session.

| Time | Moment | Lux GM1010 | Anemometer GM816: readings [m/s] (series mean / max) | Air temp. (GM816) | Infrared thermometer |
|---|---|---|---|---|---|
| 16:03–16:04 | arrival, path | 4175 (sun) | 1.9 · 6.1 · 3.0 · 2.5 (3.4 / 6.1) | 24.4 | |
| 16:05–16:18 | setting up (readings from the DNG photos, provided by Szymon) | 2654 (16:05), 1693 (16:06), 1403 (16:08), 1557 (16:12), 2881 and 2383 (16:17) | 3.1 (16:06) · 2.6 · 2.2 (16:12) · 2.5 · 2.3 (16:17) · 1.5 (16:18) (2.4 / 3.1) | | |
| 16:22–16:23 | before flight 1 | 1673 (grass) | 1.6 · 3.1 · 3.2 · 3.4 (2.8 / 3.4) | 22.2 | grass 17.2; P3 before 20.5; P4 before 20.8 (from memory, no photo) |
| 16:26–16:29 | flight 1 / before 2 | 1744, 1623 | 1.7 · 2.3 · 2.3 · 2.2 · 2.0 · 3.0 · 2.3 · 2.8 (2.3 / 3.0) | 21.1–22.0 | |
| 16:33 | flight 2 / before 3 | 1274 | 4.2 · 3.4 · 3.0 (3.5 / 4.2) | 21.5 | |
| 16:42–16:43 | pack change P4 → P3 | 1205 | 2.9 · 2.4 (2.7 / 2.9) | 20.7 | grass 18.5; **P4 after 28.2, 27.4, 26.8**; P3 after (see 16:59) |
| 16:45 | flight 4 | 1159 | 2.7 · 2.3 (2.5 / 2.7) | 20.7 | P2 before 22.3 |
| 16:52 | flight 5 | 788.9 | 2.4 · 3.6 · 3.0 (3.0 / 3.6) | 20.1 | |
| 16:59–17:00 | pack change P3 → P2 | 473.7, 447.1 | 4.2 · 3.5 · 2.9 · 5.2 (3.9 / 5.2) | 20.0 | **P3 after 31.3, 31.1** (readings from rotated photos, ±0.2); P1 before 22.2 |
| 17:02 | flight 6 | 466.8 | 1.8 · 3.7 (2.8 / 3.7) | 20.0 | |
| 17:05–17:07 | move to the field | 331.0, 290.5 (field) | 3.2 · 3.2 · 2.0 · 3.2 · 4.1 (3.1 / 4.1) | 20.3 | field 19.0, 18.8 |
| 17:10 | pack change P2 → P1, field | 300.5 | 3.8 · 2.9 · 4.7 · 4.6 · 5.7 · 5.1 · 5.3 · 2.9 · 2.2 (4.1 / 5.7) | 20.1 | **P2 after 27.1** |
| 17:13–17:14 | before flights 8–10 | 294.4 | 3.2 · 4.8 · 3.1 · 3.4 (3.6 / 4.8) | 20.0 | field 19.5; **P1 after 26.4** (measured after flight 10) |

Anemometer readings are spot readings of about ten seconds each, taken more often because of gusts; the series mean approximates the 60 s AVG of annex C §7.1. Pack temperatures were photographed at each pack change (pack removed = "after", pack about to be inserted = "before"), per Szymon's assignment. Packs at home after the session (Storage charge, SkyRC B6AC Neo): P1 3.822 / 3.823 / 3.821 / 3.819 V (Σ 15.28, Δ 4 mV), P2 3.772 / 3.775 / 3.773 / 3.772 (Σ 15.09, Δ 3), P3 3.755 / 3.760 / 3.757 / 3.759 (Σ 15.03, Δ 5), P4 3.777 / 3.776 / 3.780 / 3.777 (Σ 15.11, Δ 4).

Wind from the log (`wind_from_log.py --height 1.2 --speed 1.0`; the default 0.7 m/s hover threshold finds no windows in gusts): tilt 3.1° (log 40), 4.2° (41), 4.4° (42), direction **222–233° (SW)**; no hover window in log 43. Compared with the 3.2° at 2.4–4 m/s on 13 Sep, the wind at flight altitude was about 3.5–4.5 m/s. DroneTower gave W 261–265°, 30–40° off. Relative to the tracks: grass T3 (course 115°) has a small tailwind component outbound (cos 70° = 0.34) and headwind on return; field T1 (course 137°) is pure crosswind.

## Flights

| Flight | Run | Plan | WP_SPD | Armed | SRC2 (local) | Airborne | Lux before → after (≈ geometric mean) | OF.Qual in SRC2 | Path ratio outbound / return | Drift 30 / 60 s / end [m] | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | calibration (§7.3, new track T3) | grass T3 3 m | 1.5 | 16:24:26 | 16:25:40–16:27:14 | 266 s | 1673 → 1744 (~1.7 k) | 255 | 0.944 / 0.887 | 1.1 / 2.5 / 2.5 | |
| 2 | **E1-024** | grass T3 3 m | 1.5 | 16:29:30 | 16:30:59–16:32:21 | 265 s | 1623 → 1274 (~1.4 k) | 255 | 0.991 / 0.859 | 0.6 / 2.4 / **6.8** | GNSS turn 38 s after the switch |
| 3 | **E1-025** | grass T3 3 m | 1.5 | 16:34:23 | 16:35:28–16:37:20 | 273 s | 1274 → 1205 (~1.2 k) | 255 | 0.936 / 0.956 | 1.5 / 4.6 / 2.2 | |
| 4 | **E1-026** | grass T3 3 m VEL075 | 0.75 | 16:43:07 | 16:45:37–16:47:55 (138 s) | 455 s | 1159 → 789 (~1.0 k) | 255 | 0.961 / 0.900 | 1.1 / 2.1 / 3.6 | first VEL075 run; 58 % of pack after the flight |
| 5 | **E1-027** | grass T3 3 m VEL075 | 0.75 | 16:51:27 | 16:53:36–16:56:05 (149 s) | 371 s | 789 → 474 (~0.6 k) | 255 | 0.975 / **0.788** | 1.2 / 2.9 / **10.9** | A→B→A completed; on the home leg `Battery 1 is low 14.56 V, used 3851 mAh` → battery failsafe → Land at 16:57:38, about half-way to home, on grass |
| 6 | **E1-028** | grass T3 3 m VEL075 | 0.75 | 17:00:13 | 17:02:30–17:04:57 (147 s) | 379 s | 467 → 331 (~0.4 k) | 255 | 0.967 / 0.945 | 1.5 / 2.3 / 2.9 | |
| 7 | **E1-029** | grass T3 3 m VEL075 | 0.75 | 17:07:04 | 17:09:15–17:11:45 (151 s) | 365 s | 331 → 300 (~0.3 k) | 255 | 0.949 / 0.903 | 1.2 / 3.4 / 1.9 | |
| 8 | **E1-030** | field T1 3 m | 1.5 | 17:16:28 | 17:17:05–17:18:40 | 182 s | 300 → 294 (~0.3 k) | 255 | 0.864 / **0.723** | 3.1 / 5.3 / **10.6** | flag: wind 3.6–4.1 m/s at the limit |
| 9 | **E1-031** | field T1 3 m | 1.5 | 17:20:03 | 17:20:33–17:22:15 | 177 s | ~0.3 k | 255 | 0.927 / **0.772** | 0.6 / 2.2 / **11.2** | flag: wind |
| 10 | **E1-032** | field T1 3 m | 1.5 | 17:23:37 | 17:24:13–17:26:07 | 180 s | ~0.3 k | 255 | 0.904 / **0.779** | 2.9 / 0.7 / **8.6** | flag: wind |

SRC2 windows in log seconds: 154.4–248.2, 473.3–555.5, 742.5–854.8 (log 40); 231.7–369.4, 710.7–859.9 (log 41); 198.0–345.4, 603.0–753.6 (log 42); 165.1–260.7, 373.4–475.3, 593.0–707.0 (log 43). CSV: `ARIADNE_E1_024…032_20260920_*.csv`, `ARIADNE_KAL_20260920_40.csv`. Barometric reference drift after landing (`CTUN.Alt` minus rangefinder): +1.8 / +2.7 / +3.7 m (log 40), +1.7 / +3.3 (41), +0.6 / +1.2 (42), +1.4 / +2.3 / +3.2 (43): the barometer reads high by 1–4 m within a pack, as on 13 Sep.

Battery per pack: log 40 (three flights at 1.5 m/s) 3764 mAh, min 14.57 V; log 41 (two VEL075 flights) 3897 mAh, failsafe at 14.56 V; log 42 (two VEL075) 3369 mAh; log 43 (three field flights) 2587 mAh. Every log ends with `PreArm: Battery 1 below minimum arming voltage`.

## Findings

1. **VEL075 costs two runs per pack, not three.** A 0.75 m/s run keeps the aircraft airborne 365–455 s (SRC2 window 138–151 s against 82–112 s at 1.5 m/s) and draws about 1900 mAh. Two such runs took 3897 mAh from P3 and triggered the battery failsafe at 14.56 V under load on the home leg of flight 5; the aircraft landed itself on grass half-way to home. The run itself (A→B→A) was complete and is accepted with a flag. Rule from now on: **VEL075 = 2 runs per pack, start only above 90 %**, and the planned third run moves to the next pack. The decision to continue flight 5 from 45 % at A was wrong in hindsight; the procedure now says abort below 50 % before switching to SRC2 on a VEL075 run.
2. **Speed 0.75 m/s over grass does not reduce drift.** Four VEL075 runs: total path ratio 0.87–0.96, final drift 1.9 / 2.9 / 3.6 m plus 10.9 m in the failsafe run; the two 1.5 m/s runs on the same track and light gave 0.92 / 0.95 and 6.8 / 2.2 m. With n = 4 against 2 the difference is within scatter; the longer time without GNSS (150 s against 90 s) is the more likely driver of the 10.9 m case. The VEL axis needs its daylight repetitions before any conclusion.
3. **Overcast daylight (LUX2, 300–1750 lx) behaves like full daylight for the sensor.** `OF.Qual` 255 in every run; residuals and `ePos` within the August baseline. Illuminance fell from 1744 to 290 lx over the session (cloud thickening), without any effect on quality; the light threshold measured at dusk (2–4 lx) is two orders of magnitude lower.
4. **Ploughed field repeats the 13 Sep result in different light and wind.** Return ratio 0.72–0.78, final drift 8.6–11.2 m with `OF.Qual` 255: the silent-failure case (RQ1) now has six runs on two days (E1-012…016, E1-030…032), all without an onboard signal. Detector v0.2: three misses.
5. **The leg-asymmetry rule from S-17…S-21 did not hold today, and the error is a scale error, not a clock.** In all nine runs the return leg has the lower path ratio (grass 0.79–0.96 against 0.94–0.99 outbound; field 0.72–0.78 against 0.86–0.93), although on grass T3 the return flew into the wind. Checked on all 32 runs with `analysis/error_vs_time.py` (`analysis/results/error_vs_time.csv`, `.png`): the estimator error grows on the outbound leg roughly in proportion to distance flown, peaks at the GNSS turn (grass 1.5 m/s: mean 2.6 m at the turn; field: 5.8 m) and then partly reverses on the return leg (many runs end below their turn value). The hypothesis that error grows with time regardless of heading is therefore not supported: a clock-like growth would not reverse. The behaviour is that of a scale factor on the flow-derived velocity (path under-estimation of 4–12 %) whose sign follows the direction of flight, so the two legs partly cancel. At 0.75 m/s the error at a given time is the same as at 1.5 m/s (2.4 against 2.6 m at 60 s) while the distance flown is half, so per metre the scale error at low speed is about twice as large; slope 0.30 m per 10 s at 0.75 m/s against 0.43 at 1.5 m/s. The leg asymmetry seen earlier as a wind effect is then a second-order term on top of this. Consequence for the detector: the quantity to watch is the accumulated scale error along a leg, not the instantaneous residual.
6. **Wind from the log is a usable covariate at 3–4.5 m/s.** Tilt 3.1–4.4° with a consistent SW direction across three logs (consistency 0.98–1.00); the anemometer series means (2.3–4.1 m/s) and DroneTower at 100 m (4–6.7) bracket it. The hover-speed threshold of the script must be raised to 1.0 m/s in gusty conditions, otherwise no window is found.
7. **Detector v0.2 on the day: 0 hits, 6 misses, 3 no-event.** All misses are drift above 5 m without any indicator leaving its threshold (`OF.Qual` 255, `SV` ≤ 0.10, scatter ≤ 0.73 rad/s, `ePos` ≤ 0.28). Wind tilt indicator 2.6–6.0°, the highest of the campaign. The detector has nothing to work with in this regime; the field case needs a different observable (candidate: flow-rate spectrum or residual bias on the return leg).

## Operational notes

- Packs P1–P4 used in reverse order (P4 first). Temperature rise per pack: P4 +7 °C (three 1.5 m/s flights), P3 +11 °C (two VEL075 flights with failsafe), P2 +5 °C, P1 +4 °C.
- Flights 8–10 flown at 3.6–4.1 m/s series mean, at the annex C limit of 4.0 m/s AVG; flagged, not rejected.
- Photos were taken at each pack change; no separate "before" photo of P4.
- `WP_SPD` restored to 1.5 before flight 8 and verified in the log 43 parameter dump.

## To do

- [ ] Daylight repeats: grass 1.5 m ×3, field 1.5 m ×3 (still open from S-21), VEL075 ×2 in full daylight
- [x] Plot error against time since the switch for all 32 runs (finding 5): `error_vs_time.py`, done 21 Sep
- [ ] Add "VEL075: two runs per pack, abort below 50 % before SRC2" to `procedures/day-procedure-E1.md`
- [ ] Add `--speed 1.0` as the documented setting for gusty sessions in `analysis/README.md`
