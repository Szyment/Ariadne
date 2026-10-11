# S-24: 4 Oct 2026 early afternoon, Kępa Okrzewska: overcast midday (LUX2), heading test on T3 and on the rotated track T4, field in daylight, first daylight runs at 1.5 m

Logs: `log_47_2026-10-4-13-51-06.bin` (pack P1, flights 1–3, grass; log start 13:33:56) · `log_48_2026-10-4-14-06-06.bin` (P2, flights 4–6, grass; 13:51:57) · `log_49_2026-10-4-14-11-36.bin` (power-up before the plan was changed, no arming) · `log_50_2026-10-4-14-28-48.bin` (P3, flights 7–9, field; 14:12:04) · `log_51_2026-10-4-14-45-36.bin` (P4, flights 10–11, grass at 1.5 m; 14:31:46). Absolute times from GPS time in the logs; the log file name carries the time the log was closed. Configuration `ariadne_v2_17sep2026_1705.params` (no change; §0 preserved; `FENCE_RADIUS` 120, `WP_SPD` 1.5 in all logs). Photos: `build-log/photos/2026-10-04/` (EXIF local time; sky and surface textures as DNG: IMG_1414–1418 grass and sky at 13:35, IMG_1468–1473 field at 14:31, IMG_1487–1489 overcast sky at 14:47; two illuminance readings are in DNG frames, read by Szymon: IMG_1418 2826 fc, IMG_1470 1790 fc). Results: `analysis/results/S-24_2026-10-04_drift_analysis.txt`, `detector_v0.2_20261004.csv`, `error_vs_time.*` (49 runs), `wind_20260912.md` (S-24 section), CSV in `data/`.

Plans: `E1_grass_T3_3m_LAND` / `E1_grass_T3R_3m_LAND` (course 115° / 295°), **new track T4** `E1_grass_T4_3m_LAND` / `E1_grass_T4R_3m_LAND` (A 52.1375811, 21.1607336; B 52.1379096, 21.1609832; course 25° / 205°, 40.3 m, A 72 m and B 32 m from home; placed on 4 Oct, rotated by about 90° to T3 to test texture anisotropy), `E1_field_T1_3m_LAND` / `E1_field_T1R_3m_LAND` (137° / 317°), `E1_grass_T3_1.5m_LAND` (same A/B as T3, 1.5 m terrain frame). The plan flown in each flight was verified from the hover position at the switch (distance to A or B below 0.3 m in every case).

Purpose: (1) repeat the S-23 heading test on T3 with the sun high (sun-shadow hypothesis); (2) fly a track rotated by 90° (texture-anisotropy hypothesis); (3) the field in daylight and light wind (SURF2 baseline); (4) the first daylight runs at 1.5 m (ALT15 without the LUX confound of S-21).

Sky: full overcast (altostratus) for the whole session, the sun breaking through in places from about 14:40; the DroneTower forecast (`IMG_1405.PNG`, 12:15, hour 12–13: Kp 2.7, 17.7 °C, 1026.5 hPa, humidity 74 %, surface wind 2.3 m/s from W 288°, at 100 m 2.9 m/s from 286°, gusts 4.7, cloud cover 1/8, sunset 18:06; `IMG_1420.PNG` at 13:38: Kp 3.3, otherwise the same) did not match the sky. Phone compass at 13:33 (`IMG_1409.PNG`): 148° SE. Cell LUX2.

*Illuminance in lux, converted from the GM1010 foot-candle readings (× 10.764, annex D §8); display values in parentheses.*

## Conditions (per moment; local time from EXIF)

