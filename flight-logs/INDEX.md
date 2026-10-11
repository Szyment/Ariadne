# Index of flights and logs

*The one place where a log is tied to a session, a configuration and a card. State as of 21 Aug 2026.*

Purpose of the document: without an index the set of logs is a catalogue of files, not a dataset. The index answers three questions that file names do not: which log corresponds to which flight, under which configuration it was recorded, and which files contain the same data.

---

## Platform 2, ArduPilot (`flight-logs/platform-2-ardupilot/`)

| Log | Date | Flight times (GPS) | Arming events | Ground telemetry | Parameters in force | Card |
|---|---|---|---|---|---|---|
| `log_2_2026-8-18-16-27-49.bin` | 2026-08-18 | 16:21 (no arming) | 0 | — | `18aug2026_1734`* | S-02 |
| `log_3_2026-8-18-17-08-22.bin` | 2026-08-18 | 16:58:48 – 17:08:07 | 6 | `2026-08-18 17-33-35.tlog` | `18aug2026_1734` | S-02 |
| `log_4_2026-8-18-17-58-36.bin` | 2026-08-18 | 17:57:57 – 17:58:21 | 2 | `2026-08-18 18-15-11.tlog` | `18aug2026_1740` | S-02 |
| `log_5_2026-8-18-18-49-02.bin` | 2026-08-18 | 18:41:15 – 18:46:44 | 2 | `2026-08-18 18-48-18.tlog` | `18aug2026_1740` | S-02 |
| `log_6_2026-8-19-19-33-42.bin` | 2026-08-19 | 19:25:41 – 19:33:29 | 2 | `2026-08-19 19-33-55.tlog` | `18aug2026_1740` | S-03 |
| `log_7_2026-8-20-16-54-54.bin` | 2026-08-20 | 16:45:38 – 16:54:40 | 2 | `2026-08-20 16-55-16.tlog` | `20aug2026_2015` | S-04 |
| `log_8_2026-8-21-19-56-38.bin` | 2026-08-21 | 19:48:01 – 19:56:24 | 2 | `2026-08-21 19-56-56.tlog` | `20aug2026_2020` | S-05 |

> **The timestamp in the file name is the end of the session, not the start.** Established on 21 Aug by comparing file names with the GPS time recorded in the logs: the name is created when the log is closed, i.e. some ten to twenty seconds after the last disarming (log 7: last disarming 16:54:40, name 16-54-54; log 6: 19:33:29 versus 19-33-42; log 8: 19:56:24 versus 19-56-38). The exception is log 5, closed 2 min 18 s after disarming, because the controller remained powered.
>
> The "flight times" column comes from the GPS field in the log (week and millisecond of week, converted to local time allowing for 18 leap seconds). It is the only absolute reference in this dataset and **all comparisons with field measurements (illuminance, wind, time of day) must be counted from it**. Script: `analysis/`.

\* the assignment of parameters to `log_2` is inferred from the time and not confirmed: the 17:34 parameter snapshot was made after this log. **To be confirmed.**

`log_1` does not exist. It is a gap in the numbering, unexplained in the documentation. It remains to be settled whether the file was deleted, overwritten, or never created.

Note on parameters: parameter snapshots were made irregularly and not after every session, so the "log ↔ configuration" assignment is partly a reconstruction and not a record. From E1 onwards the rule from protocol §5.1 applies: **a parameter snapshot before the first run and after the last, in every session.**

### Parameter snapshots

| File | Changes relative to the previous one | What changed |
|---|---|---|
| `ariadne_v2_18aug2026_1734.params` | — (reference) | first record |
| `ariadne_v2_18aug2026_1740.params` | 25 | |
| `ariadne_v2_20aug2026_1145.params` | 28 | |
| `ariadne_v2_20aug2026_1148.params` | 19 | |
| `ariadne_v2_20aug2026_2015.params` | 46 | the largest jump, the AUTO session |
| `ariadne_v2_20aug2026_2020.params` | 18 | harmonic notch filter, `INS_GYRO_FILTER` 20→40, `MOT_HOVER_LEARN`→0. State before the verification flight |

All six files have different checksums, so none is a duplicate. The "what changed" column is to be completed; without it the differences have to be computed anew every time.

---

## Platform 1, Betaflight (`flight-logs/platform-1-betaflight/`)

