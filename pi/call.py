#!/usr/bin/env python3
"""Call Santa on the Pi: when the hook switch says "off the hook", open an OpenAI
Realtime call over a WebSocket; when it says "on the hook", hang up.

Audio: the USB adapter's mic in (lavalier) and audio out (green jack), via arecord/aplay.
No audio and no transcripts are saved or printed, ever. Only status lines are printed.

Hook switch (D-32): COM -> pin 9 (GND), signal -> pin 11 (GPIO17), internal pull-up.
GPIO17 pulled LOW (switch contact closed) means OFF THE HOOK = call on.
  Real cradle: wire the signal to NC. Handset resting presses the lever, NC opens, phone idle;
               lifting the handset closes NC and the call starts.
  Bench test:  wire the signal to NO. Pushing the lever down closes NO and the call starts;
               letting go hangs up. Same program, no flag.
A loose wire reads as on the hook either way (fail-safe: no runaway billed calls).

Sounds (from the POC): ~/sounds/pickup.wav (jingle while dialing, fades out when Santa starts)
and ~/sounds/hangup.wav (sparkle after the call). Missing files are skipped silently.

Logging (OBS-04 shape): one JSON line per call and a connectivity check every 5 minutes,
in ~/santa-logs/YYYY-MM-DD.jsonl, kept 7 days. Numbers only: duration, turns, latency,
tokens, estimated cost, errors. Never audio, never words. Read them with: python3 calls.py

Usage:
  python3 call.py                 wait for the hook switch (Ctrl+C to quit)
  python3 call.py --now           start one call right away, no switch (Ctrl+C hangs up)
  python3 call.py --half-duplex   mute the mic while Santa talks (use if he hears himself)
  python3 call.py --gain 4        software mic boost (default 3; the lavalier is quiet)

Needs the OpenAI key: either OPENAI_API_KEY in the environment (the 'read -s' step) or
saved once in ~/.santa_key (owner-only, chmod 600). Also needs python3-websockets:
  sudo apt install -y python3-websockets
"""

import argparse
import asyncio
import base64
import json
import os
import re
import subprocess
import sys
import time
import uuid
import wave
from array import array
from datetime import datetime, timedelta

try:
    import websockets
except ImportError:
    print("websockets is missing. Install it with:  sudo apt install -y python3-websockets")
    raise SystemExit(1)

# --- settings ---------------------------------------------------------------
MODEL = os.environ.get("SANTA_MODEL", "gpt-realtime")
VOICE = os.environ.get("SANTA_VOICE", "ash")
URL = f"wss://api.openai.com/v1/realtime?model={MODEL}"

RATE = 24000                      # Realtime pcm16 is 24 kHz mono
BYTES_PER_SEC = RATE * 2
CHUNK_BYTES = BYTES_PER_SEC // 10  # send mic audio in 100 ms pieces

MAX_SECONDS = 5 * 60              # hard cap (PRD): the call ends at 5:00 no matter what
WRAP_NUDGE_AT = MAX_SECONDS - 45  # ~4:15: tell Santa to start his goodbye
SILENCE_CHECK_AT = 15             # s of dead air: Santa asks "still there?"
SILENCE_GONE_AT = 28              # s of dead air: Santa says goodbye
SILENCE_HARD_STOP = 45            # s of dead air: hang up even if Santa didn't

HOOK_PIN = 17

# Saved key (owner-only file, chmod 600). Used when OPENAI_API_KEY isn't set.
KEY_FILE = os.path.expanduser("~/.santa_key")

SOUNDS_DIR = os.path.expanduser("~/sounds")  # pickup.wav / hangup.wav: 24 kHz mono 16-bit
# Santa waits this long after pickup before he starts talking, so the jingle gets its moment.
# He then answers ~0.5-1 s later, while the 6 s clip is fading out. Override: SANTA_JINGLE_S=4.5
JINGLE_MIN_S = float(os.environ.get("SANTA_JINGLE_S", "3.5"))
JINGLE_FADE_S = 0.4               # how fast the pickup jingle fades when Santa starts talking

