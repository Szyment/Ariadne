# Platform 2: sensor positions

*Measured 22 Aug 2026. Protocol §2.3 lists "sensor mounting height and orientation" among the variables frozen for the duration of the campaign, and until now they had not been recorded anywhere.*

## Measurement

The vehicle stands on its landing gear, on a level surface. Both sensors are bolted **under** the plate, the flight controller **on** the plate.

| Sensor | Height above ground |
|---|---|
| TFmini-S laser rangefinder (two windows) | **17 cm** |
| PMW3901 optical-flow sensor (one lens) | **18 cm** |

## Agreement with the software settings

Parameter state read from log 6 (19 Aug):

| Parameter | Value | Meaning |
|---|---|---|
| `RNGFND1_GNDCLR` | 0.17 m | rangefinder clearance above the ground after landing |
| `RNGFND1_MIN` / `RNGFND1_MAX` | 0.10 / 6.00 m | measurement range; hence the 6 m ceiling in runs without GNSS |
| `RNGFND1_ORIENT` | 25 | pointing down |
| `RNGFND1_POS_X / Y / Z` | 0.120 / 0.000 / −0.021 m | position relative to the controller |
| `FLOW_POS_X / Y / Z` | 0.095 / 0.000 / −0.031 m | position relative to the controller |
| `FLOW_ORIENT_YAW` | 0 | the sensor's "forward" axis coincides with the nose of the vehicle |

**`RNGFND1_GNDCLR` agrees with the measurement to the centimetre.** The height difference between the sensors also agrees: `FLOW_POS_Z − RNGFND1_POS_Z` is −0.010 m, that is, the optical flow lies 1 cm higher than the rangefinder, exactly as follows from the measurement of 18 cm against 17 cm. The relative geometry of the two sensors is therefore described correctly.

## Error in the settings: the wrong origin of the reference frame was assumed

**Established 22 Aug.** `BOM.md` §8 states explicitly that the values of `FLOW_POS_*` and `RNGFND1_POS_*` were calculated relative to the **mid-thickness of the battery**. This explains the negative Z values: the battery hangs under the lower plate, so the sensors are indeed above it, by 2.1 and 3.1 cm.

The problem is that ArduPilot measures these distances from something else. The documentation gives the rule unambiguously: if the `INS_POS1/2/3` parameters are non-zero, all other offsets are measured from the centre of gravity; if they are zero, the origin of the frame is the **inertial unit, that is, the centre of the flight controller board**. In log 6 all nine `INS_POS` values are zero.

The origin of the frame is therefore the Pixhawk standing on the upper plate, not the battery hanging under the lower one. The difference in the vertical axis is about 10 cm.

### Two ways to fix it

**First way, recommended: recalculate everything relative to the flight controller.** We leave `INS_POS` at zero and give the sensor positions relative to the Pixhawk.

The advantage is that the geometry stops depending on the battery. The pack is a part removed at every charge and its position changes between sessions; this is exactly what `analysis/balance.py` checks. Basing the sensor reference frame on something that moves introduces an error that nobody will find afterwards.

**Second way: leave the battery as the origin of the frame and fill in `INS_POS1/2/3`** with the position of the Pixhawk relative to the centre of the pack. Then the existing values become correct. However, this requires entering nine additional parameters and keeping them consistent with the position of the pack, so it makes no sense for this project.

### Values to enter, first way

The height of the inertial unit above the ground, denoted H below, follows from the frame measurement and from the dimensional drawing of the Standard Baseboard v2A (`pixhawk6x_baseboard_v2a_dimensions.png`).

| Component | Value | Source |
|---|---|---|
| Upper frame plate above the ground | 246 mm | measurement 22 Aug |
| Total height of the assembly above the mounting surface | 23.43 mm | drawing, front view |
| Height of the controller module (FMU) itself | 16.8 mm | Holybro data |
| Underside of the module above the mounting surface | 23.43 − 16.8 = 6.6 mm | calculation |
| Centre of the module, that is, the position of the inertial unit | 6.6 + 8.4 = **15.0 mm** | calculation |
| **H** | 246 + 15 = **261 mm** (from the frame documentation: 262 mm) | |

The controller module sits in a recess of the baseboard and protrudes above it by about 5 mm, hence the impression that "the Pixhawk is inside, a few millimetres higher".

### Measurement of 22 Aug and values to enter

The reference point, that is, (0, 0, 0), is the **centre of the flight controller module**, the square block with ribs and an arrow, recessed into the baseboard. Not the ground and not the frame plate: these serve only as a common ruler from which both heights are measured, so that they can then be subtracted.

Dimensional sketch: `sensor_geometry_sketch.png` in this directory.

| Item | Above the ground | Ahead of the module centre |
|---|---|---|
| **Centre of the controller module, (0, 0, 0)** | **257 mm** | 0 |
| TFmini-S rangefinder | 171 mm | 112 mm |
| PMW3901 optical-flow sensor | 180 mm | 88 mm |
| GNSS antenna on the mast | 300 mm (54 mm above the upper plate, to mid-height) | 96 mm **behind** the module (71 mm to the edge + 25 mm radius) |

