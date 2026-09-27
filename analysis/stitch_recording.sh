#!/bin/bash
# Joins the .h264 segments from one camera into a single MP4.
#
#   ./stitch_recording.sh <session_dir> [kam0|kam1] [output_dir]
#
# 30 fps comes from record.sh (--framerate 30). Pass it as -r on the INPUT;
# the demuxer ignores -framerate in favour of the timing from the VUI in the SPS.
# cat is enough, because --inline repeats the SPS and PPS in every segment.

set -eu

DIR="${1:?give the session directory}"
CAMERA="${2:-kam0}"
OUT="${3:-movies}"

mkdir -p "$OUT"
NAME="$(basename "$(ls "$DIR/${CAMERA}"_*_[0-9][0-9][0-9][0-9][0-9].h264 | head -n 1)" | sed -E 's/_[0-9]+\.h264$//')"

# Date for the file name: from the session directory name (sesja_NNN_YYYYMMDD-HHMM_xxx),
# and when it is not there, from the modification date of the first segment. The time
# in the name is sometimes behind (clock before the GNSS correction), but the date is reliable.
DATE="$(basename "$DIR" | sed -nE 's/^sesja_[0-9]+_([0-9]{8})-.*/\1/p')"
if [ -z "$DATE" ]; then
    FILE1="$(ls "$DIR/${CAMERA}"_*_[0-9][0-9][0-9][0-9][0-9].h264 | head -n 1)"
    DATE="$(date -u -r "$FILE1" +%Y%m%d 2>/dev/null || stat -c %y "$FILE1" | cut -d- -f1-3 | tr -d '-' | cut -c1-8)"
fi
TARGET="$OUT/${NAME%%_*}_${DATE}_${NAME#*_}.mp4"

# Camera 0 is mounted rotated by 180 degrees, and rpicam-vid does not keep the
# transform for the whole recording (see record.sh). The rotation is therefore
# applied here, as a rotation matrix in the MP4 header: no re-encoding, the same
# for the whole file, and players and ffmpeg apply it themselves when decoding.
# if, not [ ] && ...: with set -e a false test would end the script for kam1
ROTATE=""
if [ "$CAMERA" = "kam0" ]; then
    ROTATE="-metadata:s:v:0 rotate=180"
fi

cat "$DIR/${CAMERA}"_*_[0-9][0-9][0-9][0-9][0-9].h264 | ffmpeg -loglevel error -r 30 -f h264 -i - \
    -c copy -movflags +faststart $ROTATE -y "$TARGET"

echo "$TARGET  $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TARGET") s"
