# RadioMaster Pocket: EdgeTX 2.12.2 and Yaapu Telemetry

**Date performed:** 26 Aug 2026  
**Transmitter:** RadioMaster Pocket, internal ExpressLRS 2.4 GHz module, CE_LBT domain  
**EdgeTX model:** `FPV DRONE`  
**Scope:** EdgeTX and SD card update, and Yaapu installation for the 128×64 screen

## 1. Result

| Element | Before | After | State |
|---|---:|---:|---|
| EdgeTX | `2.10.0-RM` | `2.12.2` | verified on the `VERSION` page |
| EdgeTX bootloader | initial version not established | `2.12.2` | `Flash successful` message |
| SD card package | older | `bw128x64-v2.12.1` | matches the Pocket's monochrome screen |
| Model and radio settings | `FPV DRONE` | preserved | `currModel: 1`, the model starts normally |
| Yaapu Telemetry | no script | 128×64 variant installed | runs as `yaapu7` |
| ExpressLRS TX/RX | `3.3.1 CE_LBT` | unchanged | deliberately outside the scope of the update |

After the restart the radio reported `edgetx-pocket v2.12.2`. The new hexagonal splash screen comes from the current EdgeTX assets and does not indicate a loss of configuration.

## 2. Sources and identification of the correct image

