# S-26: 17 Oct 2026 midday and dusk, Kępa Okrzewska: ploughed field at 1.5 m in sunlight (eight runs) and at dusk (three), grass at 1.5 m down to the illuminance threshold (two), 0.75 m/s in sunlight (one)

Logs: `log_56_2026-10-17-13-53-08.bin` (pack P1, field T1 at 1.5 m; boot 13:36:38, log start 13:40:00 in flight) · `log_57_2026-10-17-14-09-48.bin` (P2, grass T3 at 3 m, VEL075 plan; boot 13:54:02, log start 13:57:20 in flight) · `log_58_2026-10-17-14-26-00.bin` (P3, field T1 at 1.5 m; boot 14:10:31, log start 14:12:06 in flight) · `log_59_2026-10-17-17-45-50.bin` (P1 recharged, field T1 at 1.5 m at dusk; boot 17:34:31, log start 17:35:51 in flight) · `log_60_2026-10-17-17-59-04.bin` (P4, grass T3 at 1.5 m at dusk; boot 17:46:58, log start 17:48:58). Absolute times from GPS time in the logs; the log file name carries the time the log was closed. Configuration `ariadne_v2_17sep2026_1705.params` (no change; `FS_EKF_ACTION` 2, `EK3_SRC2_VELXY` 5, `EK3_SRC2_POSZ` 1, `EK3_RNG_USE_HGT` 70, `FLOW_FXSCALER/FYSCALER` 0, `WP_SPD` 1.5, `FENCE_RADIUS` 120 in all logs). Photos: `build-log/photos/2026-10-17/` (EXIF local time; DNG: IMG_1968–1978 sky, grass and field at 13:32–13:33, IMG_1985 at 13:37, IMG_1998–2001 at 13:46, IMG_2017 at 13:51, IMG_2028–2032 at 13:58, IMG_2087–2090 at 17:32, IMG_2118–2123 at 17:49). Results: `analysis/results/S-26_2026-10-17_drift_analysis.txt`, `detector_v0.2_20261017.csv`, `error_vs_time.*` (75 runs), `scale_observable.csv` (75 runs), `wind_20260912.md` (S-26 section), CSV in `data/`.

Plans: `E1_field_T1_1.5m_LAND` (field T1: A 52.1376191, 21.1614674; B 52.1373449, 21.1618800; 137°; 1.5 m terrain frame; first flown today), `E1_grass_T3_3m_VEL075_LAND` (T3: A 52.1375457, 21.1603449; B 52.1373898, 21.1608774; 115°; `DO_CHANGE_SPEED` 0.75 m/s as the first command), `E1_grass_T3_1.5m_LAND`. The plan flown in each flight was verified from the hover position at the switch (distance to A below 0.2 m in every case) and from the `Reached command` messages.

Purpose: (1) the field at 1.5 m, the last empty cell of the E1 altitude axis (three runs planned, eight flown); (2) 0.75 m/s in daylight, open since S-22 (two planned, one flown at 0.75 m/s, see operational notes); (3) the field and the grass at 1.5 m at dusk, down to the illuminance threshold.

Sky: altocumulus with gaps at midday, the sun breaking through for most of the session, thin cloud over the sun 14:19–14:25; clear sky with a few clouds in the evening; sunset 17:37. DroneTower forecast (`IMG_2005.PNG`, 13:49): Kp 0.0, 7.2 °C, 1019.1 hPa, humidity 95 %, dew point 6.4 °C, surface wind 1.1 m/s from SE 114°, at 100 m 1.4 m/s from E 109°, gusts 2.8, cloud cover 1/8, cloud base 200 m, visibility 20 km, sunrise 07:03, sunset 17:37. Cells LUX1 (full daylight, 27–97 klx) at midday and LUXd (dusk, 54–600 lx) in the evening.

*Illuminance in lux, converted from the GM1010 foot-candle readings (× 10.764, annex D §8); display values in parentheses; the one reading taken in Lux mode is marked.*

## Conditions (per moment; local time from EXIF)

