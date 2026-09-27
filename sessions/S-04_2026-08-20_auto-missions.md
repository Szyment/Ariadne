# S-04: Session card, 20 Aug 2026

**Type:** autonomous missions, collection of the measurement baseline for the harmonic notch filter · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Log:** `log_7_2026-8-20-16-54-54.bin` (132 MB, `INS_RAW_LOG_OPT = 9`)
**Parameter snapshots:** `ariadne_v2_20aug2026_1145`, `_1148`, `_2015`, `_2020`
**In the E1–E3 dataset:** no (tuning session)

---

## Conditions

| | |
|---|---|
| Location | Field at Kuźnica Kiedrzyńska, 50.914028 N / 19.086457 E, terrain about 224 m above sea level. Mission area about 63 × 69 m, altitude up to 249 m above sea level (25 m above terrain) |
| Pilot in command | Filip Pepliński |
| Observer (VLOS role) and telemetry operator | Szymon P. Pepliński |
| Wind (GM816 anemometer) | 2–3 m/s at ground level. Proxy from the log: hover tilt 4.60° / 4.55°, above the 4° threshold adopted for this mission. Discussed in the section "Wind criterion" |
| Illuminance (GM1010) | 2450 lx, consistent with the time of day (session 16:45 – 16:54) |
| Air and pack temperature, Kp index | [TO BE COMPLETED] |
| Surface | [TO BE COMPLETED] |
| DroneTower check-in | **not done, the phone battery ran flat.** The formal and legal condition from `procedures/preflight.md` remained unmet for this session. Discussed below |
| GNSS quality criterion | Met with a large margin: 25–32 satellites, HDOP 0.47–0.57 |

> **Procedural note.** The checklist places the DroneTower check-in in the formal and legal condition, with the annotation that without the full set there is no arming, and that the policy exclusions make this condition the basis of insurance cover. On 20 August the check-in was not done because the phone battery had run flat. This is recorded deliberately: log 7 is the measurement baseline for the filter and will be cited in the documentation, so the gap should be noted, not omitted.
>
> The lesson was implemented: a charged phone was added to the formal and legal condition in the checklist. Without a phone three items drop out at once: the check-in, the pilot certificate and the zone check.

## Aim of the session

Collection of a repeatable spectral baseline for designing the harmonic notch filter. Manual flight is unsuitable for this purpose: the filter in mode 1 derives the frequency from the throttle position, and under manual control every flight has a different throttle distribution, so it cannot be decided whether a change in the spectrum results from the filter or from piloting. For this reason an autonomous mission was flown.

## Mission `S-04_Test1.plan`

Profile: take-off to 15 m, 60 s hover, transitions through 25, 8 and 15 m at the same position, a square with a side of about 46 m flown twice, return to the take-off point. 26 commands in total.

Frozen navigation parameters: `WP_SPD 5`, `WP_ACC 2.5`, `WP_RADIUS_M 2`, `WP_SPD_UP 2.5`, `WP_SPD_DN 1.5`. The same altitude, pack, starting voltage and mass. The same mission segment must be compared.

### Verification of the mission file (21 Aug)

The file `missions/S-04_Test1.plan` was checked programmatically. The description in the tuning document agrees with the contents of the file.

| Item | Command | Altitude above terrain | Note |
|---|---|---|---|
| 0 | `TAKEOFF` | 15 m | take-off point 50.914028 N / 19.086457 E, 224 m above sea level |
| 1 | `WAYPOINT` | 15 m | `hold = 60 s`, the measurement hover is a parameter of the waypoint, not a separate command |
| 3 / 5 / 7 | `WAYPOINT` | 25 / 8 / 15 m | altitude changes at the same position |
| 9–15 | `WAYPOINT` ×4 | 15 m | square, first circuit |
| 17–23 | `WAYPOINT` ×4 | 15 m | square, second circuit |
| 25 | `RTL` | — | |
| even items | `DO_CHANGE_SPEED` ×12 | — | 5 m/s before each leg |

26 commands in total. Sides of the square computed from the file: 45.2 / 49.5 / 44.4 / 46.6 m, matching the value of about 46 m given in the document. Plan metadata: `cruiseSpeed 15`, `hoverSpeed 5`.

