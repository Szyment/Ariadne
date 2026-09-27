# ArduPilot Copter: initial parameter set (v0.1, to be validated during configuration)

Target board: SpeedyBee F405 V5 (supported in the upstream branch since the turn of 2025/26). Software:
the latest stable version, first flashed via DFU from the with_bl.hex file, following the SpeedyBee procedure.
After flashing we perform the calibrations (accelerometer, compass away from metal, radio, ESC), and only
then enter the parameters given below.

## Power and propulsion (for DOGCOM 6S2P 8 Ah, Samsung 40T)
MOT_BAT_CURR_MAX = 60        # hard pack current limit (cells 70 A; four motors at 48 A each exceed this value without a limit)
BATT_LOW_VOLT    = 18.0      # 3.0 V/cell -> RTL action
BATT_CRT_VOLT    = 17.4      # 2.9 V/cell -> LAND
BATT_LOW_TIMER   = 10        # voltage sag under load in Li-ion cells does not trigger a false alarm
BATT_LOW_MAH     = 6400      # 80% depth of discharge of 8 Ah; for Li-ion the capacity-based protection takes precedence
BATT_ARM_VOLT    = 22.2      # arming lockout below about 3.7 V/cell

## MTF-01 (optical flow + rangefinder, UART; firmware variant: ArduPilot/mav_apm)
SERIALx_PROTOCOL = 1         # MAVLink1 (x = number of the port the sensor is connected to)
SERIALx_BAUD     = 115
FLOW_TYPE        = 5         # MAVLink
RNGFND1_TYPE     = 10        # MAVLink
RNGFND1_MAX_CM   = 800
RNGFND1_MIN_CM   = 2
EK3_SRC1_*       = GNSS      # baseline profile: POSXY=3, VELXY=3, POSZ=1(baro), YAW=1
EK3_SRC2_POSXY   = 0         # GNSS-denied profile: no absolute position
EK3_SRC2_VELXY   = 5         # optical flow
EK3_SRC2_POSZ    = 2         # rangefinder
RCx_OPTION       = 90        # EKF source switch on a free channel (the switch must be visible in the log)
RCy_OPTION       = 158       # FlowCal: in-flight optical-flow calibration (the fit metric is recorded in the build log)
# Automation variant for the switching: the ahrs-source-gps-optflow.lua script (ArduPilot documentation)

## Logging (the logs constitute the project dataset)
LOG_BITMASK      = default + EKF3 + OpticalFlow + RangeFinder  # with memory limited to 16 MB flash, restrict raw IMU data
LOG_DISARMED     = 0
# After delivery, check whether the board has a microSD slot or only 16 MB flash; the download strategy depends on it (every 1–2 flights or once per session)

## Safety
FS_THR_ENABLE    = 1         # RTL on loss of the RC link
RTL_ALT          = per terrain (start: 3000 = 30 m)
FENCE_ENABLE     = 1, FENCE_TYPE = 7, FENCE_RADIUS = 150, FENCE_ALT_MAX = 100
ARMING_CHECK     = 1         # all checks enabled; we do not disable them ad hoc in the field
# Modes: channel 5 -> Stabilize / AltHold / Loiter; RTL separately, on a momentary switch

Note: the EK3_SRC and FLOW values were taken from the official ArduPilot pages (MTF-01, Optical Flow Setup,
GPS/Non-GPS Transitions). At the first configuration they must be compared with the current documentation,
because parameters are sometimes renamed between stable versions.