| Time | Moment | Illuminance [lx] (GM1010 display) | Anemometer GM816 [m/s] (air temp.) | Infrared thermometer |
|---|---|---|---|---|
| 13:35–13:38 | arrival, field | 42 400, 42 400 (3940, 3939); 56 400, 58 800 (5236, 5462) | 0.0 (16.3) | P1 before 18.5 (IMG_1979); field surface 11.4 (IMG_1987) |
| 13:42–13:43 | between flights 1 and 2 | 50 300, 52 100, 54 200, 55 000, 56 000, 56 000, 69 100 (4674, 4837, 5037, 5106, 5198, 5206, 6416) | 0.0 (18.6) | |
| 13:45–13:46 | between flights 2 and 3 | 67 600 (6282); 35 500, 36 100 (3301, 3356; thin cloud) | 0.0 (19.3) | |
| 13:49–13:51 | between flights 3 and 4 and during flight 4 | 46 000, 47 700 (4273, 4435); 69 900, 71 000, 72 400 (6493, 6599, 6724); during the run 93 000, 96 600, 96 100 (8637, 8977, 8928), 80 800 (Lux X10 8081), 88 800 (8251 fc) | 0.0 (20.3) | |
| 13:53–13:54 | after flight 4, pack change P1 → P2 | | | P2 before 28.7 (IMG_2018); P1 after 35.5 (IMG_2019, 13:53:43; log 56 closed 13:53:08); field surface 22.6 (IMG_2020) |
| 13:57–13:58 | grass T3, before flight 5 | 91 900, 91 600, 92 500 (8540, 8507, 8589) | 0.0 (21.4) | grass 13.6 (IMG_2023) |
| 14:00–14:03 | between flights 5 and 6 | 67 300, 67 800 (6249, 6299); 79 000, 79 200 (7335, 7360); 74 600, 82 600 (6927, 7674) | 0.0 (24.0) | grass 5.4, 5.2 (IMG_2037, 2038) |
| 14:07–14:11 | after flight 6, pack change P2 → P3 | 75 600 (7026); 87 700 (8148); 78 000 (7246) | 0.0 (24.1) | P3 before 11.6 (IMG_2043); P2 after 15.6 (IMG_2046, 14:10:06; log 57 closed 14:09:48) |
| 14:13–14:15 | field, flight 7 | 63 400 (5889); during the run 74 300 (6898); 77 200, 76 200 (7169, 7080) | 0.0 (23.3) | |
| 14:18–14:19 | between flights 8 and 9 | 72 100, 72 200 (6699, 6708); 27 000, 26 800 (2505, 2488; thin cloud over the sun) | 0.0 (23.3) | |
| 14:21–14:25 | flights 9 and 10 | 43 300, 44 800 (4025, 4158); 33 600, 34 000 (3118, 3159); 34 400, 33 300 (3199, 3092); 32 500, 32 800 (3017, 3049) | | field surface 12.8 (IMG_2068); P3 after 25.5 (IMG_2069, 14:26:22; log 58 closed 14:26:00) |
| 17:32–17:34 | evening, field, before flight 11 | 812, 812, 686, 649 (75.4, 75.4, 63.7, 60.3) | 0.0 (19.8) | P1 before 18.0 (IMG_2091); field surface 10.1 (IMG_2093) |
| 17:36–17:39 | during flight 11 and after | during the run 649 (60.3); 526, 521 (48.9, 48.4) | 0.0 (16.0) | |
| 17:42 | between flights 12 and 13 | 420, 414, 407, 397, 392 (39.0, 38.5, 37.8, 36.9, 36.4) | | |
| 17:44–17:46 | during flight 13 and after, pack change P1 → P4 | during the run 333, 327 (30.9, 30.4); 268, 268 (24.9, 24.9) | 0.0 (12.9) | P4 before 18.7 (IMG_2115); P1 after 22.4 (IMG_2116, 17:46:50; log 59 closed 17:45:50) |
| 17:49–17:50 | grass T3, before flight 14 | 168 (15.6), 135 (12.5) | | grass 5.1 (IMG_2117) |
| 17:52–17:54 | between flights 14 and 15 | 99, 97, 95, 87, 80 (9.2, 9.0, 8.8, 8.1, 7.4) | | |
| 17:58–17:59 | after flight 15 | 37, 37 (3.4, 3.4) | | P4 after 21.7 (IMG_2136, 17:59:43; log 60 closed 17:59:04) |

