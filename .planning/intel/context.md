# Context (DOC-derived)

Lowest precedence tier (ADR > SPEC > PRD > DOC). Nothing here overrides a PRD requirement.

---

## Topic: Laptop POC — purpose and status

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

> A zero-dependency proof of concept for the [Call Santa](../call-santa-pre-prd.md) installation.
> No hardware, no booth, no Raspberry Pi — just your laptop's mic and speakers talking to
> Santa (an OpenAI Realtime voice agent) in the browser.
>
> **Goal:** prove the magic — a real-time, low-latency voice conversation with a believable Santa.

Timeline note: the pre-PRD is dated 2026-03-30 (rev 2); this POC was built afterward. It is the
only working code covered by the ingest set.

## Topic: POC file roles

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

> | `server.py` | Tiny local server (Python stdlib only). Holds your OpenAI key, mints short-lived session tokens, serves the page. Your secret key never reaches the browser. |
> | `index.html` | The "handset" UI. Click **Pick up**, talk out loud, hear Santa reply. Live transcript + LED states + 5-minute auto-wrap. |

## Topic: POC requirements and run procedure

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

> - macOS with Python 3 (already installed — `python3 --version`)
> - An **OpenAI API key** with Realtime API access
> - A modern browser (Chrome/Safari/Edge). Mic works on `localhost` without HTTPS.

```bash
cd poc
export OPENAI_API_KEY=sk-...        # your OpenAI key
python3 server.py
```

> Then open **http://localhost:8000**, click **📞 Pick up the handset**, allow mic access, and say hello.

## Topic: POC tuning knobs

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

```bash
export SANTA_VOICE=cedar            # ash (default), cedar, ballad, marin, verse, coral…
export SANTA_MODEL=gpt-realtime-2   # gpt-realtime (default, stable) or gpt-realtime-2 (newest)
export PORT=8000
```

> Santa's whole personality + guardrails live in `SANTA_INSTRUCTIONS` near the top of `server.py` —
> edit that string to change his behavior.

## Topic: What the POC proves and what it skips

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

> ✅ Proves: voice-in → Santa → voice-out, latency feel, persona quality, the vulgarity guardrail,
> the 5-minute cap, name usage, transcript display.
>
> ⏭️ Skips (all the hardware/ops wrappers): phone booth, GPIO hook switch, scheduling/admin UI,
> PIN override, Grafana/Prometheus, weatherproofing, OFF-state recording.

The skip list is a deliberate, author-declared scope boundary — not a contradiction of the PRD's
architecture. Everything skipped remains an open build item.

## Topic: POC manual test checklist

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

> - Give a name and confirm Santa uses it throughout.
> - Ask for a gift and gauge whether his reaction feels warm and "real."
> - Say something rude — confirm he delivers the goodbye line and disengages.
> - Watch the latency: does the reply come back fast enough to feel alive? (PRD target: < 2s p95.)

Note: the `< 2s p95` figure is quoted here as a testing cue. The authoritative statement lives in
the pre-PRD, Section 10.

## Topic: POC cost note

source: /Users/cj.holler/Desktop/calling_santa/poc/README.md

> The Realtime API bills per minute of audio in/out. A few test calls cost cents, but don't leave
> it running unattended. Tokens are minted on demand and expire in ~10 minutes.

## Topic: Transcript handling in the POC

source: /Users/cj.holler/Desktop/calling_santa/poc/index.html (read for provenance)

The POC renders a live transcript of both sides on screen using Realtime data-channel events, and
enables input transcription via `gpt-4o-transcribe`. Nothing is written to disk. This is display-only
and does not conflict with the PRD's no-storage privacy rule — but any production port must not
persist or log these strings. See constraints.md CON-privacy-and-retention.

---

## Repo observations (not from an ingested document)

Recorded for downstream awareness; flagged in INGEST-CONFLICTS.md as an ingest coverage gap.

- `/Users/cj.holler/Desktop/calling_santa/voice/my-project/` — a tracked Node/TypeScript scaffold
  (27 files in git, includes `@openai` packages in node_modules and a nested duplicate
  `my-project/my-project/` directory). No document in the ingest set describes it, and neither
  the pre-PRD nor the POC README references it. Its relationship to the POC is unknown.
- `.env` is correctly covered by `.gitignore` (`.env`, `.env.*`, `*.key`) — no committed secrets observed.
- Working tree clean at ingest time; HEAD is `a0d272a Add laptop POC: real-time voice "Call Santa" over OpenAI Realtime API`.
