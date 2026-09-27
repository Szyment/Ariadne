# S-17: 12 Sep 2026 (day), Vistula meadow (Kępa), first E1 measurement runs

Logs: `log_29_2026-9-12-13-27-46.bin` (pack P1, flights 1–3) · `log_30_2026-9-12-13-43-46.bin` (pack P2, flights 4–6). Configuration: `ariadne_v2_12sep2026_1113.params` (before the session; changes relative to 28 Aug: `FENCE_RADIUS` 300 → 70, the rest automatic), `ariadne_v2_12sep2026_1642.params` (after the session; only `MIS_TOTAL` and automatic values). Firmware ArduCopter 4.7.0 (1511f271). Plan: `missions/E1_grass_T1_3m_RTL.plan` (content: A 30 s → B 3 s → A 15 s → RTL). Photos and screenshots: `build-log/photos/2026-09-12/session-1-day/`. Results: `analysis/results/S-17_2026-09-12_drift_analysis.txt`, extracts in `data/`.

## Site

Vistula meadow behind the asphalt path on the dyke (Konstancin municipality). Take-off from the path: **52.1381317 / 21.1612820**, 89 m AMSL; the field is about 1.3 m lower than the path (`CTUN.Alt` higher than the rangefinder by that amount, terrain frame correct). Point A 35 m into the field (52.1380122 / 21.1607767), B 40 m from A on 140°, the leg parallel to the path, 12 m from the boundary with field 2 (slightly different surface). Zones: DRA-RH-6KM WA RPA55 (check-in without a mission up to 100 m AGL), DRA-R CTR EPWA ✓, DRA-I informational. Buildings: none in the field of view from the meadow; the leg runs away from the only farm by the path (NW of the take-off point). Advisor's assessment on 12 Sep: the site is safe, no further measurements needed. Getting there: bus 239 from Os. Kabaty, ZTM ticket zones 1+2.

Surface: **fresh grass, dry, not mown** (field 1). The reconnaissance on 6 Sep showed mown grass, the satellite image bare soil; the state on the day of the flight is decisive.

Roles: pilot in command **Filip**, VLOS observer **Szymon**. DroneTower check-in / check-out: screenshot `IMG_1974.JPG`.

## IMGW forecast (DroneTower)

Morning: surface wind 2.8 m/s from 305° (NW), at 100 m 3.5 m/s, gusts 5.3, Kp 2.3, 15.8 °C, 1022.1 hPa, humidity 74 %, cloud cover 1/8. Before the session (13:02): 2.7 m/s from 306°, gusts 5.2, Kp 1.3, 17.6 °C. After the session (13:47): 2.7 m/s from 306°, Kp 1.7. Sunrise 06:05, sunset 18:58.

## Field measurements (photos `build-log/photos/2026-09-12/session-1-day`, local times)

Block measurements: before, between packs, after. Anemometer GM816 for 60 s at 2.0 m, direction NW 305°.

| Block | Time | Wind AVG / MAX [m/s] | Lux GM1010 | Air temp. | Surface temp. | Packs |
|---|---|---|---|---|---|---|
| before flights 1–3 | ~13:05 | 1.2 / 2.1 | 3177 | 23.6 °C | 18 °C | P1 before: 18.8–22.1 °C |
| between packs | ~13:28 | 2.1 / 3.1 | 3321 | 23.4–25.4 °C | — | P1 after flights: 29.4 °C |
| after flights 4–6 | ~13:45 | 1.4 / 1.8 | 6464 | — | 13.7 °C | P2 after flights: 22.8–23.7 °C |

Wind AVG at most 2.1 m/s (field criterion 4.0; §8 threshold 5.0). Lux 3–6 thousand = the "full daylight" cell, variable cloud cover.

**Wind from log** (`analysis/results/wind_20260912.md`): hover tilt 0.7–1.6°, direction 292–312° (NW), gustiness p95 2.4–3.3°. Consistent with the anemometer.