| Time | Moment | Illuminance [lx] (GM1010 display, fc) | Anemometer GM816 [m/s] (air temp.) | Infrared thermometer |
|---|---|---|---|---|
| 13:32–13:36 | arrival, path | 32 800 (3043), 30 400 (2826, IMG_1418 DNG, 13:36) | 1.3 · 1.6 · 1.5 · 1.6 (22.0–20.2 °C) | grass 20.3; P1 before 23.4 (IMG_1406) |
| 13:40–13:41 | flight 1 / before 2 | 22 300 (2070) | 1.1 (22.6) | |
| 13:46 | after flight 2 (aborted) | 16 400 (1521) | 0.0 (22.5) | |
| 13:50–13:51 | after flight 3, pack change P1 → P2 | 12 800 (1190) | 0.7 · 0.9 (21.1–20.7) | P2 before 21.9 (IMG_1428); P1 after 29.9 (IMG_1429, 13:51:48; log 47 closed 13:51:06) |
| 13:52 | log 48 started | 12 800 (1188) | 1.1 · 1.4 · 1.7 · 1.2 (21.1–20.5) | |
| 13:57–13:58 | after flight 4 | 12 000 (1111) | 0.0 (20.7) | |
| 14:01–14:02 | after flight 5 | 12 900, 13 000 (1196, 1206) | 0.6 · 0.0 · 1.0 · 1.2 (20.3–19.4) | |
| 14:06–14:08 | pack change P2 → P3 | 12 400 (1149) | 0.7 · 0.9 · 1.1 · 1.2 · 0.8 (19.6–19.2) | P3 before 21.2 (IMG_1443); P2 after 25.8 (IMG_1444, 14:06:45; log 48 closed 14:06:06) |
| 14:11–14:12 | log 50 started (field) | 12 900 (1194) | 1.3 · 1.0 (19.5–19.2) | |
| 14:15 | before flight 7 | 13 800 (1285) | 0.8 · 0.9 (19.7–19.6) | |
| 14:20 | after flight 7 | 14 300 (1329) | 1.0 · 1.2 (20.0–19.6) | |
| 14:24–14:25 | after flight 8 | 12 100, 13 600 (1126, 1268) | 0.0 (19.9) | |
| 14:27–14:32 | after flight 9, pack change P3 → P4 | 15 600 (1446), 19 300 (1790, IMG_1470 DNG, 14:32) | 0.0 (20.1) | P4 before 20.2 (IMG_1465, 14:28:13, photo upside down); P3 after 26.0 (IMG_1466, 14:30:31); field surface 18.1 (IMG_1467) |
| 14:44–14:45 | after flight 11 | 33 600, 34 900, 35 000 (3122, 3241, 3250; the last two rotated, ±10) | 1.2 · 1.7 · 1.4 · 1.8 · 1.6 · 0.9 · 0.7 · 0.8 (21.9–20.6) | grass 14.6 (IMG_1485); P4 after 23.2 (IMG_1486, 14:46:23; log 51 closed 14:45:36) |

The lux meter was read on grass beside the path for every reading, including the field block (readings 14:11–14:27 taken on the grass beside the field path), so the field surface itself again has no reading. Pack temperatures: P1 23.4 → 29.9, P2 21.9 → 25.8, P3 21.2 → 26.0, P4 20.2 → 23.2. Packs at home (Storage, SkyRC B6AC Neo, 18:24–18:26): P1 3.783 / 3.784 / 3.780 / 3.779 V (Σ 15.13, Δ 5 mV), P2 3.796 / 3.797 / 3.794 / 3.793 (Σ 15.18, Δ 4), P3 3.797 / 3.799 / 3.798 / 3.794 (Σ 15.19, Δ 5), P4 3.811 / 3.815 / 3.811 / 3.810 (Σ 15.25, Δ 5).

Wind from the log (`wind_from_log.py --height 1.2`): tilt 1.64° / 1.56° / 1.63° (logs 47 / 48 / 50), direction 335–352° (NNW / N), consistency 0.98–0.99; no hover window in log 51 (flights at 1.5 m). About 1.5–2.5 m/s at flight altitude against 0–1.8 m/s on the anemometer at 2 m; the DroneTower forecast direction (W) was 50–60° off. Relative to the tracks: T3 (115°/295°) and T4 (25°/205°) are 50–70° off the wind axis, with a tailwind component on the 115° and 205° legs and a headwind component on the 295° and 25° legs; the field T1 lies close to the wind axis (headwind on 317°, tailwind on 137°).

## Flights

