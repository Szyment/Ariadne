# Raspberry Pi 5 as the onboard computer

*As of 27 Aug 2026. System bring-up, power supply, cameras and the MAVLink link to the Pixhawk 6X.*

## Naming note

Repository files use English names (`onboard.py`, `record.sh`, `ariadne-onboard.service`, `ariadne-record@.service`). The Pi still runs the units installed on 28 Aug 2026 under their original names (`ariadne-pokladowy`, `ariadne-nagrywanie@N`, `/usr/local/bin/pokladowy.py`, `nagrywaj.sh`). Commands below refer to the installed names until the next deployment, when both sides are renamed together.

## System

| | |
|---|---|
| Board | Raspberry Pi 5 with the original Active Cooler |
| System | Raspberry Pi OS Lite, Debian 13 (trixie), no graphical environment |
| Hostname | `ariadne-rpi` |
| User | `ariadne` |
| Card | microSD 256 GB, prepared with Raspberry Pi Imager |
| Operating temperature | 40.0–40.6 °C with two cameras and two video streams |

The graphical environment and VNC were deliberately not installed. SSH is sufficient for configuration, logs and scripts, and every additional package is a processor load that in flight comes at the expense of image processing.

SSH access with the key `ariadne_rpi_ed25519`, alias `ssh ariadne` in `~/.ssh/config` on the advisor's computer. SSH was enabled by creating an empty file `ssh` on the boot partition of the card. It works over Ethernet and over Wi-Fi.

## Power supply

Power comes from the X500 V2 power distribution board via XT30, a 5 A fuse on the positive line and a Pololu `reg15b` voltage converter from the D24VxF5 family to the GPIO header:

| Raspberry Pi | Signal |
|---|---|
| pin 2 | 5 V |
| pin 4 | 5 V |
| pin 6 | GND |
| pin 9 | GND |

Two wires per rail, to reduce the voltage drop on the connection. Ground from the XT30 goes straight to the converter's `GND`, without a fuse: interrupting the ground with a fuse turns it into a signal wire of undefined potential.

**Measurement under load, 27 Aug:** 5.01 V with two OV5647 cameras and two video streams, on the assembled vehicle. `vcgencmd get_throttled` returns `0x0`, that is, no undervoltage, no clock throttling and no undervoltage event since boot. The nominal voltage of the Raspberry Pi 5 is 5.1 V, so 5.01 V is below it, and yet it suffices with a margin.

**Automatic start requires a sharp 5 V edge (established 29 Aug).** With a slow voltage rise (soft start of the converter, capacitors, wires) the Pi 5 power controller does not start by itself: the red LED lights up and the board waits for the button. This is exactly what disabled the computer in the field on 28 Aug (card S-14). Workarounds: a momentary button from the **J2** pads (next to the clock battery connector, in parallel with the power button) brought out to the airframe, or a disconnect in the 5 V line plugged in after the converter voltage has settled; a contact edge is always sharp. The field procedure is unchanged: no `RPi: REC active` in QGC = we do not take off. **Decision 29 Aug: manual handling stays.** If the message is absent, press the power button; a relay in the 5 V line was considered and rejected as an unnecessary complication for a fault occurring once in several plug-ins.

Powering through the GPIO header bypasses the USB-C socket together with its negotiation and protection. The voltage and polarity must be measured **before** plugging in the Raspberry, and the pack voltage must never be applied to the GPIO under any circumstances.

Separate infrared illumination, if added, is to be powered from a branch at the converter output, not through the Raspberry board. Every ampere on the 5 V side is about 0.35 A on the 4S side, so before adding illuminators the draw of the whole branch at the converter input must be measured, against the 5 A fuse.

The IR illumination of the night camera consists of two **screw-on 850 nm capsules**: they are fastened to the side holes of the camera board, and the 3.3 V supply goes through the screws from the pads around the holes, that is, through the camera rail and the Raspberry, not from a separate branch (the paragraph above concerns only possible separate floodlights). Two capsules are of the order of 200 mA more; after screwing them on, repeat `vcgencmd get_throttled` under full load. The capsules heat up in continuous operation; do not route the CSI ribbon over them.

