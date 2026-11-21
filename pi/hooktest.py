#!/usr/bin/env python3
"""Hook switch test: watch the cradle switch on GPIO17 and print every lift and hang-up.

Wiring (D-32), with the Pi switched OFF while you connect it:
  switch COM -> Pi pin 9  (GND)
  switch NC  -> Pi pin 11 (GPIO17)
  switch NO  -> nothing
No 3.3V wire. The Pi's internal pull-up holds GPIO17 high.

How it reads:
  handset ON the cradle  -> lever pressed  -> NC contact open   -> pin HIGH -> "hung up"
  handset LIFTED         -> lever released -> NC contact closed -> pin LOW  -> "picked up"
  a loose or broken wire -> pin stays HIGH -> reads "hung up" (fail-safe: no runaway calls)

Usage: python3 hooktest.py      (Ctrl+C to stop)
Needs no API key and makes no calls.
"""

import time
from datetime import datetime
from signal import pause

try:
    from gpiozero import Button
except ImportError:
    print("gpiozero is missing. Install it with:  sudo apt install -y python3-gpiozero")
    raise SystemExit(1)

PIN = 17
BOUNCE_SECONDS = 0.05  # ignore contact chatter shorter than 50 ms

# pull_up=True: the pin reads HIGH until the closed NC contact connects it to GND.
# gpiozero calls a LOW pin "pressed", which here means the handset is OFF the cradle.
switch = Button(PIN, pull_up=True, bounce_time=BOUNCE_SECONDS)

lifts = 0
lifted_at = None


def stamp():
    return datetime.now().strftime("%H:%M:%S")


def picked_up():
    global lifts, lifted_at
    lifts += 1
    lifted_at = time.monotonic()
    print(f"{stamp()}  PICKED UP   (lift #{lifts})  -> a call would start here", flush=True)


def hung_up():
    held = ""
    if lifted_at is not None:
        held = f"  (off the hook {time.monotonic() - lifted_at:.1f}s)"
    print(f"{stamp()}  HUNG UP{held}  -> a call would end here", flush=True)


switch.when_pressed = picked_up
switch.when_released = hung_up

state = "PICKED UP (off the hook)" if switch.is_pressed else "HUNG UP (on the cradle)"
print(f"Watching GPIO{PIN} (pin 11). Right now the phone reads: {state}")
print("Lift and replace the handset a few times. Ctrl+C to stop.\n", flush=True)

try:
    pause()
except KeyboardInterrupt:
    print(f"\nDone. Counted {lifts} lift(s).")