| Flight | Run | Plan | Armed | SRC2 (local) | Illuminance [lx] (≈, display fc) | OF.Qual | Path ratio outbound / return | Drift 30 / 60 s / end [m] | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | calibration (§7.3) | grass T3 (A→B→A) | — (no arming event in the log; Auto from 13:36:18) | 13:37:33–13:39:09 | ~26 000 (2826 → 2070) | 255 | 0.987 / 0.934 | 2.2 / 3.0 / 3.4 | |
| 2 | test, aborted | grass T3R (B→A→B) | 13:41:33 | 13:43:00–13:44:07 (67 s) | ~19 000 | 255 | 0.948 / 0.880 (return 19.7 m) | 1.4 / 1.7 / 1.4 | the pilot switched the flight mode by accident on the return leg; 4 s re-entry into SRC2 at 13:44:13; outside the dataset |
| 3 | **E1-041** | grass T3R | 13:46:13 | 13:47:42–13:49:21 | ~14 500 (1521 → 1190) | 255 | 0.974 / 0.925 | 0.7 / 0.4 / 2.2 | |
| 4 | **E1-042** | grass T3 | 13:53:01 | 13:54:30–13:56:03 | ~12 400 (1188 → 1111) | 255 | 0.969 / 1.009 | 0.9 / 2.9 / 2.1 | |
| 5 | **E1-043** | grass T4 (A→B→A, 25°) | 13:58:01 | 13:59:23–14:00:59 | ~12 400 (1111 → 1196) | 255 | 0.985 / 0.949 | 2.1 / 2.5 / 2.2 | first run on T4 |
| 6 | **E1-044** | grass T4R (B→A→B, 205°) | 14:02:30 | 14:03:26–14:05:02 | ~12 700 (1206 → 1149) | 255 | 0.928 / 0.981 | 1.6 / 3.5 / 2.0 | |
| 7 | **E1-045** | field T1 (A→B→A, 137°) | 14:15:48 | 14:16:40–14:18:15 | ~14 100 (1285 → 1329) | 255 | 0.921 / 0.930 | 2.2 / 3.6 / 1.3 | before it a false start 14:13:06–14:14:16 (Auto with the aircraft in Land mode instead of arming; no SRC2) |
| 8 | **E1-046** | field T1R (B→A→B, 317°) | 14:20:39 | 14:21:43–14:23:16 | ~13 200 (1329 → 1126) | 255 | 0.968 / 0.850 | 1.8 / 3.5 / 4.4 | |
| 9 | **E1-047** | field T1 | 14:25:05 | 14:25:52–14:27:32 | ~14 600 (1268 → 1446) | 255 | 0.899 / 0.925 | 3.0 / 5.8 / 2.4 | |
| 10 | **E1-048** | grass T3 **1.5 m** | — (no arming event in the log; Auto from 14:34:14) | 14:36:40–14:38:06 | ~25 000 (1790 → 3122, sun breaking through) | 255 | 0.892 / 0.870 | 2.0 / 4.9 / 1.1 | rangefinder median 1.49 m; first Auto 14:34:14–14:35:33 interrupted by the pilot (QGC showed 0.3 m: altitude relative to home, point A lies about 1.2 m below the path), climb in Loiter, 4 s SRC2 test at 14:35:46, then the run |
| 11 | **E1-049** | grass T3 1.5 m | 14:40:34 | 14:42:06–14:43:42 | ~33 600 (3122 at 14:44) | 255 | 0.880 / 0.911 | 2.9 / 6.8 / 3.3 | rangefinder median 1.50 m |

SRC2 windows in log seconds: 216.5–313.0, 543.8–611.0 (aborted), 616.4–621.4 (4 s), 826.3–924.7 (log 47); 153.2–247.0, 446.7–543.0, 689.3–785.3 (48); 276.7–371.7, 579.9–672.5, 828.5–928.3 (50); 240.5–245.5 (4 s), 294.7–379.8, 620.5–716.7 (51). CSV: `ARIADNE_E1_041…049_20261004_*.csv`, `ARIADNE_KAL_20261004_47.csv`. Illuminance per run = geometric mean of the readings before and after the window. Barometric reference drift after landing +0.4 / +0.9 / +0.7 m (log 47), +0.0 / +0.3 / +0.3 (48), −0.1 / +0.3 / +0.7 / +1.0 (50), −0.0 / +0.0 (51). Battery per pack: 3590 / 3200 / 3065 / 2794 mAh, minimum under load 14.61–14.70 V; P4 ended after two runs for lack of time.

## Findings

