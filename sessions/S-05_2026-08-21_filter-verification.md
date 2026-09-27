# S-05: Session card, 21 Aug 2026

**Type:** harmonic notch filter verification flight · **Platform:** 2 · **Firmware:** ArduCopter 4.7.0
**Log:** `log_8_2026-8-21-19-56-38.bin` (124 MB) · **Ground telemetry:** `2026-08-21 19-56-56.tlog`
**Configuration:** `ariadne_v2_20aug2026_2020.params` (harmonic notch filter, `INS_GYRO_FILTER = 40`)
**In the E1–E3 dataset:** no (tuning session)

---

## Conditions

| | |
|---|---|
| Location | Field at Kuźnica Kiedrzyńska, 50.914028 N / 19.086457 E |
| Pilot in command | Filip Pepliński |
| Observer (VLOS role) and telemetry operator | Szymon P. Pepliński |
| Wind (GM816 anemometer) | **1–2 m/s** |
| Illuminance (GM1010) | **58 lx at the start → 21 lx at the end of the session**, i.e. within about nine minutes |
| Session time (from GPS time in the log) | **19:48:01 – 19:56:24** |
| Air and pack temperature, Kp index | [TO BE COMPLETED] |
| DroneTower check-in | [TO BE COMPLETED] |
| GNSS quality criterion | Met: 18–27 satellites, HDOP 0.50–0.64 |

## Course of the flights

Two runs of the mission `S-04_Test1.plan` were flown in Auto mode, the same as on 20 August.

| | Flight 1 | Flight 2 |
|---|---|---|
| Time [log s] | 141.1 → 379.9 | 413.1 → 644.8 |
| **Real time (GPS)** | **19:48:01 → 19:52:00** | **19:52:33 → 19:56:24** |
| Duration | 239 s (4.0 min) | 232 s (3.9 min) |
| Max. altitude | 25.1 m | 25.2 m |
| Mean throttle | 0.253 | 0.261 |
| VibeY IMU0 mean / p95 / max. | 25.2 / 36.3 / 82.6 | 24.1 / 34.5 / 54.4 |
| Clipping events | 0 | 0 |
| Roll tracking error p95 (whole flight) | 1.43° | 1.46° |
| Pitch tracking error p95 (whole flight) | 2.05° | 2.22° |
| Pack voltage | 16.77 → 15.98 V (min. 15.76) | 16.11 → 15.44 V (min. 15.23) |
| Cumulative consumption | 891 mAh | 1788 mAh |
| GNSS reception | 18–24 sat., HDOP 0.53–0.64 | 24–27 sat., HDOP 0.50–0.54 |

Mode sequence: Loiter → Auto (160–408 s) → Loiter → Auto (427–647 s) → Loiter.
Session balance: 16.77 → 15.54 V, minimum 15.23 V, 1790 mAh drawn, maximum current 19.8 A.

Events: heading alignment after take-off (161 and 162 s), `Arm: Auto mode not armable` at 404 s, as on 20 August, consistent with the procedure of arming in Loiter mode.

---

## Result of the filter verification

### Comparison of whole flights against the acceptance criteria

| | LOG 7 (baseline, 20 Aug) | LOG 8 (21 Aug) | Threshold | Assessment |
|---|---|---|---|---|
| VibeY mean IMU0 | 28.1 / 29.6 | 25.2 / 24.1 | <20 | not reached |
| VibeY p95 IMU0 | 42.7 / 46.1 | 36.3 / 34.5 | <30 | not reached |
| Roll error p95 | 1.84° / 1.86° | **1.43° / 1.46°** | no worse than 1.86° | met |
| Pitch error p95 | 3.77° / 2.91° | 2.05° / **2.22°** | no worse than 2.11° | met in flight 1, exceeded by 5% in flight 2 |

### Comparison of the same mission segment: 60 s hover at 15 m

The tuning document requires comparing **the same mission segment**, because the full flight includes the square circuit and the hover window does not. Below is the first hover window from each run.

| | LOG 7, run 1 | LOG 8, run 1 | LOG 7, run 2 | LOG 8, run 2 |
|---|---|---|---|---|
| Roll error p95 | 0.72° | 0.79° | 0.82° | 0.77° |
| Pitch error p95 | 1.49° | 1.06° | 1.17° | 1.30° |
| **Altitude error p95** | **0.16 m** | **0.28 m** | **0.21 m** | **0.29 m** |
| Mean \|pitch\| (wind indicator) | 1.10° | 3.02° | 1.43° | 2.55° |
| Mean \|roll\| (wind indicator) | 4.50° | 1.43° | 4.24° | 1.66° |

### Interpretation