The firmware was downloaded from the official [EdgeTX 2.12.2](https://github.com/EdgeTX/edgetx/releases/tag/v2.12.2) release. From the bundle file, the image for the `pocket` target was selected:

```text
pocket-3673c51.bin
edgetx-pocket-2.12.2 (3673c518)
size: 518012 B
SHA-256: ee7e86da38dd9fa50f72de986c830ce93f7fc9e6b832ff38683fcedbe086d19a
```

The SD package `bw128x64-v2.12.1.zip` comes from the [EdgeTX SD Card](https://github.com/EdgeTX/edgetx-sdcard/releases/tag/v2.12.1) project. The SD package number may be lower than the firmware number; it is the proper current asset release for this screen class.

Checksums of the downloaded archives:

```text
edgetx-firmware-v2.12.2.zip
a97a9d869d1dd163839689c79f20f2c117149d8099c8f7f886acf21d9c716860

bw128x64-v2.12.1.zip
9cbd143da3523b256c1cd08842fe6184101210074e998016b6f99c0871539bb5
```

The source files were kept in [`downloads/edgetx-2.12.2/`](downloads/edgetx-2.12.2/), and the extracted image in [`staging/`](staging/).

## 3. Backups

Before the change, a full copy of the SD card was made. It covers models, radio settings, scripts, sounds and earlier firmware files:

- [`backup_2026-08-26_pre-edgetx-2.12.2/`](backup_2026-08-26_pre-edgetx-2.12.2/): 1608 files from the SD card before the update;
- [`backup_2026-08-26_pre-edgetx-2.12.2/internal-flash-1MB.bin`](backup_2026-08-26_pre-edgetx-2.12.2/internal-flash-1MB.bin): a full 1 MiB read of the STM32 internal memory;
- [`backup_2026-08-26_pre-yaapu/`](backup_2026-08-26_pre-yaapu/): 125 files from the script directories before the Yaapu installation.

The STM32 memory copy has the following checksum:

```text
size: 1048576 B
SHA-256: 2081add31f0955dbe9e7eea1d3b5c9f41132e32cd1174496cb29d6d4fd268df1
```

The read was made after the bootloader update but before the main firmware update. The recovery image therefore contains the EdgeTX 2.12.2 bootloader and the main firmware `edgetx-pocket-2.10.0-RM (1fdb58ba)`.

## 4. SD card update

1. The radio was started normally and connected through the upper USB-C port.
2. `USB Storage (SD)` was selected on the radio.
3. Reading `RADIO/radio.yml` confirmed:

   ```text
   semver: 2.10.0
   board: pocket
   ```

4. The contents of the default `bw128x64-v2.12.1` package were merged onto the card.
5. The existing `MODELS`, `RADIO`, sounds, ExpressLRS scripts and other user additions were preserved.
6. The verified image `edgetx-pocket-2.12.2.bin` was copied to `/FIRMWARE`.
7. After the operation the models and settings were compared with the backup again; no content changes were found.

## 5. Bootloader and main firmware update

### Bootloader from the SD card

In the SD card browser on the radio, the EdgeTX 2.12.2 file was selected with the `Flash bootloader` command. The radio finished the operation with the message `Flash successful`.

### Full image via STM32 DFU

The microcontroller's hardware DFU mode was used to write the main firmware:

1. The radio was switched off.
2. The upper USB-C was connected without switching the radio on; a black screen is correct in this mode.
3. macOS detected `STM32 BOOTLOADER`, VID:PID `0483:df11`, serial number `388433863235`.
4. `dfu-util 0.11` reported for interface `alt=0`:

   ```text
   @Internal Flash /0x08000000/04*016Kg,01*064Kg,07*128Kg
   ```

   The map corresponds to the 1 MiB internal memory of an STM32F4 and confirms the write address `0x08000000`.

5. Before writing, the full 1 MiB of memory was read:

   ```sh
   dfu-util -d 0483:df11 -a 0 -s 0x08000000:1048576 \
     -U internal-flash-1MB.bin
   ```

6. The verified image was written with the command:

   ```sh
   dfu-util -d 0483:df11 -a 0 -s 0x08000000:leave \
     -D pocket-3673c51.bin
   ```

7. The program finished the write with the messages `Download done` and `File downloaded successfully`, then left DFU.

The warning `Invalid DFU suffix signature` concerned the absence of the optional DFU suffix in the raw `.bin` file; it did not indicate an error in the image or the write.

## 6. Yaapu Telemetry installation

The source was the supplied `master` branch package of the [Yaapu FrSky Telemetry Script](https://github.com/yaapu/FrskyTelemetryScript) project. The archive had the checksum:

```text
yaapu.zip
SHA-256: 04d423953cc5044ad694cf63dbbdcbb0aa99c2a02f33221feaa1a794ec0f5ff8
archive reference: 267060f70b85124611d5f3dcbae8e6caff9d3f24
version embedded in the script: Yaapu 2.1.0-dev (e83a693)
```

Compatibility was established on the basis of three independent features:

- the Yaapu README directs EdgeTX 2.11 and newer to the `master` branch;
- the RadioMaster Pocket has a monochrome 128×64 screen, so the correct directory is `OTX_ETX/bw128x64`;
- the header of the compiled files is `1b 4c 75 61 53` (`.LuaS`), that is, Lua 5.3 bytecode used by EdgeTX since version 2.11.

Installed:

```text
/SCRIPTS/TELEMETRY/yaapu7.luac
/SCRIPTS/TELEMETRY/yaapu/*.luac       (17 libraries)
/SCRIPTS/TOOLS/Yaapu Config.lua
/SCRIPTS/TOOLS/Yaapu Debug.lua
/SCRIPTS/TOOLS/Yaapu DebugCRSF.lua
/MODELS/yaapu/*                        (example files)
```

The card already held 511 sound files in `/SOUNDS/yaapu0`. A check comparison showed the content matched the source, so about 36 MiB of data was not copied again. The AppleDouble helper files `._*`, created by macOS during copying, were removed only from the newly installed paths.

In the `FPV DRONE` model the telemetry screen was set:

```text
DISPLAY → Screen 1 → Script → yaapu7
SYS → TOOLS → Yaapu Config → CRSF enabled
```

`NO TELEMETRY` with the drone switched off is the expected state: the RP1 V2 receiver has no power then. After the drone was powered, the radio began to detect telemetry. This is a preliminary verification on the bench; before flight, the update of all key Yaapu fields must be checked.

Yaapu requires ArduPilot and passthrough telemetry. It is not compatible with Betaflight or INAV.

## 7. Audit of the ArduPilot configuration

During this procedure **no flight controller parameters were changed**. The latest saved export of 23 Aug 2026 contains:

```text
SERIAL6_PROTOCOL = 23    # RCIN/CRSF, correct
SERIAL6_BAUD     = 57
RC_OPTIONS       = 32
```

The official [ArduPilot CRSF Telemetry](https://ardupilot.org/copter/docs/common-crsf-telemetry.html) documentation requires bit 8 of the `RC_OPTIONS` parameter for the passthrough extensions used by Yaapu. Bit 8 has the value `256`.

If, after the drone is powered, Yaapu detects the link but does not update the full ArduPilot data, the **current parameter from the controller** must be read, rather than assuming that the export of 23 Aug is still current. For the saved value `32`, the result with the passthrough bit added would be:

```text
32 + 256 = 288
```

`32` must not be replaced with `256` alone, because that would remove the existing bit 5. After any change, a parameter write, a controller restart and a repeat bench test without propellers are required. In the current export no `SERIALx_PROTOCOL` port has the value `10`, so there is no conflict with a Serial Passthrough type port as described in the ArduPilot documentation.

## 8. Elements deliberately left unchanged

- The firmware of the internal ExpressLRS module remained `3.3.1 CE_LBT`.
- The firmware of the RadioMaster RP1 V2 receiver remained `3.3.1 CE_LBT`.
- The binding phrase and the regulatory domain were not changed.
- The EdgeTX models, channel mapping, switches and failsafe were not changed.
- The Pixhawk 6X parameters were not changed.

Limiting the scope to EdgeTX and the SD script protects the working TX/RX pair from an unintended migration of the major ExpressLRS version.

## 9. Verification before flight

After the update and the script installation, a test without propellers is required:

1. confirm the version `edgetx-pocket v2.12.2`;
2. confirm the active model `FPV DRONE`;
3. check the correct stick channels and the ARM switch in Mission Planner;
4. check the ELRS link, telemetry, Yaapu and the flight mode messages;
5. switch off the transmitter with the drone disarmed and confirm the failsafe;
6. fit the propellers only after the full test.

## 10. Recovery

The full STM32 memory can be restored through the same hardware DFU mode, using only the image assigned to this transmitter and the verified address `0x08000000`. Restoring `internal-flash-1MB.bin` reverts the main firmware to `2.10.0-RM`, leaving the 2.12.2 bootloader. The SD contents are restored separately from the `backup_2026-08-26_pre-edgetx-2.12.2/` directory.

Memory restoration is an emergency procedure. It should not be performed preventively, nor with an image from a different hardware target.