All readings with the sensor pointed at the sky, on grass beside the path (field block included). Pack temperatures: P1 18.5 → 35.5 (midday), 18.0 → 22.4 (evening); P2 28.7 → 15.6 (the 28.7 was read on the pack lying in the sun); P3 11.6 → 25.5; P4 18.7 → 21.7. Packs at home before the evening (SkyRC B6AC Neo, 16:34): P1 4.190 / 4.192 / 4.189 / 4.190 V (Σ 16.76, Δ 3 mV), P2 4.110 / 4.108 / 4.108 / 4.109 (Σ 16.43, Δ 2 mV); P2 was not flown in the evening (4.112 / 4.108 / 4.108 / 4.104 on 18 Oct). P2 after the midday flights Σ 15.19 V, Δ 3 mV (15:46). Storage on 18 Oct: P1 3.835 / 3.835 / 3.830 / 3.829 (Σ 15.33, Δ 6), P3 3.774 / 3.776 / 3.776 / 3.778 (Σ 15.10, Δ 4), P4 3.826 / 3.830 / 3.830 / 3.832 (Σ 15.32, Δ 6). No pack voltages before the midday flights (not photographed).

Wind from the log (`wind_from_log.py --height 1.2`): tilt 0.77° from 255° WSW (log 56, 5 hover windows, direction consistency 0.76), 0.22° from 257° (log 57, 2 windows, 0.85), 1.11° from 85° E (log 58, 5 windows, 0.84); no hover window in logs 59 and 60. The anemometer read 0.0 m/s at every reading of the day. Tilt below 1.2° with the direction changing between packs: calm air, the direction is not given as a session value.

## Flights

| Flight | Run | Plan | Armed | SRC2 (local) | Illuminance [lx] (≈, display fc) | OF.Qual | Path ratio outbound / return | Drift 30 / 60 s / end [m] | Observable A (phases) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **E1-061** | field T1 **1.5 m** | — (log starts in flight 13:40:00) | 13:40:49–13:42:23 | ~54 400 (5462 → 4674) | 255 | 0.821 / 0.789 | 0.7 / 3.2 / 3.1 | 0.911 (4) | rangefinder median 1.50 m; 19–21 satellites |
| 2 | **E1-062** | field T1 1.5 m | 13:43:15 | 13:44:04–13:45:40 | ~68 300 (6416 → 6282) | 255 | 0.848 / 0.770 | 2.8 / 4.9 / 5.6 | 0.925 (4) | |
| 3 | **E1-063** | field T1 1.5 m | 13:46:31 | 13:47:20–13:48:52 | ~40 800 (3356 → 4273; thin cloud) | 255 | 0.973 / 0.716 | 2.3 / 7.4 / 15.1 | 0.852 (6) | drift 15.1 m at the end, the largest of the day |
| 4 | **E1-064** | field T1 1.5 m | 13:49:45 | 13:50:38–13:52:08 | ~80 200 (6724 → 8251; sun breaking through during the run, up to 8977) | 255 | 0.842 / 0.859 | 4.2 / 4.6 / 1.8 | 0.983 (5) | |
| 5 | **E1-065** | grass T3 3 m, VEL075 plan, **flown at 1.5 m/s** | — (log starts in flight 13:57:20) | 13:58:52–14:00:22 | ~78 900 (8589 → 6249) | 255 | 0.930 / 0.936 | 1.8 / 3.5 / 1.5 | 0.875 (5) | A → B in 30 s, GNSS speed 1.57 m/s; counted as a plain T3 run (cell VEL15) |
| 6 | **E1-066** | grass T3 3 m **VEL075** | 14:02:00 | 14:04:32–14:06:58 | ~79 000 (7674 → 7026) | 255 | 0.963 / 0.945 | 1.2 / 1.9 / 1.5 | 0.939 (4) | A → B in 57 s, GNSS speed 0.77 m/s; window 146 s |
| 7 | **E1-067** | field T1 1.5 m | — (log starts in flight 14:12:06) | 14:13:19–14:14:47 | ~69 900 (5889 → 7169; 6898 during the run) | 255 | 0.833 / 0.841 | 7.5 / 9.5 / 5.0 | 0.827 (6) | |
| 8 | **E1-068** | field T1 1.5 m | 14:15:40 | 14:16:33–14:18:01 | ~74 100 (7080 → 6699) | 255 | 0.939 / 0.831 | 3.2 / 4.0 / 5.8 | 0.840 (5) | |
| 9 | **E1-069** | field T1 1.5 m | 14:18:58 | 14:19:45–14:21:24 | ~34 100 (2488 → 4025; thin cloud over the sun) | 255 | 0.843 / 0.768 | 2.8 / 4.3 / 5.9 | 0.758 (6) | |
| 10 | **E1-070** | field T1 1.5 m | 14:22:22 | 14:23:11–14:24:44 | ~33 200 (3159 → 3017) | 255 | 0.827 / 0.787 | 3.0 / 4.7 / 3.0 | 0.788 (7) | pack minimum under load 14.13 V |
| 11 | **E1-071** | field T1 1.5 m, dusk | — (log starts in flight 17:35:51) | 17:36:38–17:38:13 | ~600 (63.7 → 48.9; 60.3 during the run) | 255 | 0.765 / 0.764 | 2.9 / 7.2 / 2.0 | 0.893 (5) | 18–23 satellites, HDOP up to 0.76 |
| 12 | **E1-072** | field T1 1.5 m, dusk | 17:39:10 | 17:39:59–17:41:37 | ~470 (48.4 → 39.0) | 255 | 0.841 / 0.884 | 2.7 / 8.0 / 3.0 | 0.878 (6) | |
| 13 | **E1-073** | field T1 1.5 m, dusk | 17:42:28 | 17:43:17–17:44:52 | ~320 (36.4 → 24.9; 30.9, 30.4 during the run) | 255 | 0.847 / 0.686 | 3.8 / 3.0 / 11.7 | 0.830 (6) | |
| 14 | **E1-074** | grass T3 1.5 m, dusk | 17:49:10 | 17:50:38–17:52:11 | ~115 (12.5 → 9.2) | 255 | 0.854 / 0.809 | 3.9 / 7.7 / 3.2 | 1.021 (4) | |
| 15 | **E1-075** | grass T3 1.5 m, dusk, threshold | 17:54:15 | 17:55:42–17:57:23 | ~54 (7.4 → 3.4) | min 0, median 255 | 0.809 / 0.875 | 2.8 / 10.3 / 5.9 | 0.901 (7) | image quality below 255 in 37 % of the samples, 0 in 6 %, first zero 24 s after the switch, longest run of zeros 0.4 s; no EKF failsafe, run completed, landed 17:58:50 |