**In the dynamic segments the filter helped.** The tracking error computed over the whole flight improved clearly: roll from 1.84–1.86° to 1.43–1.46°, pitch from 3.77–2.91° to 2.05–2.22°. Since the full flight includes the square circuit and the hover window does not, the improvement concerns above all the motion phase, i.e. the phase in which raising `INS_GYRO_FILTER` from 20 to 40 Hz was meant to reduce the phase lag. The hypothesis that the harmonic notch filter would cover a sufficiently wide band was confirmed in this respect.

**The result is however burdened with three caveats and should not be announced as a clean success.**

First, **the conditions favoured the verification flight**. The resultant hover tilt today was about 3.3° versus 4.6° on 20 August, and the anemometer showed 1–2 m/s versus 2–3 m/s. The wind also blew from a different direction, which is visible in the swap of roles between the axes: on 20 August the roll channel was loaded (|roll| 4.2–4.5°), and today the pitch channel (|pitch| 2.6–3.0°). Part of the improvement therefore comes from the weather, not from the filter. This is exactly the risk noted in card S-04 before the flight.

Second, **the altitude hold error in hover deteriorated by 40–75%**, from 0.16 and 0.21 m to 0.28 and 0.29 m. The direction of the change is opposite to the other metrics and occurs in both runs, so it is not a coincidence. It requires explanation before autotune.

Third, **the VibeY thresholds were not reached and were probably badly chosen**. VibeY describes the vibration level measured by the accelerometer, i.e. a physical phenomenon. The harmonic notch filter acts on the signal passed to the controller and does not remove vibration of the structure. Expecting a drop from 28 to below 20 solely through a change in filtering had no basis. The drop of 13–20% that actually occurred most likely results from the lighter wind and lower load on the propulsion. **To be decided: whether VibeY should be an acceptance criterion for the filter at all.**

### Conclusion

The filter can be regarded as verified to the extent to which it was meant to be verified: it did not worsen angle tracking despite raising `INS_GYRO_FILTER`, and in the motion phase it improved it. It is not a clean measurement, however, because the atmospheric conditions could not be repeated.

**Recommendation: repeat the flight in wind similar to 20 August** (resultant hover tilt 4–5°) or note in the documentation that the comparison was made in more favourable conditions, and by how much.

---

## Finding on the illuminance axis

The session took place at dusk and yielded the first measurement in the band where the expected operating threshold of optical flow lies.

| Session | Time | Illuminance |
|---|---|---|
| 20 Aug | 16:45 → 16:54 | 2450 lx |
| 18 Aug | 16:21 → 18:46 | 1330 lx |
| 19 Aug | 19:25 → 19:33 | 355 lx |
| **21 Aug** | **19:48 → 19:56** | **58 → 21 lx** |

The values of 58 and 21 lx fall within the range that protocol §2.1.1 describes as "dusk, 10–100 lx". The session thus gave a fourth measurement point on the LUX axis, spanning four orders of magnitude.

**Operational finding of major importance for E1 planning.** Illuminance fell from 58 to 21 lx, i.e. by **64% within nine minutes** (19:48–19:57, confirmed by GPS time from the log). Converted to a single run lasting a minute and a half, this gives a drop of the order of 11%. Protocol §8 requires rejecting a run in which the illuminance changed by more than 30%. This means that:

- a single run at dusk fits within the criterion, but with a small margin;
- **a matrix cell at a given illuminance holds for two, at most three runs**, after which the conditions pass into the next cell;
- repetitions of one dusk cell cannot be collected in a single session. They must be spread over successive days, at the same time of day, which with the required five repetitions means five evenings for one cell.

This is a logistical constraint that the protocol does not account for, and which concerns the most important part of the matrix. It requires a decision before the start of E1: either the dusk cells are carried out in a hall with controlled lighting (protocol §2.1.1 warns that this changes the surface and introduces a confound), or a smaller number of repetitions is adopted for them and reported openly.

**To be checked before planning the dusk cells:** the legal requirements for flights after sunset. Protocol §11 leaves this question open, and today's session lasted from 19:48 to 19:56, i.e. at a time when sunset in the second half of August had already occurred or was just occurring.

---

## Open after this session

- [ ] Explain the deterioration of the altitude hold error in hover (0.16–0.21 → 0.28–0.29 m)
- [ ] Decide whether VibeY is the right acceptance criterion for the filter
- [x] `INS_RAW_LOG_OPT` = 0 from 23 Aug. Log 10 is 27 MB
- [x] Snapshots made: `ariadne_v2_22aug2026_1519.params`, `ariadne_v2_23aug2026_1237.params`
- [ ] Possible repetition of the verification flight in wind similar to 20 August
- [ ] Autotune (`RC8_OPTION` 16 → 17), calm day, more than one pack
