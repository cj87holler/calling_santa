# Call Santa

## What This Is

An outdoor, unattended holiday installation for the front yard: a red British-style phone box with a
vintage handset inside. A neighborhood child walks up, lifts the handset, and has a real-time spoken
conversation with an AI Santa. No adult intervention, no parent setup, no screen. It runs on a
schedule the owner controls from their phone, and it must be live by the first week of December 2026.

A working laptop proof of concept of the conversation already exists (`poc/server.py`,
`poc/index.html`). None of the hardware, headless session control, scheduling, admin, or
observability layers are built.

## Core Value

A child picks up the handset and talks to a Santa who feels real — warm, fast, and never says
anything a parent would object to.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- ✓ Real-time voice conversation with a believable Santa persona is achievable at acceptable latency
  — proven by the laptop POC (browser/WebRTC, OpenAI Realtime API). Evidence only; the POC control
  loop does not ship.

### Active

Full detail with IDs in `.planning/REQUIREMENTS.md` (37 v1 requirements across 7 categories).

- [ ] Headless session manager on a Raspberry Pi 5 drives the whole conversation loop — no browser
- [ ] Off-hook GPIO starts a session, on-hook ends it, exactly one session at a time
- [ ] 5-minute cap with a spoken wrap-up, 15s/28s silence ladder, clean reset to IDLE
- [ ] Turn latency under 2s p95
- [ ] Vulgarity terminates the call with the scripted goodbye, via a mechanism that is verified, not assumed
- [ ] Weatherproof booth, sealed electronics, operable 20°F–50°F, outdoor power
- [ ] Local-network admin UI: dashboard, schedule editor, PIN override, session log, system health
- [ ] Prometheus + Grafana observability the owner can read without SSH
- [ ] Zero audio and zero transcripts persisted, anywhere, ever

### Out of Scope

- **Camera / video component** — removed entirely from v1 (no hardware, no mount point, no MJPEG
  stream, no admin video surface, no budget line). PRD Section 9 wins over Sections 5.3 / 6.5 / 11.
- **Physical traffic-awareness (PRD 6.5)** — depends on the camera; falls with it.
- **Multi-language support** — English only; the audience is one neighborhood.
- **Recording or replaying calls** — direct conflict with the children's-privacy rule.
- **Multiple simultaneous callers** — one handset by construction.
- **Internet-facing / remote admin access** — local network only; keeps the attack surface at zero.
- **Peak-concurrent-wait indicator and outdoor queue light** — PRD marks these future.
- **Modular voice stack (Whisper + Claude + ElevenLabs)** — CD-01 resolved in favor of Realtime.

## Context

**Timeline is the organizing constraint.** Today is 2026-08-11. The installation must be live in the
front yard by roughly the first week of December 2026 — about 16 weeks of part-time evenings and
weekends by one person, with Claude implementing. Every structural choice in the roadmap is made to
protect that date. Hardware with shipping lead time is ordered in Phase 1, not later; a late
enclosure order is the single most likely way this misses the season.

**The POC is evidence, not a head start.** `poc/index.html` holds the entire control loop in browser
JavaScript: the `RTCPeerConnection` handshake, `getUserMedia` mic capture, the 300s session cap, the
255s wrap-up nudge, the 15s/28s silence ladder, LED state, and `end_call` teardown. The target is a
headless session manager on a Pi driven by a GPIO hook switch and a USB audio adapter — no browser,
no screen, no `getUserMedia`. Only `server.py`'s token-broker role and the `SANTA_INSTRUCTIONS`
persona string transfer directly. Transport, audio I/O, timers, guardrail teardown, and the state
machine all need headless re-implementation. This is a substantial phase of its own, not a
"deploy to Pi" task.

**Documentation status.** The source pre-PRD (rev 2, 2026-03-30) is explicitly concept-stage with
Author TBD. Zero ADRs existed at ingest. Apart from the three decisions locked below, nothing in the
ingested documents is binding — the 28 PRD requirements are the baseline, carried forward as
PRD-derived rather than locked.

**Repo state.** Git repo on `main`, clean tree, pushed to GitHub. Secrets handled correctly (`.env`
gitignored, key read from environment, never committed). There is an undocumented second codebase at
`voice/my-project/` — 27 tracked files, Node/TypeScript, `@openai` packages, plus a nested duplicate
`my-project/my-project/`. No ingested document describes it. Phase 1 decides whether it is dead
scaffolding to delete or something to keep.

**Cost exposure.** The Realtime API bills per minute of audio in and out. The default schedule is 12
hours/day, 7 days/week, unattended, outdoors, with unsupervised children as the load generator. A
spend ceiling is a Phase 1 item, not an afterthought.

## Constraints

- **Timeline**: Live in the front yard by the first week of December 2026 — hard external deadline,
  the season does not move. ~16 weeks from 2026-08-11, part-time, one person.
- **Privacy**: No audio stored. No transcripts stored. Ever. Session logs carry session ID, duration,
  states visited, and errors only; rotated daily, retained 7 days. The headless port must not add
  debug logging of Realtime data-channel events — that would silently violate this.
