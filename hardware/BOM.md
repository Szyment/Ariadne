# Bill of materials (BOM): platform 2 (Ariadne)

*As of 21 Aug 2026. This document fills the gap noted in `STRUCTURE.md`: the `hardware/` directory was empty.*

Rule adopted in this document: the *Source* column indicates where a given piece of information comes from. Items marked **TO BE CONFIRMED** are not guessed; they remain explicitly open and require checking on the hardware or in the purchase documents.

---


## 1. Airframe structure

| Item | Model / specification | Qty | Source |
|---|---|---|---|
| Frame | Holybro X500 V2, 500 mm wheelbase, body 144 × 144 mm | 1 | project docs |
| Arms | carbon tubes ⌀16 mm, fibre-reinforced nylon connectors | 4 | Holybro |
| Landing gear | carbon tubes ⌀16 mm and ⌀10 mm | 2 | Holybro |
| Battery plate | Battery Mounting Board V2 (mounted underneath, adjustable) | 1 | project docs |
| Payload Platform Board | payload plate V2, carrier of the optical-flow sensor and the ToF rangefinder | 1 | order of 7 Aug |
| GPS mast | tube with base (included with the frame) | 1 | project docs |

## 2. Propulsion

| Item | Model / specification | Qty | Source |
|---|---|---|---|
| Motors | Holybro 2216, 920 KV, 2 × CW and 2 × CCW | 4 | Holybro (spare parts X500 V2) |
| ESC | Holybro BLHeli S 20 A | 4 | Holybro |
| PDB | Holybro X500 V2, XT30 factory-soldered | 1 | Holybro |
| Propellers | 1045 (10 × 4.5"), self-tightening, 2 × CW and 2 × CCW | 4 | Holybro + inspection 21 Aug |

The propeller coding is as follows: a silver nut corresponds to the motor with the silver shaft (CCW), a black nut to the motor with the black shaft (CW). The tightening direction is stamped on the hub.

> **Diagnostic note.** During tuning on 18 Aug it was found that the motor mounts were seated at an angle. The diagonals diverged by 370 µs, and about 45% of the yaw authority was permanently spent on holding the course. The source of the misalignment was not established. After the correction a residual of 85–95 µs remained, which cannot be removed on this structure. The motor model and its mounting method are diagnostic information here, not cosmetic.

## 3. Avionics

| Item | Model / specification | Qty | Source |
|---|---|---|---|
| Flight controller | Holybro Pixhawk 6X | 1 | PM-7112 kit |
| Firmware | ArduCopter 4.7.0 (ChibiOS), `FRAME_CLASS = 1`, `FRAME_TYPE = 1` (Quad X) | — | project docs |
| GNSS with compass | Holybro M10 (IST8310 magnetometer), on the mast at the rear | 1 | PM-7112 kit |
| Power module | **TO BE CONFIRMED**: the variant, PM02D or PM03D, was not recorded. `BATT_MONITOR = 21` (INA2XX), the monitor works correctly (deviation 0.02 V) | 1 | — |

The parameter `COMPASS_ORIENT = 6` (270° rotation) was set automatically by the calibration. It remains to be verified physically whether it is the module on the mast that is rotated, or the IST8310 board inside the housing.

## 4. Research sensors

| Item | Model / specification | Qty | Source |
|---|---|---|---|
| Optical flow | Holybro PMW3901, `FLOW_TYPE = 4` (CXOF) | 1 | order of 7 Aug |
| ToF rangefinder | Benewake TFmini-S, range 12 m, `RNGFND1_TYPE = 20` | 1 | order of 7 Aug |

Both sensors are located on the Payload Platform Board at the front, ahead of the edge of the battery pack, so that the field of view of the optical-flow sensor remains unobstructed. The lenses are 17–18 cm above the ground, that is, above the dead zone of the TFmini-S (0–10 cm).

The value `RNGFND1_MAX = 6.00` (6 m outdoors, 10 indoors) defines the altitude ceiling of runs without GNSS: with `SRC2_POSXY = None` the drone will not climb above the rangefinder's range.

## 5. Communications

| Item | Model / specification | Qty | Source |
|---|---|---|---|
| Telemetry, airborne | SiK 433 MHz | 1 | PM-7112 kit |
| Telemetry, ground | SiK 433 MHz, USB | 1 | PM-7112 kit |
| RC receiver | RadioMaster RP1 V2, ExpressLRS 3.3.1, CE_LBT firmware (reflashed from ISM2G4) | 1 | project docs |
| RC transmitter | RadioMaster Pocket Internal 2.4 GHz, ELRS 3.3.1 CE_LBT | 1 | from platform 1 |
| Transmitter software | EdgeTX 2.12.2, `pocket` board (`RADIO/radio.yml`, `semver: 2.12.2`; file `FIRMWARE/edgetx-pocket-2.12.2.bin` flashed 26 Aug 2026) | | transmitter SD card |
| SD card contents | EdgeTX 2.12.1 (`edgetx.sdcard.version`) | | transmitter SD card |
| Telemetry script | Yaapu 2.1.0-dev (`SCRIPTS/TELEMETRY/yaapu/`) | | transmitter SD card |

Control channel map:

| Channel | Switch | Function |
|---|---|---|
| 5 | | `RC5_OPTION` = 18 |
| 6 | SB | |
| 7 | | `RC7_OPTION` = 90, EKF3 source-set switch |
| 8 | | `RC8_OPTION` = 16, autotune |
| 9 | SE | shutdown of the onboard computer system; `RC9_OPTION` = 0, because the decision is made by the program on the Raspberry, not by ArduPilot |

ExpressLRS remains at `3.3.1 CE_LBT` in the transmitter and in the receiver: the transmitter update of 26 Aug covered only EdgeTX and the SD card, not the radio module. Regulatory domain, binding phrase and channel mapping unchanged. Record of the procedure, SHA-256 sums and recovery path: `firmware/README_radiomaster-pocket.md`.

The card contents (2.12.1) are one release older than the flashed firmware (2.12.2). With a matching minor version this makes no difference to sounds and scripts, but at the next update the card must be updated together with the transmitter.

**ELRS telemetry ratio: 1:4 at 250 Hz.** A transmitter module setting, changed from the `elrsV3` Lua screen (`Telem Ratio`, `Packet Rate`), stored in the module, not in the model. At a lower ratio the link carries only ordinary CRSF frames, and ArduPilot's custom telemetry packets 0x5001–0x5006 do not get through at all. These are the packets carrying the rangefinder reading, so without this setting the Yaapu screen does not show altitude above ground. Symptom before the change: all counters in `Yaapu DebugCRSF` stand at zero, and the vehicle log contains no `custom telem init done` message.

Binding phrase: `ariadne2026`. CRSF protocol. LBT mode is a legal requirement in Poland, and at the same time it turned out to be the reason why the link did not work despite the receiver being correctly bound to the transmitter and the firmware versions matching.

## 6. Power

| Item | Model / specification | Qty | Source |
|---|---|---|---|
| Battery | Gens Ace Bashing 4S1P 5000 mAh 60C, 74 Wh, XT90 connector | 2 (P1, P2) | inventory as of 21 Aug |
| Battery | Gens Ace Bashing 4S1P 5000 mAh 60C, XT90 connector | 2 (P3, P4) | 12 Sep 2026, ; delivered 15 Sep |
| Propellers | Holybro 1045 (2 pairs CW/CCW, quick-release with latch, X500 V2) | 2 sets | ordered 14 Sep 2026 after the S-20 collision, delivery Thu 18 Sep; one set on the drone, the second in the bag for the session |
| Adapter | XT90 male → XT60 female | 2 | 12 Sep 2026,  |
| Charger | SkyRC B6AC Neo, 200 W, 10 A, 1–6S | 1 | 12 Sep 2026 |
| Charger | iMAX B6AC v2, 50 W (up to ~3 A) | 1 | earlier inventory |
| LiPo Safe bag | 23 × 30 cm | 2 | 12 Sep 2026,  |

Purchase of 12 Sep 2026 in total with delivery. After delivery: 4 packs, that is, 2 sessions of 12 runs each without charging in the field, or one session with a reserve. Label the new packs P3 and P4, first charge on the Neo at 5.0 A (1C), Balance mode, and record the cell voltages in `preflight.md`.

Voltage thresholds: full 16.8 V · `BATT_ARM_VOLT` 15.2 · `BATT_LOW_VOLT` 14.8 · `BATT_CRT_VOLT` 14.4 · `BATT_FS_*_ACT = 1`. Land was chosen instead of RTL, because RTL requires GPS, and in E2–E3 runs GPS is cut off.

The measurement from LOG 6 (19 Aug) gave 411 s of flight and 1818 mAh at an average draw of 15.9 A. The session ended by reaching the `BATT_ARM_VOLT` threshold, not by the pilot's decision.

The measurement of 23 Aug (card S-07) gave **855.8 s airborne, 3207 mAh, 13.45 A average**. The difference from LOG 6 comes from the flight profile, not from the pack. The value of 23 Aug applies to campaign planning.

The energy density is 176 Wh/kg, which is more than in the aviation Tattu 4S 25C packs (157–161), so a replacement is not justified.

There are 2 packs in stock (established 21 Aug), and the drone carries one at a time. One run according to protocol §6 takes about 90 s of flight, and with stabilisation and manoeuvres about 122 s, which at 855.8 s gave **7 runs per pack and 14 per session**.

**Recalculation after mounting the onboard computer, 28 Aug.** The mass rose from 1698 to 1838 g. Hover power grows approximately as thrust to the power of 1.5 (momentum theory), so with a mass increase of 8.2% the power rises by 12.6%:

| | 21 Aug, 1698 g | 28 Aug, 1838 g |
|---|---|---|
| Average current | 13.45 A | **15.65 A** (measured, log 20) |
| Time airborne | 855.8 s | about **735 s** (recalculated from current) |
| Runs per pack | 7 | **6** |
| Runs per session, 2 packs | 14 | **12** |

The current was measured in hover on 28 Aug (estimate from mass: 15.1 A, error 4%). The time airborne remains a recalculation to be confirmed by a run-to-depletion measurement. Item B1 in `sessions/MISSING_DATA.md` remains closed: 12 runs per session still fits within the campaign assumptions.

### Onboard computer power supply

| Item | Model | Qty | Source |
|---|---|---|---|
| 5 V voltage converter | Pololu from the D24VxF5 family, board `reg15b` | 2 | in stock |

The board variant is either D24V60F5 (6 A) or D24V90F5 (9 A). Both have a fixed 5 V output with 4% accuracy, 5–38 V input, protection against reverse polarity, short circuit and overheating, and a PG output. Both exceed the 5 A required by the Raspberry Pi 5, so the distinction does not matter for the project.

Measurements of 25 Aug 2026, laboratory power supply:

| Input | Load | Output |
|---|---|---|
| 16.0 V | none | 5.01 V |
| 12.8 V | none | 5.01 V |
| 16.8 V | none | 5.03 V |
| 16.8 V | Arduino, a few tens of mA | 4.98 V on the Arduino board |
| 16.8 V | Raspberry Pi 5, two OV5647 cameras, two video streams, vehicle assembled | 5.01 V |

Line regulation: 20 mV over the range 12.8–16.8 V. The 30 mV drop at a few tens of mA occurred on the connecting wires, not on the converter.

The measurement under full load was performed on 27 Aug on the assembled vehicle. `vcgencmd get_throttled` returned `0x0`, that is, no undervoltage, no clock throttling and no undervoltage event since boot. A voltage of 5.01 V is sufficient, even though the Raspberry Pi 5 has a nominal voltage of 5.1 V.

Power is brought to the GPIO header, two wires each for 5 V and for ground, not through the USB-C socket. The USB-C plug with a 56 kΩ resistor, considered earlier, is no longer needed.

Connection on the supply side: XT30 from the power distribution board → 5 A fuse on the positive line → converter `VIN`; ground from the XT30 straight to `GND`, without a fuse.

## 7. Pixhawk 6X port map

| Port | Connected | Protocol |
|---|---|---|
| TELEM1 (SERIAL1) | SiK 433 MHz radio | MAVLink2, 57600 |
| TELEM2 (SERIAL2) | PMW3901 | `SERIAL2_PROTOCOL = 18`; 19200 hard-coded in `AP_OpticalFlow_CXOF::init()` |
| TELEM3 (SERIAL5) | Benewake TFmini-S | Rangefinder (9), 115200 |
| GPS1 (SERIAL3) | M10 module | GPS (5), 230400 |
| GPS2 (SERIAL4) | Raspberry Pi 5 | `SERIAL4_PROTOCOL = 2` (MAVLink2), 115200 |
| UART4 & I2C (7-pin) | RadioMaster RP1 V2 | `SERIAL6_PROTOCOL = 23` (RCIN) |
| MAIN 1–4 | ESC M1–M4 | PWM, `SERVO1-4_FUNCTION = 33–36` |

UART4 connector: VCC on pin 1, TX4 on pin 2, RX4 on pin 3, GND on pin 7. The port has 7 pins, not 6 like the standard TELEM ports; pin 6 is NFC_GPIO. The TELEM port mapping must not be carried over here.

The TFmini-S was soldered to TELEM3 with crossed TX/RX lines: red to pin 1 (VCC), white (RX) to pin 2 (TX), green (TX) to pin 3 (RX), black to pin 6 (GND).

Three wires were connected to GPS2: pin 2 (TX8) to Raspberry Pi pin 10 (RX), pin 3 (RX8) to pin 8 (TX), pin 6 (GND) to the Raspberry ground. Pin 1 (+5 V) remains unconnected, because the onboard computer has its own power supply. Details in `hardware/RPi5_onboard_computer.md`.

The RC IN input is not used. The RCIN pin supports all receiver protocols except CRSF/ELRS and SRXL2, which require a true UART port.

## 8. Sensor geometry

| Parameter | Value [m] |
|---|---|
| `FLOW_POS_X` / `_Y` / `_Z` | 0.095 / 0.00 / −0.031 |
| `RNGFND1_POS_X` / `_Y` / `_Z` | 0.12 / 0.00 / −0.021 |
| `RNGFND1_GNDCLR` | 0.17 |

ArduPilot convention: X forward, Y right, Z down.

**The values above were calculated relative to the mid-thickness of the battery and are therefore incorrect.** ArduPilot measures these distances from the origin of the vehicle reference frame, and with `INS_POS1/2/3` equal to zero, as here, the origin of the frame is the inertial unit, that is, the centre of the flight controller board. The battery hangs under the lower plate, the controller stands on the upper plate, so the difference is about 10 cm in the vertical axis. Correction and calculation: `SENSOR_GEOMETRY.md`.

## 9. Mass (measured 21 Aug 2026)

| | Mass |
|---|---|
| Without battery | 1263 g |
| **Take-off mass (AUW) with onboard computer, 28 Aug** | **1838 g** |
| Battery Gens Ace Bashing 4S1P 5000 mAh | 434 g (23.6% AUW) |
| Vehicle without pack | 1404 g |
| Take-off mass before mounting the computer, 21 Aug | 1698 g |

The configuration of 21 Aug included the 4S pack, 1045 propellers, PMW3901, TFmini-S, M10 GPS on the mast, RP1 V2 receiver and 433 MHz radio. The state of 28 Aug adds to this the Raspberry Pi 5 with active cooling, two OV5647 cameras with lenses, the voltage converter, the fuse holder and the harnesses.

**Mass increase: 140 g, that is, 8.2%.** The vehicle itself without the pack grew by 141 g, so the entire increase is in the equipment, and the pack remained the same to the gram.

Consistency check: a 4S 5000 mAh pack at an average voltage of about 15.2 V has about 76 Wh, and 76 Wh divided by 0.435 kg gives 175 Wh/kg against 176 Wh/kg recorded independently in the tuning document. The results agree.

The comparison with platform 1 is instructive, because the masses are almost identical with a completely different balance:

| | Platform 1 (Rekon7 7") | Platform 2 (X500 V2) |
|---|---|---|
| AUW | 1635 g | 1838 g |
| Battery | 903 g (55% AUW) | 434 g (24% AUW) |
| Pack energy | 6S2P 8 Ah ≈ 178 Wh | 4S 5 Ah ≈ 76 Wh |
| Flight time | — | **14 min 16 s** (measured 23 Aug, log 10) |

Platform 2 is 203 g heavier and carries 2.3 times less energy. The increase in structural mass absorbed what was saved on the pack.

**Correction 23 Aug.** The ~6.9 min recorded above came from log 6 (411 s, average current 15.9 A) and was a value from an interrupted flight, not from pack depletion. The run-to-depletion flight of 23 Aug (log 10) gave **855.8 s at 3207 mAh and an average current of 13.45 A**, that is, about 208 W in hover. The conclusion about short sessions does not hold: two packs give 14 runs per session. Item B1 in `MISSING_DATA.md` closed.

The thrust-to-weight ratio remains to be calculated, and one datum is missing. The parameter `MOT_THST_HOVER = 0.267` describes the controller output in hover, not the fraction of maximum thrust. The recalculation requires the maximum thrust of the 2216 920 KV motor with the 1045 propeller on a 4S pack, read from the datasheet or measured on a test stand. Without it, neither the payload margin for the Raspberry Pi with camera (RQ2) nor for the fibre-optic spool (RQ4) can be calculated, and README §4.3 contains a mass budget calculated for the seven-inch airframe that no longer exists.

## 10. Geofence (verified 21 Aug)

`FENCE_ENABLE 1 · TYPE 7 (alt max + circle + polygon) · RADIUS 300 m · ALT_MAX 100 m · ACTION 1 (RTL/Land) · MARGIN 2 m · TOTAL 0 (no polygon)`.

The `Test1` mission fits within the envelope with a large margin: at most about 50 m from the take-off point, altitude 25 m. `RTL_ALT_M = 15`. The geofence configuration existed from the start, but the `FENCE_ENABLE` switch remained at zero until 20 Aug.

---

## 11. What is missing from this list

1. ~~Take-off mass (AUW)~~: measured 21 Aug: 1698 g with pack, 1263 g without pack (see §9). The maximum thrust of the motors remains open; without it there is no thrust-to-weight ratio and no payload budget for RQ2 and RQ4.
2. ~~Number of packs in stock~~: two, sufficient. Settled by the measurement of 23 Aug (§9).
3. Power module variant: to be read from the label.
5. Small items: antennas, JST-GH cables, TPU-printed parts, power wiring. They were never counted anywhere.
