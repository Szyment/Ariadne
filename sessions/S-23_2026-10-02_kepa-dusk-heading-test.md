# S-23: 2 Oct 2026 evening, Kępa Okrzewska: heading test (tracks flown in both directions) at dusk, calm air

*Illuminance in lux, converted from the GM1010 foot-candle readings (× 10.764, annex D §8, 4 Oct 2026); X10-range readings are display × 10 fc, converted the same way (annex D §8, 11 Oct 2026).*

Logs: `log_44_2026-10-2-17-54-06.bin` (pack P1, flights 1–3, grass) · `log_45_2026-10-2-18-11-24.bin` (P2, flights 4–6, grass) · `log_46_2026-10-2-18-26-52.bin` (P3, flights 7–9, field). Packs used in order P1, P2, P3; P4 not flown (see below). Configuration `ariadne_v2_17sep2026_1705.params` (no change; §0 preserved; `FENCE_RADIUS` 120, `WP_SPD` 1.5 in all logs). Photos: `build-log/photos/2026-10-02/` (file times UTC +2 h). Flight times are from GPS time in the logs; the log file name carries the time the log was closed, not opened (this card was corrected on 4 Oct 2026: the first version had every flight 14–17 min too late and the illuminance assigned to the wrong flights; finding 3 changed as a result). Results: `analysis/results/S-23_2026-10-02_drift_analysis.txt`, `detector_v0.2_20261002.csv`, `error_vs_time.*` (40 runs), CSV in `data/`.

Purpose (S-22 finding 5): separate leg order from heading in the return-leg scale error by flying each track alternately forward and reversed within one pack. Plans: `E1_grass_T3_3m_LAND` (A → B → A, course 115° outbound) and `E1_grass_T3R_3m_LAND` (B → A → B, course 295° outbound); `E1_field_T1_3m_LAND` (course 137°) and `E1_field_T1R_3m_LAND` (317°). The plan flown in each flight was verified from the hover position at the switch (distance to A or B below 0.1 m in every case).

Sky clear all afternoon (DroneTower 17:36, `IMG_1240.PNG`, hour 17–18: Kp 0.3, 17.2 °C, 1033.0 hPa, humidity 58 %, wind at the surface 2.7 m/s from SE 120°, at 100 m 5.7 m/s from SE 131°, gusts 5.7, cloud cover 0/8, sunset **18:11**). Wind direction from the phone compass at 17:36 (`IMG_1235.PNG`): 134° SE. The session ran into dusk, so the cell is LUXd. Wind 0 on the anemometer with isolated readings of 0.6–1.5 m/s.

## Conditions (per moment; local time)

| Time | Moment | Illuminance [lx] (GM1010) | Anemometer GM816 [m/s] (air temp.) | Infrared thermometer |
|---|---|---|---|---|
| 17:34–17:36 | arrival, path; low sun | 4670 (grass in shade), 5890 (17:38) | 0.0 · 0.9 · 0.6 · 1.3 (21.1–21.3 °C) | grass 14.7; P1 before 22.8 (IMG_1234) |
| 17:43–17:44 | after flight 1 | 3530, 3210 | 0.0 · 0.0 (18.9–19.1) | |
| 17:48 | after flight 2 | 2780 | 0.0 (17.7) | |
| 17:52–17:54 | after flight 3, pack change P1 → P2 | 2200 | 0.0 (16.7) | grass 14.8; P1 after 31.0 (IMG_1255, 17:54:51); P2 before 21.5 (IMG_1254) |
| 17:55–17:57 | log 45 started | 1870, 1700 | 0.0 (16.4) | |
| 18:00–18:01 | after flight 4 | 1360, 1240 | 1.0 · 1.5 · 1.3 · 0.0 (15.9–16.3) | |
| 18:03 | flight 5 | 1110 | | |
| 18:06 | before flight 6 | 865 | 0.0 (15.2) | |
| 18:10–18:12 | pack change P2 → P3, move to the field | 644, 538 | 0.0 (14.5) | grass 13.5; P3 before 22.5 (IMG_1274); P2 after 29.4 (IMG_1275, 1276) |
| 18:15–18:16 | flight 7 | 320 | 0.0 (14.3) | field 15.9 |
| 18:20 | flight 8 | 196 | 0.0 (14.3) | |
| 18:23–18:26 | flight 9 | 139, 110, 88.3 | | field 14.2 |
| 18:27 | pack change P3 → P4 | | | P3 after 24.5 (IMG_1291, 18:27:45, measured after a longer while) |
| 18:28–18:29 | before the P4 attempt | 64.6 | 0.0 (13.3) | |
| 18:29–18:35 | P4 attempt (reference hover, `OF.Qual` 0, abandoned) | ≤ 65, falling | | |