- **Performance**: Turn latency < 2s p95 (child stops speaking → Santa responds). Long pauses break
  immersion for a child.
- **Safety**: Zero inappropriate content delivered to a child. Zero-tolerance, unattended, unsupervised
  audience. Requires a defined verification method before launch.
- **Environmental**: Outdoor, unattended, 20°F–50°F typical. Sealed electronics, sealed cord entry,
  door latch against wind swing, powered from an outdoor outlet.
- **Network**: Admin UI local-network only. PIN stored hashed on device. No internet-facing surface.
- **Concurrency**: Exactly one session — single handset, single by construction.
- **Budget**: ~$850–1,050 total hardware, camera line removed. Booth dominates ($600–800 mahogany;
  $150–300 smaller Etsy props are the fallback).
- **Tech stack**: Raspberry Pi 5 (8GB), driverless USB audio adapter, normally-closed lever-arm
  microswitch on the cradle, OpenAI Realtime API. POC runtime is Python 3 stdlib only — keep the
  dependency footprint small enough to debug in a cold booth.
- **Cost**: Realtime API bills per audio-minute; spend ceiling must be in place before any unattended
  runtime.

## Key Decisions

<decisions>

### Locked

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| **CD-01 — Voice pipeline: OpenAI Realtime API (Option A). LOCKED.** The modular Whisper + Claude + ElevenLabs path (Option B) is out of scope. No A/B evaluation phase. | A working POC on Option A already exists and proves latency and persona quality. Option B adds three vendor integrations and stage-to-stage latency for voice control we do not need. | — Pending |
| **CD-05 — Camera fully out of v1. LOCKED.** No camera, no mount point, no MJPEG stream, no admin video surface, no PRD 6.5 physical traffic-awareness. Budget line removed. | PRD Section 9 is the scope statement; Sections 5.3 / 6.5 / 11 were never reconciled with it. Cutting it removes a feature, an admin screen surface, and $50–70. | — Pending |
| **Realtime API consequence — per-stage metrics are unimplementable. LOCKED.** The Realtime API is one unified STT+LLM+TTS loop with no per-stage boundaries. `santa_stt_latency_ms`, `santa_llm_latency_ms`, `santa_tts_latency_ms` and the `santa_api_errors_total{service="stt\|llm\|tts"}` label set are dropped and replaced with a total-turn-latency / session-event / connection-error contract. | Follows directly from CD-01. Building against a metric contract the runtime cannot satisfy would produce tasks that cannot be completed. Resolves ingest warning #2. | — Pending |
| **Latency alert aligned to target.** The high-turn-latency warning fires at p95 > 2s, not the PRD's 3s. | The PRD success criterion is < 2s p95 while its alert only fired above 3s, leaving a 2–3s band where the system silently misses its own criterion. | — Pending |

### Open — carried forward, do not invent answers

| ID | Decision needed | Forced in | Why it matters |
|----|-----------------|-----------|----------------|
| CD-02 | Vulgarity detection: prompt-based in-LLM vs separate classifier, and how "zero inappropriate content" gets verified before launch | Phase 4 | Gates a zero-tolerance safety criterion for an unattended installation used by unsupervised children. The PRD rates it Medium; that understates it. Today it rests on prompt text plus the model choosing to call `end_call`, with no deterministic backstop. |
| CD-03 | Admin UI + observability hosting: on the Pi itself vs a separate home server | Phase 5 (surfaced), Phase 6 (settled) | Structural deployment topology. Determines the Pi's CPU/thermal budget in a cold outdoor enclosure and whether an observability outage takes the phone down with it. |
| CD-04a | WiFi range vs LTE dongle | Phase 1 | Needs a physical site range test. A bad assumption here invalidates the connectivity plan and the bill of materials late. |
| CD-04b | Handset weatherproofing solution | Phase 3 | Sealed cord entry at the cradle. |
| CD-04c | Attract-state music source and speaker | Phase 5 | The only deferred item attached to a stated experience requirement (IDLE attract state). |
| CD-04d | Signage and decoration | Phase 7 | Low. Affects whether children understand what the box is. |
| CD-04e | PIN complexity and reset-if-forgotten | Phase 5 | Low. |
| CD-06 | Final handset purchase — full rotary phone vs standalone handset | Phase 1 | Stated preference: full rotary phone (cradle and hook switch already built in). Must be ordered in Phase 1. |
| CD-07 | Final enclosure purchase — vendor and material | Phase 1 | Stated preference: mahogany over MDF for outdoor durability. Longest lead time in the project; dominant budget line. |
| — | Pi Realtime transport: WebRTC vs WebSocket | Phase 2 | The POC's browser WebRTC path has no headless equivalent for free. Settle before writing the transport. |
| — | `voice/my-project/` — delete or keep | Phase 1 | Undocumented 27-file Node/TypeScript codebase with a nested duplicate. Nothing references it. |

</decisions>

---
*Last updated: 2026-08-11 after document ingest and initial roadmap*