The height of the module itself is 16.6 mm, so it extends from 248.7 to 265.3 mm above the ground. This does not enter the calculation; 257 is already the centre.

### Complete set of values

| Parameter | Currently | To enter | From |
|---|---|---|---|
| `RNGFND1_POS_X` | 0.120 | **+0.112** | measurement |
| `RNGFND1_POS_Y` | 0.000 | 0.000 | axis of symmetry |
| `RNGFND1_POS_Z` | −0.021 | **+0.086** | 257 − 171 |
| `FLOW_POS_X` | 0.095 | **+0.088** | measurement |
| `FLOW_POS_Y` | 0.000 | 0.000 | axis of symmetry |
| `FLOW_POS_Z` | −0.031 | **+0.077** | 257 − 180 |
| `GPS1_POS_X` | 0.000 | **−0.096** | measurement, antenna at the rear |
| `GPS1_POS_Y` | 0.000 | 0.000 | mast on the axis |
| `GPS1_POS_Z` | 0.000 | **−0.043** | 257 − 300, antenna higher |

X axis forward, Y right, Z down. A sensor located below the controller has positive Z.

Values are given to three decimal places. Rounding to two loses part of the nine millimetres of vertical difference between the sensors, and this difference in particular is known precisely, because it comes from two measurements made with the same ruler.

### Check against the frame documentation

Landing gear 215 + lower plate 2 + spacing 28 + upper plate 2 gives 247 mm to the upper surface of the upper plate, against a direct measurement of 246 mm. The baseboard with the module raises the reference point by a further 11 mm, to 257 mm. The breakdown agrees with the measurement.

### Why this is not a minor detail

`FLOW_POS_*` is used to subtract from the optical-flow reading the component that comes from the rotation of the vehicle rather than from its translation. The correction has the form of the cross product of the angular velocity and the sensor position vector. A 10 cm error in this vector gives, at an angular velocity of 30°/s, about 0.05 m/s of velocity error, that is, about four metres of drift in a run lasting a minute and a half. The measured effect is of the same order of magnitude.

The error acts only in runs without GNSS, because only there does optical flow enter the estimator as a velocity source, which is exactly where the result of the work lies.

## An untested item: `FLOW_ORIENT_YAW`

The parameter is 0, which means that the "forward" axis of the flow sensor is supposed to coincide with the nose of the vehicle. **This has never been checked in flight**, because optical flow has not yet been used as a velocity source; `EK3_SRC2_VELXY = 5` is waiting for the first run without GNSS.

An error of 90° or 180° in this parameter shows no symptom as long as the vehicle flies on GNSS. In the first run without GNSS it shows immediately: the estimator receives a velocity pointing the wrong way and the vehicle drives off. The risk concerns the first run of the campaign, that is, the worst possible moment.

**Check before the first run, on the ground, without propellers:** arm the vehicle on the table, lift it by hand to a height of about 1 m above a patterned surface, move it slowly forward, then to the right. In the log (`OF` message, fields `flowX` and `flowY`) check whether forward motion gives a reading in the X axis and rightward motion in the Y axis, and whether the signs agree. This takes five minutes and removes a risk that cannot otherwise be detected before take-off.

---

## GNSS antenna position not set

`GPS1_POS_X`, `GPS1_POS_Y` and `GPS1_POS_Z` are zero, even though the antenna stands on a mast at the **rear** of the vehicle, that is, in a different place from the flight controller. Zero tells the estimator that the antenna is exactly at the reference point.

Why this matters in this project in particular: GNSS reception is here the **reference measurement**, against which the estimator drift in runs without GNSS will be calculated. An antenna offset by twenty-odd centimetres from the reference point introduces a constant offset into the reference track, and during rotations additionally a velocity error equal to the cross product of the angular velocity and the lever arm; at 30°/s and 0.2 m that is about 0.1 m/s. The measured effect is of the order of metres, so this does not vanish in the noise.

To be measured, with the vehicle standing on its landing gear, relative to the underside of the controller housing:

| Parameter | What to measure | Sign |
|---|---|---|
| `GPS1_POS_X` | distance of the antenna rearward from the controller | **negative** |
| `GPS1_POS_Y` | sideways offset, if the antenna is not on the axis | positive to the right |
| `GPS1_POS_Z` | height of the antenna above the controller | **negative** |

Measure to the centre of the antenna, not to the base of the mast.

## Things that turned out to be set correctly

- `RNGFND1_GNDCLR` = 0.17 m, agrees with the measurement
- Direction of the X axis: the sensors are at the front of the vehicle, so positive `RNGFND1_POS_X` and `FLOW_POS_X` have the right sign; only the magnitude remains to be corrected
- `COMPASS_DEC` = 0.1053 rad, that is, **6.0° east**, the magnetic declination for this location, set automatically from the geomagnetic field model. Closes the item from Annex C §5.4
- `COMPASS_ORIENT` = 6 (Yaw270), `COMPASS_EXTERNAL` = 1: external magnetometer in the GNSS module, orientation declared