| File | Log sessions | Size | Status |
|---|---|---|---|
| `BTFL_BLACKBOX_LOG_20260720_231913...BBL` | 9 | 4.6 MB | unique |
| `BTFL_BLACKBOX_LOG_20260724_130252...BBL` | 1 | 560 KB | unique |
| `BTFL_BLACKBOX_LOG_20260724_144229...BBL` | 11 | 5.3 MB | unique |
| `BTFL_BLACKBOX_LOG_20260726_164226...BBL` | 2 | 636 KB | unique |
| `BTFL_BLACKBOX_LOG_ARIADNE_20260726_175927...BBL` | 5 | 5.0 MB | unique |
| `BTFL_BLACKBOX_LOG_ARIADNE_20260816_195821...BBL` | 3 | 1.2 MB | **last flight of platform 1.** The name carries the download date (16 Aug), not the flight date. Contains the incident that ended with the loss of the platform on 26 Jul |

### The `last/` directory contains duplicates and unique data

The contents of this directory must not be treated uniformly. State verified byte by byte on 21 Aug:

| File | Size | Relation to the rest of the dataset |
|---|---|---|
| `btfl_all.bbl` | 2 000 896 B | exact concatenation of `btfl_001` + `002` + `003` + `004`, 100 % redundant |
| `btfl_001.bbl` | 462 848 B | content also present in the file of 16 Aug |
| `btfl_002.bbl` | 460 800 B | content also present in the file of 16 Aug |
| `btfl_003.bbl` | 1 075 200 B | does not occur in any other file, unique data |
| `btfl_004.bbl` | 2 048 B | does not occur in any other file, unique data |

> The table was made because of the following risk: without it, an analysis covering the whole directory would count the flights from `btfl_001`, `002` and `all` twice, and one case even three times. In a dataset released publicly this is an error that undermines the results, not a minor housekeeping matter.
>
> Recommendation: delete nothing, in line with the project rule, but in analysis and publication of the dataset exclude `btfl_all.bbl` as derived and treat `last/` as archival material and not as a source.

---

## Convention in force from E1

Tuning logs keep their original names and do not enter the dataset. Measurement logs from E1 onwards are named according to protocol §9.1:

```
ARIADNE_E{phase}_{run_number}_{date}_{cell}.bin
```

Example: `ARIADNE_E2_047_20261012_LUX2-SURF1-ALT2-VEL0.bin`

Each run receives a row in this index on the day of the session, not later.

---

## Integrity

Checksums of all project files (except the ArduPilot clone) are in `CHECKSUMS.sha256` in the root.

Verification:

```bash
shasum -a 256 -c CHECKSUMS.sha256 | grep -v ': OK$'
```

An empty result means that nothing has changed or been corrupted.

- Run after every session and after every copy to another medium.
- Regenerate the manifest after deliberately adding files.

## E1 measurement runs, mapping run → log → window (from 12 Sep 2026)

Protocol §9.1 assumed one log per run. In practice one log covers several flights (a log is created on arming, and in the session of 12 Sep the aircraft was not disarmed between runs within a pack). Instead of copying 20 MB under each name, this table defines the dataset: run = file + log time window from `Using EKF Source Set 2` to `Using EKF Source Set 1`. The script `analysis/drift_analysis.py` cuts out the windows automatically.

