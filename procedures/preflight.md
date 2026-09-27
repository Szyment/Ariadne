# Preflight checklist

*v0.3, 6 Sep 2026 (E: charging and storage rule). v0.2, 23 Aug 2026. Energy and sensor values carried over from Platform 1 to Platform 2.*

## A. Formal and legal conditions (basis of the liability insurance cover; without the full set we do not arm the drone)
- [ ] Check the zones (DroneRadar / PANSA UTM) and confirm that the location meets the A3 requirements: ≥150 m from buildings
- [ ] Submit the flight notification in DroneTower; confirm that the flight is active
- [ ] Have the pilot certificate on the phone; check that the operator number on the airframe is legible
- [ ] Assign roles: pilot and observer [name]; for an FPV flight the observer is mandatory
- [ ] Check the weather: **wind AVG at 2.0 m ≤ 4.0 m/s** (`ANNEX_C` §7.1; for autotune ≤ 2.0 m/s), no thunderstorm, Kp index checked
- [ ] Check the phone: charged to at least 50%, power bank in the bag. Without the phone there is no flight notification, no certificate and no zone check, so three items of this list drop out at once. Item added 21 Aug after the session of 20 Aug, in which the flight notification failed because of a discharged phone

## B. Energy
- [ ] Measure the resting voltage of the 4S pack: **16.7–16.8 V (full)**, not less than **15.2 V** (`BATT_ARM_VOLT`; below this the autopilot will not arm); temperature >10 °C (in winter carry in an insulated bag)
- [ ] Secure the pack with two straps and check that the cable is not under tension; charge the transmitter and the phone
- [ ] **Check the pack orientation:** connector to the rear, pack within the plate outline, **does not obstruct the rangefinder or the flow sensor**. Item added 23 Aug after a flight in which a pack fitted the wrong way round obstructed the rangefinder and the flight had to be rejected
- [ ] Check that the pack sits in the same place as before; the reference value of the payload offset is **4.1 mm** (`balance.py`, session card S-06); a discrepancy above 5 mm in the post-session result means the pack went back in a different place

## C. Mechanics
- [ ] Check the propellers: tightened, no cracks or chips, directions matching the markings
- [ ] Check the motors (free rotation, no play) and the frame (screws tightened, no cracks from the previous flight)
- [ ] Check the PMW3901 flow sensor and the TFmini-S rangefinder: clean lenses, **downward field of view completely unobstructed**, neither by the pack, nor by wiring, nor by landing gear elements

## D. Systems (first power-up of the day through the smoke stopper)
- [ ] Check the GPS fix: number of satellites ≥ 8, HDOP ≤ 1.5 (quality criterion of the reference measurement; below 6 satellites the session is flagged)
- [ ] Check the compass and calibration: no warnings in Mission Planner, arming without pre-arm errors
- [ ] Perform the failsafe test on the ground: switch off the transmitter and check that the response matches the configuration; set the return altitude appropriately for the terrain
- [ ] Confirm the assignment of modes to switches (Stabilize / Loiter / RTL and the EK3 source switch)
- [ ] Check logging: free space on the card or in flash memory, controller clock synchronised with GPS

## E. After the flight
- [ ] Close the flight in DroneTower and complete the entry in the session card (the .bin log is copied after return)
- [ ] Check the motor temperature by hand (none may be noticeably warmer than the others); inspect the propellers and the frame
- [ ] Remove the packs from the drone; **immediately after returning from the session** set the charger (iMAX B6AC v2) to LiPo STORAGE, 4S; it will bring the pack to **3.85 V/cell (15.4 V)**. Do this on a partially discharged pack: the charger then only tops up (minutes); discharging a full pack takes 5–7 h (discharge power ~5 W)
- [ ] Do not charge to full "in reserve". Full charging (LiPo Balance, 4S, **3.0 A**, the charger's real current at 50 W for 4S, ~1.7 h) is done **in the evening before the session**. Pack: Gens Ace 4S1P 5000 mAh 60C, 74 Wh
- [ ] Before charging, read the cell voltages from the charger and enter them in the session card with the pack number; note a spread between cells above 0.03 V (first sign of ageing). Reference 6 Sep 2026: both packs 4.19/4.19/4.19/4.19 V

## F. Post-incident check (collision, hard landing), before fitting propellers

Introduced 15 Sep 2026 after S-20 (collision with a tree, one propeller cracked).

1. Motors: even rotation by hand, no grinding, no bearing play; bell gap clean (grass, sand, bark); shaft does not wobble.
2. Arms: carbon tubes against the light and with a fingernail, a white scratch = a crack; stiffness at the motor and at the plate the same as the others.
3. Motor and arm mounting screws: check with a spanner.
4. Payload Platform Board: PMW3901 and TFmini-S in place, lenses clean and unscratched, plugs pushed in.
5. GPS mast, 433 MHz antenna, ELRS antenna: straight, cables intact.
6. Landing gear: legs and clips.
7. The pack from the flight: no swelling, dents or smell; otherwise into the LiPo Safe bag, do not charge.
8. On the bench, without propellers, in QGC: heading follows the rotation of the aircraft smoothly; roll/pitch ≈ 0 on a level surface; rangefinder and `OPTICAL_FLOW.quality` respond to a hand. Calibrate only if one of the tests deviates.
9. New propellers: 1045 on the snap-lock quick release (X500 V2), CW/CCW according to the adapter marking; replace the whole set, not single ones. `Motor Test` in QGC: every propeller blows downward.
10. First flight: 60 s hover on GNSS low over the path; compare `VIBE` from the log with the baseline (log 20, 28 Aug); only then runs.

## G. Dusk rules (from S-20)

- `OF.Qual` in the hover at A: 255 → full flight; 100–254 → full flight, watch the departure; 1–99 → test hover only (in motion the quality drops to 0, S-21); 0 → abandon (outcome known: EKF failsafe after ~8 s).
- In AUTO keep the throttle stick near the centre: on a failsafe to AltHold the aircraft reads it immediately.
- After an EKF failsafe (AltHold): controlled climb to 10–15 m (throttle about 60 %), RC7 Low within 5 s, then **Loiter**, return over the path in Loiter, land on the path. No manual horizontal flight in AltHold. `FS_EKF_ACTION` stays 2 (decision of 18 Sep: private land, land in place ruled out).
- Land from the switch only over open, known terrain. Over trees: Loiter and return.
- Light threshold test only with A at least 30 m from the tree line.