1. **The grass asymmetry of S-23 does not reproduce at midday; across three sessions the leg with a tailwind component is the lower one.** On T3 today the 115° leg reads 0.987, 0.925, 0.969 (mean 0.96) and the 295° leg 0.934, 0.974, 1.009 (0.97): no heading effect with the sun high and the wind from the NNW, against 1.00 / 0.93 at dusk on 2 Oct with the wind from the ESE. On the rotated T4 the 25° leg (headwind component) reads 0.985, 0.981 and the 205° leg (tailwind component) 0.949, 0.928: a difference of 0.04 in the direction of the wind, not of the swaths. On the field the 317° leg (headwind) reads 0.930, 0.968, 0.925 and the 137° leg (tailwind) 0.921, 0.850, 0.899. Put together with S-22 (wind SW 3.5–4.5 m/s, return legs on 295° and 317° at 0.72–0.96) and S-23 (wind ESE 0.5–1 m/s, 295° leg at 0.93), the leg flown with the wind from behind has the lower path ratio in every session in which the wind had a component along the track, by 0.04–0.10 depending on wind strength. The sun-shadow and texture-anisotropy hypotheses of S-23 are not needed. Candidate mechanism: the airframe attitude needed to hold the commanded ground speed differs between the two legs, and the flow scale (tilt compensation and the rangefinder geometry) does not remove it fully. Next test: both directions on one track on a windier day, with the wind along the track, and the same at 0.75 m/s.
2. **Altitude 1.5 m over grass in daylight: scale 8 % lower than at 3 m, drift at 60 s the largest of the grass runs.** E1-048 and E1-049 give 0.892 / 0.870 and 0.880 / 0.911 against 0.93–1.01 on the same track at 3 m an hour earlier, both legs, with `OF.Qual` 255 and the rangefinder at 1.49–1.50 m; drift 4.9 and 6.8 m at 60 s (grass at 3 m today: 0.4–3.5 m). This confirms the direction of S-21 (E1-022: return leg 0.73 at dusk) and separates the altitude effect from the light: at 1.5 m in daylight the under-reading is about 8 %, at dusk it was 27 %. Candidate: the grass height (0.2–0.3 m) is a larger fraction of the range at 1.5 m, so the rangefinder-to-texture distance and the flow-rate scale disagree more. Operational: at 1.5 m the QGC altitude readout is relative to home and shows 0.3 m over point A, which is about 1.2 m lower than the path; the plan was correct, the rangefinder is the reference.
3. **The field in daylight and light wind sits between the two earlier field sessions.** Path ratios 0.85–0.97, final drift 1.3–4.4 m, 60 s drift 3.5–5.8 m, against 0.87–0.90 and 0.6–2.7 m in calm dusk (S-23) and 0.72–0.78 and 8.6–11.2 m at 3.5–4.5 m/s (S-22). The field is not isotropic when the wind is along the track (finding 1); the 10 % under-reading of S-23 is the calm-air floor.
4. **Overcast midday at 12–15 klx behaves as full daylight for the sensor**, as on 20 Sep: `OF.Qual` 255 in every run.
5. **Detector v0.2: 6 no-event, 4 misses** (E1-046 and E1-047 on the field, E1-048 and E1-049 at 1.5 m: error above 5 m with every indicator inside its threshold). Campaign total after 49 runs: 2 early warnings, 16 misses, no hits, no false alarms. The two regimes that produce silent drift, the field and 1.5 m, are both scale errors without an onboard signature.
6. `error_vs_time.py` on 49 runs: grass 1.5 m/s 1.1 / 2.8 / 2.5 m at 30 / 60 / 90 s (n = 30), field 2.2 / 4.7 / 4.5 m (n = 15), grass 0.75 m/s 1.0 / 2.4 / 2.5 m (n = 4).

## Operational notes

- Flight 2 was aborted by an accidental flight-mode switch on the transmitter; the run is logged as a test. Log 49 is a power-up before the plan was changed, without a flight. The first Auto in log 50 was a false start (Land mode selected instead of arming).
- The first 1.5 m attempt (log 51) was interrupted because QGC showed 0.3 m (altitude relative to home); the rangefinder held 1.49 m.
- Only two runs on P4 (time), so the third 1.5 m run and the third pair on T4 are open.
- Pack temperature rise: P1 +6.5 °C (three grass flights), P2 +3.9, P3 +4.8, P4 +3.0.

## To do

- [ ] Both directions on one track on a windier day with the wind along the track (finding 1); the same at 0.75 m/s
- [ ] Third run at 1.5 m over grass in daylight; field 1.5 m ×3
- [ ] Third pair on T4 (T4, T4R) to complete three per direction
- [ ] VEL075 ×2 in daylight (still open from S-22)
- [x] GM1010: side-by-side FC/Lux comparison in full daylight (S-25, annex D §8); read the field surface, not the grass beside the path (open)