The flight area restriction comes from the parameter file, not from the plan (the section in the plan is empty): `FENCE_RADIUS 300 m`, `FENCE_ALT_MAX 100 m`, `FENCE_ACTION 1` (return or land), `FENCE_MARGIN 2 m`. The mission fits within this envelope with a large margin, since it moves away by at most about 50 m and reaches an altitude of 25 m. `RTL_ALT_M = 15`.

The file `S-04_Test1.kml` does not replace the plan. As warned in the tuning document, the KML export contains neither the return to the take-off point nor the speed change commands; the check confirmed the absence of the twelve `DO_CHANGE_SPEED` commands and of `RTL`. Since these determine the repeatability of the mission, `S-04_Test1.plan` remains the reference file.

The mission is flown with the sources set to set 1 (GNSS), at an altitude of 15–25 m, and does not constitute a GNSS-denied run. For GNSS-denied runs the altitude limit of 6 m resulting from `RNGFND1_MAX` applies.

## Wind criterion: log 7 exceeded the adopted threshold

The tuning document §4 sets a threshold for this mission of hover tilt below 4°. The comparison table §3 gives values of 4.60° and 4.55° for log 7. The baseline against which the harmonic notch filter is to be assessed was therefore produced above the threshold that the same document deems acceptable.

The anemometer at ground level indicated 2–3 m/s. The discrepancy is explained by the vertical wind speed gradient: the mission was flown at an altitude of 15–25 m, while the measurement was taken at operator height. With an exponent of 0.2, typical of open terrain, 2–3 m/s at ground level corresponds to 3.3–5.0 m/s at 25 m, which is consistent with the observed tilt.

This matters for the verification flight. The acceptance criteria include a roll tracking error p95 no worse than 1.86° and pitch p95 no worse than 2.11°. If the verification flight takes place in weaker wind, an improvement in angle tracking may result from the atmospheric conditions rather than from the filter, leading to a false positive conclusion. During the verification flight the hover tilt must therefore be recorded, and the comparison is to be regarded as meaningful only at a similar value. In clearly different conditions the flight should be repeated or the result interpreted with a caveat.

## Course of the flights according to the log

| | Flight 1 | Flight 2 |
|---|---|---|
| Time [log s] | 129 → 367 | 435 → 671 |
| **Real time (GPS)** | **16:45:38 → 16:49:36** | **16:50:44 → 16:54:40** |
| Duration | 238 s (4.0 min) | 236 s (3.9 min) |
| Max. altitude | 24.5 m | 25.7 m |
| Mean throttle over the whole flight | 0.248 | 0.256 |
| Throttle in hover (windows 158–220 s / 461–523 s) | 0.263 | 0.270 |
| VibeY IMU0 mean / p95 / max. | 28.1 / 42.7 / 74.4 | 29.6 / 46.1 / 75.5 |
| Clipping events | 0 | 0 |
| Roll tracking error p95 | 1.84° | 1.86° |
| Pitch tracking error p95 | 3.77° | 2.91° |
| Pack voltage | 16.78 → 16.05 V (min. 15.86) | 16.17 → 15.47 V (min. 15.28) |
| Cumulative consumption | 866 mAh | 1767 mAh |
| GNSS reception | 25–28 sat., HDOP 0.53–0.57 | 28–32 sat., HDOP 0.47–0.54 |

Mode sequence: Land → Stabilize → Loiter → Auto (148–432 s) → Loiter → Auto (451–679 s) → Loiter.

Balance for the whole session: voltage 16.78 → 15.57 V, minimum 15.28 V, 1768 mAh drawn, maximum current 20.6 A. Two full mission runs fit on one pack, and the maximum current was 47% lower than during the manual flight of 19 August (20.6 A versus 38.8 A), because the autonomous profile is smooth.

## Repeatability validation

The spectra from the first and second flight differ by less than 1.6 dB at every peak. This confirms the usefulness of the mission as a comparison baseline; without such confirmation a comparison of the state before and after the filter would be worthless.

Confirmation in the log data: throttle in hover 0.263 versus 0.270 (2.7% difference), roll tracking error p95 1.84° versus 1.86°, VibeY p95 42.7 versus 46.1.

## Spectral measurement

Sensor ICM45686, sampling 3224.69 Hz, no gaps in the data.