Each capsule has a photoresistor and **switches the LEDs on by itself in the dark**. Consequence for the protocol: in the RQ1 illumination-envelope runs the lamps would illuminate the scene for the optical flow (the silicon sensor sees 850 nm) and shift the measured limit; therefore **for RQ1 sessions the capsules are unscrewed, for RQ2 sessions with markers they are screwed on**, and their state is recorded in the session conditions. The TFmini-S rangefinder works in the same 850 nm band, but measures with modulated light at a background immunity of 70 klx; the illuminators do not harm it. Before the first flight with capsules: an A/B test on the bench in the dark (`OF.Qual`, rangefinder reading, frame uniformity), because the fronts of the capsules protrude ahead of the lens plane and could shine sideways into the flow sensor or into the rangefinder windows.

## Shutdown

Cutting 5 V without shutting down the system risks damaging the memory card. Shutdown: `sudo poweroff` locally or `ssh -t ariadne sudo poweroff` from the advisor's computer. The red LED stays lit, because it signals the presence of voltage, not system activity; disconnect only ten to twenty seconds after shutdown.

### Kill switch (SE): failure of version 1 and the fix, 28 Aug

The first implementation worked on the bench and failed in the field the same day. Cause: the program requested the `RC_CHANNELS` stream **once, at its own start**, and a Pixhawk restart clears such requests. In the field the Pixhawk was restarted from QGC after a parameter change, the Raspberry with the running program stayed on, and from that moment the program sat deaf, without frames, without an error and without a trace in the journal, because version 1 had neither retries nor logging.

The audit revealed two further errors that had not yet had the chance to show. First, two version 1 programs (the GNSS clock and the kill switch) would have opened the same serial port simultaneously, and the port distributes received bytes among readers at random; no MAVLink parser would see whole frames. The clock service, however, was never installed, so the conflict remained latent. Second, the kill switch timed the three seconds with the wall clock (`time.time()`), which the clock service shifts by decades; a jump during the countdown would have produced an immediate shutdown from a single frame. Version 2 measures time with `time.monotonic()`.

The fix: **a single daemon `ariadne-pokladowy`** (repository unit `onboard/ariadne-onboard.service`, file `onboard/onboard.py`), the only process on the port, handling the clock and the kill switch together, repeating the stream requests every 30 s (a Pixhawk restart clears the message intervals), and on SE activation first stopping the recording services and executing `sync`, and only then shutting the system down. Version 1 was moved to `archive/_do_usuniecia/onboard-rpi5-v1/`.

Independent emergency path: **the factory power button on the board** (next to the LED). On Raspberry Pi OS Lite a single short press starts a clean system shutdown, a press while off but powered restarts the board, and holding it forces a hard cut-off. It works without MAVLink, so it is the rescue path when the daemon does not respond.

### Kill switch (SE), principle of operation

In the field there is neither a network nor a laptop, so shutting the system down via SSH is out. The solution uses a link that already works anyway: the transmitter's **SE** switch is mapped to channel 9, the Pixhawk reports its state in the `RC_CHANNELS` message on `SERIAL4`, and the `ariadne-wylacznik` service on the Raspberry triggers the system shutdown. Program and service unit: `onboard/`.

Measured channel values: 999 at rest, 2000 when pressed. The threshold in the program is 1700.

Three decisions recorded in the code:

**React to the edge, not to the state.** When the RC link is lost, channels can be frozen or take failsafe values. If the switch was pressed before the loss, there will be no edge and the computer survives the link loss, that is, the moment when its recording is most valuable.

**Remember the state at the first reading.** Powering on with the switch pressed does not shut the system down right after start.

**No arming check.** The Raspberry does not control the flight, so an accidental shutdown costs the data of a run, not the vehicle. The inability to shut the system down in the field would cost the memory card at every pack removal.

