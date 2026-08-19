# Call Santa

Call Santa is an outdoor phone box for a front yard. A neighborhood child walks up, lifts a real
handset, and has a live spoken conversation with an AI Santa powered by the OpenAI Realtime API —
no screen, no app, no adult standing by to set it up. The installation runs unattended on a
schedule the owner controls, and it has to be live by the first week of December 2026.

## Repository layout

| Path | Role |
|---|---|
| `poc/` | **The single authoritative implementation path.** A working laptop proof of concept: a Python-stdlib token-broker server and a browser handset UI that together prove the real-time voice conversation. All production work builds forward from here. |
| `.planning/` | The roadmap, requirements, phase context, phase plans, and execution state. `.planning/ROADMAP.md` is the phase-by-phase plan; `.planning/REQUIREMENTS.md` is the requirement register. |
| `call-santa-pre-prd.md` | The source concept document the project was ingested from. Concept-stage; superseded by `.planning/` wherever the two disagree. |

If you are looking for the code that runs Santa, it is in `poc/`. There is no second candidate.

## Removed code

A pre-POC Vite and TypeScript scaffold under `voice/` was removed in Phase 1: it was referenced by
no code and no document in the repository, it predated the working POC, and its entry module inlined
a standing OpenAI key into a browser bundle through a `VITE_`-prefixed environment variable — the
exact client-side-credential pattern requirement OPS-02 forbids. It was deleted rather than
documented and kept, because keeping an unreferenced duplicate implementation is precisely what the
"exactly one authoritative implementation path" requirement (OPS-01) exists to prevent.

One fact from that scaffold is worth preserving: the `@openai/agents` package exposes `RealtimeAgent`
and `RealtimeSession` abstractions over the Realtime API, which are relevant if the Phase 2 headless
transport decision favours Node/TypeScript over Python.

## Running the POC

See [`poc/README.md`](poc/README.md) for requirements, the run command, and the optional tuning
environment variables. It is the authoritative instructions for the POC and is not restated here.

The POC reads its OpenAI credential from the `OPENAI_API_KEY` environment variable. No key value is
ever committed to this repository: `.env`, `.env.*` and `*.key` are gitignored, and the key is read
from the environment at runtime and never sent to the browser.
