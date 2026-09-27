# Project Ariadne: Platform 2

**Holybro X500 V2 + Pixhawk 6X + ArduCopter 4.7.0**
Tuning log, sessions of 18, 19 and 20 Aug 2026

This document continues `02_commissioning.md`, which ended with the statement of readiness for the first hover. This log begins with the first flights.

Status: harmonic notch filter entered but not verified in flight. AutoTune not started.

---

## 1. Corrections to earlier documents

| Topic | Was | Is |
|---|---|---|
| SC mapping | "Set 1 / 2 / 3" | Set 1 = down, Set 2 = middle, Set 3 = up. AUTO flights use down or up (both GPS), never the middle |
| Mode slots | FLTMODE1/4/6 populated | SB is three-position, so it reaches only slots 1, 4 and 6. Slots 2, 3 and 5 are unreachable from the transmitter |
| `BATT_FS_*_ACT = 1` (Land) | — | Stays unchanged. RTL requires GPS, and in the E2–E3 runs GPS is cut off |
| "GPS Glitch or Compass error" | open item from 15 Aug | Still open. The symptom occurred indoors on 20 Aug, it does not occur in the field |

---

## 2. Yaw imbalance: fault and repair

### Symptom (LOG 5, 18 Aug)

Motors C1 and C2 ran 370 µs higher than C3 and C4. About 45% of the yaw authority was permanently consumed to hold the heading. C3 ran at 1260 µs and C1 at 1639 µs. The drone's rotation and its correction were present before take-off.

The phenomenon was present from the first flight of the session and did not grow during it:

| | Diagonal difference |
|---|---|
| Flight 1 | +334 µs |
| Flight 2 | +362 µs |
| Flight 3 | +407 µs |

The cause was motor mounts seated at an angle. The source of the misalignment was not established.

### Tip-over after landing, LOG 5, t = 502.9–504.1 s

After touchdown in the grass the drone tipped over before the motors were shut off. The crash check (Subsys 12, ECode 1) triggered at 505.6 s.

In the body frame, pitch changed from −3° to −68°, roll from −0.5° to −10.2° and settled at −4.6°, and yaw from 310° to 316°. The motors ran throughout the tip-over (at 504.5 s C1 = 1534, C3 = 1453) and dropped to 1000 only at 505.6 s, that is, on disarming.

The incident has no causal link to the yaw imbalance, because that was present earlier.

### Effect of the correction

| | LOG 5 | LOG 6 |
|---|---|---|
| Diagonal difference | +370 µs | +84 µs |
| Steady YawOut | +0.449 | +0.098 |
| Clipping | 21 | 0 |
| VibeY p95 | 94.7 | 32.1 |
| pitch p95 | 6.26° | 4.01° |

The remaining residual of 85–95 µs is the irreducible level on this airframe. Yaw saturation is 0.00%.

The measure remains YawOut, not the diagonal difference. The latter grows in wind and in faster flight with unchanged mechanics (84 → 95 µs between 19 and 20 Aug).

---

## 3. Session comparison

| | LOG 5 (18 Aug) | LOG 6 (19 Aug) | LOG 7 (20 Aug) |
|---|---|---|---|
| Mode | manual | manual | AUTO, mission ×2 |
| ERR | 3 | 0 | 0 |
| Clipping | 21 | 0 | 0 |
| Diagonal difference | +370 µs | +84 µs | +95 µs |
| Steady YawOut | +0.449 | +0.098 | +0.1005 |
| VibeY mean / p95 | 30.4 / 94.7 | 19.9 / 32.1 | 30.3 / 44.8 |
| roll p95 | — | 3.16° | 1.86° |
| pitch p95 | 6.26° | 4.01° | 2.11° |
| Altitude error p95 | — | 0.79 m | 0.38 m |
| GPS sat / HDop | — | 25 / 0.63 | 25 / 0.57 |
| Wind (hover tilt) | 1.86° | 1.47° | 4.60° / 4.55° |

---

## 4. Measurement mission (`S-04_Test1.plan`)

The filter in mode 1 derives its frequency from the throttle position. In manual flight every flight has a different throttle distribution, so it cannot be decided whether the spectrum changed because of the filter or because of the pilot.

