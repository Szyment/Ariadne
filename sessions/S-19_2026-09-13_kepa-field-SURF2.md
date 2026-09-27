# S-19: 13 Sep 2026, the same meadow, SURF2 cell (ploughed field), two directions relative to the wind

Logs: `log_33_2026-9-13-12-22-06.bin` (pack 1, flights 1–3) · `log_34_2026-9-13-12-40-38.bin` (pack 2, flights 4–6). Configuration: `ariadne_v2_13sep2026_1100.params` (the only change relative to 12 Sep: `FENCE_RADIUS` 70 → 90, the geofence does not affect the estimator, §0 preserved). Photos and screenshots: `build-log/photos/2026-09-13/session-1-day/`. DroneTower check-in at the take-off point (`IMG_0341.PNG` forecast: surface wind 2.7 m/s from 190°, gusts 5.3, 16.1 °C, 1020.5 hPa, cloud cover 1/8).

## Site

Take-off (home) from the path 52.1377186 / 21.1618933 (62 m SE of the take-off point of 12 Sep). Surface SURF2: ploughed field, clods of soil with stubble remains and tufts of grass (not clean sand), `IMG_0351`, `IMG_0404`. Advisor's assessment: the site is safe.

Two plans, both: home → A (30 s, RC7 Mid after 20 s) → B (3 s) → A (30 s, RC7 Low) → home 3 m → LAND, 41.5 m, 3.0 m, 1.5 m/s:
- `E1_field_T1_3m_LAND.plan`: A 52.1376191 / 21.1614674, B 52.1373449 / 21.1618800, course A→B **137°** (upwind on the outbound leg, about 1 m/s head-on + 2 m/s crosswind)
- `E1_field_T2_3m_LAND.plan`: A 52.1372714 / 21.1612269, B 52.1376149 / 21.1614645, course A→B **23°** (downwind on the outbound leg, as on 12 Sep)

## Conditions (measurements per flight, between flights)

| Time | After flight | Lux GM1010 | Wind GM816 [m/s] | Temp. GM816 | Infrared thermometer | Notes |
|---|---|---|---|---|---|---|
| 12:03–12:06 | before 1 | 8323, 8531, 8676 | 3.3 / 4.1 | 21.9 / 21.8 °C | soil 23.5 °C (avg 24.0) | DNG photos |
| 12:12–12:13 | 1 (cal.) | 19 790, 20 550 | 2.4 / 2.5 | 28.6 / 27.7 °C | — | sun through cirrus |
| 12:16–12:17 | 2 | 17 740, 15 490 | 2.9 / 3.7 / 4.0 / 3.1 | 28.7 / 29.4 / 29.4 / 27.3 °C (in the sun) | — | |
| 12:21–12:23 | 3 | 5771, 5194 | 1.6 / 2.1 / 2.9 | 28.3 / 27.2 / 27.0 °C | soil 13.6 °C (avg 13.7); pack 1 after 3 flights 17.7 °C (avg 16.5) / 18.0 °C (avg 16.8); pack 2 before flights 15.9 °C (avg 16.9) | full sun; pack change |
| 12:24 | before 4 | 6725 | 2.3 / 4.0 / 4.1 / 3.3 | | | |
| 12:30 | 4 | 5119, 5118, 4900 | 2.3 / 3.2 / 2.4 | | | |
| 12:35 | 5 | 7145, 7524 | 3.9 / 3.7 / 4.2 / 3.8 | 24.2 / 24.2 / 23.9 / 23.8 °C | | |
| 12:39–12:41 | 6 | 6573, 6914, 8281 | 3.2 / 4.1 | 27.7 / 25.1 °C | pack 2 after 3 flights 27.0 °C (avg 26.1) | |

Lux by time: 8323, 8531, 8676 → 19 790, 20 550 → 17 740, 15 490 → 5771, 5194 → 6725 → 5119, 5118, 4900 → 7145, 7524 → 6573, 6914, 8281 lx. Range 4.9–20.6 klx, variable cloud cover (cirrus); flights 1–2 at ~15–20 klx, flights 3–6 at 5–8 klx. Wind from the anemometer 1.6–4.2 m/s (before flight 1: 3.3 / 4.1), direction per DroneTower 190–205° (S/SSW). Wind from log (`wind_from_log.py`, log 33, window 861–878 s): tilt **3.21°**, direction **209° (SSW)**, p95 6.0°, consistent with DroneTower; more than twice the value of 12 Sep (1.1–1.5°). Hover at A in the logs: 3–5° of tilt (E1-015), versus 0–1.6° the day before.