| Run | Cell | Log | SRC2 window [log s] | Card | Status | Wind from log: tilt / direction / p95 |
|---|---|---|---|---|---|---|
| S-17 calibration | LUX1-SURF1-ALT3-VEL15 | `log_29_2026-9-12-13-27-46.bin` | 398.1–481.7 | S-17 | outside the dataset (§7.3) | — |
| E1-001 | LUX1-SURF1-ALT3-VEL15 | `log_29_2026-9-12-13-27-46.bin` | 670.4–745.9 | S-17 | accepted | — |
| E1-002 | LUX1-SURF1-ALT3-VEL15 | `log_29_2026-9-12-13-27-46.bin` | 967.0–1046.8 | S-17 | accepted | 1.26° / 257° / 3.3° |
| E1-003 | LUX1-SURF1-ALT3-VEL15 | `log_30_2026-9-12-13-43-46.bin` | 141.4–230.0 | S-17 | accepted, LUX flag | — |
| E1-004 | LUX1-SURF1-ALT3-VEL15 | `log_30_2026-9-12-13-43-46.bin` | 405.7–486.9 | S-17 | accepted, LUX flag | 0.73° / 292° / 2.4° |
| E1-005 | LUX1-SURF1-ALT3-VEL15 | `log_30_2026-9-12-13-43-46.bin` | 644.5–714.6 | S-17 | accepted, LUX flag | 1.55° / 312° / 2.8° |
| E1-006 | LUXd (~2480 lx)-SURF1-ALT3-VEL15 | `log_31_2026-9-12-18-50-42.bin` | 176.5–270.2 | S-18 | accepted | — |
| E1-007 | LUXd (~1750 lx)-SURF1-ALT3-VEL15 | `log_31_2026-9-12-18-50-42.bin` | 452.9–531.4 | S-18 | accepted | 0.65° / 225° / 1.5° |
| E1-008 | LUXd (~1210 lx)-SURF1-ALT3-VEL15 | `log_31_2026-9-12-18-50-42.bin` | 674.6–769.6 | S-18 | accepted | 0.59° / 236° / 2.1° |
| E1-009 | LUXd (~700 lx)-SURF1-ALT3-VEL15 | `log_32_2026-9-12-19-05-18.bin` | 145.4–232.5 | S-18 | accepted | — |
| E1-010 | LUXd (~506 lx)-SURF1-ALT3-VEL15 | `log_32_2026-9-12-19-05-18.bin` | 374.6–466.3 | S-18 | accepted | 0.65° / 210° / 1.7° |
| E1-011 | LUXd (~323 lx)-SURF1-ALT3-VEL15 | `log_32_2026-9-12-19-05-18.bin` | 616.8–712.0 | S-18 | accepted | 0.69° / 212° / 1.8° |
| S-19 calibration | LUX1-SURF2-ALT3-VEL15 | `log_33_2026-9-13-12-22-06.bin` | 182.2–277.8 | S-19 | outside the dataset (§7.3) | 3.21° / 209° / 6.0° (session) |
| E1-012 | LUX1-SURF2-ALT3-VEL15, course 137° (upwind outbound) | `log_33_2026-9-13-12-22-06.bin` | 430.5–522.1 | S-19 | accepted | as above |
| E1-013 | LUX1-SURF2-ALT3-VEL15, course 137° (upwind outbound) | `log_33_2026-9-13-12-22-06.bin` | 719.7–815.9 | S-19 | accepted | as above |
| E1-014 | LUX1-SURF2-ALT3-VEL15, course 23° (downwind outbound) | `log_34_2026-9-13-12-40-38.bin` | 199.0–297.2 | S-19 | accepted, final drift 5.6 m | as above |
| E1-015 | LUX1-SURF2-ALT3-VEL15, course 23° (downwind outbound) | `log_34_2026-9-13-12-40-38.bin` | 487.8–585.1 | S-19 | accepted, final drift 6.2 m | as above |
| E1-016 | LUX1-SURF2-ALT3-VEL15, course 23° (downwind outbound) | `log_34_2026-9-13-12-40-38.bin` | 788.7–885.2 | S-19 | accepted | as above |
| E1-017 | LUXd (~125 lx)-SURF1-ALT3-VEL15 | `log_35_2026-9-13-19-09-16.bin` | 188.8–282.5 | S-20 | accepted | 0.60° / 182° / 1.4° (session) |
| E1-018 | LUXd (~77.5 lx)-SURF1-ALT3-VEL15 | `log_35_2026-9-13-19-09-16.bin` | 426.5–523.5 | S-20 | accepted | 0.77° / 164° / 1.4° |
| E1-019 | LUXd (~44.1 lx)-SURF1-ALT3-VEL15 | `log_35_2026-9-13-19-09-16.bin` | 654.5–747.3 | S-20 | accepted, flag: OF.Qual < 255 (17 % of samples) | 0.76° / 166° / 1.8° |
| S-20 threshold test | LUXd (~18.3 lx), OF.Qual = 0 | `log_36_2026-9-13-19-18-50.bin` | 146.3–162.7 (EKF failsafe 154.2) | S-20 | outside the dataset; collision with a tree at 195.7 s | — |
| S-21 calibration | LUXd (~1040 lx)-SURF1-ALT3-VEL15, new propellers and A/B | `log_38_2026-9-17-18-53-30.bin` | 259.1–348.8 | S-21 | outside the dataset (§7.3) | 1.0° / 214° / 1.4° |
| E1-020 | LUXd (~646 lx)-SURF1-ALT3-VEL15 | `log_38_2026-9-17-18-53-30.bin` | 550.5–649.1 | S-21 | accepted | 0.6° / 206° / 1.8° |
| E1-021 | LUXd (~377 lx)-SURF1-ALT3-VEL15 | `log_38_2026-9-17-18-53-30.bin` | 835.0–930.7 | S-21 | accepted | 0.4–0.7° / 160–170° |
| E1-022 | LUXd (~140 lx)-SURF1-**ALT15**-VEL15 | `log_39_2026-9-17-19-11-58.bin` | 164.0–247.8 | S-21 | accepted, flag: two factors (ALT + LUX); return 0.732, drift 14.2 m | 0.8° / 186° / 4.9° |
| E1-023 | LUXd (~42.0 lx)-SURF2-ALT3-VEL15 | `log_39_2026-9-17-19-11-58.bin` | 624.9–717.9 | S-21 | accepted, flag: OF.Qual < 255 (45 %) | 1.4° / 185° / 2.4° |
| S-21 test | LUXd (~19.4 lx)-SURF2, OF.Qual 0 in motion | `log_39_2026-9-17-19-11-58.bin` | 840.5–892.3 (EKF failsafe 872.6) | S-21 | outside the dataset; climb to 37 m in AltHold | 0.9° / 160° |
| S-22 calibration | LUX2 (~18 klx)-SURF1-ALT3-VEL15, track T3 | `log_40_2026-9-20-16-23-06.bin` | 154.4–248.2 | S-22 | outside the dataset (§7.3) | 3.1° / 223° / 8.9° (log 40) |
| E1-024 | LUX2 (~20 klx)-SURF1-ALT3-VEL15 | `log_40_2026-9-20-16-23-06.bin` | 473.3–555.5 | S-22 | accepted, final drift 6.8 m | as above |
| E1-025 | LUX2 (~22 klx)-SURF1-ALT3-VEL15 | `log_40_2026-9-20-16-23-06.bin` | 742.5–854.8 | S-22 | accepted | as above |
| E1-026 | LUX2 (~15 klx)-SURF1-ALT3-**VEL075** | `log_41_2026-9-20-16-41-46.bin` | 231.7–369.4 | S-22 | accepted; first VEL075 run | 4.2° / 222° / 5–8° (log 41) |
| E1-027 | LUX2 (~13 klx)-SURF1-ALT3-**VEL075** | `log_41_2026-9-20-16-41-46.bin` | 710.7–859.9 | S-22 | accepted, flag: battery failsafe (Land) on the home leg after A→B→A; return 0.788, drift 10.9 m | as above |
| E1-028 | LUX2 (~11 klx)-SURF1-ALT3-**VEL075** | `log_42_2026-9-20-16-59-12.bin` | 198.0–345.4 | S-22 | accepted | 4.4° / 233° / 6–8° (log 42) |
| E1-029 | LUX2 (~6.5 klx)-SURF1-ALT3-**VEL075** | `log_42_2026-9-20-16-59-12.bin` | 603.0–753.6 | S-22 | accepted | as above |
| E1-030 | LUX2 (~4.3 klx)-SURF2-ALT3-VEL15 | `log_43_2026-9-20-17-14-20.bin` | 165.1–260.7 | S-22 | accepted, flag: wind 3.6–4.1 m/s at the limit; drift 10.6 m | — (no hover window; session SW) |
| E1-031 | LUX2 (~3.2 klx)-SURF2-ALT3-VEL15 | `log_43_2026-9-20-17-14-20.bin` | 373.4–475.3 | S-22 | accepted, flag: wind; drift 11.2 m | — |
| E1-032 | LUX2 (~3.2 klx)-SURF2-ALT3-VEL15 | `log_43_2026-9-20-17-14-20.bin` | 593.0–707.0 | S-22 | accepted, flag: wind; drift 8.6 m | — |
| S-23 calibration | LUXd (~1830 lx)-SURF1-ALT3-VEL15, T3 forward | `log_44_2026-10-2-17-54-06.bin` | 195.6–297.3 | S-23 | outside the dataset (§7.3) | 1.2° / 138° (log 44) |
| E1-033 | LUXd (~3010 lx)-SURF1-ALT3-VEL15, **T3 reversed** (B→A→B) | `log_44_2026-10-2-17-54-06.bin` | 515.2–619.2 | S-23 | accepted | as above |
| E1-034 | LUXd (~2480 lx)-SURF1-ALT3-VEL15, T3 forward | `log_44_2026-10-2-17-54-06.bin` | 815.5–914.2 | S-23 | accepted | as above |
| E1-035 | LUXd (~1510 lx)-SURF1-ALT3-VEL15, T3 reversed | `log_45_2026-10-2-18-11-24.bin` | 168.0–267.7 | S-23 | accepted | 0.9° / 122° (log 45) |
| E1-036 | LUXd (~969 lx)-SURF1-ALT3-VEL15, T3 forward | `log_45_2026-10-2-18-11-24.bin` | 466.9–561.5 | S-23 | accepted | as above |
| E1-037 | LUXd (~753 lx)-SURF1-ALT3-VEL15, T3 reversed | `log_45_2026-10-2-18-11-24.bin` | 764.6–859.0 | S-23 | accepted | as above |
| E1-038 | LUXd (~409 lx, beside the path)-SURF2-ALT3-VEL15, T1 forward | `log_46_2026-10-2-18-26-52.bin` | 140.0–233.7 | S-23 | accepted | 0.7° / 120° (log 46) |
| E1-039 | LUXd (~248 lx)-SURF2-ALT3-VEL15, **T1 reversed** | `log_46_2026-10-2-18-26-52.bin` | 384.1–482.4 | S-23 | accepted | as above |
| E1-040 | LUXd (~118 lx)-SURF2-ALT3-VEL15, T1 forward | `log_46_2026-10-2-18-26-52.bin` | 719.7–815.0 | S-23 | accepted | as above |
| S-24 calibration | LUX2 (~26 klx)-SURF1-ALT3-VEL15, T3 forward | `log_47_2026-10-4-13-51-06.bin` | 216.5–313.0 | S-24 | outside the dataset (§7.3) | 1.6° / 335° (log 47) |
| S-24 test | LUX2 (~19 klx)-SURF1-ALT3-VEL15, T3 reversed, aborted by a flight-mode switch | `log_47_2026-10-4-13-51-06.bin` | 543.8–611.0 | S-24 | outside the dataset | as above |
| E1-041 | LUX2 (~14.5 klx)-SURF1-ALT3-VEL15, T3 reversed | `log_47_2026-10-4-13-51-06.bin` | 826.3–924.7 | S-24 | accepted | as above |
| E1-042 | LUX2 (~12.4 klx)-SURF1-ALT3-VEL15, T3 forward | `log_48_2026-10-4-14-06-06.bin` | 153.2–247.0 | S-24 | accepted | 1.6° / 352° (log 48) |
| E1-043 | LUX2 (~12.4 klx)-SURF1-ALT3-VEL15, **T4 forward** (course 25°) | `log_48_2026-10-4-14-06-06.bin` | 446.7–543.0 | S-24 | accepted; first run on T4 | as above |
| E1-044 | LUX2 (~12.7 klx)-SURF1-ALT3-VEL15, T4 reversed (205°) | `log_48_2026-10-4-14-06-06.bin` | 689.3–785.3 | S-24 | accepted | as above |
| E1-045 | LUX2 (~14.1 klx)-SURF2-ALT3-VEL15, T1 forward | `log_50_2026-10-4-14-28-48.bin` | 276.7–371.7 | S-24 | accepted | 1.6° / 340° (log 50) |
| E1-046 | LUX2 (~13.2 klx)-SURF2-ALT3-VEL15, T1 reversed | `log_50_2026-10-4-14-28-48.bin` | 579.9–672.5 | S-24 | accepted; drift 5.2 m at 77 s | as above |
| E1-047 | LUX2 (~14.6 klx)-SURF2-ALT3-VEL15, T1 forward | `log_50_2026-10-4-14-28-48.bin` | 828.5–928.3 | S-24 | accepted; drift 6.1 m at 44 s | as above |
| E1-048 | LUX2 (~25 klx)-SURF1-**ALT15**-VEL15, T3 forward | `log_51_2026-10-4-14-45-36.bin` | 294.7–379.8 | S-24 | accepted; first daylight run at 1.5 m; drift 6.9 m at 38 s | — (no hover window at 1.5 m) |
| E1-049 | LUX2 (~34 klx)-SURF1-**ALT15**-VEL15, T3 forward | `log_51_2026-10-4-14-45-36.bin` | 620.5–716.7 | S-24 | accepted; drift 7.5 m at 41 s | — |
| S-25 calibration | grass T3 1.5 m plan left from 4 Oct, source set 2 from power-up, aborted by the pilot | `log_52_2026-10-11-12-20-32.bin` | — (no switch message; GNSS from 304.9 s) | S-25 | outside the dataset (§7.3) | 1.3° / 287° (log 52) |
| E1-050 | LUX1 (~62 klx)-SURF1-ALT3-VEL15, **T5 self-test** (course 121°, four 10 m segments with 3 s stops outbound) | `log_52_2026-10-11-12-20-32.bin` | 523.0–638.5 | S-25 | accepted; first run on T5 and first self-test | as above |
| E1-051 | LUX1 (~74 klx)-SURF1-ALT3-VEL15, T5 self-test | `log_52_2026-10-11-12-20-32.bin` | 749.5–866.5 | S-25 | accepted | as above |
| E1-052 | LUX1 (~35 klx)-SURF1-ALT3-VEL15, T5 self-test | `log_53_2026-10-11-12-33-54.bin` | 120.2–229.1 | S-25 | accepted | 1.5° / 274° (log 53) |
| E1-053 | LUX1 (~42 klx)-SURF1-ALT3-VEL15, T5 self-test | `log_53_2026-10-11-12-33-54.bin` | 343.1–454.7 | S-25 | accepted | as above |
| E1-054 | LUX1 (~61 klx)-SURF1-ALT3-VEL15, T5 forward (plain) | `log_53_2026-10-11-12-33-54.bin` | 584.8–680.9 | S-25 | accepted; drift 5.3 m at 60 s | as above |
| E1-055 | LUX1 (~78 klx)-SURF2-ALT3-VEL15, T1 self-test (137°) | `log_54_2026-10-11-12-49-50.bin` | 175.9–287.6 | S-25 | accepted; drift 6.6 m at 60 s | — (no hover window) |
| E1-056 | LUX1 (~85 klx)-SURF2-ALT3-VEL15, T1 self-test | `log_54_2026-10-11-12-49-50.bin` | 395.3–515.3 | S-25 | accepted; drift 5.7 m at the end | — |
| E1-057 | LUX1 (~74 klx)-SURF2-ALT3-VEL15, T1 forward (plain) | `log_54_2026-10-11-12-49-50.bin` | 654.2–743.5 | S-25 | accepted; drift 5.1 m at 60 s | — |
| E1-058 | LUX1 (~39 klx)-SURF1-**ALT15**-VEL15, T3 forward | `log_55_2026-10-11-13-10-06.bin` | 138.2–231.4 | S-25 | accepted; drift 12.3 m at 30 s, 15.2 m at 60 s | — (flights at 1.5 m) |
| E1-059 | LUX1 (~41 klx)-SURF1-**ALT15**-VEL15, T3 forward | `log_55_2026-10-11-13-10-06.bin` | 439.2–530.3 | S-25 | accepted; drift 10.0 m at 30 s, 13.7 m at 60 s | — |
| E1-060 | LUX1 (~55 klx)-SURF1-**ALT15**-VEL15, T3 forward | `log_55_2026-10-11-13-10-06.bin` | 725.3–812.0 | S-25 | accepted; drift 6.5 m at the end | — |

