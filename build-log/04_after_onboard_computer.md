# Platform 2: clearance for flight after installing the onboard computer

*Procedure of 27 Aug 2026, corrected 28 Aug (step C4). Execution: steps A–C passed 28 Aug, mass 1838/1404 g, compasses calibrated, hover throttle 0.282 against the predicted 0.289. Steps D and E passed on the evening of 28 Aug at 2 m/s: `YawOut` +0.017 (threshold 0.098), roll p95 1.15° / pitch 1.26° / altitude 0.35 m, all within the criteria, autotune not needed. Session card S-14. Procedure closed, the aircraft is cleared for measurement flights.*

*Applies to the state after adding the Raspberry Pi 5, two OV5647 cameras, the voltage converter and the harnesses. Perform in the order given; each step records a number on which the next step depends.*

## Why in this order

Mass changes the hover throttle. The hover throttle is at the same time the reference point of the harmonic notch filter (`INS_HNTCH_REF` = `MOT_THST_HOVER` = 0.267), so until the new hover throttle is known, the filter sits beside the peaks it is meant to attenuate. Balance cannot be assessed before the filter is correct, because vibration adds noise to the motor loading. Tuning makes no sense to assess before balance.

---

## A. On the bench, without propellers

**A1. Weigh the aircraft.** Two numbers: with the pack and without the pack. The baseline from 21 Aug is 1698 g and 1263 g. Record in `hardware/BOM.md` §9.

**A2. Check the sensors' field of view.** Neither the computer, nor the cameras, nor the harnesses may enter the field of view of the optical-flow sensor or the rangefinder. The lenses of both sit 17–18 cm above the ground, at the front of the payload plate.

**A3. Measure the camera geometry** relative to the IMU, as was done for the flow sensor: offset in three axes and orientation. Record in `hardware/SENSOR_GEOMETRY.md`. Without this, the position computed from a marker will be offset by a constant that nobody will later be able to guess.

**A4. Check the computer's power supply under load.** Start both cameras and both streams, then on the Raspberry:

```bash
vcgencmd measure_temp
vcgencmd get_throttled
```

Required: `throttled=0x0`. Measure the voltage on the GPIO header pins, not on the voltage converter.

**A5. Raspberry shutdown button.** `dtoverlay=gpio-shutdown` in `/boot/firmware/config.txt`, a momentary button between pin 5 (GPIO3) and ground. Check that pressing shuts the system down and pressing again wakes it. Without this, every unplugging of the pack risks damaging the memory card.

**A6. Check torques and mountings.** The computer, the voltage converter, the fuse holder and the harnesses must be tied to the structure, not hanging loose. A freely hanging wire at 200 Hz vibration works like a pendulum and tears out solder joints.

---

## B. Compass calibration, in the field

**B1.** Compass calibration at the flying site, away from the car and the fence. A switching converter and wires carrying an ampere of current have been added close to the GNSS mast.

**B2.** Record the new calibration offsets. The jump relative to the previous values is in itself information about the size of the disturbance.

Static calibration does not detect a current-dependent disturbance. That is checked only from the log, in step E1.

---

## C. Flight 1: hover throttle

Calm air, altitude above ground effect, that is, at least 3 m.

**C1.** Set `MOT_HOVER_LEARN` = 2 (learns and saves).

**C2.** Hover in AltHold for **60 s**, sticks neutral.

**C3.** Land, disarm, read the new `MOT_THST_HOVER`.

**C4.** **Leave `INS_HNTCH_REF` unchanged** (0.267). Correction of 28 Aug: the `FREQ`/`REF` pair is one measured calibration point, "at throttle 0.267 the vibration peak lies at 210 Hz", and that is a property of the motors and propellers, not of the mass. In throttle-scaling mode the filter computes `FREQ × √(throttle / REF)` by itself, so at a higher hover throttle it follows the higher motor speed. Entering the new throttle into `REF` would anchor the curve at a point that nobody has measured. The original version of this step required the value to be overwritten; it was wrong.

**C5.** `MOT_HOVER_LEARN` back to **0**.

**Safety criterion:** if the new hover throttle exceeds **0.45**, the aircraft is too heavy, and no further flights are to be performed, only mass removed. At 0.2667 on 21 Aug the margin was large, but the maximum thrust of the motors has still not been measured and remains an open item.

---

## D. Flight 2: balance

**D1.** Fly `S-06_Balance1.plan`, the same mission on four fixed courses.

**D2.** From the log, compute the motor loading on each course and compare the diagonals, as in the analysis of 22 Aug described in `hardware/YAW_ASYMMETRY.md`.

**Criterion:** the steady component of `YawOut` no worse than **0.098**, that is, the value after the mount correction of 22 Aug. A degradation means that the computer has shifted the centre of gravity and the payload plate or the pack must be moved.

---

## E. Flight 3: tuning and filter check

**E1.** Fly `S-04_Test1.plan`, the same profile used to compare tunings.

**E2.** From the log, extract and compare with the baseline of 23 Aug:

| Quantity | Baseline |
|---|---|
| `VIBE` mean, IMU0 | from the flight of 23 Aug |
| `VIBE` p95, IMU0 | from the flight of 23 Aug |
| roll tracking error, p95 | from the flight of 23 Aug |
| pitch tracking error, p95 | from the flight of 23 Aug |
| altitude error, p95 | from the flight of 23 Aug |

A degradation of the attitude tracking errors means that the increase in the moment of inertia requires a new autotune. A degradation of vibration alone with correct errors means that the filter must be recomputed from the spectrum, not merely adjusted via `INS_HNTCH_REF`.

**E3.** Check the compass disturbance from current: plot the length of the `MAG` vector against the current `BAT.Curr` over the whole flight. A dependence between them means a disturbance from the power supply, which static calibration does not remove.

---

## F. After the flights: documentation

**F1.** New mass and new hover throttle to `BOM.md` §9.

**F2.** Recompute the flight time. Baseline: 855.8 s and 3207 mAh at 1698 g, which gave 7 runs per pack and 14 per session. Consumption grows roughly in proportion to mass, so at a 12% increase about 6 runs per pack are to be expected. The measured value replaces the estimate.

**F3.** Save the new parameter snapshot to `firmware/` with the date.

**F4.** Session card in `sessions/`.

---

## What not to do

**Do not calibrate the accelerometer.** The calibration relates to the orientation of the controller, and the Pixhawk has not moved. A repeat calibration will only introduce a new error.

**Do not run autotune "just in case".** Autotune uses up a pack and introduces new gains that nobody can later compare with the previous ones. Run it only if step E2 shows a degradation.

**Do not fly measurement runs until steps C, D and E are passed.** The configuration is to be frozen during the campaign (protocol §2.3), and these are precisely configuration changes.
