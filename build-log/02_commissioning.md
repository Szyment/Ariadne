# Project Ariadne: Platform 2

**Holybro X500 V2 + Pixhawk 6X + ArduCopter 4.7.0**
Commissioning log, sessions of 15 and 18 Aug 2026

Status: configuration closed, platform ready for the first hover.

---

## 1. Hardware configuration

### Top plate

| Element | Location | Notes |
|---|---|---|
| Pixhawk 6X | centre of the top plate | arrow aligned with the direction of flight |
| GPS M10 (IST8310) | mast, rear | vertical separation from the power harness |
| Telemetry Radio 433 MHz | top plate next to M2 | antenna within the plate outline |
| RadioMaster RP1 V2 | top plate | T antenna away from carbon and the pack |

The telemetry radio was placed next to M2 instead of M1 because in the M1 position the antenna protruded beyond the plate outline.

### Bottom plate / Platform Board

| Element | Location |
|---|---|
| Benewake TFmini-S | Platform Board, front, farther from the centre |
| PMW3901 | Platform Board, front, closer to the centre |
| 4S battery | under the bottom plate, centred |

Both sensors sit ahead of the front edge of the battery, so the field of view of the optical-flow sensor remains unobstructed.

### Wiring

| Port | Device | Protocol |
|---|---|---|
| TELEM1 (SERIAL1) | Telemetry Radio 433 | MAVLink2, 57600 |
| TELEM2 (SERIAL2) | PMW3901 | OpticalFlow (18) |
| TELEM3 (SERIAL5) | TFmini-S | Rangefinder (9), 115200 |
| GPS1 (SERIAL3) | GPS M10 | GPS (5), 230400 |
| UART4 & I2C (SERIAL6) | RadioMaster RP1 V2 | RCIN (23) |
| MAIN 1–4 | ESC M1–M4 | PWM |

The TFmini-S was soldered to TELEM3 with the TX/RX lines crossed:

| TFmini-S | TELEM3 pin |
|---|---|
| red (+5V) | 1 (VCC) |
| white (RX) | 2 (TX) |
| green (TX) | 3 (RX) |
| black (GND) | 6 (GND) |

The RP1 V2 was soldered to the UART4 & I2C port (seven-pin connector):

| RP1 V2 | UART4 pin |
|---|---|
| 5V | 1 (VCC, red wire) |
| RX | 2 (TX4) |
| TX | 3 (RX4) |
| GND | **7 (GND)** |

Pins 4 and 5 (SCL/SDA) and 6 (NFC_GPIO) remain unused. Ground is on pin 7, not 6, because this port has 7 pins, unlike the standard TELEM ports.

The RC IN input is not used. The RCIN pin supports all receiver protocols except CRSF/ELRS and SRXL2, which require a true UART port.

---

## 2. Sensor geometry

ArduPilot convention: X positive forward, Y positive to the right, Z positive down. The reference point is the mid-thickness of the battery.

| Parameter | Value [m] |
|---|---|
| `FLOW_POS_X` | 0.095 |
| `FLOW_POS_Y` | 0.00 |
| `FLOW_POS_Z` | −0.031 |
| `RNGFND1_POS_X` | 0.12 |
| `RNGFND1_POS_Y` | 0.00 |
| `RNGFND1_POS_Z` | −0.021 |
| `RNGFND1_GNDCLR` | 0.17 |

The Z values are negative because the sensor lenses sit above the mid-thickness of the battery (the pack hangs under the bottom plate).

With the drone standing on its legs, the lens height above the ground is 17 cm for the lidar and 18 cm for the optical-flow sensor. Both values lie above the dead zone of the TFmini-S (0–10 cm).

---

## 3. EKF3 configuration: the core of the RQ1 protocol

Three source sets are provided, switched in flight with switch SC (channel 7).

| Parameter | SRC1 (GPS) | SRC2 (optical flow) | SRC3 (GPS) |
|---|---|---|---|
| `POSXY` | 3 (GPS) | 0 (none) | 3 (GPS) |
| `VELXY` | 3 (GPS) | 5 (OpticalFlow) | 3 (GPS) |
| `POSZ` | 1 (Baro) | 1 (Baro) | 1 (Baro) |
| `VELZ` | 3 (GPS) | 0 (none) | 3 (GPS) |
| `YAW` | 1 (Compass) | 1 (Compass) | 1 (Compass) |

```
RC7_OPTION = 90        (EKF Source Set, switch SC)
EK3_SRC_OPTIONS = 0    (FuseAllVelocities disabled)
```

Switch SC mapping:
```
up     → Set 3 → GPS (safe return)
middle → Set 2 → optical flow + lidar (run without GNSS)
down   → Set 1 → GPS (reference trajectory)
```

Set SRC3 was deliberately made identical to SRC1. The upper switch position is a safe return to GPS, not a state with no position source at all.

