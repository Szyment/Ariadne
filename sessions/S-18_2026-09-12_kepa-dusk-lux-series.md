# S-18: 12 Sep 2026 evening, the same meadow, illuminance descent series (dusk)

Logs: `log_31_2026-9-12-18-50-42.bin` (pack 1, flights 7–9) · `log_32_2026-9-12-19-05-18.bin` (pack 2, flights 10–12). Configuration: `ariadne_v2_12sep2026_1642.params` (diff relative to `1113`: only automatic values, i.e. reference pressure, gyroscope offsets, counters, MAVLink streams, plus `MIS_TOTAL` 1 → 6 after uploading plan v2; estimator unchanged, §0 preserved). Plan: `missions/E1_grass_T1_3m_LAND.plan` (A 30 s → B 3 s → A 30 s → home → LAND), take-off from the path as in S-17. Sunset 18:58. Photos and screenshots: `build-log/photos/2026-09-12/session-2-dusk/`. DroneTower check-in (RPA55): 18:44–20:44, 50 m AGL, radius 100 m, 52°08'18"N 21°09'40"E (screenshot `IMG_1980.PNG`), made shortly after the first take-off (flight 7 from 18:39); check-out after the session, "finished on time". Session calibration flight: shared with S-17 (`ARIADNE_KAL_20260912_29`), configuration unchanged.

In practice this is **the illuminance descent series from protocol §3.2** (E1 provides for it "at the most favourable remaining configuration"): six runs in the same SURF/ALT/VEL cell, with illuminance falling from ~170 to ~30 lx.

## Conditions

| Time | Wind GM816 AVG [m/s] | Air temp. | Lux GM1010 | Infrared thermometer | Notes |
|---|---|---|---|---|---|
| 18:33 | 0.0 | 21.9 °C | 279.0 | surface 13.1 °C | before flight 7; IMGW forecast: 1.6 m/s from 326°, gusts 4.2, Kp 0.7, 15.6 °C, 1021.4 hPa, clear sky |
| 18:43 | — | — | 188.7 | — | after flight 7 / before 8 |
| 18:47 | — | — | 141.1 | — | after 8 / before 9 |
| 18:50–18:51 | 0.0 | 14.3 °C | 88.9 | pack 25.0 °C | after 9, pack change |
| 18:53 | — | — | 72.8 | — | before 10 |
| 18:57 | — | — | 58.5 | — | after 10 / before 11 |
| 19:00–19:01 | — | — | 35.9 (grass), 38.8 (gravel) | — | after 11 / before 12 |
| 19:05–19:07 | 0.0 | 10.7 °C | 23.8 | pack 24.1 °C, surface 8.9 °C | after 12 |

Wind practically zero throughout the session (anemometer below its starting threshold). From the log (`analysis/results/wind_20260912.md`): a constant tilt of about 0.6° from SW (210–265°) at different courses, i.e. a weak wind of about 0.3–0.5 m/s, below the GM816 threshold; gustiness p95 1.1–2.1° versus 2.4–3.3° during the day. Surface as in S-17: fresh grass, dry, not mown. Illuminance fell 279 → 24 lx in 32 min (on average −7.5 %/min, consistent with −7.27 %/min from S-08).

## Results (`analysis/results/S-18_2026-09-12_drift_analysis.txt`)

Absolute time from GPS in the log. Lux measured before and after each flight (column "Lux before → after"); the run value = the geometric mean of the pair.

| Flight | Run | Log | SRC2 window [s] | Local time | Lux before → after (mean) | Outbound | Return | Whole | Drift 15/30/60 s [m] | Final drift [m] | GNSS sat / HDOP | CTUN.Alt after flight |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | E1-006 | 31 | 176–270 | 18:39:29–18:41:02 | 279 → 189 (230) | 0.951 | 0.963 | 0.957 | 0.90 / 1.01 / 3.02 | 2.20 | 18–22 / 0.65–0.78 | −0.32 |
| 8 | E1-007 | 31 | 453–531 | 18:44:05–18:45:24 | 189 → 141 (163) | 0.932 | 0.939 | 0.935 | 0.59 / 3.06 / 2.72 | 0.99 | 25–27 / 0.52–0.58 | +0.08 |
| 9 | E1-008 | 31 | 675–770 | 18:47:47–18:49:22 | 141 → 89 (112) | 0.918 | 0.957 | 0.937 | 0.37 / 0.14 / 2.92 | 0.96 | 27–29 / 0.50–0.56 | −0.42 |
| 10 | E1-009 | 32 | 145–233 | 18:54:32–18:55:59 | 73 → 59 (65) | 0.967 | 0.958 | 0.963 | 0.11 / 0.39 / 1.76 | 0.33 | 29–30 / 0.48–0.51 | −0.15 |
| 11 | E1-010 | 32 | 375–466 | 18:58:22–18:59:53 | 59 → 37 (47) | 0.956 | 0.972 | 0.964 | 0.15 / 0.76 / 1.79 | 0.97 | 29–30 / 0.48–0.51 | +0.01 |
| 12 | E1-011 | 32 | 617–712 | 19:02:24–19:03:59 | 37 → 24 (30) | 0.969 | 0.905 | 0.936 | 0.22 / 0.41 / 1.23 | 2.71 | 28–31 / 0.47–0.52 | −0.53 |

`OF.Qual` = 255 in all six, rangefinder median 3.0 m, max 3.20 m.

## Findings

1. **Down to ~30 lx (pair 37 → 24) over grass, 3.0 m, 1.5 m/s, optical flow shows no degradation.** Path ratio 0.935–0.964 (S-17 during the day: 0.944–0.974), final drift 0.3–2.7 m, `OF.Qual` without any drop. The threshold from §2.1.1 lies below ~25 lx; to be found in the next dusk session (start later, or longer after sunset).
2. **Without wind, the leg asymmetry disappears.** Outbound/return: 0.951/0.963, 0.932/0.939, 0.918/0.957, 0.967/0.958, 0.956/0.972, 0.969/0.905. Differences in both directions, with no systematic direction. Supports the hypothesis from S-16 that the asymmetry depends on wind and not on track geometry.
3. Altitude reference drift (`CTUN.Alt` after the flight) above 0.3 m in three of six flights (−0.32, −0.42, −0.53), slightly more than during the day. To be observed; a possible link with barometer temperature while the air temperature falls quickly (21.9 → 10.7 °C).
4. Plan v2 (home + LAND in the mission) worked: modes in the log Auto → Loiter → Land without manual piloting.
5. Flight 7: GNSS 18–22 satellites, HDOP up to 0.78, still far from the §8 threshold (10 / PDOP 2.0).

## §8 decision (preliminary)

E1-006…E1-011: **accepted**. Wind 0, GNSS OK, logs complete, no interventions. Criterion "lux change > 30 % during the run": the before/after pairs also cover the breaks between flights (3–10 min), so the change within the 90-second window itself is ~11 % at −7.5 %/min, below the threshold. Between runs the change is intentional (descent series), so each run receives its own LUX value (geometric mean of the pair), not a cell. In the index the code `LUXd` + value.

## Packs after the session

P1: 3.81/3.81/3.81/3.81 V, 40 %. P2: 3.80/3.81/3.81/3.80 V, 38 %. Again exactly the storage level after 3 flights.

## To do

- [ ] Next dusk session: start ~10 min after sunset to get below 20 lx; lux before and after each flight as today.
- [ ] Photos `build-log/photos/2026-09-12/session-1-day` and `_2` to `build-log/photos/2026-09-12/` (script).