The lux meter was read beside the path on grass unless marked "field". Pack temperatures (assignment by Szymon): P1 22.8 → 31.0, P2 21.5 → 29.4, P3 22.5 → 24.5; P4 not measured. Packs at home (Storage, SkyRC B6AC Neo): P1 3.777 / 3.781 / 3.776 / 3.777 V (Σ 15.11, Δ 5 mV), P2 3.782 / 3.783 / 3.780 / 3.779 (Σ 15.12, Δ 4). Photographs IMG_1238–1239, 1242, 1279–1280 are DNG texture shots.

Wind from the log (`wind_from_log.py --height 1.2`): tilt 1.16° / 0.87° / 0.69° (logs 44 / 45 / 46), direction 120–138° (ESE / SE), consistency 0.89–0.99: a weak air flow of about 0.5–1 m/s from the ESE, below the anemometer's starting speed. This agrees with the phone compass (134°) and with DroneTower (120° at the surface); the forecast speed (2.7 m/s) was higher than measured. On grass T3 (course 115°) this is a headwind outbound and a tailwind on return, the opposite of S-22.

## Flights

| Flight | Run | Plan | Armed | SRC2 (local) | Illuminance [lx] (≈) | OF.Qual | Path ratio outbound / return | Drift 30 / 60 s / end [m] | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | calibration (§7.3) | grass T3 (A→B→A) | 17:39:00 | 17:40:12–17:41:54 | ~4520 (5890 → 3530) | 255 | 1.057 / 0.899 | 0.3 / 2.2 / 5.0 | |
| 2 | **E1-033** | grass T3R (B→A→B) | 17:44:20 | 17:45:32–17:47:16 | ~3010 (3210 → 2780) | 255 | 0.953 / 0.987 | 0.8 / 2.3 / 0.9 | |
| 3 | **E1-034** | grass T3 | 17:49:15 | 17:50:32–17:52:11 | ~2480 (2780 → 2200) | 255 | 0.988 / 0.913 | 1.6 / 2.3 / 3.2 | |
| 4 | **E1-035** | grass T3R | 17:56:53 | 17:58:10–17:59:49 | ~1510 (1870, 1700 → 1360) | 255 | 0.978 / 1.010 | 0.3 / 2.4 / 2.0 | |
| 5 | **E1-036** | grass T3 | 18:01:55 | 18:03:08–18:04:43 | ~969 (1110 → 861) | 255 | 0.990 / 0.910 | 0.9 / 1.3 / 3.5 | |
| 6 | **E1-037** | grass T3R | 18:06:50 | 18:08:06–18:09:41 | ~753 (861 → 646) | 255 | 0.927 / 0.974 | 1.8 / 2.9 / 2.3 | |
| 7 | **E1-038** | field T1 (A→B→A) | 18:13:58 | 18:14:40–18:16:13 | ~409 (538 → 323) | 255 | 0.898 / 0.870 | 1.7 / 2.4 / 2.7 | |
| 8 | **E1-039** | field T1R (B→A→B) | 18:17:55 | 18:18:44–18:20:22 | ~248 (323 → 194) | 255 | 0.897 / 0.899 | 2.4 / 4.4 / 0.6 | |
| 9 | **E1-040** | field T1 | 18:23:41 | 18:24:19–18:25:55 | ~118 (140, 108 → 86) | 255 | 0.900 / 0.901 | 1.4 / 2.1 / 2.1 | |
| 10 | not started | field, P4 | | | ≤ 65 (last reading 64.6 at 18:29) | 0 in the reference hover | | | abandoned per rule §G; consistent with the 17 Sep threshold |