Switching verification (18 Aug 2026, 17:42):
```
Using EKF Source Set 2
Using EKF Source Set 3
Using EKF Source Set 1
```
Each change is logged with a timestamp, which marks the exact time boundary between the phases of a run.

### Operational envelope limit

When optical flow is the only horizontal position source (`SRC2_VELXY = OpticalFlow`, `SRC2_POSXY = None`) and the flight takes place in a mode that requires a position estimate (Loiter, PosHold), the drone will not climb above the value of `RNGFND1_MAX`.

The altitude ceiling in runs without GNSS is therefore 6 m. This value defines the envelope for experiments E2–E3 and must go into the measurement protocol.

---

## 4. Other parameters

### Firmware and frame
```
ArduCopter 4.7.0 (ChibiOS, Pixhawk6X)
FRAME_CLASS = 1 (Quad)
FRAME_TYPE  = 1 (X)
MOT_PWM_TYPE = 0 (plain PWM)
SERVO1-4_FUNCTION = 33, 34, 35, 36
```

### Sensors
```
FLOW_TYPE = 4 (CXOF)
RNGFND1_TYPE = 20 (BenewakeTFmini-Serial)
RNGFND1_MIN = 0.10, RNGFND1_MAX = 6.00, RNGFND1_ORIENT = 25 (Down)
COMPASS_ORIENT = 6   ← set automatically by the calibration
```

The `SERIAL2_BAUD` parameter was not changed, because the CXOF driver opens the port at a hard-coded 19200 baud (`AP_OpticalFlow_CXOF::init()`).

### Battery: Gens Ace Bashing 4S1P 5000 mAh 60C
```
BATT_MONITOR   = 21 (INA2XX)
BATT_CAPACITY  = 5000
BATT_ARM_VOLT  = 15.2   (3.80 V/cell)
BATT_LOW_VOLT  = 14.8   (3.70 V/cell)
BATT_CRT_VOLT  = 14.4   (3.60 V/cell)
BATT_FS_LOW_ACT = 1 (Land)
BATT_FS_CRT_ACT = 1 (Land)
```

The Land action was chosen instead of RTL, because RTL requires GPS, and in the E2–E3 runs GPS is cut off. Land works under all conditions.

Manufacturer thresholds (LiPo Normal Voltage): charge to 4.20 V/cell (16.8 V), discharge cut-off at 3.55 V/cell (14.2 V), storage at 3.80–3.85 V/cell (15.2–15.4 V).

Manufacturer storage recommendations: during a break in flying, we store the pack at 15.2–15.4 V, check its condition every two weeks, and once every two months perform one full charge and discharge cycle. This matters for a measurement campaign that runs until November.

### Flight modes and switches
```
FLTMODE_CH = 6 (switch SB, three-position)
FLTMODE1 = 0 (Stabilize)
FLTMODE4 = 2 (AltHold)
FLTMODE6 = 5 (Loiter)

RC5_OPTION = 18 (Land, switch SA)
RC7_OPTION = 90 (EKF Source Set, switch SC)
```

### RC link: ExpressLRS
```
Transmitter: RadioMaster Pocket Internal 2.4GHz, ELRS 3.3.1 CE_LBT
Receiver: RadioMaster RP1 V2, ELRS 3.3.1 CE_LBT
Binding phrase: ariadne2026
Protocol: CRSF
```

### Transmitter and Yaapu, 26 Aug 2026

The RadioMaster Pocket was updated from EdgeTX `2.10.0-RM` to `2.12.2`, together with the bootloader and the SD package `bw128x64-v2.12.1`. Models and radio settings were preserved. The ExpressLRS transmitter and receiver firmware remained `3.3.1 CE_LBT`; the update changed neither the regulatory domain, nor the binding phrase, nor the channel mapping.

Yaapu Telemetry `2.1.0-dev` in the 128×64 variant was installed on the SD card and `yaapu7` was assigned to the first telemetry screen of the `FPV DRONE` model. CRSF support was enabled in `Yaapu Config`. With the drone powered off the script correctly reports `NO TELEMETRY`; after the RP1 V2 was powered, the radio began to detect the telemetry stream. Full refresh of all Yaapu fields remains to be tested on the bench without propellers.

A detailed record of the procedure, the SHA-256 sums, the full STM32 memory copy and the recovery path are in [`firmware/README_radiomaster-pocket.md`](../../firmware/README_radiomaster-pocket.md).

---

## 5. Tests passed

| Test | Result |
|---|---|
| Accelerometer calibration | OK (full, not Simple) |
| Compass calibration | Both compasses in the green range |
| Telemetry 433 | Wireless link works |
| GPS fix | 16 sat, 3D DGPS Lock, HDOP 0.9, VDOP 1.1 |
| Optical flow | `quality = 255`, `flow_comp_m_x/y` respond to motion |
| Rangefinder | `current_distance` 54 → 15 cm, responds correctly |
| RC link | `chan1_raw`–`chan4_raw` change with stick movement |
| RC calibration | OK |
| Motors: numbering A/B/C/D → M1–M4 | OK |
| Motors: rotation directions CW/CCW | OK |
| Motors: arming in Stabilize | all 4 start, speed rises and falls evenly |
| Battery monitor | 16.62 V vs 16.6 V measured, deviation 0.02 V |
| EKF3 switching | three sets, each change logged |
| EdgeTX / Yaapu over CRSF | installation OK; telemetry detected after powering the drone, full field test before flight |

