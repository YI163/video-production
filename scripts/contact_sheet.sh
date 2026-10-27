#!/usr/bin/env bash
# Quick 1s contact sheet for a video file.
# Usage: ./contact_sheet.sh input.mp4 out.jpg [columns] [width]
set -euo pipefail
IN="${1:?usage: contact_sheet.sh input.mp4 out.jpg [cols] [width]}"
OUT="${2:?usage: contact_sheet.sh input.mp4 out.jpg [cols] [width]}"
COLS="${3:-5}"
WIDTH="${4:-320}"
FF="${FFMPEG:-$(command -v ffmpeg || true)}"
if [ -z "$FF" ]; then
  for c in tools/ffmpeg ../../../../tools/ffmpeg ../../../tools/ffmpeg ../../tools/ffmpeg /opt/homebrew/bin/ffmpeg /usr/local/bin/ffmpeg; do
    if [ -x "$c" ]; then FF="$c"; break; fi
  done
fi
FF="${FF:-ffmpeg}"
"$FF" -hide_banner -loglevel error -i "$IN" \
  -vf "fps=1,scale=${WIDTH}:-1,tile=${COLS}x6:padding=4:margin=4" \
  -frames:v 1 "$OUT" -y
echo "wrote $OUT"
