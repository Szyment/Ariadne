# Project Ariadne: Platform 2

**Holybro X500 V2 + Pixhawk 6X**
Commissioning log, 15 Aug 2026

---

## 1. Hardware configuration

### Top plate

| Element | Location | Notes |
|---|---|---|
| Pixhawk 6X | centre of the top plate | arrow aligned with the direction of flight |
| GPS M10 (IST8310) | mast, rear | vertical separation from the power harness |
| Telemetry Radio 433 MHz | top plate next to M2 | antenna within the plate outline |

The radio was placed next to M2 instead of M1 because in the M1 position the antenna protruded beyond the plate outline, which risked mechanical damage during transport.

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
| TELEM1 | Telemetry Radio 433 | MAVLink2, 57600 |
| TELEM2 (SERIAL2) | PMW3901 | OpticalFlow (18) |
| TELEM3 (SERIAL5) | TFmini-S | Rangefinder, 115200 |
| GPS1 (SERIAL3) | GPS M10 | GPS, 230400 |
| MAIN 1–4 | ESC M1–M4 | to do |
| RC IN | ELRS receiver | none, to be ordered |

The TFmini-S was soldered to TELEM3 with the TX/RX lines crossed:

| TFmini-S | TELEM3 pin |
|---|---|
| red (+5V) | 1 (VCC) |
| white (RX) | 2 (TX) |
| green (TX) | 3 (RX) |
| black (GND) | 6 (GND) |

Pins 4 and 5 (CTS/RTS) remain unused.

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

## 3. Parameters set

### Firmware and frame
```
ArduCopter 4.7.0 (ChibiOS, Pixhawk6X)
FRAME_CLASS = Quad
FRAME_TYPE  = X
```

### Optical flow
```
FLOW_TYPE        = CXOF (4)
SERIAL2_PROTOCOL = OpticalFlow (18)
```
The `SERIAL2_BAUD` parameter was not changed, because the CXOF driver opens the port at a hard-coded 19200 baud (`AP_OpticalFlow_CXOF::init()`).

### Rangefinder
```
RNGFND1_TYPE     = BenewakeTFmini-Serial
RNGFND1_MIN      = 0.10
RNGFND1_MAX      = 6.00      (6 = outdoors, 10 = indoors)
RNGFND1_ORIENT   = Down
SERIAL5_PROTOCOL = Rangefinder
SERIAL5_BAUD     = 115200
```

### Compass
```
COMPASS_ORIENT (Mag 0) = 6   ← set automatically by the calibration
```
ArduPilot detected a 270° rotation of the external compass relative to the drone axes and compensated for it on its own. Physical verification is required to establish whether it is the GPS module on the mast that is rotated, or the IST8310 board inside the M10 housing.

---

## 4. Tests passed

| Test | Result |
|---|---|
| Accelerometer calibration | OK (full, not Simple) |
| Compass calibration | Both compasses in the green range |
| Telemetry 433 | Wireless link works |
| GPS fix | 16 sat, 3D DGPS Lock, HDOP 0.9, VDOP 1.1 |
| Optical flow | `quality = 255`, `flow_comp_m_x/y` respond to motion |
| Rangefinder | `current_distance` 54 → 15 cm, responds correctly |

The quality of the GPS fix (HDOP < 1.0) confirms that the logged GNSS trajectory is usable as the reference trajectory for RQ1.

---

## 5. Open items

### Blocking the first flight
- No RC receiver. The RadioMaster RP1 V2 (EU-LBT) was lost together with Platform 1. The model has been discontinued but is still available in Poland (NobShop, BZB UAS, MegaDron). Alternatives are the RadioMaster XR1 Nano or any ELRS 2.4 GHz receiver in the LBT version. The ExpressLRS version (major.minor) must match the Pocket transmitter, with the same binding phrase.

### To do without the receiver
- Connect the ESCs to MAIN 1–4 according to the M1–M4 markings on the arms
- Motor Test in QGC: verify numbering and rotation directions, without propellers
- Calibrate the battery monitor (`BATT_MONITOR`) and set the voltage failsafe thresholds
- Level Horizon, gyroscope and barometer calibration

### After installing the receiver
- RC calibration and flight mode configuration
- `RCx_OPTION = 90`: three-position switch for the EKF3 source sets
- `EK3_SRC1_*` (GPS) and `EK3_SRC2_*` (optical flow and lidar)
- Verify the switching in SITL before flight

### To verify in the field
- The message "GPS Glitch or Compass error" appeared indoors, probably because of the missing fix and metal in the surroundings. Requires confirmation in the field.
- Repeat the compass calibration at the flying site (the magnetic field differs from the one at home)
- Telemetry range test with the motors running at about 50% throttle, tethered. The difference from the static measurement is a measure of the noise introduced by the ESCs.
- PMW3901 orientation: the notch on the board that marks the rear must face the rear of the drone

---

## 6. Findings from this session

The ARF kit does not include an RC receiver. Holybro omits it deliberately, because the receiver must match the user's transmitter (ELRS, Crossfire, FrSky and Spektrum are mutually incompatible). The two 433 MHz telemetry modules in the box form an air–ground pair, not two onboard radios.

Optical coupling between the flow sensor and the lidar is not a problem. Manufacturers integrate both sensors on one board (CubePilot HereFlow, optical flow and lidar, both at 940 nm; MicoAir MTF-01), so mounting them side by side on the Platform Board is safe. An empirical verification is nevertheless advisable: flow readings with the lidar on and off, with the drone stationary.

Holybro gives no recommended position for the telemetry radio. The assembly manual covers only the GPS, the onboard computer and the depth camera mount. The radio position remains the builder's decision, constrained by the length of the JST-GH cable and the free space on the plate.

MAIN, AUX and RC IN are three separate ports. MAIN carries the outputs to the ESCs (I/O PWM OUT), AUX the auxiliary outputs (FMU PWM OUT), and RC IN is the receiver input. The power module does not supply voltage to the + and − pins of the PWM OUT ports.
