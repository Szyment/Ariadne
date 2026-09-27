# missions

QGroundControl mission plans for the E1 campaign: A → B → A → home → LAND in the terrain frame at 1.5 m/s. Naming convention and the A/B track register follow.

## Naming convention from 12 Sep 2026 (Kępa Okrzewska)

`E1_<surface>_T<n>_<altitude>_<ending>.plan`

- surface: `trawa` (grass, the meadow behind the dyke) or `pole` (ploughed field)
- T<n>: track number, i.e. the A/B pair of points on the given surface
- altitude: `3m` or `1.5m` (terrain frame, rangefinder)
- ending: `LAND` (A → B → A → home → LAND) or `RTL` (A → B → A → RTL)

Run: hold at A 30 s → B 3 s → A 30 s (in `RTL`: 15 s). Speed: `WP_SPD` 150 = 1.5 m/s. The VEL 0.75 level has its own file `*_VEL075_*` with `DO_CHANGE_SPEED` 0.75 m/s at the start of the mission; because this command disappears on re-entering Auto (S-10), before a VEL 0.75 flight we also set `WP_SPD` 75 in QGC and restore 150 after the flight. The file exists so that the flight maps onto the plan; the parameter is the safeguard. Build the plan in QGC after reading the take-off position on site.

## Tracks (Kępa)

| Track | A | B | Course A→B | Home | Sessions |
|---|---|---|---|---|---|
| grass T1 | 52.1380122 / 21.1607767 | 52.1377369 / 21.1611530 | 140° | 52.1381317 / 21.1612820 (path) | S-17, S-18, S-20 |
| grass T2 | 52.1376277 / 21.1604128 | 52.1373418 / 21.1608037 | 140° | 52.1381317 / 21.1612820 (path), A 82 m from home | S-21 (file removed 20 Sep: too deep in the field) |
| grass T3 | 52.1375457 / 21.1603449 | 52.1373898 / 21.1608774 | 115° | 52.1381317 / 21.1612820 (path), A 91 m from home | from 20 Sep (T1 too close to the trees, T2 too deep in the field) |
| field T1 | 52.1376191 / 21.1614674 | 52.1373449 / 21.1618800 | 137° | 52.1377186 / 21.1618933 | S-19 flights 1–3, S-21 |
| field T2 | 52.1372714 / 21.1612269 | 52.1376149 / 21.1614645 | 23° | 52.1377186 / 21.1618933 | S-19 flights 4–6 |

## Files

| File | Sessions | Notes |
|---|---|---|
| `E1_grass_T1_3m_RTL.plan` | S-17 | reconstruction from the card and `log_29/30` (the plan of 12 Sep was not saved in the repository) |
| `E1_grass_T1_3m_LAND.plan` | S-18, S-20 | recreated on 20 Sep from the T2 template with the T1 coordinates; T1 too close to the trees |
| `E1_grass_T3_3m_LAND.plan` | from 20 Sep | track T3 |
| `E1_grass_T3_1.5m_LAND.plan` | from 20 Sep | track T3, 1.5 m |
| `E1_grass_T3R_3m_LAND.plan` | from S-23 | track T3 **reversed**: B 30 s → A 3 s → B 30 s → home → LAND; flown alternately with the forward plan to separate leg order from heading (S-22 finding 5) |
| `E1_field_T1R_3m_LAND.plan` | from S-23 | track T1 reversed, same purpose |
| `E1_grass_T3_3m_VEL075_LAND.plan` | from 20 Sep | track T3, 3 m, `DO_CHANGE_SPEED` 0.75 m/s as the first command; additionally `WP_SPD` 75 in QGC before the flight (see below) |
| `E1_field_T1_3m_LAND.plan` | S-19 flights 1–3, S-21 | |
| `E1_field_T1_1.5m_LAND.plan` | not yet flown | |
| `E1_field_T2_3m_LAND.plan` | S-19 flights 4–6 | reconstruction from the card and `log_34` |

The reconstructions were made on 18 Sep 2026: points, holds and altitudes consistent with what was flown; the order of the JSON fields may differ from the QGC record.

## Sessions 20–29 Aug (Częstochowa)

Files prefixed with the number of the session in which they were created; their READMEs lie next to them under the same name.

| File | Sessions |
|---|---|
| `S-04_Test1.plan`, `S-04_Test1.kml` | S-04, S-05, S-09, S-13, S-14 (AUTO test mission) |
| `S-06_Balance1.plan` | S-06, S-13, S-14 (balance check) |
| `S-10_Drift1.plan` | S-10 |
| `S-12_Drift2.plan` | S-11, S-12 |
| `S-15_Drift3.plan` | S-15, S-16 |

The drafts of 5 Sep (`Dryf_E1_*`, near the pond, not flown) were removed on 18 Sep 2026.

## Files

| File | Title |
|---|---|
| [`E1_field_T1R_3m_LAND.plan`](E1_field_T1R_3m_LAND.plan) |  |
| [`E1_field_T1_1.5m_LAND.plan`](E1_field_T1_1.5m_LAND.plan) |  |
| [`E1_field_T1_3m_LAND.plan`](E1_field_T1_3m_LAND.plan) |  |
| [`E1_field_T2_3m_LAND.plan`](E1_field_T2_3m_LAND.plan) |  |
| [`E1_grass_T1_3m_LAND.plan`](E1_grass_T1_3m_LAND.plan) |  |
| [`E1_grass_T1_3m_RTL.plan`](E1_grass_T1_3m_RTL.plan) |  |
| [`E1_grass_T3R_3m_LAND.plan`](E1_grass_T3R_3m_LAND.plan) |  |
| [`E1_grass_T3_1.5m_LAND.plan`](E1_grass_T3_1.5m_LAND.plan) |  |
| [`E1_grass_T3_3m_LAND.plan`](E1_grass_T3_3m_LAND.plan) |  |
| [`E1_grass_T3_3m_VEL075_LAND.plan`](E1_grass_T3_3m_VEL075_LAND.plan) |  |
