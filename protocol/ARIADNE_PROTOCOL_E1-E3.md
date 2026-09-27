# Measurement campaign protocol E1-E3
*English translation (20 Sep 2026) of the Polish original frozen on 7 Aug 2026, kept in `docs/pl/protocol/`. In case of doubt the Polish text is binding.*

**Project:** Ariadne
**Research question RQ1:** operational envelope of optical-flow navigation in GNSS-denied environments
**Protocol version:** 1.0, 2026-08-07
**Dataset freeze:** 2026-11-15

---

## 0. Guiding principle

This document is written before the first measurement and, once frozen, is not modified.

If during the campaign it turns out that some element requires a change, the change is permitted, but it must be recorded in the log together with the date and the justification, and the data from before and after the change must be analysed separately. This distinction separates an experiment from data collection.

---

## 1. Aim and problem statement

### 1.1 Question

Under what conditions does navigation based on an optical-flow sensor stop delivering a position usable for controlling a small drone in a GNSS-denied environment?

### 1.2 What the work does not claim

The work does not claim that a drone for tunnel inspection has been built. The work measures the operating limits of a specific, low-cost sensor configuration and publishes those limits together with the dataset.

### 1.3 Final result

- A map of the operating envelope: the ranges of illuminance, surface type, altitude and speed within which navigation maintains the required accuracy
- A model of the probability of navigation failure as a function of conditions
- An open dataset of raw logs with metadata

---

## 2. Variables

### 2.1 Independent variables (factors)

| Factor | Symbol | Levels (proposed) | How controlled |
|---|---|---|---|
| Illuminance | LUX | see 2.1.1 | lux meter at ground level, measured before and after the run |
| Surface type | SURF | asphalt, grass, smooth concrete, low-texture surface | choice of site |
| Altitude above ground | ALT | 1 m, 2 m, 4 m | set in AltHold mode, verified with TFmini-S |
| Horizontal speed | VEL | 0 (hover), 0.5 m/s, 1.5 m/s | commanded, verified from the log |

**2.1.1 Illuminance levels.** Do not set them arbitrarily. In phase E1, determine experimentally the threshold at which `FLOW_QUAL` starts to fall, and only then distribute the levels around it. Starting point for the reconnaissance: full sun (of the order of 10 000 to 100 000 lx), overcast (1 000 to 10 000 lx), dusk (10 to 100 lx), night with artificial lighting (1 to 10 lx).

Note: the LUX axis is the hardest logistically, because in the field it depends on the time of day and the weather. Consider whether the night cells should be carried out in a hall or under a roof with controlled lighting. Such a solution changes the surface, however, and introduces a confound, so it must be recorded.

### 2.2 Dependent variables (metrics)

**Primary:**
- Position drift [m] as the Euclidean distance between the position estimated by EKF3 (source: optical flow) and the position from the recorded GNSS, which is not included in the estimate, measured at t = 15, 30, 60 s from the moment of the source switch

**Derived:**
- Drift rate [m/s] as the slope of a straight line fitted to the drift in the 10 to 60 s window
- Position RMSE over the whole run window
- CEP50 and CEP95 for the 60 s horizon, aggregated per matrix cell

**Binary:**
- FAILURE = 1 if any of the following events occurred during the run: drift exceeded 5 m before 60 s elapsed, EKF3 reported loss of the estimate, the pilot had to take over control for safety reasons

**Diagnostic (not a result, serves interpretation):**
- `FLOW_QUAL` (flow quality, statistics: median, 10th percentile)
- TFmini-S rangefinder reading and its availability
- Measured illuminance
- Wind speed

### 2.3 Controlled variables (frozen for the duration of the campaign)

- ArduPilot firmware version, a specific number, no updates until 15 November
- The complete parameter set, saved as a file and versioned
- Take-off mass, checked on a scale before every session
- Propellers, the same type, replaced only when damaged, replacement recorded
- Mounting height and orientation of the sensors
- Accelerometer and magnetometer calibration, performed once, verified every session

### 2.4 Confounding variables, measured but not controlled

Wind (anemometer, measured before every run), temperature, humidity, battery state of charge at the start of the run, battery pack number.

---

## 3. Experimental design

### 3.1 Feasibility problem, to be considered before planning the matrix

