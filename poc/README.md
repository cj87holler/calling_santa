# Call Santa — Laptop POC

A zero-dependency proof of concept for the [Call Santa](../call-santa-pre-prd.md) installation.
No hardware, no booth, no Raspberry Pi — just your laptop's mic and speakers talking to
Santa (an OpenAI Realtime voice agent) in the browser.

**Goal:** prove the magic — a real-time, low-latency voice conversation with a believable Santa.

## What's here

| File | Role |
|---|---|
| `server.py` | Tiny local server (Python stdlib only). Holds your OpenAI key, mints short-lived session tokens, serves the page. Your secret key never reaches the browser. |
| `index.html` | The "handset" UI. Click **Pick up**, talk out loud, hear Santa reply. Live transcript + LED states + 5-minute auto-wrap. |

## Requirements

- macOS with Python 3 (already installed — `python3 --version`)
- An **OpenAI API key** with Realtime API access
- A modern browser (Chrome/Safari/Edge). Mic works on `localhost` without HTTPS.

## Run it

```bash
cd poc
export OPENAI_API_KEY=sk-...        # your OpenAI key
python3 server.py
```

Then open **http://localhost:8000**, click **📞 Pick up the handset**, allow mic access, and say hello.

## Tuning (optional env vars)

```bash
export SANTA_VOICE=cedar            # ash (default), cedar, ballad, marin, verse, coral…
export SANTA_MODEL=gpt-realtime-2   # gpt-realtime (default, stable) or gpt-realtime-2 (newest)
export PORT=8000
```

Santa's whole personality + guardrails live in `SANTA_INSTRUCTIONS` near the top of `server.py` —
edit that string to change his behavior.

## What this POC proves (and what it skips)

✅ Proves: voice-in → Santa → voice-out, latency feel, persona quality, the vulgarity guardrail,
the 5-minute cap, name usage, transcript display.

⏭️ Skips (all the hardware/ops wrappers): phone booth, GPIO hook switch, scheduling/admin UI,
PIN override, Grafana/Prometheus, weatherproofing, OFF-state recording.

## Things to try while testing

- Give a name and confirm Santa uses it throughout.
- Ask for a gift and gauge whether his reaction feels warm and "real."
- Say something rude — confirm he delivers the goodbye line and disengages.
- Watch the latency: does the reply come back fast enough to feel alive? (PRD target: < 2s p95.)

## Cost note

The Realtime API bills per minute of audio in/out. A few test calls cost cents, but don't leave
it running unattended. Tokens are minted on demand and expire in ~10 minutes.
