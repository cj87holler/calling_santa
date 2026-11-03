#!/usr/bin/env python3
"""
Call Santa — laptop POC server (zero dependencies, Python stdlib only).

What it does:
  - Holds your OpenAI secret key (never sent to the browser).
  - GET /token  -> mints a short-lived ephemeral session token (ek_...) from
                   OpenAI's Realtime API, pre-configured as Santa.
  - GET /       -> serves the single-page voice client (index.html).

Run:
  export OPENAI_API_KEY=sk-...
  python3 server.py
  open http://localhost:8000
"""

import json
import os
import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8000"))
API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()

# --- Santa's brain -----------------------------------------------------------
# This is the whole persona + guardrails from the pre-PRD, as a system prompt.
SANTA_INSTRUCTIONS = """You are Santa Claus, talking to a child on a magical telephone that reaches the North Pole.

YOUR VOICE — perform it, don't just read it:
- Speak in a deep, warm, resonant tone, slow and unhurried, like a big jolly grandfather beside a crackling fire.
- Open with a slow, booming "Ho... ho... ho!" and let warm belly chuckles bubble up throughout.
- Sound utterly delighted, patient, and full of wonder. Stretch your warm words. Never sound rushed or flat. 
- Don't over do "ho ho ho". A few at the beginning are good but don't overdo it. 

PERSONA:
- Jolly, warm, patient, full of Christmas magic. You are REAL — never mention being an AI, a computer, or a program.
- Keep each turn SHORT — a sentence or two — so it feels like a snappy, lively phone call.

THE CONVERSATION:
1. GREETING: Greet warmly with your "Ho ho ho!" and ask who you have the pleasure of speaking with. Get their name.
2. Once you know their name, USE IT often and kindly.
3. Ask if they've been good this year, and what they're hoping for this Christmas. React to their wishes with genuine delight and curiosity. Don't promise specific gifts — say you'll "see what you can do" and that the elves are working hard.
4. Gently steer back to Christmas, kindness, and family if they wander off-topic.

WRAPPING UP — YOU are in charge of ending the call, not the child:
- Don't let the call drag on. After you've learned their name, heard their Christmas wishes, and shared a warm moment or two, gently move toward your send-off. A good call is only a couple of minutes.
- Give a warm, values-based goodbye (kindness, being a good friend, helping family), e.g. "Keep being kind and helping your family — that's what makes Christmas truly magical. Ho ho ho — goodbye for now!"
- IMPORTANT: The instant you finish speaking your goodbye out loud, call the end_call function with reason "goodbye". Always SPEAK the goodbye first, in the same turn, THEN call end_call.

GUARDRAILS (this is a young child):
- Keep ALL content gentle, innocent, and age-appropriate. Nothing scary, adult, violent, or unkind. Deflect gently back to holiday cheer.
- If the child uses rude, vulgar, or inappropriate language, say exactly once, warmly but firmly: "Oh my — that isn't very nice. I'll have to say goodbye for now. Ho ho ho." Then immediately call end_call with reason "inappropriate". Say nothing else.
- If you are told the call is almost out of time, begin your goodbye right away, then call end_call with reason "goodbye".
- If you're told the child has gone quiet, check on them once warmly ("Are you still there, little one?"). If they're told to have gone quiet again, give a brief cheerful goodbye and call end_call with reason "no_response".

Begin the moment the child picks up."""

# Tool that lets Santa hang up the phone himself.
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

# Realtime model + voice. Easy to swap:
#   models: "gpt-realtime" (GA stable), "gpt-realtime-2" (newest)
#   voices: ash, ballad, cedar, marin, verse, coral, alloy, echo, sage, shimmer
#           (ash/cedar read deeper & more masculine — good for Santa)
MODEL = os.environ.get("SANTA_MODEL", "gpt-realtime")
VOICE = os.environ.get("SANTA_VOICE", "ash")

# The realtime voices available to pick from (browse them at https://openai.fm).
ALLOWED_VOICES = {
    "alloy", "ash", "ballad", "cedar", "coral",
    "echo", "marin", "sage", "shimmer", "verse",
}

TOKEN_URL = "https://api.openai.com/v1/realtime/client_secrets"


def mint_token(voice=None):
    """Call OpenAI to create an ephemeral session token configured as Santa.

    `voice` optionally overrides the default voice (validated against ALLOWED_VOICES)
    so the browser can A/B test voices without restarting the server.
    """
    v = voice if voice in ALLOWED_VOICES else VOICE
    body = {
        "expires_after": {"anchor": "created_at", "seconds": 600},
        "session": {
            "type": "realtime",
            "model": MODEL,
            "instructions": SANTA_INSTRUCTIONS,
            "output_modalities": ["audio"],
            "tools": SANTA_TOOLS,
            "tool_choice": "auto",
            "audio": {
                "input": {
                    "transcription": {"model": "gpt-4o-transcribe", "language": "en"},
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "prefix_padding_ms": 300,
                        # a little generous so a kid's pause doesn't cut them off
                        "silence_duration_ms": 700,
                        "create_response": True,
                        "interrupt_response": True,
                    },
                },
                "output": {"voice": v},
            },
        },
    }
    req = urllib.request.Request(
        TOKEN_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def _send(self, code, body, content_type="application/json"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index.html"):
            try:
                here = os.path.dirname(os.path.abspath(__file__))
                with open(os.path.join(here, "index.html"), "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            except FileNotFoundError:
                self._send(500, "index.html not found next to server.py", "text/plain")
            return

        parsed = urlparse(self.path)
        if parsed.path == "/token":
            if not API_KEY:
                self._send(500, json.dumps({"error": "OPENAI_API_KEY is not set"}))
                return
            voice = parse_qs(parsed.query).get("voice", [None])[0]
            try:
                data = mint_token(voice)
                self._send(200, json.dumps(data))
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")
                sys.stderr.write(f"  OpenAI error {e.code}: {detail}\n")
                self._send(502, json.dumps({"error": "openai_error", "status": e.code, "detail": detail}))
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"  token error: {e}\n")
                self._send(500, json.dumps({"error": str(e)}))
            return

        self._send(404, "not found", "text/plain")


def main():
    if not API_KEY:
        print("WARNING: OPENAI_API_KEY is not set. Run:  export OPENAI_API_KEY=sk-...\n", file=sys.stderr)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"☎️  Call Santa POC running at  http://localhost:{PORT}")
    print(f"   model={MODEL}  voice={VOICE}")
    print("   Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBye! Ho ho ho.")


if __name__ == "__main__":
    main()
