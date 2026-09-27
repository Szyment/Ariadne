# Annex C: wind measurement

*Annex to the protocol `ARIADNE_PROTOCOL_E1-E3.md`. In force from the first run of campaign E1.*

In this experiment wind is a confound (protocol §2.4) and at the same time the basis of the run rejection criterion (§8). Until now only a bare number was recorded, for example "2–3 m/s", with no information on how long the measurement lasted, at what height and at which point of the session. Such a record does not allow two sessions to be compared or a run rejection to be defended. This annex establishes the procedure.

---

## 1. The instrument and its limits

Anemometer **Benetech GM816**: vane impeller, range 0–30 m/s, resolution 0.1 m/s, declared accuracy ±5%. Built-in NTC thermometer: −10 to +45 °C, ±2 °C. Three display modes: **CU** (instantaneous), **AVG** (average), **MAX** (largest since switch-on).

Three things must be known before this instrument is trusted.

**The declared accuracy of ±5% applies to the middle of the range, not to the lower end.** A vane impeller has a starting speed: below a certain value it simply does not start, and between the starting speed and roughly twice that value it under-reads. The manufacturer does not state the starting speed. For instruments of this class it is of the order of 0.3–0.7 m/s. Practical conclusion: **readings below 1 m/s are treated as "below 1 m/s", not as a number.** A record of "0.4 m/s" suggests an accuracy that this instrument does not have at this end of the range.

**The averaging period in AVG mode is not documented.** The manual states that the mode exists; it does not state after what time the average refreshes or whether it counts from switch-on. The procedure below therefore does not rely on the instrument's internal logic: **we define the averaging window ourselves by switching the instrument on at the start of the measurement and off at its end.** Used this way, AVG is the average over our whole window regardless of how the manufacturer implemented it.

**The instrument does not give direction.** Direction is determined by rotating the instrument, which is a discretionary reading. Direction is therefore recorded in 45° sectors, not in degrees, and checked independently from the flight log (§7).

---

## 2. Measurement site

**A fixed point for the whole campaign.** A driven stake or another permanent marker, whose position is recorded once in coordinates and which stands in the same place through all sessions. A measurement taken once next to the car and once in the middle of the field describes two different places, not two different weathers.

Requirements for this point:

- distance from any obstacle (tree, car, building, haystack) of at least **ten times its height**; for a tree 10 m high that is 100 m;
- at least **10 m from the aircraft**, and the measurement taken **before arming or after the motors are shut down**, never with the propellers running (the wash from the rotors reaches many propeller diameters);
- exposed from the direction the wind is blowing from.

**How to hold it.** Stand **facing the wind** and extend the arm forward, so that the instrument is closer to the wind than the person measuring. One's own body placed on the windward side shields the impeller and can under-read by several tens of percent.

---

## 3. Measurement height

**We measure at a height of 2.0 m**, an arm raised above the head of an adult. The height is recorded in the card, because without it the number means nothing.

Height matters because wind speed increases with distance from the ground. For a surface covered with short grass or stubble, the profile follows a logarithmic relation in which the speed at height *z* relates to the speed at the reference height as the logarithms of the ratios to the surface roughness (of the order of 0.03 m for short grass). This gives the following conversion factors from the measurement at 2 m:

| Height | Multiplier relative to the measurement at 2 m |
|---|---|
| 6 m: altitude of the runs without GNSS | ×1.26 |
| 10 m: reference height in meteorology and in ERA5 | ×1.38 |
| 15 m: hover in mission `S-04_Test1.plan` | ×1.48 |
| 25 m: square flight in mission `S-04_Test1.plan` | ×1.60 |

The multipliers are approximate; they depend on the surface roughness, which changes between mown grass and stubble, and on the stability of the surface layer. We treat them as an order of magnitude, not as a correction to the measurement. **The raw reading from 2 m is recorded in the card.** The conversion to the altitude of the run is done in the analysis, explicitly, not in the field.

Practical conclusion for planning: a reading of 3 m/s at ground level means roughly 3.8 m/s at the 6 m altitude and about 4.5 m/s at the mission hover height. The margin to the 5 m/s threshold is therefore smaller than it looks on the anemometer.

---

## 4. Measurement duration and mode