The quality of the GPS fix (HDOP < 1.0) confirms that the logged GNSS trajectory is usable as the reference trajectory for RQ1.

---

## 6. Known symptom: Motor Test "All"

Symptom: in the "All motors" test, one of the motors (once B, once C) randomly fails to start. Single tests A/B/C/D always pass, regardless of the throttle level (5%, 20%, 35%).

Log analysis (RCOU, log of 18 Aug 2026):
```
time    C1    C2    C3    C4
281.78  1100  1000  1100  1100
301.88  1150  1000  1150  1150
313.38  1190  1190  1190  1190   ← once all four
323.58  1190  1000  1190  1190
387.88  1340  1000  1340  1340
```

The Pixhawk itself sends no signal on channel 2. The value 1000 means idle, not a missing ESC response. The output configuration is correct and symmetrical (SERVO1-4_FUNCTION = 33–36, all MIN/MAX values identical).

Ruled out: ESCs, wiring, battery voltage and the ESC dead zone (the symptom does not depend on the throttle level).

The resolution came from arming in Stabilize mode: all four motors start, and the speed rises and falls evenly and repeatably. The problem therefore concerns only the Motor Test function, not the flight control path.

The symptom is known from the ArduPilot forum (thread 119035, June 2024), where another user reported it with a different configuration. No root cause was found there, and it was not confirmed whether the drone eventually flew. The symptom is not removed by changing `MOT_SPIN_ARM` or `MOT_SPIN_MIN`, changing the ESC protocol, or Bdshot firmware.

Conclusion for project Ariadne: Motor Test "All" is not a necessary condition. The propulsion is verified by arming in Stabilize mode, in accordance with the ArduPilot documentation.

---

## 7. Findings from the sessions

The ARF kit does not include an RC receiver. Holybro omits it deliberately, because the receiver must match the user's transmitter (ELRS, Crossfire, FrSky and Spektrum are mutually incompatible). The two 433 MHz telemetry modules in the box form an air–ground pair, not two onboard radios.

The ELRS regulatory domain must match on both sides of the link. The RP1 V2 receiver came from the factory set to ISM2G4, while the Pocket transmitter has CE_LBT, so the link did not work despite correct binding and the matching version 3.3.1. The solution was to reflash the receiver firmware with the `Regulatory_Domain_EU_CE_2400` setting and a shared binding phrase. LBT mode is also a legal requirement in Poland.

The RC IN input does not support CRSF/ELRS. These protocols require a true UART port, in this case UART4 (SERIAL6, protocol 23).

The UART4 & I2C port has 7 pins, not 6. Ground is on pin 7, while pin 6 is NFC_GPIO. Standard TELEM ports have 6 pins with ground on pin 6, so the pin mapping must not be carried over between these ports.

Optical coupling between the flow sensor and the lidar is not a problem. Manufacturers integrate both sensors on one board (CubePilot HereFlow, optical flow and lidar, both at 940 nm; MicoAir MTF-01), so mounting them side by side on the Platform Board is safe.

Holybro gives no recommended position for the telemetry radio. The assembly manual covers only the GPS, the onboard computer and the depth camera mount.

MAIN, AUX and RC IN are three separate ports. MAIN carries the outputs to the ESCs (I/O PWM OUT), AUX the auxiliary outputs (FMU PWM OUT), and RC IN is the receiver input.

---

## 8. Open items

### Before the first flight
- Level Horizon, gyroscope and barometer calibration
- Repeat the compass calibration at the flying site (the magnetic field differs from the one at home)
- Telemetry range test with the motors running at about 50% throttle, tethered. The difference from the static measurement is a measure of the noise introduced by the ESCs.
- PMW3901 orientation: the notch on the board that marks the rear must face the rear of the drone
- Verify the message "GPS Glitch or Compass error" in the field (indoors its occurrence is expected)

### First flight
- Propellers and preflight check
- Hover in Stabilize, then AltHold
- Loiter only after the previous modes have been mastered. A Loiter flight on set SRC2 is the test of whether including optical flow and lidar in the estimate yields a usable position.
- Observer present, open terrain, weather forecast checked

### To plan
- Verify source switching in SITL before the first run without GNSS
- Empirical test of the coupling between the flow sensor and the lidar: flow readings with the lidar on and off, with the drone stationary
- Configuration freeze: export the parameter file to the project repository as a parameter snapshot documenting the hardware state for EUCYS

---

## 9. Deadlines

| Date | Task |
|---|---|
| 2026-11-15 | Measurement data freeze |
| 2026-12-31 | EUCYS / Odkrycia documentation |