SRC2 windows in log seconds: 250.9–344.6, 445.3–541.6, 641.7–733.3, 840.2–930.1 (log 56); 290.0–380.5, 630.4–776.3 (57); 168.0–256.7, 362.2–450.0, 554.5–653.4, 760.4–853.0 (58); 126.4–221.8, 327.8–426.0, 525.9–620.3 (59); 220.3–313.7, 524.2–625.4 (60). CSV: `ARIADNE_E1_061…075_20261017_*.csv`. Illuminance per run = geometric mean of the last reading before and the first after the window. Observable A = `scale_observable.py` `r_pair` (number of acceleration and deceleration phases in parentheses). Barometric reference drift after landing +0.8 / +1.1 / +1.9 / +2.0 m (log 56), −0.1 / +0.1 (57), +0.4 / +0.6 / +1.8 / +1.7 (58), −0.5 / −0.8 / −0.5 (59), −1.2 / −1.5 (60). Battery per pack: P1 3246 mAh (791 / 802 / 814 / 839 per flight), P2 3091 (1111 / 1980), P3 3285 (786 / 817 / 832 / 850), P1 again 2438 (801 / 813 / 824), P4 2380 (1175 / 1205); minimum under load 14.65 / 14.70 / 14.13 / 14.81 / 14.76 V. Every log starts in flight, so the first flight of each pack has no arming time in the log and the figure for that flight is a lower bound.

GNSS ground speed during the 1.5 m runs (median while moving, from the GPS message): 1.62–1.97 m/s at a commanded 1.5 m/s (E1-061…064: 1.79, 1.84, 1.62, 1.68; E1-067…070: 1.61, 1.55, 1.78, 1.73; E1-071…073: 1.84, 1.64, 1.97; E1-074, 075: 1.76, 1.63); at 3 m 1.57 (E1-065) and 0.77 at a commanded 0.75 (E1-066).

## Findings