One measurement is **60 seconds**. A shorter one does not average the gusts: in gusty wind a single instantaneous reading can differ from the average by a factor of two.

Procedure for a single measurement:

1. Take position at the fixed point, facing the wind, instrument at a height of 2.0 m.
2. **Switch the instrument on.** This zeroes the AVG and MAX readings and starts our window.
3. Hold still, correcting the direction only as much as needed to keep the impeller in the wind.
4. After 60 seconds read **AVG**, **MAX** and **CU** in turn.
5. **Switch the instrument off.** The next measurement starts with a new switch-on.

When we measure:

- **before the first run of the session** (the measurement goes into the session card);
- **before every run**, immediately before arming;
- **after every run**, immediately after landing and shutting down the motors.

With eight runs in a session this gives seventeen minutes of wind measurement alone. This is a cost that has to be included in the session plan, not something that will shrink on its own. If it proves impossible to sustain, it is permissible to reduce to a measurement before and after a **pair** of runs carried out immediately one after the other, but this is then recorded in the card, because the sampling density of the conditions changes.

---

## 5. Direction

The GM816 anemometer does not give direction. The "rotate until it reads the most" method is worse than it seems: the impeller responds to the component of the wind along its axis, and this varies with the cosine of the angle. At a deviation of 20° the reading falls by 6%, which is less than the scatter of the wind itself. The maximum is therefore flat and cannot be hit more precisely than to about ±30°. Something else is used to determine direction.

### 5.1 Direction indicator on the stake (primary method)

To the fixed measurement point, at a height of 2 m, we tie a **ribbon 30–50 cm long**; surveyor's tape or a strip of light foil about 2 cm wide is enough. It responds from roughly 0.5 m/s, shows the direction continuously, and changes and gusts are visible on it.

Reading the direction:

1. Stand **behind the ribbon, looking along it** in the direction in which it is blown.
2. Hold the phone level, at arm's length, **at least 5 m from the car, from the aircraft and from the battery packs**; the magnets in the motors and the current in the wires deflect the phone's compass by several tens of degrees.
3. Read the azimuth and **subtract 180°**; the ribbon shows the direction the wind blows to, and we record the direction it blows from.
4. Record a **45° sector** (N, NNE, NE, ...). The accuracy of this method does not justify degrees.
5. Take a photograph of the ribbon. The photograph is a record that cannot be challenged later, and it costs a second.

A better version, if you decide to buy one: a **small windsock** on a mast, like those at model airfields. It shows the direction unambiguously and its angle of deflection gives a rough speed class. Cost of the order of a hundred zloty, and it tidies up session safety at the same time.

### 5.2 In light wind there is simply no direction

Below roughly 1 m/s the ribbon droops and the direction ceases to be defined. **We then record "variable" and do not guess.** This applies especially to dusk sessions, in which the wind usually dies down; the session of 21 August had 1–2 m/s and was already at the limit. Entering a sector that was not seen is worse than admitting that there was no direction.

### 5.3 What actually enters the analysis: angle relative to the run axis

The absolute azimuth is needed for comparisons with ERA5 and for detecting errors. For the experiment itself something else matters more: **whether the wind was a headwind, crosswind or tailwind relative to the direction of the run**. Optical flow and the controller respond differently to wind along the axis of motion than across it, and this is the quantity that can distort the result.

In the run card we therefore record both: the absolute sector and the angle relative to the run axis in three classes, **headwind (±45°), crosswind (45–135°), tailwind (135–180°)**. The relative class can be determined more reliably than the azimuth, because it is seen directly: it is enough to compare the direction of the ribbon with the direction in which the aircraft is to fly.

### 5.4 Magnetic declination

The phone's compass may show magnetic or true north, depending on the app. In central Poland the difference is of the order of a few degrees east, which is less than the width of a sector, so it does not matter for the sector classification. It does matter when comparing with ERA5, which gives direction relative to true north. **Value for the field at Kuźnica Kiedrzyńska: 6.0° east.** Read on 22 Aug 2026 from the parameter `COMPASS_DEC` = 0.1053 rad in log 6, where ArduPilot sets it automatically from the geomagnetic field model for the aircraft's coordinates. Magnetic direction plus 6° gives the direction relative to true north, i.e. the one used by ERA5.

### 5.5 Post-flight check