Cell code: LUX1 = full daylight (12 Sep: 34–70 klx, variable cloud cover; 13 Sep: 53–93 klx, 167–221 klx with direct sun on the dome, variable cirrus), SURF1 = fresh grass, not mown, SURF2 = ploughed field (clods with stubble remains, S-19), ALT3 = 3.0 m, VEL15 = 1.5 m/s, VEL075 = 0.75 m/s (`WP_SPD` 0.75 and `DO_CHANGE_SPEED` in the plan, from S-22). LUX2 = overcast daylight (20 Sep: 3120–18 800 lx, cloud cover 7–8/8 after 16:20). LUXd = illuminance descent series (dusk), the lx value = the geometric mean of the measurement before and after the flight, see S-18. Configuration: `ariadne_v2_12sep2026_1113.params`, ArduCopter 4.7.0 (1511f271); from 13 Sep `ariadne_v2_13sep2026_1100.params` (only `FENCE_RADIUS` 70 → 90); from 17 Sep `ariadne_v2_17sep2026_1705.params` (`FENCE_RADIUS` 90 → 120) and a new set of 1045 propellers. ALT15 = 1.5 m.

Wind from log (`wind_from_log.py`, `analysis/results/wind_20260912.md`): resultant tilt in the hover with GNSS immediately before the cut-off, the direction the wind blows from, and the p95 of the instantaneous tilt (gustiness). A covariate for analysis, not a matrix factor; the §8 criterion remains the anemometer. "—" = no hover window ≥ 15 s before the given run (first flight of a pack); the session value then applies: S-17 about 1.1° NW, S-18 about 0.6° SW.