Power-on happens exclusively by applying voltage. After a shutdown with the pack connected, a restart requires interrupting the power or a physical button on GPIO3 (`dtoverlay=gpio-shutdown`), which remains an optional emergency path.

**Field procedure:** land, press SE and hold for three seconds, wait until the card activity LED goes out, disarm, unplug the pack.

## Cameras

Two cameras with the OV5647 sensor, detected as `0` and `1` by `rpicam-hello --list-cameras`. The Raspberry Pi 5 has 22-pin connectors, the cameras 15-pin, so 22 → 15 ribbons were used.

Modes of both cameras: 640×480 at 62.5 fps, 1296×972 at 46.3, 1920×1080 at 32.8, 2592×1944 at 15.6.

Both streams work simultaneously:

```bash
rpicam-vid --camera 0 -t 0 --inline --listen -o tcp://0.0.0.0:8888
rpicam-vid --camera 1 -t 0 --inline --listen -o tcp://0.0.0.0:8889
```

**Assembly pitfall.** The first camera was not detected (`No cameras available!`) because of a ribbon inserted the wrong way round on the Raspberry side. The orientation is determined by the side with the exposed contacts, not by the colour of the ribbon. The ribbon is inserted with the power off.

The cameras differ and are not interchangeable:

| | `kam0` | `kam1` |
|---|---|---|
| Lens | small, factory, non-adjustable focus | large, manually focused |
| Infrared filter | present | **none** (NoIR version) |
| IR illumination | — | 850 nm capsules |
| Mounting | rotated by 180° | upright |
| Rotation correction | `rotate=180` in the MP4 when concatenating | none |

The absence of an infrared cut filter in `kam1` gives a permanent pink tint to the image in daylight. This is not a white balance error and cannot be fixed in software; the sensor sees 850 nm together with visible light. It is irrelevant for marker detection, because that works on brightness, not on colour; before any colour tuning one must be aware of it.

### Finding: image rotation only at output, never at recording

`kam0` is mounted rotated by 180° and requires correction. Three ways of setting the rotation at recording were measured and all three fail in the same way: the transformation holds for the first ~8 seconds, after which it disappears **in the middle of the same file**, with a single `rpicam-vid` process:

| Method | Session | Result |
|---|---|---|
| `--rotation 180` | 004 | drops out at the 8th second |
| `--hflip --vflip` | 009 | drops out at the 8th second |
| `dtoverlay=ov5647,rotation=180` in `config.txt` | 012 | drops out at the 8th second |

Even the driver level fails, because libcamera itself programs the flip bits in the sensor when configuring the stream and overwrites the state from the device tree. This is visible in the raw `.h264`, so the concatenation has nothing to do with it.

Final architecture: **1:1 recording without any transformation** (`OBROT=""` in `record.sh` for both cameras; the raw file is then uniform from the first frame to the last, `kam0` upside down), and the rotation is added by `stitch_recording.sh` as a `rotate=180` rotation matrix in the MP4 header, only for `kam0`. No re-encoding, uniform for the whole file; players and ffmpeg apply the matrix themselves. The raw segments remain unrotated; any image processing from `kam0` (markers, calibration) must account for the rotation itself.

Confirmed on `sesja_014`: zero orientation changes in the raw files of both cameras (170 measurement frames each), `rotate=180` present in the `kam0` MP4, orientation of both recordings confirmed visually over the whole length.

The versions of the onboard files are reconciled with the repository by SHA-256 sums (scripts in `/usr/local/bin`, services in `/etc/systemd/system`). The source of truth is `onboard/`; on the onboard computer there are only copies deployed by `install`, no editing in place.

Archival recordings from before 29 Aug (`sesja_010`) have the image of both cameras upside down and require `-vf hflip,vflip` when concatenating.