The mission comprises 26 commands: take-off to 15 m, hover for 60 s, then altitude changes to 25, 8 and 15 m at the same position, two laps of a square with a side of about 46 m, and return in RTL mode.

Frozen mission parameters: `WP_SPD 5 · WP_ACC 2.5 · WP_RADIUS_M 2 · WP_SPD_UP 2.5 · WP_SPD_DN 1.5`.
We keep the same altitude, battery, starting voltage and mass, and always compare the same mission segment.

Validation: the spectra of flight 1 and flight 2 differ by less than 1.6 dB at every peak.

Wind criterion: hover tilt below 4°.

The mission flies on set SRC1 (GPS), at 15–25 m. It is not a run without GNSS, for which the 6 m ceiling from `RNGFND1_MAX` still applies.

---

## 5. Harmonic notch filter

### Measurement (LOG 7, hover 158–220 s and 461–523 s)

The measurement was taken with the ICM45686 sensor at 3224.69 Hz, with no gaps in the data. Hover throttle was 0.263 and 0.270.

| Peak (X axis) | Flight 1 | Flight 2 |
|---|---|---|
| 96 Hz | −30.9 dB | −32.5 |
| 177 Hz | −26.4 | −26.5 |
| 213 Hz | −26.9 | −27.1 |
| 243 Hz | −21.2 | −22.2 |

The second harmonic covers the band 369–486 Hz.

The four peaks correspond to four motors running at different speeds. The ratio f_max/f_min is 1.37, and the throttle ratio C1/C3 is 1.30. The ArduPilot documentation describes such a distribution as the signature of a yaw imbalance. It is the same phenomenon as the 95 µs diagonal difference, seen from the spectrum side.

### Settings

```
INS_HNTCH_ENABLE  1
INS_HNTCH_MODE    1
INS_HNTCH_FREQ    210     centre of the 177–243 cluster
INS_HNTCH_BW      80      covers the whole cluster
INS_HNTCH_ATT     40
INS_HNTCH_REF     0.267   measured hover throttle
INS_HNTCH_HMNCS   3
INS_GYRO_FILTER   40      ← the actual goal
MOT_HOVER_LEARN   0       freeze the reference
```

The 96 Hz peak remains untouched and is 10 dB weaker than the others. It is a candidate for a second notch filter.

The purpose of the settings is to allow `INS_GYRO_FILTER` to be raised from 20 to 40 Hz. The noise is concentrated in the 177–243 Hz band, and the control band covers 0–40 Hz, so the low-pass filter set at 20 Hz was already attenuating it by about 35 dB. Without raising the frequency of that filter, the notch alone contributes nothing.

---

## 6. Parameter additions

```
MOT_BAT_VOLT_MAX = 16.8    voltage compensation (a condition of notch mode 1)
MOT_BAT_VOLT_MIN = 13.2    clamp of the compensation curve, NOT a protection threshold
FENCE_ENABLE     = 1       the configuration existed, the switch was at zero
RC8_OPTION       = 16      Auto Mode on SD
FLTMODE2 = 15 (AutoTune) · FLTMODE3 = 3 (Auto) · FLTMODE5 = 6 (RTL)
INS_RAW_LOG_OPT  = 9       temporary, to be removed after the filter verification
```

The `MOT_BAT_VOLT_MIN` parameter is not a battery protection threshold. That function is performed by `BATT_LOW_VOLT` and `BATT_CRT_VOLT`, already set in the previous session.

The battery percentage indicator shows consumption counted from power-on, not the state of charge of the pack. A pack at storage voltage (15.24 V) indicated 99%. Look at the voltage.

The energy density of the pack is 176 Wh/kg, which is more than the aviation-grade Tattu 4S 25C packs (157–161). A replacement is not justified.

---

## 7. Transmitter: workaround for the three-position SB

Switch SB reaches only slots 1, 4 and 6, so the Auto, AutoTune and RTL modes remained unreachable from the transmitter. Instead of a mixer on channel 6, the following division was adopted:

| Switch | Function |
|---|---|
| SA | Land (`RC5_OPTION = 18`) |
| SB | Stabilize / AltHold / Loiter |
| SC | EKF Source Set (`RC7_OPTION = 90`) |
| SD | Auto (`RC8_OPTION = 16`) |

