# Platform 2: yaw torque imbalance, RESOLVED

*Detected 22 Aug 2026 on logs 5–8, cause removed the same day, confirmed by a check flight (log 9).*

## Resolution

The cause was the **alignment of the arms in the clamps**. After correcting them, the yaw asymmetry fell from +15–17% to −2.3%, and the mixer's constant yaw output from 48–60 µs to −8 µs, that is, from one third of `MOT_YAW_HEADROOM` to one twenty-fifth.

| Session | Log | Windows of settled heading | Yaw asymmetry | Yaw output | Yaw headroom used |
|---|---|---|---|---|---|
| 18 Aug evening | 5 | rough calculation | +69% | — | — |
| 19 Aug | 6 | 1 | +16.8% | +60 µs | 30% |
| 20 Aug | 7 | 4 | about +14% | about +60 µs | about 30% |
| 21 Aug | 8 | 4 | about +15% | about +48 µs | about 24% |
| **22 Aug, after correction** | **9** | **5** | **−2.3%** | **−8 µs** | **4%** |

Motor outputs in hover: 1524 / 1424 / 1515 / 1453 µs against 1531 / 1624 / 1483 / 1459 µs the day before. The difference between the counter-rotating pairs, that is, the one that creates the yaw torque, fell from 141 to 8 µs.

The propellers were inspected visually: a uniform set, no damage. They were not swapped between motors and there was no need to.

Autotune is unblocked.

The values for logs 7 and 8 are given as approximate, because they were calculated with the version of the script from before the thrust model correction. The order of magnitude remains.

---

## Record of the diagnosis, for the record

*The description below was written on 22 Aug before the matter was resolved and is kept as a trace of the reasoning.*

## What the record shows

In hover with a settled heading, the pair of motors rotating counter-clockwise (1, front right; 2, rear left) works permanently harder than the opposite pair. The yaw controller maintains a constant corrective output the whole time, that is, the vehicle is continuously fighting a torque originating from the structure.

| Session | Log | Windows of settled heading | Yaw asymmetry | Yaw output | Yaw headroom used |
|---|---|---|---|---|---|
| 18 Aug evening | 5 | rough calculation, no hover | +69% | — | — |
| 19 Aug | 6 | 1 | +22.3% | +60 µs | 30% |
| 20 Aug | 7 | 4 | +18.0% | about +60 µs | about 30% |
| 21 Aug | 8 | 4 | +19.7% | about +48 µs | about 24% |

The load distribution is repeatable per motor: **motor 3 (front left, CW) works the lightest in every window of every session**, and motors 1 and 2 the hardest. The pattern does not change between sessions, between batteries or between headings.

## Why it is neither wind nor payload

Wind does not produce a constant torque about the vertical axis. Nor does a shifted battery: it causes a difference between front and rear or between left and right, that is, between adjacent motors, not between the counter-rotating pairs. A CCW–CW difference has one cause: mechanical.

The most common source of a false result was also excluded: windows in which the controller was executing a commanded turn. In all the calculated windows the commanded heading change is below 0.5°/s.

## Scale of the problem

`MOT_YAW_HEADROOM` is 200 µs; this is how much range ArduPilot reserves for yaw control. A constant output of the order of 48–60 µs means that **one quarter to one third of this headroom is used up in calm hover**, before any gust or commanded turn appears. This is not a state in which the vehicle is about to fall, but it is a permanent reduction of the control margin in the axis where the platform is weakest anyway, because heading comes exclusively from the magnetometer.

Side effects: one pair of motors works closer to saturation than the other, which shortens flight time and reduces the power reserve in gusts.

## Why this must be settled before autotune

Autotune determines the gains for the vehicle as it is at the moment of tuning. Performed on a structure with an asymmetry, it will write the asymmetry into the settings and perpetuate it. Protocol §2.3 freezes the full parameter set for the duration of the campaign, so after the freeze a geometry correction would mean invalidating the tuning and repeating it.

Besides, the work will have to describe the measurement platform. A structure that constantly spends thirty percent of its yaw control headroom fighting its own asymmetry is a fact that is either fixed or described, not passed over in silence.

## What to check on the bench

In order from most to least likely:

1. **Rotation of the arms in the clamps.** The X500 V2 arms are tubes clamped in collars. A rotation of the tube by two or three degrees tilts the motor axis tangentially to the circle and gives exactly the torque seen in the record. Calculation: to produce the observed torque, an axis deviation of the order of 2–3° on one or two arms is enough. This is invisible to the naked eye. Check with a spirit level (or a spirit-level app on a phone) the attitude of the upper plate of each motor with the vehicle standing on a level table; all four should read the same.
2. **Propellers.** Whether all four are the same model and pitch, whether the CW and CCW pairs are correctly matched, whether none is bent or cracked. If propellers were replaced after the incident of 18 August, check that the set is uniform.
3. **Motor seating.** Whether the mounting screws are not loose and whether no motor plate was deformed during the tip-over after landing on 18 August.
4. **Rotation directions.** Confirm that each motor spins according to the Quad X layout and that the propeller matches the rotation direction.

## How to check whether the correction worked

After each change: mission `missions/S-06_Balance1.plan`, four hovers of 30 s on headings 0°, 90°, 180° and 270°, absolute headings, altitude 15 m, about three minutes of flight. Then `analysis/balance.py`. The measure is the yaw output in microseconds; target below 20 µs, that is, below 10% of the headroom.

**22 Aug: the motor alignment in the clamps was corrected.** The propellers were inspected visually: a uniform set, no damage; they were not swapped between motors. The effect of the correction is unknown until the check flight.

During this flight it is worth collecting material for a second thing currently missing: **a 30 s hover on four headings differing by 90°**. Only such material allows the battery offset to be separated from the wind-induced torque. All flights so far have hover windows in a fan of headings narrower than 60°, at which the separation is ill-conditioned and the "payload" and "wind" values reported by the script are not reliable. One battery is enough for both tasks.

## History

On 18 August the yaw asymmetry was +69% and the vehicle lost heading in flight despite full controller intervention; the session ended with a tip-over after landing. The geometry correction made after that session removed most of the problem; from 19 August the value has stayed at the level of 18–22%. The next correction, made between 19 and 20 August, did not change this level: 22.3% before it, 18.0% and 19.7% after it. **The cause of the remaining asymmetry has therefore not yet been found.**