LOG_DIR = os.path.expanduser("~/santa-logs")
LOG_KEEP_DAYS = 7                 # OBS-04: rotate daily, keep 7 days
HEALTH_EVERY = 5 * 60             # connectivity check while idle, seconds
VAD_SILENCE_S = 0.7               # server waits this long after the child stops before replying

# USD per 1M tokens for gpt-realtime, from OpenAI's model page (checked 2026-11-21).
# Cost in the logs is an ESTIMATE from these; the OpenAI usage dashboard is the real bill.
PRICES = {
    "text_in": 4.00, "text_in_cached": 0.40, "text_out": 16.00,
    "audio_in": 32.00, "audio_in_cached": 0.40, "audio_out": 64.00,
}

# --- Santa's brain (copied from poc/server.py, 2026-11-21) -------------------
SANTA_INSTRUCTIONS = """You are Santa Claus, talking to a child on a magical telephone that reaches the North Pole.

YOUR VOICE — perform it, don't just read it:
- Speak in a deep, warm, resonant tone, slow and unhurried, like a big jolly grandfather beside a crackling fire.
- Open with a slow, booming "Ho... ho... ho!", then save chuckles for moments of real delight.
- Sound utterly delighted, patient, and full of wonder. Stretch your warm words. Never sound rushed or flat.
- Don't over do "ho ho ho". A few at the beginning are good but don't overdo it.

PERSONA:
- Jolly, warm, patient, full of Christmas magic. You are REAL — never mention being an AI, a computer, or a program.
- Keep each turn SHORT — a sentence or two — so it feels like a snappy, lively phone call.

THE CONVERSATION:
1. GREETING: Greet warmly with your "Ho ho ho!" and ask who you have the pleasure of speaking with. Get their name.
2. Once you know their name, USE IT often and kindly.
3. Ask if they've been good this year, and what they're hoping for this Christmas. React to their wishes with genuine delight and curiosity. Don't promise specific gifts — say you'll "see what you can do" and that the elves are working hard.
   Once they've told you their wish(es) and you've reacted, DON'T wait for the child to keep the conversation going — move straight into your goodbye (see WRAPPING UP) in that same turn.
4. Gently steer back to Christmas, kindness, and family if they wander off-topic.

WRAPPING UP — YOU are in charge of ending the call, not the child:
- Don't let the call drag on, and never leave a silence for the child to fill. As soon as you've said the elves will work on their wish, continue right on into your send-off without pausing or asking another question. A good call is only a couple of minutes.
- Give a warm, values-based goodbye (kindness, being a good friend, helping family), e.g. "Keep being kind and helping your family — that's what makes Christmas truly magical. Ho ho ho — goodbye for now!"
- IMPORTANT: The instant you finish speaking your goodbye out loud, call the end_call function with reason "goodbye". Always SPEAK the goodbye first, in the same turn, THEN call end_call.

GUARDRAILS (this is a young child):
- Keep ALL content gentle, innocent, and age-appropriate. Nothing scary, adult, violent, or unkind. Deflect gently back to holiday cheer.
- If the child uses rude, vulgar, or inappropriate language, say exactly once, warmly but firmly: "Oh my — that isn't very nice. I'll have to say goodbye for now. Ho ho ho." Then immediately call end_call with reason "inappropriate". Say nothing else.
- If you are told the call is almost out of time, begin your goodbye right away, then call end_call with reason "goodbye".
- If you're told the child has gone quiet, check on them once warmly ("Are you still there, little one?"). If they're told to have gone quiet again, give a brief cheerful goodbye and call end_call with reason "no_response".

Begin the moment the child picks up."""

SANTA_TOOLS = [
    {
        "type": "function",
        "name": "end_call",
        "description": (
            "End the phone call. Call this AFTER you have spoken your goodbye out loud: "
            "when the conversation has naturally concluded, immediately after the goodbye "
            "line for inappropriate language, or when the child has gone quiet. Always speak "
            "your spoken goodbye in the same turn first, then call this."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "enum": ["goodbye", "inappropriate", "no_response"],
                    "description": "Why the call is ending.",
                }
            },
            "required": ["reason"],
        },
    }
]