---

## Sources of dimensions

- Dimensional drawing of the Standard Baseboard v2A: `pixhawk6x_baseboard_v2a_dimensions.png` in this directory
- Controller module height 16.8 mm: Holybro data for the Pixhawk 6X
- Frame heights: Holybro X500 V2 manual, §8.1 "Mechanical Specifications", https://manuals.plus/m/151a8940d716f84da87464df4e269308dc47305d0f42fc40e425b0d8658f7b0f_optim.pdf
- The 500 mm wheelbase from the same table confirms the value of 354 mm adopted in `analysis/balance.py` as the distance between the axes of the front and rear motors (500 · cos 45°)

---

## Note on the GNSS antenna

The value of `GPS1_POS_*` should describe the **phase centre of the antenna**, that is, roughly the centre of the ceramic patch inside the housing, not the outline of the dome nor the base of the mast. The difference is a few millimetres and at the accuracy needed here it does not matter, but if the measurement is ever repeated it must be made to the same point.

The significance of this correction in this project is greater than usual: GNSS reception is the **reference measurement**, against which the estimator drift in runs without GNSS will be calculated. An antenna offset by 71 mm rearward and 43 mm upward introduces a constant offset into the reference track, and during rotations additionally a velocity error equal to the cross product of the angular velocity and the lever arm. At 30°/s and a lever arm of 83 mm this gives about 0.04 m/s.

---

## Entry status: closed 22 Aug 2026

All nine values entered and confirmed in the parameter snapshot `firmware/ariadne_v2_22aug2026_1519.params`:

| Parameter | Value |
|---|---|
| `RNGFND1_POS_X` | 0.112 |
| `RNGFND1_POS_Y` | 0.000 |
| `RNGFND1_POS_Z` | 0.086 |
| `FLOW_POS_X` | 0.088 |
| `FLOW_POS_Y` | 0.000 |
| `FLOW_POS_Z` | 0.077 |
| `GPS1_POS_X` | −0.096 |
| `GPS1_POS_Y` | 0.000 |
| `GPS1_POS_Z` | −0.043 |

The earlier snapshot `ariadne_v2_22aug2026_1514.params` is kept as an intermediate state; it still had `FLOW_POS_X` = 0.095 and `GPS1_POS_X` = −0.070.

The distances 112 and 88 were measured to the **centres of the sensor modules**, 71 to the **edge of the antenna**; hence the correction of 25 mm, that is, the radius of the M10 module with a diameter of 50 mm. The height of 54 mm was measured to mid-height of the antenna.

`COMPASS_DEC` in both snapshots is 0, because `COMPASS_AUTODEC` = 1 and the declination is set only after a position fix is obtained, and the snapshots were taken without reception. The in-flight value, 0.1053 rad, that is, 6.0° east, remains current.

## `FLOW_ORIENT_YAW`: checked 22 Aug, correct

The parameter is 0 and until 22 Aug it had never been verified, because optical flow had not yet been a velocity source; `EK3_SRC2_VELXY` = 5 is waiting for the first run without GNSS. An error of 90° or 180° shows no symptom as long as the vehicle flies on GNSS, and would reveal itself only in the first second of the first measurement run.

Checked without an additional flight, on the records of 18 and 19 August, with the script `analysis/flow_orientation.py`:

| Pair | log 5 | log 6 |
|---|---|---|
| flowX ↔ bodyX | +0.46 | +0.74 |
| flowY ↔ bodyY | +0.59 | +0.70 |
| flowX ↔ bodyY | −0.11 | −0.03 |
| flowY ↔ bodyX | −0.01 | −0.02 |

The matching pairs are high and positive, the crossed pairs are in the noise. The orientation is correct, nothing needs to be changed.

Incidentally: `OF.Qual` in both flights over grass stands at the maximum of the range (255), and in the ground trials of log 3 it varied from 0 to 218. The driver reports the true reading quality, so its drop at dusk will be a measurable indicator of approaching the sensor's operating limit.


## Update 28 Aug 2026: payload plate moved 1 cm forward

The plate with the optical-flow sensor, the rangefinder and the cameras was moved 1 cm forward relative to the centre of the vehicle (during the mounting of the onboard computer and after rotating the camera). Only the X components change, by +0.010:

| Parameter | Before | After |
|---|---|---|
| `FLOW_POS_X` | 0.088 | **0.098** |
| `RNGFND1_POS_X` | 0.112 | **0.122** |

`Y`, `Z` and `RNGFND1_GNDCLR` unchanged; the shift was purely horizontal. The camera geometry measured in step A3 of the post-mounting procedure applies relative to the new plate position; a measurement made before the shift requires adding 1 cm to the X component.