The direction determined with the ribbon is compared after the session with two independent sources: the aircraft tilt in hover (`analysis/wind_from_log.py`) and the ERA5 reanalysis (`analysis/session_weather.py`). Agreement within one sector means that all three work. Details in §8.

## 6. What goes into the card

Into the **run card** (`sessions/TEMPLATE_run_card.md`):

| Field | Source |
|---|---|
| Wind before the run: AVG / MAX [m/s] | 60 s measurement before arming |
| Wind after the run: AVG / MAX [m/s] | 60 s measurement after landing |
| Wind direction (45° sector) | determined by rotating |
| Measurement height [m] | 2.0 by default; entered every time |

Into the **session card** go the range over the whole session and information on whether the conditions were steady.

**Conditions are considered unsteady** if the two measurements bracketing one run differ in AVG by more than **1.0 m/s** or if the direction changed by more than one sector. This is not a reason to reject the run, but it must be recorded, because it enters the analysis as a covariate.

---

## 7. Rejection criterion and which number decides

Protocol §8 rejects a run with wind **above 5 m/s in the run window**. As long as there was no procedure, it was also not known which number settles this. Decision:

**The larger of the two AVG values decides, the one from before the run and the one from after it, measured at a height of 2.0 m.** MAX serves to describe gustiness, not for rejection; a single gust does not invalidate a run, because gusts occur in all conditions and rejecting on MAX would cut out whole matrix cells.

### 7.1 Decision of 23 Aug 2026

**The 5 m/s threshold applies at the altitude of the run, not at the measurement point.** The quantity being measured is the wind in which the aircraft flies.

The runs without GNSS have an altitude of 6 m, imposed by `RNGFND1_MAX`. The conversion factor from 2.0 m to 6 m is ×1.26 (§6), so:

> **Field criterion: AVG at a height of 2.0 m must not exceed 4.0 m/s.**

One number, no conversion in the field. It corresponds to 5.0 m/s at the altitude of the run.

The cost of this decision is zero in the light of the data so far. All August sessions fall below the threshold: 18 Aug 2.5 m/s, 19 Aug 2–3, 20 Aug 2–3, 21 Aug 1–2, 22 Aug 2, 23 Aug 3. None would have been rejected.

The criterion applies to AVG, not to MAX, in accordance with the paragraph above.

---

## 8. Independent check from the flight log

The script `analysis/wind_from_log.py` computes from the log the wind direction and an indicator of its strength, based on the averaged tilt of the aircraft in hover windows. An aircraft holding position tilts towards the direction the wind blows from.

This check is independent of a human, covers the whole duration of the run and applies to the altitude of the run, not the height of a hand. It does not replace the anemometer; it does not give speed in metres per second, because that would require knowledge of the aircraft's aerodynamic drag, which has not been determined.

**We run it after every session** and compare three directions: from the anemometer, from the flight log and from ERA5 (`session_weather.py`). Agreement within one sector means that all three work. A discrepancy is a signal: either the measurement was taken on the lee side, or the compass needs calibration, or the measurement was taken at a different time than the flight.

### 8.1 Check by drift in AltHold mode

A method simpler than tilt in hover and requiring no script. In AltHold the aircraft holds altitude and attitude but does not hold position, so with the sticks in the neutral position it drifts exactly with the wind.

Execution: hover at 3–4 m, sticks neutral, **10 seconds without touching the transmitter**. The course in which the aircraft drifted away is the direction **to which** the wind blows. We record this direction minus 180° in the card.

From the log this is extracted from the fields `GPS.Spd` and `GPS.GCrs` in windows in which `RCIN.C1` and `RCIN.C2` stay within 25 µs of 1500 and `ATT.Roll` and `ATT.Pitch` do not exceed 0.5°.

The method has one limitation: it separates wind from a force associated with the airframe only when the aircraft's heading changes during the measurement. Without a rotation both give the same result. **We take the measurement twice, rotating the aircraft by 180° between attempts.** A drift direction fixed to the ground means wind; a direction that rotates together with the nose means a levelling error or tilt of the motor mounts.

### 8.2 Mistake of 25 Aug 2026

The evening direction reading was recorded as 293°. The drift in AltHold in the same session had a direction of 282–303° (twelve windows, logs 15 and 16), which corresponds to wind **from 110–125°**. The reading was recorded reversed, by 180°.