Switch SB has priority over SD. Moving SB interrupts the mission regardless of the SD position. After such an interruption, switching SD again will not resume the mission, because ArduPilot reacts to a change of the switch position, not to its state. SD must be moved down and back up.

For the duration of AutoTune (flight 3), `RC8_OPTION` must be changed to 17.

---

## 8. Mission start procedure

1. Charge the pack to 16.8 V
2. Set SC down (Set 1, GPS). The middle position is Set 2, that is, optical flow without a position source, in which the mission will not start
3. Set SD down, SB to Loiter, and leave SA unchanged
4. Check that there are no yellow errors in QGC
5. Arm in Loiter mode and wait ten to twenty seconds, away from concrete and metal
6. Lift the drone manually to 1–2 m
7. Set SD up to start the mission; keep your thumb on SD until it ends

Rationale for step 5: in logs 5 and 6 the EKF reported "in-flight yaw alignment" at every arming, that is, it aligned the heading only after take-off.

---

## 9. Pitfalls

| Topic | Conclusion |
|---|---|
| KML does not export RTL or speed commands | Verify the mission from the `.plan` file |
| Filter Review uses absolute time, and the log starts at 90.2 s | Count windows from log time |
| `MOT_HOVER_LEARN = 2`: drift 0.35 → 0.2667 in two days | Freeze at 0, because this value is the filter reference |
| `GPS1_TYPE` reset itself to 0, `COMPASS_DEC` zeroed | Check after every parameter session |

---

## 10. Baseline for the verification flight

Thresholds from manual flights do not transfer to AUTO mode. In manual flight the commanded angle comes from the sticks and changes stepwise, whereas in AUTO mode the controller generates it and the profile is smooth. The reference baseline is LOG 7.

| | Baseline | Threshold |
|---|---|---|
| VibeY mean IMU0 | 30.3 | <20 |
| VibeY p95 IMU0 | 44.8 | <30 |
| Spectrum 177–243 Hz | full amplitude | cut |
| roll p95 | 1.86° | no worse |
| pitch p95 | 2.11° | no worse |
| Altitude error p95 | 0.38 m | no worse |

The last two rows decide. The `INS_GYRO_FILTER` parameter was raised from 20 to 40, which reduces the phase lag but lets more noise into the loop. A degradation of attitude tracking would mean that the notch does not cover a wide enough band.

---

## 11. Open

### This cycle
- [ ] Filter verification flight, same mission
- [ ] `INS_RAW_LOG_OPT = 0` after the flight is passed
- [ ] AutoTune (`RC8_OPTION = 17`), calm day, more than one pack
- [ ] Tuning assessment flight, same mission
- [ ] `COMPASS_DEC`: check after obtaining a GPS fix (expected value about 0.10)

### Carried over from the commissioning log, still open
- [ ] Repeat the compass calibration at the flying site
- [ ] Telemetry range test with the motors at about 50% throttle, tethered
- [ ] Empirical test of the coupling between the optical-flow sensor and the lidar
- [ ] Verify source switching in SITL before the first run without GNSS
- [ ] "GPS Glitch or Compass error": confirm absence of the symptom in the field

### Outside the tuning cycle
- [ ] `AVOID_ENABLE`: set to zero or add a proximity sensor
- [ ] ESC telemetry: settles the origin of the residual yaw imbalance and is the best data source for the filter
- [ ] Simple / Super Simple on a switch: assessment of orientation over the field (the LEDs are not enough in daylight)

---

## 12. Files

| | |
|---|---|
| `log_5_2026-8-18-18-49-02.bin` | 3 manual flights, yaw imbalance, tip-over after landing |
| `log_6_2026-8-19-19-33-42.bin` | 3 manual flights after the mount correction |
| `log_7_2026-8-20-16-54-54.bin` | 2 AUTO missions, raw gyroscope logging, baseline for the filter |
| `S-04_Test1.plan` | measurement mission, do not edit |
| `ariadne_v2_20aug2026_2020.params` | state before the verification flight |

---

## 13. Deadlines

| Date | Task |
|---|---|
| 2026-11-15 | Measurement data freeze |
| 2026-12-31 | EUCYS / Odkrycia documentation |
