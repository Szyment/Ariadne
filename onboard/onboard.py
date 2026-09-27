#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ariadne, onboard daemon for the Raspberry Pi 5. Version 3, 28 Aug 2026.

ONE process on the serial port to the Pixhawk. The daemon is only an
OBSERVER of the recording. This is an architectural decision from 28 Aug,
after three field failures: the recording is governed by systemd itself
(start at boot, stop at system shutdown), because every link added to
that chain lowered reliability, and a recording of the flight is an
absolute requirement. Every daemon failure degrades the system towards
"records too much", never "does not record".

Tasks:
1. Clock from GNSS time (SYSTEM_TIME, from the autopilot only).
2. System shutdown with the SE button of the transmitter (channel 9):
   a rising edge held for ZWLOKA seconds; before poweroff it stops the
   camera services so that the last segment is closed explicitly.
3. STATUSTEXT reports in QGC: recording state after start
   (REC active / REC off) and a warning when a camera dies
   (REC cam DOWN). Field rule: no "REC active" means no take-off.

Decisions in the code:
- Edge, not level: when the RC link is lost the channels freeze; if SE
  was up before the loss there will be no edge and the computer
  survives the link loss.
- Channel values 0 and >=65535 mean "no RC reception", not a button
  position: the state returns to unknown, so switching the transmitter
  on with SE up does NOT produce an edge and does not shut the system
  down.
- No arming check in the shutdown switch (decision of 27 Aug).
- time.monotonic() for the countdown: the daemon itself moves the wall
  clock by decades.
- After a daemon restart in flight the state is read from systemd
  (services active = recording in progress), not assumed from scratch;
  otherwise every restart would create an empty directory for a new
  session.