The full matrix of 4 surfaces × 4 illuminance levels × 3 altitudes × 3 speeds comprises **144 cells**. With 5 repetitions this gives **720 runs**. At a realistic 4 to 6 runs per battery pack and 3 packs per session, that is about 15 runs per session, i.e. **48 sessions**. That number cannot be achieved in the window up to 15 November.

For this reason the campaign has a three-stage structure, and that is how the designations E1, E2, E3 are to be understood.

The realistic budget comprises about **150 to 200 runs** at two sessions per week over 6 to 7 weeks. The experimental design must fit within this budget.

### 3.2 E1: screening (about 30 runs, 2 to 3 sessions)

**Aim:** to establish which factors matter at all, and to determine the illuminance threshold roughly.

A 2^4 factorial design (the two extreme levels of each factor), 2 repetitions, plus a descending illuminance series at the most favourable configuration of the remaining factors.

**E1 result:** a ranking of the factors by their effect on drift, a rough LUX threshold, confirmation that the measurement procedure works.

### 3.3 E2: main matrix (about 90 to 120 runs, 6 to 8 sessions)

**Aim:** to measure the dependence of drift on the factors that E1 identified as significant.

If E1 shows, as is likely, that illuminance and surface dominate while altitude and speed have a secondary effect, the matrix reduces to:

4 LUX levels × 4 surfaces × 5 repetitions = **80 runs**, at a fixed altitude of 2 m and in hover.

To this is added a control series checking the effect of altitude and speed: 3 ALT × 3 VEL × 3 repetitions = 27 runs at one reference combination of LUX and surface.

### 3.4 E3: locating the boundary (about 40 runs, 3 to 4 sessions)

**Aim:** to locate precisely the threshold at which the probability of failure exceeds 50 percent.

Densified measurement points around the threshold detected in E2, with 8 to 10 repetitions per point, because the variance is largest near the threshold.

### 3.5 Randomisation and blocking

**Randomisation:** the order of runs within a session is drawn at random, and not carried out in ascending order of the factor value. Perform the draw before the session and record it in the session card.