The focus of `kam1` was set on 29 Aug on the TCP stream preview, on printed text at about 1 m. At a short focal length the depth of field extends from a few tens of centimetres to infinity, so the 3.5 m of the run lies in the middle of the range and there is no need to focus from flight altitude. The boundary is around 6 mm focal length; above it the focus distance starts to matter.

Preview for focusing, with a delay small enough to turn the ring:

```bash
ssh ariadne 'sudo systemctl stop ariadne-nagrywanie@1'
ssh ariadne 'rpicam-vid --camera 1 -t 0 --inline --listen -o tcp://0.0.0.0:8889'
ffplay -fflags nobuffer -flags low_delay -framedrop -analyzeduration 0 -probesize 32 tcp://ariadne-rpi:8889
```

The recording services hold both cameras, so before the preview they must be stopped, and after focusing started again and **checked** that they came up:

```bash
ssh ariadne 'sudo systemctl start ariadne-nagrywanie@0 ariadne-nagrywanie@1 && \
             systemctl is-active ariadne-nagrywanie@0 ariadne-nagrywanie@1'
```

## MAVLink link to the Pixhawk 6X

The Pixhawk's GPS2 port, that is, UART8, that is, `SERIAL4`:

| Pixhawk GPS2 | Raspberry Pi |
|---|---|
| pin 2, TX8 | pin 10, GPIO15, RX |
| pin 3, RX8 | pin 8, GPIO14, TX |
| pin 6, GND | pin 14, GND |
| pin 1, +5 V | not connected |

Vehicle parameters: `SERIAL4_PROTOCOL` = 2 (MAVLink2), `SERIAL4_BAUD` = 115, `SERIAL4_OPTIONS` = 0, `GPS2_TYPE` = 0.

### Finding: on the Raspberry Pi 5 `/dev/serial0` leads to the wrong place

The port opened, `minicom` saw it, and there was no heartbeat. The cause lies in device naming, not in the soldering.

On the Raspberry Pi 5 the symlink `/dev/serial0` points to `/dev/ttyAMA10`, that is, to UART10 brought out on a **separate three-pin debug connector**. The UART on pins 8 and 10 of the GPIO header is UART0, that is, **`/dev/ttyAMA0`**. On the Raspberry Pi 4 and earlier, `serial0` pointed to the GPIO header, and this is where the widespread advice to always use this alias comes from. On the Pi 5 it is wrong.

Bring-up:

1. `/boot/firmware/config.txt`, section `[all]`:

```text
dtparam=uart0=on
```

2. Reboot and check that `/dev/ttyAMA0` exists.
3. `/boot/firmware/cmdline.txt` must not contain `console=ttyAMA0` or `console=serial0`. In this installation there is only `console=tty1`.
4. The user must belong to the `dialout` group, because the device has permissions `crw-rw---- root dialout`.
5. In applications give `/dev/ttyAMA0` directly, never through the `serial0` alias.

### Confirmation

```bash
sudo stty -F /dev/ttyAMA0 115200 raw -echo
sudo timeout 5 cat /dev/ttyAMA0 | hexdump -C
```

First frame received on 27 Aug at 20:02:

```text
fd 09 00 00 a6 01 01 00 00 00 00 00 00 00 02 03 51 03 03 a5 c1
```

Breakdown: `fd` MAVLink 2 marker, `09` payload length, `a6` sequence number, `01 01` system 1 and component 1, that is, the autopilot, `00 00 00` message 0, that is, HEARTBEAT, then custom mode 0 (Stabilize), type 2 (quadrotor), autopilot 3 (ArduPilotMega), mode flags `0x51` not armed, status 3 (standby), MAVLink version 3. Message 111, TIMESYNC, also appears in the stream.

Reception with pymavlink in the `~/venvs/mav` environment:

```python
from pymavlink import mavutil
m = mavutil.mavlink_connection('/dev/ttyAMA0', baud=115200)
m.wait_heartbeat(timeout=10)
```