The midday measurement of the same day, 124°, agrees with the drift from log 14 and with the aircraft tilt (130°). The azimuth of the turn-around point in `missions/S-10_Drift1.plan` was computed from the midday value and remains correct.

Conclusion for the procedure: **every recorded wind direction requires a check against the log of the same session.** A single hand reading is not data.

---

## 9. To be done once, at the next session

- [ ] Check how the AVG mode behaves: hold the instrument for 60 s, read AVG, hold for another 60 s without switching off and read again. If the second value is the average over 120 s, the procedure of §4 (switch-on at the start of the measurement) is correct. If AVG refreshes every few seconds, several CU readings must be noted instead.
- [ ] Determine the practical starting speed of the impeller: in calm weather, check at what reading the instrument starts to respond at all.
- [ ] Establish and mark the fixed measurement point, record its coordinates in the session card.
- [ ] Check the magnetic declination for the field's coordinates and enter it in §5.
- [ ] Settle the threshold of §7.

---

## 10. Wind computed by the autopilot itself: a possibility we deliberately do not use in the campaign

ArduPilot can compute wind speed and direction without an airspeed sensor, from a drag model of the aircraft. It requires three parameters: `EK3_DRAG_BCOEF_X` (mass divided by frontal area), `EK3_DRAG_BCOEF_Y` (mass divided by side area) and `EK3_DRAG_MCOEF` (drag from the propellers, usually 0.1–1.0). The result goes into the `WIND` message in telemetry and into the `VWN` and `VWE` fields of the `XKF2` message in the flight log.

**Current state: disabled.** In all logs so far, `EK3_DRAG_BCOEF_X`, `EK3_DRAG_BCOEF_Y` and `EK3_DRAG_MCOEF` have the value 0, and the `VWN` and `VWE` fields in `XKF2` are zero throughout the record. Checked in logs 3 and 4 of 18 August.

**Why we do not enable it for the duration of the campaign.** The drag model does not serve only to compute wind; it is an additional observation fed into the estimator and allows it to maintain velocity by dead reckoning when there is no GNSS reception. This is exactly the capability whose error growth we study in RQ1. Enabling the drag model would reduce the drift in runs without GNSS and thereby distort the main result of the work. It must not be done during the campaign, and if it is ever enabled, it becomes part of the configuration under study and must be declared explicitly.

**What it is nevertheless worth using for, once, before the parameter freeze.** The script `wind_from_log.py` gives tilt and horizontal acceleration, but not metres per second, because we do not know the aircraft's drag. Estimation by the EKF gives metres per second. One tuning flight with the drag model enabled would allow the coefficient converting tilt to speed to be fitted, after which the model can be disabled and the conversion factor applied to all campaign logs, without touching the estimator during the measurements.

Order of steps, should the team decide to do this:

- [ ] Weigh the aircraft in flight configuration (known: 1698 g) and measure the frontal and side areas from photographs against a grid or a ruler. Keep the photographs; they are material for the paper
- [ ] Compute `EK3_DRAG_BCOEF_X` and `_Y` as mass [kg] divided by area [m²]
- [ ] Determine `EK3_DRAG_MCOEF` from flight, starting from 0.5
- [ ] Fly in Loiter in wind measured with the anemometer, compare `XKF2.VWN/VWE` with the reading and with the tilt
- [ ] Fit the conversion factor tilt → m/s and record it in `wind_from_log.py`
- [ ] **Zero all three parameters and confirm in the log that `VWN`/`VWE` have returned to zero** before the first E1 run starts

### 10.1 Second consequence of this decision: the barometer

Disabling the aerodynamic drag fusion also rules out **compensation of the wind effect on the barometer** (`BARO1_WCF_ENABLE`), because it uses the same wind estimate from EKF3.

Scale of the error measured on 23 Aug (session S-07, wind 3 m/s with gusts to 5.6): the barometric altitude exceeded the rangefinder reading by **0.9–1.9 m** in flight at 1.7 m. The calculation agrees with the observation: dynamic pressure q = ½ · 1.19 · 5.6² = 18.7 Pa at a gradient of 11.7 Pa/m gives 1.6 m of apparent altitude.

**Run altitude below 6 m is recorded from the rangefinder, not from `CTUN.Alt`.**