**Blocking:** a session constitutes a block. Within one session, try to fit a complete repetition of the set of cells, rather than all repetitions of one cell. Otherwise the session effect (weather, state of the battery packs, the pilot's condition) will be confounded with the factor effect.

**Repetitions:** a minimum of 5 per cell in E2, a minimum of 8 near the threshold in E3.

---

## 4. Reference measurement and uncertainty budget

### 4.1 Method

ArduPilot EKF3 with source switching. `EK3_SRC1` configured for GNSS (normal flight), `EK3_SRC2` for optical flow (measurement run). Switching in flight with an RC switch.

GNSS remains enabled and is logged throughout, but after the switch to SRC2 it is not included in the estimate. The recorded GNSS track constitutes the reference measurement against which the drift of the optical-flow estimate is computed.

### 4.2 Limitation that must be stated in the paper

GNSS without RTK correction has a horizontal accuracy of the order of **1 to 3 m** (CEP), depending on the number of satellites and the PDOP. This value is significant in relation to the drifts being measured.

**Consequences:**
- Drifts below about 2 m lie at the resolution limit of the method and must be reported with this caveat
- Drifts of the order of 5 m and larger are measured reliably
- For every run, log the number of satellites and the PDOP, and reject runs with PDOP above 2.0

**Strengthening the method, if the budget allows:** an RTK module (u-blox ZED-F9P) with corrections from the ASG-EUPOS network via NTRIP gives centimetre accuracy and removes this limitation. It remains under consideration as an extension, not as a necessary condition.

### 4.3 Averaging of the starting position

Before switching the source, hold a hover in the GNSS mode for a minimum of 20 s. The position averaged over this window is the zero point for the drift measurement. Averaging reduces the effect of a momentary GNSS error on the result.

---

## 5. Platform configuration

### 5.1 Freeze

Before the first E1 run:

- Save the full ArduPilot parameter list to a file, name with the date, to the repository
- Note the firmware version (exact number and hash)
- Weigh the drone in flight configuration, record the result
- Perform and record the calibrations: accelerometer, magnetometer, compass, ESC
- Perform FlowCal, i.e. the optical-flow calibration, and record the resulting parameters

### 5.2 Verification before every session

The checklist is in annex A. The verification covers above all: mass, no changes in the parameters (comparison with the reference file), cleanliness of the optical-flow sensor and rangefinder lenses, condition of the propellers, condition of the battery packs.

### 5.3 Sensors

- **Optical-flow sensor:** Holybro PMW3901, `FLOW_TYPE` as per the documentation, orientation facing down
- **Rangefinder:** Benewake TFmini-S, `RNGFND1_ORIENT = 25`
- **Methodological note:** the rangefinder is used by EKF3 to scale the optical flow, so its failure is a failure of the whole navigation channel. Log its availability separately and treat loss of reading as a separate failure category.

---

## 6. Procedure for a single run

Duration: about 3 minutes, of which 90 s of flight.

1. **Measurement of conditions.** Lux meter at ground level at the site of the run, three readings, record the median. Anemometer, 30 s, record the mean and the maximum.
2. **Recording of metadata** in the run card (annex B): run number, matrix cell, time, conditions, battery pack number, starting voltage.
3. **Take-off** in the GNSS mode. Climb the drone to the commanded altitude ALT.
4. **Stabilisation**, a minimum of 20 s of hover with GNSS. This window defines the zero point.
5. **Switch to SRC2** (optical flow). Note the time of the switch, even though it will also be recorded in the log.
6. **Execution of the run**, 60 s:
   - for VEL = 0: hover with no stick input
   - for VEL > 0: flight at constant speed along a straight line, out and back
7. **Completion:** switch back to SRC1, landing.
8. **Emergency abort:** if the drift endangers the surroundings, take over control immediately. Mark the run as FAILURE and record the reason.
9. **Saving the log** with the run number in the file name.

### 6.1 Rules that must not be broken

**Do not correct drift with the sticks during the run.** Any intervention invalidates the measurement. If an intervention proves necessary, the run is terminated and marked as FAILURE.

**Do not change parameters between runs.** A parameter change starts a new series, recorded in the log.

**Do not reject a run after seeing the result.** The rejection criteria are listed in section 8 and are applied on the basis of the data on conditions, not on the outcome.

---

## 7. Session procedure

1. **Before departure:** random draw of the run order, printout of the session card, check of the forecast (wind up to 5 m/s), charged battery packs, free space on the dataflash
2. **On site:** checklist (annex A), measurement of baseline conditions, photograph of the site and the surface
3. **Calibration flight:** one run under reference conditions (good illumination, asphalt, 2 m, hover) at the start of every session. It serves to detect systematic drift between sessions. This run does not enter the matrix; it constitutes a quality control.
4. **Execution of the runs** in the drawn order
5. **After the session:** download of the logs, backup, completion of the log, preliminary review of the data

### 7.1 Criterion for aborting a session

Abort the session if: the wind exceeds 5 m/s, the lighting conditions change during the execution of one cell, the drone is damaged, doubts arise about the sensor's functioning.

---

## 8. Run rejection criteria

A run is rejected from the analysis if, **before the result was seen**, any of the following was found:

- PDOP above 2.0 or number of satellites below 10
- Wind above 5 m/s in the run window
- Pilot intervention for reasons other than drift (obstacle, bystander)
- Detected hardware fault
- Incomplete log
- Change of illuminance during the run by more than 30 percent

Rejections are recorded together with the reason. The number of rejections and their distribution over the matrix cells go into the paper, because systematic rejection in one cell is itself information.

---

## 9. Data recording

### 9.1 Naming

```
ARIADNE_E{phase}_{run_number}_{date}_{cell}.bin
```
Example: `ARIADNE_E2_047_20261012_LUX2-SURF1-ALT2-VEL0.bin`

### 9.2 Repository structure

```
/dane
  /logi_surowe        .bin files from the dataflash, unmodified
  /karty_przebiegow   spreadsheet with the metadata of all runs
  /karty_sesji        one per session
  /parametry          frozen configuration, versioned
  /zdjecia            surfaces, sites, configuration
/analiza
  /skrypty
  /wyniki
/dziennik.md
```

### 9.3 Backups

After every session: a copy to a second medium and to the cloud. Loss of the dataset two weeks before the freeze means the end of the project.

---

## 10. Analysis plan, fixed before data collection

This section is recorded in advance to avoid fitting the analysis to the results.

### 10.1 Descriptive analysis

For every cell: median and interquartile range of the drift at 60 s, CEP50, CEP95, failure rate.

Plots: drift as a function of time (curves for the individual cells), drift at 60 s as a function of illuminance broken down by surface, `FLOW_QUAL` as a function of illuminance.

### 10.2 Failure model

Logistic regression: probability of failure as a function of log10(LUX), surface type, altitude and speed.

**Main numerical result:** the illuminance value at which the predicted probability of failure is 50 percent, with a confidence interval, separately for each surface.

### 10.3 Analysis of factor effects

ANOVA or its non-parametric equivalent, depending on the distribution of the residuals (the distribution must be checked, not assumed). Report effect sizes, not only significance.

### 10.4 What not to do

Do not choose significance levels after seeing the results. Do not remove outliers without a justification from section 8. Do not change the primary metric after data collection has started.

---

## 11. Safety

- Flights exclusively in the open category in accordance with the A1/A3 qualifications, terrain without bystanders
- Measurement altitudes up to 4 m, but always with a margin for taking over control
- Carry out runs with a predicted high risk of navigation failure (low illuminance) in an open space, away from obstacles, because the drone will drift away
- Pilot with a thumb on the source switch throughout the run
- A second observer at every session
- Flights in low light and after dusk: before planning these cells, check the legal requirements for night flights

---

## 12. Schedule

**Change of 23 Aug 2026.** The schedule is moved forward by about four weeks. The change was introduced **before the first run entering the dataset**, so it does not divide the data into before and after periods in the sense of §0.

Justification: the maximum illuminance at this latitude falls from 84 400 lx at the end of August to 38 600 lx in mid-November (clear sky, sun at noon). The upper cells of the LUX axis are achievable only in September. The lower cells are easier in November than in September, because an overcast afternoon holds 300–1000 lx for hours, whereas the August dusk falls at 7.27 %/min (measurement S-08).

Order: **bright cells first, dark cells at the end of the campaign.**

| Period | Task |
|---|---|
| by 31 Aug | control flight after tuning, **a run without GNSS for the full 60 s**, 5 to 10 trial runs (not entering the dataset) |
| by 10 Sep | surface reconnaissance: asphalt, smooth concrete, low-texture surface |
| 1 to 20 Sep | **E1**, screening: bright cells first |
| 20 to 25 Sep | analysis of E1, decision on the shape of the E2 matrix |
| 25 Sep to 25 Oct | **E2**, main matrix |
| 25 Oct to 10 Nov | **E3**, locating the boundary: dark cells |
| **15 Nov** | **dataset freeze** |
| 15 Nov to 20 Dec | analysis and written paper |
| by 31 Dec | submission |

Previous version: E1 from 1 Oct, E2 from 15 Oct, E3 from 5 Nov.

**Reserve:** the schedule contains no buffer for bad weather and failures. A loss of 30 percent of the planned sessions should be assumed. For this reason it is better to plan three sessions per week and cancel some of them than to plan two and run out of time.

---

## Annex A: session checklist

**Before departure**
- [ ] Battery packs charged and measured (cell voltages)
- [ ] Dataflash empty or with spare space
- [ ] Parameters consistent with the reference file
- [ ] Drawn run order printed
- [ ] Lux meter and anemometer, batteries working
- [ ] Run cards, pen
- [ ] Forecast: wind up to 5 m/s

**On site, before the first flight**
- [ ] Take-off mass consistent with the reference
- [ ] Optical-flow sensor and rangefinder lenses clean
- [ ] Propellers undamaged, tightened
- [ ] Sensor and GPS connectors secured
- [ ] GNSS fix established: minimum 10 satellites, PDOP below 2.0
- [ ] Rangefinder reading sensible (hand test)
- [ ] `FLOW_QUAL` non-zero when the drone is lifted
- [ ] Terrain without bystanders
- [ ] Calibration flight performed

---

## Annex B: run card

| Field | Value |
|---|---|
| Run number | |
| Phase (E1/E2/E3) | |
| Date and time | |
| Matrix cell (LUX/SURF/ALT/VEL) | |
| Illuminance [lx], median of 3 | |
| Wind [m/s], mean / maximum | |
| Surface, verbal description | |
| Battery pack number | |
| Starting voltage [V] | |
| Satellites / PDOP | |
| Log file name | |
| Run accepted / rejected | |
| Reason for rejection | |
| Pilot's remarks | |

---

## Closing remarks

The greatest risk of this campaign is organisational, not technical. With 150 runs spread over 15 sessions, inconsistency comes easily: a changed parameter, a different procedure, a missing item of metadata. Discipline in filling in the cards means more than the number of runs.

100 runs carried out rigorously are worth more than 200 uncertain ones. The jury will assess the quality of the research design, not the volume of the dataset.
