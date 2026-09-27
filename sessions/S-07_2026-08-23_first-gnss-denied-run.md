# S-07: Session card, 23 Aug 2026

**Type:** GNSS-denied run + battery endurance test · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Log:** `log_10_2026-8-23-12-54-18.bin` (27 MB) · **Ground telemetry:** `2026-08-23 12-56-16.tlog`
**Configuration:** `ariadne_v2_23aug2026_1237.params`
**In the E1–E3 dataset:** no

---

## Conditions

| | |
|---|---|
| Location | field at Kuźnica Kiedrzyńska, 50.913978 N / 19.086452 E, 234 m above sea level |
| Pilot in command | Filip Pepliński |
| Observer (VLOS role) | Szymon P. Pepliński |
| Flight | 12:39:48 – 12:54:04 local time |
| Wind (GM816) | 3 m/s on average, gusts 5.6–5.7 m/s |
| Ground temperature (AX-7510) | 30 °C |
| Air temperature (transmitter) | 22–24 °C |
| Cloud cover | variable: at times full sun, at times complete overcast |
| Surface condition | after the rain of 22 Aug, ground generally dried out |

The coordinates and altitude are the median of 4504 GNSS samples from the log, consistent with the location of sessions S-02 – S-06 to within 6 m.

On 22 Aug all-day rain, heavy towards the end of the day. On 23 Aug puddles in the forest.

### Illuminance

Four GM1010 readings within a few tens of minutes under a similar sky:

| Reading | Sensor orientation |
|---|---|
| 21 500 lx | near the ground |
| 30 000 lx | at ground level |
| 60 000 lx (6000 × 10) | aimed at the sun |

Solar elevation at 12:47 was 50.4°, upper bound for a cloudless sky 84 800 lx. All three readings fall below it.

Until 23 Aug the protocol specified neither the sensor orientation nor the obligation to record the range multiplier, so the readings are not mutually comparable. Convention established 23 Aug: `protocol/ANNEX_D_illuminance_measurement.md`.

---

## Course of the session

One flight, Loiter mode throughout. Change to LAND at 950.4 s by the autopilot's decision.

| Event | Log time | Local time |
|---|---|---|
| Arming (EV 10) | 104.6 s | 12:39:37 |
| Lift-off (EV 28) | 115.4 s | 12:39:48 |
| EKF3 in-flight heading alignment | 131.6 / 132.2 s | 12:40:04 |
| Source set 3 | 168.1 s | 12:40:41 |
| **Source set 2** | **168.4 s** | **12:40:41** |
| **Source set 1** | **188.1 s** | **12:41:00** |
| Battery failsafe, LAND mode | 950.4 s | 12:53:43 |
| Landing complete (EV 18) | 971.2 s | 12:54:04 |
| Disarming (EV 11) | 971.8 s | 12:54:04 |

Local time reconstructed from the GPS week and milliseconds, Europe/Warsaw zone, 18 leap seconds.

Time airborne: **855.8 s (14 min 16 s)**.

One error entry in the whole flight: `ERR` subsystem 6, code 1, battery failsafe. The EKF failsafe did not trigger.

---

## GNSS-denied run

19.7 s on source set 2. `EK3_SRC2_POSXY` = 0, `EK3_SRC2_VELXY` = 5: no horizontal position source, position integrated from optical-flow velocity.

| | |
|---|---|
| Altitude per `CTUN.Alt` | 3.63 m mean (2.99–3.99) |
| Altitude per rangefinder | 1.83 m mean (1.63–2.12) |
| Resultant tilt | 5.44° mean, max. 8.70° |
| Heading | 128° |
| `OF.Qual` | 255 throughout the window |
| XKF4 innovation test ratios | SV max. 0.04 · SP max. 0.00 · SH max. 0.12 · SM max. 0.03 |

Threshold `FS_EKF_THRESH` = 0.80. Highest ratio in the window 0.12.

### Estimate divergence relative to the recorded GNSS

| Time since switching | Divergence |
|---|---|
| 5 s | 0.07 m |
| 10 s | 0.17 m |
| 15 s | 0.26 m |
| maximum in the window | **0.45 m** |

An upper bound, not a drift measurement. The displacement per GNSS in the window was at most 0.58 m, so the divergence is of the order of the reference noise at HDOP 0.52–0.71.

### Limitations