| Peak (X axis) | Flight 1 | Flight 2 |
|---|---|---|
| 96 Hz | −30.9 dB | −32.5 |
| 177 Hz | −26.4 | −26.5 |
| 213 Hz | −26.9 | −27.1 |
| 243 Hz | −21.2 | −22.2 |

The second harmonic covers the band 369–486 Hz.

The four peaks correspond to the four motors running at different speeds. The ratio of the extreme frequencies is 1.37, and the ratio of C1 throttle to C3 throttle is 1.30. The ArduPilot documentation describes such a picture as the signature of yaw torque imbalance; it is the same phenomenon as the 95 µs difference between the diagonal outputs, observed in the frequency domain.

## Parameter changes made after the session

Values entered, not verified in flight:

```
INS_HNTCH_ENABLE 1 · MODE 1 · FREQ 210 · BW 80 · ATT 40 · REF 0.267 · HMNCS 3
INS_GYRO_FILTER  20 → 40        ← the actual purpose of the change
MOT_HOVER_LEARN  2 → 0          ← freezing the reference value for the filter
MOT_BAT_VOLT_MAX 16.8 · MOT_BAT_VOLT_MIN 13.2
FENCE_ENABLE     1              ← the configuration existed, the switch remained at zero
RC8_OPTION       16 (Auto mode on switch SD)
FLTMODE2 15 (AutoTune) · FLTMODE3 3 (Auto) · FLTMODE5 6 (RTL)
INS_RAW_LOG_OPT  9              ← temporary, to be removed after verification
```

The 96 Hz peak was left untouched; it is 10 dB weaker than the others and is a candidate for a second harmonic notch filter.

## Significant events

| Time [log s] | Event | Interpretation |
|---|---|---|
| 146 | `EKF3 IMU0/IMU1 MAG0 in-flight yaw alignment complete` | Repeated heading alignment after take-off, the same as on 19 August |
| 402 | `Arm: Auto mode not armable` | Arming attempt in Auto mode. Consistent with the take-off procedure, which provides for arming in Loiter mode and starting the mission only with switch SD |
| 414 | `PreArm: Hardware safety switch` | Routine event |
| — | No `GPS Glitch or Compass error` message in the field | Consistent with the supposition; the symptom occurred that day indoors |

## Observations recorded during the session

| Issue | Conclusion |
|---|---|
| The KML export contains neither the return to the take-off point nor the speed commands | Verify the mission from the `.plan` file |
| The Filter Review tool uses absolute time, and the record starts at 90.2 s | Count analysis windows from the record time |
| `MOT_HOVER_LEARN = 2` caused the value to drift from 0.35 to 0.2667 over two days | Freeze at 0, because it is the reference value for the filter |
| `GPS1_TYPE` spontaneously took the value 0, and `COMPASS_DEC` was reset to zero | Check after every parameter-change session |
| The pack percentage indicator counts consumption from power-on | Go by voltage; a pack in storage state (15.24 V) indicated 99% |
| Switch SB overrides SD | Moving SB aborts the mission regardless of the SD position, and switching SD again will not resume it, because ArduPilot responds to a change of position, not to its state |

## Baseline for the filter verification flight

The baseline is log 7. Thresholds established on manual flights do not carry over to autonomous mode: under manual control the commanded angle comes from the sticks and changes stepwise, whereas in autonomous mode it is generated by the controller and the profile is smooth.

| | Baseline per document | Baseline from log (IMU0) | Threshold |
|---|---|---|---|
| VibeY mean | 30.3 | 28.1 / 29.6 | <20 |
| VibeY p95 | 44.8 | 42.7 / 46.1 | <30 |
| Spectrum 177–243 Hz | full amplitude | — | attenuated |
| Roll tracking error p95 | 1.86° | 1.84° / 1.86° | no worse |
| Pitch tracking error p95 | 2.11° | 3.77° / 2.91° | no worse |
| Altitude hold error p95 | 0.38 m | — | no worse |

The last two rows are decisive. The parameter `INS_GYRO_FILTER` was raised from 20 to 40 Hz, which reduces the phase lag but passes more noise into the control loop. A deterioration in angle tracking would mean that the harmonic notch filter does not cover a sufficiently wide band.

The values in the "from log" column were computed over the whole arming period, and those in the "per document" column over selected hover windows. The difference in the pitch error p95 (3.77° versus 2.11°) arises because the full flight includes the square circuit, which the hover window does not. During the verification flight the same mission segment must be compared.