## Flights

| Flight | Run | Plan / course | SRC2 window [log s] | Path ratio outbound / return | Drift 30 s / 60 s / final [m] | OF.Qual | Notes |
|---|---|---|---|---|---|---|---|
| 1 | session calibration (§7.3, outside the dataset) | sand / 137° | 182.2–277.8 | 0.842 / 0.916 | 2.6 / 7.6 / 3.0 | 255 | |
| 2 | **E1-012** | sand / 137° | 430.5–522.1 | 0.908 / 0.879 | 2.0 / 2.9 / 2.2 | 255 | |
| 3 | **E1-013** | sand / 137° | 719.7–815.9 | 0.915 / 0.859 | 0.6 / 3.8 / 3.3 | 255 | |
| 4 | **E1-014** | windS / 23° | 199.0–297.2 | 0.846 / 0.951 | 5.2 / 9.5 / 5.6 | 255 | |
| 5 | **E1-015** | windS / 23° | 487.8–585.1 | 0.845 / 0.961 | 5.2 / 10.1 / 6.2 | 255 | |
| 6 | **E1-016** | windS / 23° | 788.7–885.2 | 0.857 / 0.930 | 5.5 / 8.9 / 4.4 | 255 | |

Details: `analysis/results/S-19_2026-09-13_drift_analysis.txt`. CSV per run: `data/ARIADNE_E1_012…016_20260913_LUX1-SURF2-ALT3-VEL15.csv` (v0.2, with XKF5).

## Findings

1. **SURF2 gives a clearly larger path under-estimation than grass at the same image quality.** Whole-run path ratio 0.877–0.899 (SURF1 on 12 Sep: 0.93–0.98). `OF.Qual` 255 throughout, optical-flow measurement residuals and `ePos` within norm. The sensor "sees well", and the estimate drifts away by 10 m in 60 s (E1-014, E1-015). This is exactly the silent failure case from RQ1, recorded under controlled conditions.
2. **The leg asymmetry depends on the wind direction, confirmed in three configurations.** The leg flown **downwind** has the lower path ratio: 12 Sep (NW, downwind outbound): outbound 0.92–0.975 < return 0.95–0.99. 13 Sep course 137° (upwind outbound): outbound 0.91 > return 0.86–0.88. 13 Sep course 23° (downwind outbound): outbound 0.85 < return 0.93–0.96. Mechanism to be described (candidate: coupling of airframe tilt with the flow when flying downwind, when the drone tilts less than the compensation assumes).
3. **Final drift 2.2–6.2 m**, in E1-014/015 above 5 m; under §8 it remains to be decided whether the drift threshold applies to the end or to the maximum (max 10 m).
4. **Altitude reference drift (`CTUN.Alt` after landing) +1.2 … +4.8 m**, growing with each flight in the log (2.3 → 3.9 → 4.9 m; 1.4 → 2.6 → 4.1 m), as the aircraft warms up in the sun (anemometer 21.8 → 29.4 °C). Flight in the terrain frame is unaffected (`RFND` median 3.0 m), but this is an argument against any use of the barometer as a reference. On the evening of 12 Sep it was −0.5 m while cooling, the direction consistent with temperature.
5. Detector v0.2: 0 warnings, 3 misses (E1-014…016, error > 5 m after ~30 s). All four onboard indicators at baseline. `ePos` max 0.21–0.24 (12 Sep: ≤ 0.11), slightly higher, still below the threshold.

## §8 decision (preliminary)

E1-012…016 accepted into the dataset, cell LUX1-SURF2-ALT3-VEL15, with an annotation of the direction relative to the wind (137° upwind / 23° downwind). Wind 1.6–4.2 m/s within the session limits. Lux sunny per block, no flag. Drift > 5 m in E1-014/015: keep in the dataset, because this is a phenomenon and not a fault; refine the §8 criterion (end versus maximum).

## To do

- `build-log/photos/2026-09-13/session-1-day/` → `build-log/photos/2026-09-13/` by script, DNG outside synchronisation.
- `flight-logs/INDEX.md`: rows E1-012…016 (added).
- Asymmetry mechanism: compare airframe tilt and `flow − body` in both legs of E1-014 versus E1-012.
- Packs: cell voltages after charging to `preflight.md`.
