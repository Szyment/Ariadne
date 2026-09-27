#!/bin/bash
# Continuous recording from one camera, in 60 s segments.
# Usage: record.sh <camera_number>
#
# The file name carries the process start stamp (kamN_HHMMSS_%05d.h264):
# if rpicam-vid died in flight and was restarted by systemd, the new
# process would start the segment counter from zero and WITHOUT the stamp
# would overwrite the earlier segments of the same session.
#
# 60 s segments: a sudden loss of power costs at most the last file.
# Raw H.264 without a container: the stream can be played back even when
# cut in half, MP4 requires a closed header.

KAMERA="$1"
KATALOG=/home/ariadne/nagrania
MIN_WOLNE_MB=5000

# NO transform in rpicam-vid, for both cameras.
#
# Finding of 29 Aug: camera 0 requires a 180 degree rotation, but a transform
# requested here (both --rotation 180 and --hflip --vflip) holds only for the
# first eight seconds, after which it disappears in the middle of the same
# file, within a single rpicam-vid process. It is visible in the raw .h264, so
# libcamera loses it when reconfiguring the pipeline, not the concatenation.
# Camera 1, without a transform, is stable for the whole recording.
#
# Therefore the recording is written without any transform (the whole file is
# then uniform) and the rotation of camera 0 is added by stitch_recording.sh as
# a rotation matrix in the MP4. This costs nothing, because it needs no
# re-encoding, and it is the same for the whole recording.
OBROT=""

mkdir -p "$KATALOG"

sprawdz_miejsce() {
    wolne=$(df -Pm "$KATALOG" 2>/dev/null | awk 'NR==2 {print $4}')
    case "$wolne" in
        ''|*[!0-9]*)
            echo "Cannot read the free space, aborting." >&2
            return 1 ;;
    esac
    if [ "$wolne" -lt "$MIN_WOLNE_MB" ]; then
        echo "Not enough space: ${wolne} MB, ${MIN_WOLNE_MB} MB required." >&2
        return 1
    fi
    return 0
}
sprawdz_miejsce || exit 1

# session directory: one per boot, shared by both cameras (lock +
# boot identifier); the number is always the highest existing + 1
SESJA=""
if true; then
    exec 9>"${KATALOG}/.blokada" || exit 1
    flock 9
    BOOT=$(cut -c1-8 /proc/sys/kernel/random/boot_id)
    SESJA=$(find "$KATALOG" -maxdepth 1 -type d -name "sesja_*_${BOOT}" | head -1)
    if [ -z "$SESJA" ]; then
        NNN=$(find "$KATALOG" -maxdepth 1 -type d -name 'sesja_*' -printf '%f\n' \
              | sed -E 's/sesja_0*([0-9]+).*/\1/' | sort -n | tail -1)
        NNN=$(printf "%03d" $(( ${NNN:-0} + 1 )))
        if [ "$(date +%Y)" -ge 2026 ]; then
            DATA=$(date +%Y%m%d-%H%M)
        else
            DATA="bez-zegara"
        fi
        SESJA="${KATALOG}/sesja_${NNN}_${DATA}_${BOOT}"
        mkdir -p "$SESJA" || exit 1
    fi
    flock -u 9
fi

ZNACZNIK=$(date +%H%M%S)

# %05d numbers the segments; --inline inserts the SPS/PPS headers into
# every segment, so that each file can be played back on its own
#
# --profile baseline disables B-frames. Raw .h264 carries no timestamps, so
# when concatenating, ffmpeg numbers the frames in CODING order and writes
# pts equal to dts. With B-frames the coding order differs from the display
# order, the player reorders the frames by the POC from the stream but takes
# the timing from the container, and the picture stutters. Verified on 29 Aug
# on session 010: re-encoding the same fragment with -bf 0 removed the
# stutter completely. The baseline profile also has no CABAC, so it takes
# some work off the processor, which on the Pi 5 encodes two streams at once
# in software.
rpicam-vid \
    --camera "$KAMERA" \
    --timeout 0 \
    --nopreview \
    --width 1296 --height 972 --framerate 30 \
    --codec h264 --inline --profile baseline \
    --segment 60000 \
    $OBROT \
    --output "${SESJA}/kam${KAMERA}_${ZNACZNIK}_%05d.h264" &
PID=$!

# INT ends rpicam-vid cleanly (closes the segment); should the process have
# inherited an ignored SIGINT (this is how the shell treats background
# processes), TERM follows after 5 s
ZATRZYMANE_PRZEZ_NAS=0
zatrzymaj() {
    ZATRZYMANE_PRZEZ_NAS=1
    kill -INT "$PID" 2>/dev/null
    for _ in 1 2 3 4 5; do
        kill -0 "$PID" 2>/dev/null || return
        sleep 1
    done
    kill -TERM "$PID" 2>/dev/null
}
trap 'zatrzymaj' INT TERM

# at start rpicam-vid opens a zero-byte file with the literal pattern
# name; -size 0 protects against deleting anything with content
sleep 3
find "$SESJA" -maxdepth 1 -name "kam${KAMERA}_${ZNACZNIK}_%05d.h264" -size 0 -delete

# supervision: free-space check every minute; below the threshold stop the
# recording cleanly instead of letting rpicam-vid fill the card to zero
while kill -0 "$PID" 2>/dev/null; do
    sleep 60 &
    SPIACY=$!
    wait "$SPIACY" 2>/dev/null
    if ! kill -0 "$PID" 2>/dev/null; then
        break
    fi
    if ! sprawdz_miejsce; then
        echo "Running out of space, stopping the recording of camera ${KAMERA}." >&2
        zatrzymaj
        break
    fi
done
while kill -0 "$PID" 2>/dev/null; do
    wait "$PID"
done
# an rpicam-vid crash without our decision must be a service failure; then
# Restart=on-failure restarts the camera (new stamp, no overwriting);
# a stop by signal or by the space supervision is a clean exit
if [ "$ZATRZYMANE_PRZEZ_NAS" -eq 0 ]; then
    echo "rpicam-vid exited on its own, reporting failure for restart" >&2
    exit 1
fi
exit 0