SRC2 windows in log seconds: 195.6–297.3, 515.2–619.2, 815.5–914.2 (log 44); 168.0–267.7, 466.9–561.5, 764.6–859.0 (45); 140.0–233.7, 384.1–482.4, 719.7–815.0 (46). Lux per flight is the geometric mean of the readings before and after the SRC2 window (table above). Barometric reference drift after landing −1.1 … +0.5 m, the smallest of the campaign (stable evening air). Battery: 3793 / 3723 / 2683 mAh per pack.

## Findings

1. **Heading, not leg order, decides the grass asymmetry.** On track T3 the leg flown on course 115° (ESE) has a path ratio of 1.057, 0.988, 0.990 when it is the outbound leg and 0.987, 1.010, 0.974 when it is the return leg: mean **1.00**. The leg on course 295° (WNW) gives 0.953, 0.978, 0.927 as outbound and 0.899, 0.913, 0.910 as return: mean **0.93**. The direction effect (about 7 %) is independent of order; the order effect is about 0.03 (the second leg slightly worse in both plans). This explains S-17…S-22: every grass track so far returned on a westerly course (T1 320°, T2 320°, T3 295°), so "the return leg is worse" was "the westward leg is worse". Candidates for a direction-dependent scale: surface texture anisotropy (the meadow was cut and the swaths lie in one direction), the low sun and its shadows (sunset 18:11; during flights 1–6, 17:40–18:10, the sun was in the WSW at 3–0° elevation, so the WNW leg flew towards the low sun and the bright horizon), or a residual flow-sensor yaw misalignment interacting with the heading. The shadow hypothesis is testable by flying T3 at midday; texture anisotropy by a track rotated 90°.
2. **The ploughed field is isotropic and simply under-reads by 10 %.** Forward and reversed legs 0.87–0.90 in all six legs, no heading effect. Compared with S-22 (same track, wind 3.6–4.1 m/s: return 0.72–0.78) the calm-air field runs are much better, so on the field the wind-driven part is as large as the surface part. Final drift 0.6–2.7 m against 8.6–11.2 m on 20 Sep.
3. **The field holds `OF.Qual` 255 down to about 10 on the meter; the P4 attempt at ≤ 6 gave 0.** The three field runs flew at about 38, 23 and 11 (meter beside the path on grass); the last reading before the P4 attempt was 6.0 at 18:29 and the reference hover at about 18:30–18:35 gave `OF.Qual` 0, so the attempt was abandoned per rule §G. This is the same threshold region as on 17 Sep over grass (quality falling at ~4, 0 at ~2, meter on grass); the field at low sun gives no evidence of a different threshold. From now on illuminance is read on the surface flown, not beside the path.
4. **Calm-air baseline for the dataset.** Nine runs at 0–1.5 m/s wind, tilt 0.7–1.2° from the ESE, barometer stable: the cleanest conditions of the campaign. Grass drift 0.9–3.5 m, field 0.6–2.7 m.
5. **Detector v0.2: 7 no-event, 1 miss** (E1-034, error 5.4 m at 60 s with all indicators inside their thresholds). Campaign total after 40 runs: 2 early warnings, 12 misses, no hits, no false alarms at the threshold.
6. `error_vs_time.py` on 40 runs: grass 1.5 m/s 1.0 / 2.5 / 2.5 m at 30 / 60 / 90 s (n = 24), field 2.3 / 4.8 / 4.9 m (n = 12): the picture from S-22 holds.

## Operational notes

- Pack temperature rise: P1 +8 °C, P2 +8 °C (three grass flights each), P3 +2 °C.
- Reversed plans work as intended; the reference hover is at B, `OF.Qual` read there.
- Lux meter position was beside the path; for field runs it must be on the field.

## To do

- [ ] Heading test at midday on T3 (sun high, no long shadows) to separate the sun-shadow hypothesis from texture anisotropy
- [ ] A grass track rotated by about 90° (course ~25° / 205°), flown both ways, to test texture anisotropy
- [ ] Field in daylight and calm air (SURF2 baseline without wind and without dusk)
- [ ] Still open: grass 1.5 m ×3 and field 1.5 m ×3 in daylight, wind ≤ 2 m/s; VEL075 ×2 in daylight
- [ ] Add "read illuminance on the surface flown" to `procedures/day-procedure-E1.md`