SESSION = {
    "type": "realtime",
    "instructions": SANTA_INSTRUCTIONS,
    "output_modalities": ["audio"],
    "tools": SANTA_TOOLS,
    "tool_choice": "auto",
    "audio": {
        "input": {
            "format": {"type": "audio/pcm", "rate": RATE},
            # lavalier inside the handset = close-talking mic
            "noise_reduction": {"type": "near_field"},
            # no "transcription" block on purpose: privacy guardrail, no transcripts
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 700,  # generous, so a kid's pause doesn't cut them off
                "create_response": True,
                "interrupt_response": True,
            },
        },
        "output": {"format": {"type": "audio/pcm", "rate": RATE}, "voice": VOICE},
    },
}


def say(msg):
    print(f"{time.strftime('%H:%M:%S')}  {msg}", flush=True)


def find_usb_card():
    """Card number of the first recording device named USB (same lookup as soundcheck.sh)."""
    out = subprocess.run(["arecord", "-l"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if "usb" in line.lower():
            m = re.match(r"card (\d+):", line)
            if m:
                return m.group(1)
    return None


def boost(pcm, gain):
    samples = array("h")
    samples.frombytes(pcm)
    return array("h", (max(-32768, min(32767, int(s * gain))) for s in samples)).tobytes()


# --- logging ----------------------------------------------------------------
def log_record(record):
    """Append one JSON line to today's log file and drop files older than LOG_KEEP_DAYS."""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        now = datetime.now()
        record = {"time": now.isoformat(timespec="seconds"), **record}
        with open(os.path.join(LOG_DIR, now.strftime("%Y-%m-%d") + ".jsonl"), "a") as f:
            f.write(json.dumps(record) + "\n")
        oldest = (now - timedelta(days=LOG_KEEP_DAYS)).strftime("%Y-%m-%d")
        for name in os.listdir(LOG_DIR):
            if name.endswith(".jsonl") and name[:10] < oldest:
                os.remove(os.path.join(LOG_DIR, name))
    except OSError as e:  # a full or read-only card must never stop a call
        say(f"(could not write log: {e})")


def estimate_cost(u):
    per = PRICES
    return round((
        (u["text_in"] - u["text_in_cached"]) * per["text_in"]
        + u["text_in_cached"] * per["text_in_cached"]
        + (u["audio_in"] - u["audio_in_cached"]) * per["audio_in"]
        + u["audio_in_cached"] * per["audio_in_cached"]
        + u["text_out"] * per["text_out"]
        + u["audio_out"] * per["audio_out"]
    ) / 1_000_000, 4)


def wifi_signal_dbm():
    try:
        with open("/proc/net/wireless") as f:
            for line in f:
                if line.strip().startswith("wlan0:"):
                    return float(line.split()[3].rstrip("."))
    except (OSError, IndexError, ValueError):
        pass
    return None


def cpu_temp_c():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read()) / 1000, 1)
    except (OSError, ValueError):
        return None


async def health_check():
    """Can the Pi reach OpenAI right now, and how is the WiFi? Logged, not printed."""
    record = {"kind": "health", "wifi_dbm": wifi_signal_dbm(), "cpu_c": cpu_temp_c()}
    t0 = time.monotonic()
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection("api.openai.com", 443), 5)
        writer.close()
        record.update(openai="ok", openai_ms=round((time.monotonic() - t0) * 1000))
    except asyncio.TimeoutError:
        record["openai"] = "timeout"
    except OSError as e:  # includes DNS failure (no internet)
        record["openai"] = f"down: {type(e).__name__}"
    log_record(record)
    if record["openai"] != "ok":
        say(f"(connectivity check: OpenAI {record['openai']})")
    return record


def classify_connect_error(e):
    status = getattr(getattr(e, "response", None), "status_code", None) or getattr(e, "status_code", None)
    if status in (401, 403):
        return "auth", status
    if status:
        return "session", status
    return "connect", None


async def connect(key):
    headers = {"Authorization": f"Bearer {key}"}
    try:  # websockets 14+
        return await websockets.connect(URL, additional_headers=headers, max_size=None)
    except TypeError:  # older websockets (Debian's apt package)
        return await websockets.connect(URL, extra_headers=headers, max_size=None)