## Flights

| Flight | Run | Log | SRC2 window [log s] | Pack | Outbound (downwind) | Return (upwind) | Whole | Drift 15 / 30 / 60 s [m] | Final drift [m] | CTUN.Alt after flight | §8 decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | session calibration | 29 | 398–482 | P1 | 0.944 | 0.985 | 0.964 | 1.06 / 3.31 / 3.97 | 3.70 | +0.11 | outside the dataset (§7.3) |
| 2 | E1-001 | 29 | 670–746 | P1 | 0.933 | 0.964 | 0.948 | 1.18 / 3.09 / 3.00 | 2.17 | −0.13 | accepted |
| 3 | E1-002 | 29 | 967–1047 | P1 | 0.940 | 0.947 | 0.944 | 0.18 / 0.53 / 3.84 | 0.90 | +0.78 | accepted |
| 4 | E1-003 | 30 | 141–230 | P2 | 0.975 | 0.972 | 0.974 | 0.14 / 1.42 / 3.51 | 2.14 | −0.13 | accepted, LUX flag |
| 5 | E1-004 | 30 | 406–487 | P2 | 0.944 | 0.976 | 0.959 | 0.30 / 1.83 / 3.56 | 2.18 | +0.07 | accepted, LUX flag |
| 6 | E1-005 | 30 | 645–715 | P2 | 0.920 | 0.990 | 0.954 | 2.14 / 3.90 / 4.84 | 4.20 | −0.26 | accepted, LUX flag |

Cell: **LUX1-SURF1-ALT3-VEL15** (full daylight / fresh grass, not mown / 3.0 m / 1.5 m/s). RC7 switch times, voltages, satellites and altitudes are in the log; the dataset = the phase from `Using EKF Source Set 2` to `Set 1` (A→B→A), the flight to A and the return are outside the dataset.

All flights: `OF.Qual` 255, rangefinder median 2.99–3.02 m, max 3.28 m (margin ≥ 0.9 m to the 4.2 m threshold), GNSS 24–32 satellites, HDOP 0.45–0.60, logs complete, no interventions. LUX flag for flights 4–6: between the "between" block and the "after" block the lux rose from 3321 to 6464 (passing clouds), and there was no measurement at each flight, so the criterion "change > 30 % during the run" cannot be decided per flight. Flights 2–3: 3177 → 3321 (5 %), no reservations.

## Findings

1. Path ratio outbound 0.920–0.975, return 0.947–0.990. Downwind/upwind asymmetry in 5 of 6 runs (exception: flight 4), weaker than on 29 Aug in 2–2.5 m/s wind (outbound 0.81–0.85). In the evening, without wind, the asymmetry disappears (S-18).
2. Final drift 0.9–4.2 m, below the 5 m failure threshold; drift at 60 s 3.0–4.8 m, close to the GNSS resolution (1–3 m), to be reported with the caveat of §4.2.
3. Altitude reference drift after the flight within the 0.3 m criterion except for flight 3 (+0.78 m).
4. Packs: after 3 flights both at 3.80–3.82 V per cell (P1 36 %, P2 38 %), P1 ended log 29 with the message `Battery 1 below minimum arming voltage` (3348 mAh from the log). **3 flights per pack is the hardware limit.** Cell spread 0.00 V.
5. RTL not used (no RTL position on the transmitter): returns flown manually in Loiter, landings in Land. Solution: plan v2 with a home point and LAND in the mission (from S-18).
6. In log 29 a one-second SRC2 switch (487–489 s), RC7 moved twice; no effect on the data.
7. Lesson: lux and wind at every flight, not per block. Introduced in S-18.

## To do

- [ ] Photos `build-log/photos/2026-09-12/session-1-day` to `build-log/photos/2026-09-12/` (script); DNG outside the synchronised directory.
- [ ] Cell code `LUX1-SURF1-ALT3-VEL15` to be confirmed by the author.