1. **Ploughed field at 1.5 m in sunlight: path ratio 0.80–0.88 over eight runs (0.804, 0.807, 0.825, 0.850, 0.837, 0.881, 0.803, 0.806), drift 3.2–9.5 m at 60 s, image quality 255 throughout.** The same track at 3 m gave 0.885–0.903 in sunlight (S-25) and the grass at 1.5 m in sunlight 0.81–0.84 (S-25). At 1.5 m the field and the grass read the same scale; the 10 % difference between the two surfaces at 3 m is gone. The altitude effect of about 0.15–0.20 is the largest single factor of the E1 matrix and it does not depend on the surface.
2. **Dusk changes nothing at 1.5 m until the sensor goes dark.** Field at 320–600 lx: 0.765, 0.862, 0.756; grass at 54–115 lx: 0.830, 0.841. Both inside the daylight range of the same tracks at 1.5 m. The illuminance axis and the altitude axis are independent down to about 50 lx.
3. **The illuminance threshold over grass at 1.5 m is where it is at 3 m.** E1-075 ran from 80 lx (7.4 fc) at the start to 37 lx (3.4 fc) after landing: image quality below 255 in 37 % of the samples, 0 in 6 %, the first zero 24 s after the switch, the longest run of zeros 0.4 s, no failsafe, the run completed with ratio 0.841. At 3 m, E1-019 at 44 lx had 17 % of the samples below 255, and the threshold test at 18 lx went to image quality 0 and an EKF failsafe (S-20). Halving the altitude does not move the 20–45 lx band.
4. **0.75 m/s in sunlight: 0.954 (E1-066, grass T3, 79 klx), against 0.933 for the same plan flown at 1.5 m/s nine minutes earlier (E1-065) and 0.90–0.97 at 0.75 m/s under overcast (S-22).** Speed does not change the scale in sunlight either. Drift at 60 s 1.9 m against 3.5 m, in proportion to the distance flown.
5. **The scale error is visible in the ground speed.** In source set 2 the controller holds the estimated speed at the commanded value, so the true speed is the command divided by the scale: 1.5 m/s commanded gives 1.6–2.0 m/s over the ground at 1.5 m (scale 0.76–0.88) and 1.57 m/s at 3 m over grass (0.933). The GNSS speed is not available on board without GNSS, but the number explains why a run at 1.5 m reaches 43–55 m from A (most runs 49–55 m) instead of 42–44 m.
6. **Detector v0.2: 12 misses, 2 no-event, 1 hit with negative lead time.** All twelve runs at 1.5 m apart from the threshold run exceed 5 m of error with every indicator inside its threshold. E1-075 produces the first warning from image quality (57 s after the switch), 21.7 s after the error had crossed 5 m through the 1.5 m scale error. Campaign total after 75 runs: 1 hit (late), 2 early warnings, 35 misses, 37 no-event, no false alarms.
7. `error_vs_time.py` on 75 runs: field 1.5 m/s 2.5 / 5.0 / 4.8 m at 30 / 60 / 90 s (n = 29, of which eleven at 1.5 m), grass 1.5 m/s 1.8 / 3.7 / 3.0 m (n = 41, of which eight at 1.5 m), grass 0.75 m/s 1.0 / 2.3 / 2.2 m (n = 5). Observable A over 75 runs: correlation with the reference 0.49 (`r_pair`), 0.35 (acceleration phases), 0.28 (deceleration phases).

## Operational notes

- The `DO_CHANGE_SPEED` command of `E1_grass_T3_3m_VEL075_LAND` executed in both flights of log 57 (`Mission: 1 ChangeSpeed` at 13:57:29 and 14:02:10) with `WP_SPD` at 1.5 throughout, and the aircraft flew the first mission at 1.5 m/s and the second at 0.75 m/s. The log does not show what differed. `WP_SPD` 0.75 set in QGC before the flight remains the only safeguard (S-10, `missions/README.md`); it was not set today. The 1.5 m/s flight is kept as a plain T3 run.
- Every log of the day starts in flight: the first arming of each pack precedes the log start.
- Pack P3 reached 14.13 V under load in its fourth flight (E1-070); four runs at 1.5 m on one pack use 3250–3290 mAh.
- The GM1010 was in FC mode for every reading except IMG_2015 (13:51:03, Lux X10 8081 = 80 810 lx), switched back five seconds later.
- The evening packs were P1 (recharged in the car to 16.76 V after the midday flights) and P4; P2 at 16.43 V was not flown.
- Flight 15 ended at 37 lx with image quality dropping to 0 for up to 0.4 s at a time; the EKF kept the solution. The S-20 failsafe at 18 lx remains the lower limit.

## To do

- [ ] Both directions on one track at 3 m/s or more with the wind along the track (open since S-22)
- [ ] 0.75 m/s in sunlight ×1 more, with `WP_SPD` 0.75 set before the flight
- [ ] Third forward/reverse pair on T4
- [ ] RQ2: tag rows on grass and on the field (Kuźnica), 3 m ×3 and 1.5 m ×3 per surface
- [ ] Detector: the 1.5 m regime now has 19 runs (E1-022, 048, 049, 058–060, 061–064, 067–075); scale from the ground-speed-to-command ratio is not available on board; observable A remains the only candidate