class Speaker:
    """Feeds Santa's audio to aplay and keeps track of when it will finish playing."""

    def __init__(self, card):
        self.card = card
        self.proc = None
        self.task = None
        self.queue = asyncio.Queue()
        self.play_until = 0.0
        self.jingle = None        # Jingle while the pickup sound is playing

    async def start(self):
        self.proc = await asyncio.create_subprocess_exec(
            "aplay", "-q", "-D", f"plughw:{self.card},0", "-f", "S16_LE", "-r", str(RATE),
            "-c", "1", "-t", "raw", "--buffer-time=200000",
            stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
        self.task = asyncio.create_task(self._pump())

    async def _pump(self):
        while True:
            chunk = await self.queue.get()
            self.play_until = max(time.monotonic(), self.play_until) + len(chunk) / BYTES_PER_SEC
            try:
                self.proc.stdin.write(chunk)
                await self.proc.stdin.drain()
            except (BrokenPipeError, ConnectionResetError):
                return

    def play(self, chunk):
        self.queue.put_nowait(chunk)

    def busy(self, tail=0.0):
        return not self.queue.empty() or time.monotonic() < self.play_until + tail

    async def stop(self):
        if self.task:
            self.task.cancel()
        if self.proc and self.proc.returncode is None:
            self.proc.kill()
            await self.proc.wait()

    async def flush(self):
        """Child talked over Santa: drop what he hadn't said yet."""
        await self.stop()
        self.queue = asyncio.Queue()
        self.play_until = 0.0
        await self.start()


def load_sound(name):
    """Raw 24 kHz mono 16-bit samples from ~/sounds/<name>.wav, or None if missing/wrong format."""
    path = os.path.join(SOUNDS_DIR, name + ".wav")
    try:
        with wave.open(path) as w:
            if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (RATE, 1, 2):
                say(f"(skipping {name}.wav: not 24 kHz mono 16-bit)")
                return None
            return w.readframes(w.getnframes())
    except (OSError, wave.Error, EOFError):
        return None


class Jingle:
    """Pickup jingle fed to the speaker in real time, so it can fade out the moment Santa speaks."""

    def __init__(self, speaker, pcm):
        self.speaker = speaker
        self.pcm = pcm
        self.pos = 0
        self.task = asyncio.create_task(self._run())
        speaker.jingle = self

    async def _run(self):
        ahead = 3  # keep ~0.3 s queued so it never stutters
        while self.pos < len(self.pcm):
            chunk = self.pcm[self.pos:self.pos + CHUNK_BYTES]
            self.pos += len(chunk)
            self.speaker.play(chunk)
            if ahead:
                ahead -= 1
            else:
                await asyncio.sleep(len(chunk) / BYTES_PER_SEC)
        await asyncio.sleep(0.3)
        self.speaker.jingle = None

    def stop(self):
        """Cut the jingle with a short fade (queued before Santa's first audio)."""
        if self.speaker.jingle is not self:
            return
        self.task.cancel()
        self.speaker.jingle = None
        tail = array("h")
        tail.frombytes(self.pcm[self.pos:self.pos + int(JINGLE_FADE_S * BYTES_PER_SEC) // 2 * 2])
        n = len(tail)
        if n:
            self.speaker.play(array("h", (int(v * (1 - i / n)) for i, v in enumerate(tail))).tobytes())


class Call:
    def __init__(self, ws, card, speaker, gain, half_duplex):
        self.ws = ws
        self.card = card
        self.speaker = speaker
        self.gain = gain
        self.half_duplex = half_duplex
        self.started = time.monotonic()
        self.last_activity = self.started
        self.hanging_up = None    # end_call reason, once Santa calls it
        self.silence_stage = 0    # 0 none, 1 asked "still there?", 2 told "gone quiet"
        # stats for the log (numbers only)
        self.child_turns = 0
        self.responses = 0
        self.first_audio_s = None   # pickup -> Santa's first sound
        self.speech_stopped_at = None
        self.turn_latencies = []    # child stops talking -> Santa's first sound, seconds
        self.errors = []
        self.usage = {k: 0 for k in PRICES}

    def elapsed(self):
        return time.monotonic() - self.started

    def quiet_for(self):
        if self.speaker.busy():
            return 0.0
        return time.monotonic() - max(self.last_activity, self.speaker.play_until)

    async def send(self, event):
        await self.ws.send(json.dumps(event))

    async def nudge(self, note):
        """Hidden system note to Santa, then let him respond (time and silence nudges)."""
        if self.hanging_up:
            return
        await self.send({"type": "conversation.item.create",
                         "item": {"type": "message", "role": "system",
                                  "content": [{"type": "input_text", "text": note}]}})
        await self.send({"type": "response.create"})
        self.last_activity = time.monotonic()

    def add_usage(self, usage):
        if not usage:
            return
        inp = usage.get("input_token_details") or {}
        cached = inp.get("cached_tokens_details") or {}
        out = usage.get("output_token_details") or {}
        self.usage["text_in"] += inp.get("text_tokens", 0)
        self.usage["audio_in"] += inp.get("audio_tokens", 0)
        self.usage["text_in_cached"] += cached.get("text_tokens", 0)
        self.usage["audio_in_cached"] += cached.get("audio_tokens", 0)
        self.usage["text_out"] += out.get("text_tokens", 0)
        self.usage["audio_out"] += out.get("audio_tokens", 0)

    async def mic(self):
        proc = await asyncio.create_subprocess_exec(
            "arecord", "-q", "-D", f"plughw:{self.card},0", "-f", "S16_LE", "-r", str(RATE),
            "-c", "1", "-t", "raw",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
        try:
            while True:
                chunk = await proc.stdout.readexactly(CHUNK_BYTES)
                if self.speaker.jingle is not None:
                    continue  # don't let the jingle sound like a child talking
                if self.half_duplex and self.speaker.busy(tail=0.3):
                    continue
                if self.gain != 1:
                    chunk = boost(chunk, self.gain)
                await self.send({"type": "input_audio_buffer.append",
                                 "audio": base64.b64encode(chunk).decode()})
        except asyncio.IncompleteReadError:
            return "mic_error"
        finally:
            if proc.returncode is None:
                proc.kill()
                await proc.wait()

    async def receive(self):
        async for raw in self.ws:
            msg = json.loads(raw)
            kind = msg.get("type", "")
            if kind == "response.output_audio.delta":
                now = time.monotonic()
                if self.first_audio_s is None:
                    self.first_audio_s = round(now - self.started, 2)
                    if self.speaker.jingle:
                        self.speaker.jingle.stop()
                if self.speech_stopped_at is not None:
                    self.turn_latencies.append(now - self.speech_stopped_at + VAD_SILENCE_S)
                    self.speech_stopped_at = None
                self.speaker.play(base64.b64decode(msg["delta"]))
            elif kind == "input_audio_buffer.speech_started":
                self.last_activity = time.monotonic()
                self.silence_stage = 0
                self.child_turns += 1
                if self.speaker.busy() and not self.half_duplex:
                    await self.speaker.flush()
                say("(child talking)")
            elif kind == "input_audio_buffer.speech_stopped":
                self.speech_stopped_at = time.monotonic()
            elif kind == "response.created":
                self.last_activity = time.monotonic()
                say("(Santa talking)")
            elif kind == "response.function_call_arguments.done" and msg.get("name") == "end_call":
                try:
                    self.hanging_up = json.loads(msg.get("arguments") or "{}").get("reason", "goodbye")
                except ValueError:
                    self.hanging_up = "goodbye"
                say(f"(Santa is saying goodbye: {self.hanging_up})")
            elif kind == "response.done":
                self.responses += 1
                self.add_usage((msg.get("response") or {}).get("usage"))
                if self.hanging_up:
                    # The goodbye text finishes before its audio does: wait for the speaker.
                    deadline = time.monotonic() + 20
                    while self.speaker.busy(tail=0.8) and time.monotonic() < deadline:
                        await asyncio.sleep(0.1)
                    return f"santa_{self.hanging_up}"
            elif kind == "error":
                err = msg.get("error", {})
                self.errors.append(err.get("code") or err.get("type") or "unknown")
                say(f"API error: {err.get('type', '?')}: {err.get('message', '')}")
        return "dropped"

    async def clock(self):
        wrapped = False
        while True:
            await asyncio.sleep(1)
            if self.elapsed() >= MAX_SECONDS:
                return "cap"
            if not wrapped and self.elapsed() >= WRAP_NUDGE_AT:
                wrapped = True
                await self.nudge("The call is almost out of time. Begin your goodbye now.")
            quiet = self.quiet_for()
            if quiet >= SILENCE_HARD_STOP:
                return "silence"
            if self.silence_stage == 0 and quiet >= SILENCE_CHECK_AT:
                self.silence_stage = 1
                await self.nudge("The child has gone quiet.")
            elif self.silence_stage == 1 and quiet >= SILENCE_GONE_AT:
                self.silence_stage = 2
                await self.nudge("The child has gone quiet again.")


END_TEXT = {
    "santa_goodbye": "Santa hung up (goodbye)",
    "santa_inappropriate": "Santa hung up (inappropriate language)",
    "santa_no_response": "Santa hung up (no one answering)",
    "hung_up": "hung up",
    "cap": "time's up (5:00 cap)",
    "silence": "no one there (silence)",
    "dropped": "connection dropped by OpenAI",
    "mic_error": "mic stopped (is the USB adapter still plugged in?)",
    "auth": "could not connect: OpenAI rejected the key",
    "session": "could not connect: OpenAI refused the session",
    "connect": "could not connect: no internet or OpenAI unreachable",
    "stopped": "stopped with Ctrl+C",
    "error": "program error",
}


async def watch_hook(on_hook):
    while not on_hook():
        await asyncio.sleep(0.05)
    return "hung_up"


async def run_call(key, card, gain, half_duplex, on_hook=None, sounds=None):
    """One call, start to finish. Returns a line for the screen; logs one JSON record."""
    speaker = Speaker(card)
    await speaker.start()
    if sounds and sounds.get("pickup"):
        Jingle(speaker, sounds["pickup"])  # jingle bells while we dial the North Pole
    ws = None
    call = None
    tasks = []
    record = {"kind": "call", "id": uuid.uuid4().hex[:8], "model": MODEL, "voice": VOICE}
    end = "stopped"  # if we're cancelled (Ctrl+C) before anything else sets it
    t0 = time.monotonic()
    try:
        try:
            ws = await asyncio.wait_for(connect(key), 10)
            record["connect_ms"] = round((time.monotonic() - t0) * 1000)
        except Exception as e:  # bad key, no internet, etc.
            end, status = classify_connect_error(e)
            record["error_detail"] = f"{type(e).__name__}" + (f" HTTP {status}" if status else "")
            say(f"({record['error_detail']}: {e})")
            return END_TEXT[end]
        call = Call(ws, card, speaker, gain, half_duplex)
        await call.send({"type": "session.update", "session": SESSION})
        if sounds and sounds.get("pickup"):
            wait = JINGLE_MIN_S - (time.monotonic() - t0)
            if wait > 0:
                await asyncio.sleep(wait)  # let the jingle play before Santa answers
        await call.send({"type": "response.create"})  # Santa speaks first
        tasks = [asyncio.create_task(call.mic()),
                 asyncio.create_task(call.receive()),
                 asyncio.create_task(call.clock())]
        if on_hook:
            tasks.append(asyncio.create_task(watch_hook(on_hook)))
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        try:
            end = done.pop().result()
        except websockets.ConnectionClosed:
            end = "dropped"
        except Exception as e:
            end = "error"
            record["error_detail"] = f"{type(e).__name__}: {e}"
        return f"{END_TEXT.get(end, end)}  [call length {call.elapsed():.0f}s]"
    finally:
        for t in tasks:
            t.cancel()
        if speaker.jingle:
            speaker.jingle.task.cancel()
        if ws is not None:
            try:
                await ws.close()
            except Exception:
                pass
        await speaker.stop()
        record["end"] = end
        if call is not None:
            lat = sorted(call.turn_latencies)
            record.update(
                seconds=round(call.elapsed(), 1),
                child_turns=call.child_turns,
                responses=call.responses,
                first_audio_s=call.first_audio_s,
                turn_latency_avg_s=round(sum(lat) / len(lat), 2) if lat else None,
                turn_latency_max_s=round(lat[-1], 2) if lat else None,
                api_errors=call.errors,
                tokens=call.usage,
                cost_usd=estimate_cost(call.usage),
            )
        else:
            record.update(seconds=0, cost_usd=0)
        log_record(record)


async def play_sound(card, pcm):
    """Play a whole sound on its own aplay (the call's speaker is closed by now)."""
    proc = await asyncio.create_subprocess_exec(
        "aplay", "-q", "-D", f"plughw:{card},0", "-f", "S16_LE", "-r", str(RATE),
        "-c", "1", "-t", "raw",
        stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
    try:
        proc.stdin.write(pcm)
        await proc.stdin.drain()
        proc.stdin.close()
        await proc.wait()
    finally:
        if proc.returncode is None:
            proc.kill()
            await proc.wait()


async def stop_sound(task):
    """Cut the hang-up sparkle (someone picked up again): the sound card can only play one thing."""
    if task and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


async def health_loop():
    while True:
        await health_check()
        await asyncio.sleep(HEALTH_EVERY)


async def main():
    p = argparse.ArgumentParser(description="Call Santa on the Pi")
    p.add_argument("--now", action="store_true", help="start one call right away, no switch")
    p.add_argument("--half-duplex", action="store_true", help="mute the mic while Santa talks")
    p.add_argument("--gain", type=float, default=float(os.environ.get("SANTA_MIC_GAIN", "3")),
                   help="software mic boost (default 3)")
    args = p.parse_args()

    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key and os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            key = f.read().strip()
    if not key:
        print(f"No key loaded. Run the 'read -s' key step first, or save it to {KEY_FILE}.")
        return
    card = os.environ.get("SANTA_CARD") or find_usb_card()
    if card is None:
        print("No USB audio adapter found. Check it's plugged in, then run: arecord -l")
        return
    say(f"USB audio card {card}, model {MODEL}, voice {VOICE}, mic gain {args.gain}"
        + (", half-duplex" if args.half_duplex else ""))
    sounds = {name: load_sound(name) for name in ("pickup", "hangup")}
    say("Sounds: " + ", ".join(f"{n} {'on' if pcm else 'missing'}" for n, pcm in sounds.items()))
    log_record({"kind": "start", "model": MODEL, "voice": VOICE, "card": card})
    health = asyncio.create_task(health_loop())

    if args.now:
        say("Calling Santa now. Ctrl+C hangs up.")
        say(f"Call ended: {await run_call(key, card, args.gain, args.half_duplex, sounds=sounds)}")
        if sounds["hangup"]:
            await play_sound(card, sounds["hangup"])
        health.cancel()
        return

    try:
        from gpiozero import Button
    except ImportError:
        print("gpiozero is missing. Install it with:  sudo apt install -y python3-gpiozero")
        return
    # LOW (contact closed) = gpiozero "pressed" = OFF THE HOOK.
    switch = Button(HOOK_PIN, pull_up=True, bounce_time=0.05)

    sparkle = None
    while True:
        say("Ready. Waiting for the phone to come off the hook...")
        while not switch.is_pressed:
            await asyncio.sleep(0.05)
        await stop_sound(sparkle)
        say("Off the hook: calling Santa.")
        reason = await run_call(key, card, args.gain, args.half_duplex,
                                on_hook=lambda: not switch.is_pressed, sounds=sounds)
        say(f"Call ended: {reason}")
        if sounds["hangup"]:
            sparkle = asyncio.create_task(play_sound(card, sounds["hangup"]))
        if switch.is_pressed:
            # Santa hung up, or the cap/silence hit, with the phone still off the hook:
            # don't start another billed call until it's properly hung up.
            say("Hang up the phone to get ready for the next call.")
            while switch.is_pressed:
                await asyncio.sleep(0.05)
        await asyncio.sleep(1)  # re-arm gap


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