"""

import subprocess
import time

from pymavlink import mavutil

PORT = "/dev/ttyAMA0"   # Pi 5: UART on pins 8/10; /dev/serial0 is the debug connector
BAUD = 115200
KANAL = 9               # SE button of the transmitter
PROG = 1700             # idle ~999, pressed ~2000
ZWLOKA = 3.0            # seconds held up required for shutdown
PROG_ROKU_2026 = 1767225600  # 1 Jan 2026 UTC; a time older than the project is garbage
OKRES_OKRESOWY = 30.0   # re-requesting the streams and checking the cameras
NAGRYWANIE = ["ariadne-nagrywanie@0", "ariadne-nagrywanie@1"]  # unit names as currently installed on the Pi; repository files are ariadne-record@.service (rename together with the next deployment)


def log(tekst):
    print(tekst, flush=True)


def melduj(m, tekst):
    """STATUSTEXT; the Pixhawk forwards it to the other links, so it is
    visible in the QGC message window, the only view of the daemon in
    the field."""
    try:
        m.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,
                              tekst[:50].encode())
    except Exception:
        pass


class Wylacznik:
    """SE button logic, separated so that it can be tested without the loop."""

    def __init__(self):
        self.poprzednio = None      # None = unknown state
        self.od_kiedy = None        # time.monotonic() of the edge

    def podaj(self, wartosc, teraz):
        """Returns True when the system should be shut down."""
        if wartosc <= 0 or wartosc >= 65535:
            # no RC reception, not a button position; the state returns to
            # unknown, so RC appearing with SE up is not an edge
            self.poprzednio = None
            self.od_kiedy = None
            return False
        wysoko = wartosc > PROG
        if self.poprzednio is None:
            self.poprzednio = wysoko
            return False
        if wysoko and not self.poprzednio:
            self.od_kiedy = teraz
        elif not wysoko:
            self.od_kiedy = None
        self.poprzednio = wysoko
        return self.od_kiedy is not None and teraz - self.od_kiedy > ZWLOKA


def popros_o_strumienie(m):
    for msg_id, okres_us in ((mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS, 200000),
                             (mavutil.mavlink.MAVLINK_MSG_ID_SYSTEM_TIME, 1000000)):
        m.mav.command_long_send(
            m.target_system or 1, 1,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
            msg_id, okres_us, 0, 0, 0, 0, 0)


def ustaw_zegar(unix_s):
    """Returns True only when the clock has been confirmed set."""
    nap = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(unix_s))
    try:
        wynik = subprocess.run(["/usr/bin/date", "-u", "-s", nap], timeout=10)
        if wynik.returncode != 0:
            return False
        subprocess.run(["/sbin/hwclock", "-w"], check=False, timeout=10)
    except Exception:
        return False
    log("clock set to %s UTC" % nap)
    return True


def aktywne_kamery():
    """List of recording services in the active state."""
    out = []
    for u in NAGRYWANIE:
        try:
            w = subprocess.run(["/usr/bin/systemctl", "is-active", "--quiet", u],
                               timeout=10)
            if w.returncode == 0:
                out.append(u)
        except Exception:
            pass
    return out


def kontrola_kamer(m, zgloszone):
    """Report every NEWLY dead camera; zgloszone is the set of cameras
    already reported, cleared when the camera comes back to life."""
    zywe = aktywne_kamery()
    brak = frozenset(NAGRYWANIE) - frozenset(zywe)
    nowe = brak - zgloszone
    if nowe:
        n = ",".join(sorted(u[-1] for u in nowe))
        log("WARNING: camera(s) %s not recording" % n)
        melduj(m, "RPi: REC cam %s DOWN" % n)
    return brak


def zamknij_system():
    log("shutting down the system")
    try:
        subprocess.run(["/usr/bin/systemctl", "stop"] + NAGRYWANIE,
                       check=False, timeout=60)
    except Exception as e:
        log("stopping the recording at shutdown: %s" % e)
    try:
        subprocess.run(["/bin/sync"], check=False, timeout=30)
    except Exception:
        pass
    subprocess.run(["/sbin/poweroff"], check=False)


def polacz():
    while True:
        try:
            # source_system=1 (same as the vehicle), component 191 (onboard
            # computer): QGC shows our STATUSTEXT as vehicle messages
            m = mavutil.mavlink_connection(PORT, baud=BAUD,
                                           source_system=1,
                                           source_component=191)
            hb = None
            while hb is None:
                hb = m.wait_heartbeat(timeout=30)
            log("heartbeat from system %d" % m.target_system)
            popros_o_strumienie(m)
            melduj(m, "RPi: shutdown switch ready")
            return m
        except Exception as e:
            log("connection failed (%s), retrying in 5 s" % e)
            time.sleep(5)


def od_autopilota(m, msg):
    return msg.get_srcComponent() == 1 and msg.get_srcSystem() == m.target_system


def main():
    m = polacz()
    wyl = Wylacznik()
    zegar_ustawiony = False
    if len(aktywne_kamery()) == len(NAGRYWANIE):
        melduj(m, "RPi: REC active")
    else:
        melduj(m, "RPi: REC off")
    kamery_zgloszone = frozenset()
    ostatni_okres = time.monotonic()

    while True:
        try:
            msg = m.recv_match(type=["RC_CHANNELS", "SYSTEM_TIME"],
                               blocking=True, timeout=10)
        except Exception as e:
            log("port error (%s), reconnecting" % e)
            m = polacz()
            wyl = Wylacznik()
            continue

        teraz = time.monotonic()
        if teraz - ostatni_okres > OKRES_OKRESOWY:
            popros_o_strumienie(m)       # a Pixhawk restart clears the intervals
            kamery_zgloszone = kontrola_kamer(m, kamery_zgloszone)
            ostatni_okres = teraz

        if msg is None:
            continue

        typ = msg.get_type()

        if typ == "SYSTEM_TIME":
            if not od_autopilota(m, msg):
                continue                 # the time must come from GNSS, not from the laptop
            if not zegar_ustawiony and msg.time_unix_usec / 1e6 > PROG_ROKU_2026:
                if ustaw_zegar(msg.time_unix_usec / 1e6):
                    zegar_ustawiony = True
                    melduj(m, "RPi: clock set from GNSS")
            continue

        if not od_autopilota(m, msg):
            continue                     # RC_CHANNELS only from the autopilot

        wartosc = getattr(msg, "chan%d_raw" % KANAL)
        stara_faza = wyl.od_kiedy
        if wyl.podaj(wartosc, teraz):
            melduj(m, "RPi: shutting down")
            zamknij_system()
            return
        if wyl.od_kiedy is not None and stara_faza is None:
            log("SE up, counting down %.0f s" % ZWLOKA)
            melduj(m, "RPi: SE detected, hold %.0f s" % ZWLOKA)
        elif wyl.od_kiedy is None and stara_faza is not None:
            log("SE released before the delay elapsed")
            melduj(m, "RPi: SE released, no shutdown")


if __name__ == "__main__":
    main()