returns `HEARTBEAT {type: 2, autopilot: 3, base_mode: 81, custom_mode: 0, system_status: 3, mavlink_version: 3}`.

`pymavlink` was installed in a virtual environment, because the package is not available through APT in Debian 13.

## Recording architecture: final decision, 28 Aug 2026

After three field failures and two code audits the architecture is frozen. Changing this section requires a new full audit.

**Rule: recording is governed exclusively by systemd.** The camera services start at boot and end at system shutdown. The onboard daemon is an observer: it reports status in QGC (`REC active` / `REC off` after start, `REC cam N DOWN` separately for each failed camera), sets the clock from GNSS and handles the SE switch; on SE it stops the cameras just before shutdown, so that the last segment is closed explicitly. Arming-gated start was rejected deliberately: it added the chain daemon → port → heartbeat to the start of recording, and the flight recording is an absolute requirement, against which saving card space (1.3 GB/h on a 256 GB card) carries no weight.

Failure matrix: every single failure degrades the system towards "records too much", never "does not record":

| Failure | Effect |
|---|---|
| daemon | continuous recording without reports; no `REC active` in QGC = we do not take off |
| camera process in flight | the service ends in failure, systemd restarts it after 2 s; a new timestamp in the name rules out overwriting; `REC cam N DOWN` in QGC |
| full card | start blocked below 5 GB; during recording a clean stop by the watchdog every 60 s |
| wrong clock | directory `bez-zegara`, the files exist |
| power loss | at most the current 60 s segment is lost, the rest is playable (raw H.264, headers in every segment) |
| **Raspberry power path** | **the only failure without a software guard**, hence the field rule: no `REC active` in QGC before take-off = we do not fly; it is this rule that also detects a dead computer power supply (the failure of the evening of 28 Aug) |

The final adversarial review (28 Aug) confirmed requirements R1/R2/R4/R6 by execution and pointed out three defects fixed before the freeze: the camera script exited with code 0 after an `rpicam-vid` crash and blocked the restart; the `cam DOWN` report lost the failure of the second camera during an incident of the first; `RC_CHANNELS` was not filtered by sender. The systemd journal is persistent (`/var/log/journal`), so every future failure leaves a trace.

## Continuous recording

Recording is controlled by arming: the onboard daemon starts the services `ariadne-nagrywanie@0` and `@1` on arming and stops them on disarming, so only flight material lands on the card. Each arming cycle gets its own directory `~/nagrania/sesja_NNN_DATA/` (the number is always highest + 1, never reused), and the file names carry the process start timestamp, so that a camera restart in flight does not overwrite earlier segments. Recording in segments of 60 s, raw H.264 with headers in every segment (`--inline`). The script refuses to start below 5 GB of free space and monitors space every minute during recording; if a camera fails in flight, the daemon reports `RPi: REC cam N DOWN` in QGC. Manual start for ground tests: `systemctl start ariadne-nagrywanie@0`; it gets its own session directory.

Version 3 of these programs was preceded by a code audit (28 Aug), which found, among other things, a session directory created by root without write permission for the camera user, no supervision of the cameras in flight, session splitting after a daemon restart, and the possibility of setting the clock from the ground control station computer instead of from GNSS. All the audit findings are fixed and covered by tests executed off the drone, including a write-permission test with a real root/ariadne user separation.

Safe termination of recording has three paths, in order from best: the SE switch (the daemon stops recording, executes `sync`, shuts the system down), the factory power button (systemd sends SIGINT to `rpicam-vid`, the segment is closed), unplugging the pack without anything (only the last segment, at most 60 seconds, is lost; the others are playable, because the H.264 stream does not require a closed header, unlike MP4).

### Viewing the recordings

The segments of one run are concatenated by a plain `cat`, because `--inline` puts the decoder headers into each of them. The whole is done by `analysis/stitch_recording.sh`:

```bash
rsync -av ariadne:nagrania/<katalog_sesji>/ ~/Documents/Projects/Ariadne/tmp-nagrania/
cd ~/Documents/Projects/Ariadne
analysis/stitch_recording.sh tmp-nagrania kam0
analysis/stitch_recording.sh tmp-nagrania kam1
```

The output goes to `movies/`, outside the git repository; recordings from one flight weigh several hundred megabytes.

The frame rate of 30 fps comes from `record.sh`, where it is set. Give it as the **input** option `-r`; `-framerate` does not work, because the demuxer then reads the timing from the VUI in the SPS header and ignores the option; verified on ffmpeg 4.4 and 6.1.

### Finding: B-frames make the image stutter after concatenation

The recordings of 29 Aug stuttered on playback, even though the live stream from the same camera was smooth. Measurements excluded everything else:

| Checked | Result |
|---|---|
| Dropped frames | each of the 24 segments has exactly 1830 frames per 61 s |
| Repeated frames | 599 of 600 unique in a 20 s window (`mpdecimate`) |
| Frame order in the MP4 | consistent with decoder order, 266 of 268 identical |
| In-frame skew from vibration | standard deviation 1.5 px on a height of 972 (`vidstabdetect`) |

The cause is B-frames. The raw `.h264` carries no timestamps, so ffmpeg numbers the frames in **coding** order and writes `pts` equal to `dts`; in the finished MP4 there are no composition offsets. With B-frames the coding order differs from the display order: the player reorders the frames according to the POC from the stream, but takes the timing from the container, and these two orders diverge. The TCP stream had no container at all, so the decoder used only the order from the stream and there was no stutter.

Resolution: the same 30-second fragment re-encoded with `-bf 0` stopped stuttering completely.

Fix at the source: `--profile baseline` in `record.sh`. The baseline profile has neither B-frames nor CABAC, so the problem disappears at recording and nothing needs to be re-encoded, and the Pi 5 processor, software-encoding two streams at once, gets less work. After the first recording check:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=has_b_frames -of csv=p=0 plik.h264
```

Required `0`. Recordings from before this change are re-encoded and lie in `movies/_bez_klatek_B/`.

### Finding: the time in the file name is not the recording time

The timestamp in the name is created at the start of `record.sh`, that is, before `onboard.py` sets the clock from GNSS. Without an RTC battery the Raspberry resumes the clock on power-up from the moment of the last shutdown (`fake-hwclock`), so the timestamp is set back by as long as the computer was off.

Measured 29 Aug:

| Session | Time in the name | Measured start | Discrepancy |
|---|---|---|---|
| `sesja_009` | 10:44:28 | 08:49:15 UTC = 10:49:15 local | 4 min 47 s |
| `sesja_010` | 11:15:35 | 09:53:04 UTC = 11:53:04 local | 37 min 29 s |

The discrepancy grows, because `sesja_010` started after a reboot: its name, 11:15:35, falls 15 s after the end of `sesja_009`, that is, exactly where `fake-hwclock` saved the clock at shutdown. The computer was off for 37 minutes and the clock was set back by that much.

Two conclusions. To align the video with the Pixhawk log, use `mtime`, not the file name; this is what the script calculates anyway. An RTC battery (`RPI-23926`) removes the cause; until it is fitted, the file name remains only an identifier, not a time.

The agreement of both cameras is a check in itself: for both sessions `kam0` and `kam1` gave the same start to the second, with a difference of one frame in the frame count.

## To do

- [ ] Raise the `SERIAL4` speed to 921600 if the MAVLink streams at 115200 turn out to be too slow
- [ ] Measure the draw of the whole 5 V branch at the converter input before adding infrared illumination
- [ ] Mount the computer and harnesses on the vehicle and check the effect on take-off mass and balance

Screenshots from the bring-up of 27 Aug (RPi terminal and camera preview 19:37, `SERIAL4_PROTOCOL` 19:42, `SERIAL4_BAUD` 19:43): `build-log/photos/2026-08-27/2026-08-27_mac-screenshot_*`.
