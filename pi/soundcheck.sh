#!/bin/sh
# Sound check for the USB audio adapter: find it, record 5 seconds from the
# lavalier mic, report how loud it was, and play it back through the speaker.
# Usage: sh soundcheck.sh [seconds]   (default: 5)
# Needs no API key. The recording stays on the Pi and is deleted at the end.

SECS="${1:-5}"
CLIP=/tmp/soundcheck.wav

echo "== Sound cards the Pi can record from =="
arecord -l
echo

# Find the USB adapter's card number (the first recording card named "USB").
CARD=$(arecord -l | grep -i usb | head -n 1 | sed -n 's/^card \([0-9]*\):.*/\1/p')
if [ -z "$CARD" ]; then
  echo "No USB recording device found."
  echo "Check the adapter is plugged in, then run: lsusb"
  exit 1
fi
echo "Using USB adapter: card $CARD"
echo

echo "== Recording $SECS seconds. Talk into the mic NOW (count out loud) =="
arecord -q -D "plughw:$CARD,0" -f S16_LE -r 48000 -c 1 -d "$SECS" "$CLIP" || {
  echo "Recording failed. Paste the error above back to Claude."
  exit 1
}

# How loud was it? Peak level as a percent of maximum.
python3 - "$CLIP" <<'PY'
import sys, wave, array
w = wave.open(sys.argv[1])
s = array.array("h", w.readframes(w.getnframes()))
peak = max((abs(x) for x in s), default=0)
pct = round(100 * peak / 32768)
print(f"Peak mic level: {pct}%")
if pct < 3:
    print("  -> Basically silence. Mic not powered, wrong plug type (TRRS?), or muted.")
elif pct < 15:
    print("  -> Quiet. Works, but we'll want to raise the mic gain.")
elif pct < 95:
    print("  -> Good level.")
else:
    print("  -> Very loud / clipping. We'll lower the mic gain.")
PY
echo

echo "== Playing it back through the speaker =="
aplay -q -D "plughw:$CARD,0" "$CLIP" || echo "Playback failed. Paste the error above back to Claude."
rm -f "$CLIP"
echo "Done."