1. 19.7 s against the 60 s provided for by the protocol. Extrapolation is unjustified.
2. `OF.Qual` saturated (255) throughout the flight. The effect of grass waving in the wind on the flow vectors is unmeasured.
3. One surface, one illuminance, one altitude.

---

## Item B1 closed

| | |
|---|---|
| Time airborne | **855.8 s** |
| Consumption | **3207 mAh of 5000 (64%)** |
| Mean current | **13.45 A** |
| Maximum current | 19.5 A |
| Voltage | 16.41 → 14.92 V, momentary minimum 13.24 V |
| Mean altitude over the whole flight | 10.09 m (max. 11.56) |
| Mean throttle | 0.252 |

The calculation in `MISSING_DATA.md` §B1 was based on 411 s of flight per pack (log 6, 19 Aug). Measurement: 855.8 s, **2.08×**.

### Battery failsafe

```
950.4 s   Battery 1 is low 14.72V used 3135 mAh
950.4 s   Battery Failsafe → LAND mode
```

`BATT_FS_VOLTSRC` = 0: the threshold `BATT_LOW_VOLT` = 14.8 V is compared with the voltage measured under load. 36% of capacity remained in the pack.

`BATT_RESISTANCE` does not exist in ArduCopter 4.7.0, checked in the full parameter dump from log 10. The fix has not been determined.

---

## Other indicators

| | S-07 | S-06 (22 Aug) |
|---|---|---|
| Roll tracking error p95 | 1.13° | 2.25° / 1.98° |
| Pitch tracking error p95 | 1.13° | 2.46° / 2.58° |
| Mean resultant tilt | 7.49° (max. 15.58) | 5.42° |
| Wind from anemometer | 3 m/s, gusts 5.6 | 2 m/s, gusts 3.2 |
| Mean current | 13.45 A | 12.59 A |
| Satellites / HDOP | 18–27 / 0.52–0.71 | 23–30 / 0.45–0.52 |

The tracking error comparison settles nothing about tuning: S-07 is a hover at one altitude, S-06 is a mission with transits and climbs to 25 m. The same remark applies to the mean current.

---

## Barometric altitude

In the GNSS-denied window `CTUN.Alt` indicated 3.63 m, the rangefinder 1.83 m, i.e. 1.66 m above ground after subtracting `RNGFND1_GNDCLR` = 0.17.

Terrain ruled out: `GPS.Alt` − `RFND` gives 224.1 – 224.5 m above sea level throughout the low-flight phase, and the window lay 2.5 m from the take-off point.

Rangefinder ruled out: on the ground it indicated 0.15 m with `RNGFND1_GNDCLR` = 0.17.

`CTUN.Alt` coincides with `BARO.Alt` to within 0.3 m. The altitude comes from the barometer: `EK3_SRC1_POSZ` = 1, `EK3_RNG_USE_HGT` = −1.

Barometer − rangefinder difference in successive windows: 0.10 · 1.16 · 0.87 · **1.89** · 1.15 m. Variable, not growing.

**Cause: static pressure error at the barometer inlet induced by the airflow.** The dynamic pressure at 5.6 m/s is q = ½ · 1.19 · 5.6² = **18.7 Pa**, and the vertical pressure gradient 1.19 · 9.81 = **11.7 Pa/m**, which gives **1.6 m of apparent altitude**. This agrees with the observed 0.9 – 1.9 m and explains the variability, because the gusts are variable.

`BARO1_WCF_ENABLE` = 0: wind compensation of the barometer is disabled and **remains disabled**. It requires a wind estimate from EKF3, and that requires `EK3_DRAG_BCOEF_X/Y` and `EK3_DRAG_MCOEF`. Aerodynamic drag fusion aids dead reckoning without GNSS, i.e. it changes the quantity measured in RQ1. Disabling drag fusion is established in `ANNEX_C_wind_measurement.md` §10.

Consequence for the campaign: the altitude of a run below 6 m is recorded **from the rangefinder**, not from `CTUN.Alt`.

---

## Source switch

The pilot mistakenly performed the sequence 1 → 2 → 3 → 2. The log records set 3 at 168.1 s and set 2 at 168.4 s; the first, brief entry into set 2 was not recorded.

No effect on the measurement: set 3 uses GNSS. The GNSS-denied phase counts from 168.4 s. The phase boundary is defined by the message in the log.

---

## Open

None.
