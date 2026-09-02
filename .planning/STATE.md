---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
stopped_at: "Compute locked (DECISION pi-5). Enclosure deprioritized off the critical path (D-28); mount now removable (D-27); deployment is seasonal (D-26). 3 checkpoints remain open: 01-03, 01-05, 01-06"
last_updated: "2026-09-02T02:04:26.532Z"
last_activity: 2026-09-02
progress:
  total_phases: 7
  completed_phases: 0
  total_plans: 10
  completed_plans: 3
  percent: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-11)

**Core value:** A child picks up the handset and talks to a Santa who feels real — warm, fast, and
never says anything a parent would object to.
**Current focus:** Phase 01 — procurement-site-survey-repo-cleanup

## Current Position

Phase: 01 (procurement-site-survey-repo-cleanup) — EXECUTING
Plan: 3 of 10 complete (01-01, 01-02, 01-04)
Status: BLOCKED at 3 human checkpoints — no agent work remains until they clear
Last activity: 2026-09-02

Progress: [███░░░░░░░░] 30%

### Open checkpoints (all blocking, all human-only)

| Plan | Type | Awaiting | Unblocks |
|------|------|----------|----------|
| 01-05 | human-action | Place enclosure / phone / site-hardware orders → reply "ordered" | 01-08, 01-10 |
| 01-03 | human-action | Yard visit: fill ETHERNET-SCOPING.md + set VERDICT → reply "scoped" | 01-07 |
| 01-06 | human-action | OpenAI dashboard: limits, alerts, key revocation → reply "configured" | 01-09 (deletion gate), 01-10 |

01-04 (compute decision) resolved 2026-09-01: `DECISION: pi-5`, 8GB board-only from pishop.us.
`COMPUTE-DECISION.md` is now available for plan 07 (PoE splitter sizing) and plan 08 (electronics
order).

Resume with `/gsd:execute-phase 1` after answering; each checkpoint resumes via a fresh
continuation agent that verifies prior commits first.

**Critical path (revised 2026-09-01, D-28):** 01-06 (revocation token gates plan 09's irreversible
`rm -rf voice/`). **The enclosure is no longer on the critical path** — the owner will build custom
housing if no stock unit fits, which removes the lead-time premise Phase 1's urgency was built on.
Ordering priority is now compute → connectivity/power → phone, with the enclosure and its mount
following whenever they settle.

**Hard deadline:** installation live in the front yard by ~2026-12-01 (~16 weeks).
Phase 1 must complete by 2026-08-25 — a late enclosure order is the top risk to the season.

## Performance Metrics

**Velocity:**

- Total plans completed: 0
- Average duration: —
- Total execution time: 0.0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| - | - | - | - |

**Recent Trend:**

- Last 5 plans: —
- Trend: —

*Updated after each plan completion*
| Phase 01 P01 | 12 | 3 tasks | 9 files |
| Phase 01 P04 | 25min | 1 tasks | 1 files |

## Accumulated Context

### Decisions

Full log in PROJECT.md Key Decisions. Locked at project start:

- **CD-01 — OpenAI Realtime API (Option A) locked.** No modular Whisper/Claude/ElevenLabs branch,
  no A/B evaluation phase.

- **CD-05 — Camera fully out of v1.** No hardware, mount point, MJPEG stream, admin video surface,
  or PRD 6.5 traffic-awareness. Budget line removed.

- **Metric contract revised.** Per-stage STT/LLM/TTS latency metrics and the
  `santa_api_errors_total{service=...}` label set dropped as unimplementable under a unified
  Realtime loop; replaced with total turn latency, session/response counts, and typed connection
  and API error counters.

- **Latency alert aligned to target** — warns at p95 > 2s, not the PRD's 3s.

Open decisions carried forward: CD-02 (vulgarity mechanism, forced in Phase 4), CD-03 (admin and
observability hosting, settled in Phase 6), CD-04a–e (connectivity, handset weatherproofing, attract
music source, signage, PIN complexity), CD-06/CD-07 (final hardware purchases, forced in Phase 1),
plus Pi transport choice — WebRTC vs WebSocket — forced in Phase 2.

- [Phase 01]: Phase 1 gate (verify.sh) tests filled order values, never printed field labels — a blank order form cannot green the HW-01 gate over unspent money (T-1-40).
- [Phase 01]: verify.sh distinguishes NOT-YET (a later wave deliberately falsifies this) from FAIL, so the gate is quiet during waves 1-3; --gate upgrades PENDING and NOT-YET to FAIL.
- [Phase 01]: HW-06 gating is branch-aware: verify.sh reads evidence/site-survey/CONNECTIVITY-BRANCH (ethernet | wireless) to select the assertion set (D-06..D-09).
- [Phase 01]: ROADMAP Phase 1 success criteria 1, 2 and 3 rewritten to match CONTEXT.md D-01 (post-mounted cabinet), D-07/D-10 (branch-neutral compute and cabling) and D-06/D-09 (three-outcome connectivity with a cited number).
- [Phase 01] 2026-09-01: **D-10 resolved — `DECISION: pi-5`**, 8GB (SC1112), board-only from pishop.us, $239.75 all-in. Hook switch is the GPIO header with a normally-closed lever-arm microswitch on an internal pull-up; the same header carries the three HW-04 LEDs at $0 added hardware.
- [Phase 01] 2026-09-01: **D-26 — the installation is seasonal.** Box, mount and cable all come down each January and are stored dry. Reverses the permanence assumption behind D-01 and D-02. The cabinet's outdoor duty cycle is ~6 weeks/year, not 52.
- [Phase 01] 2026-09-01: **D-27 — removable ground stake with ballast base supersedes D-02.** 4x4 post, fast-setting concrete, post cap and brackets all leave the BOM. **The concrete cure-time urgency that made Phase 1 schedule-critical dissolves with it.**
- [Phase 01] 2026-09-01: **D-28 — enclosure deprioritized, custom build admitted.** Removes the enclosure from the critical path. Interior fit (>=15x13x20) is retained as a design target, not a purchase gate. Evaluated: Wonderjune B0DK6PZ123 fails on depth (~9.5" interior vs a 9" phone body); B0GSSQVJD7 (21x14.5x12.8" exterior, 35.4" spike, ballastable planter base) fits with margin **if** its shelf is confirmed removable.
- [Phase 01]: DECISION: pi-5 (8GB, board-only from pishop.us, configuration A1) locked as the installation compute; hook-switch input path is the GPIO header with a normally-closed lever-arm microswitch on a pull-up pin, pin assignment deferred to Phase 3

### Pending Todos

- **01-03 form is still blank.** The owner walked the route on 2026-09-01 and reported preliminary
  findings verbally, but `ETHERNET-SCOPING.md` has not been filled and no `CONNECTIVITY-BRANCH`
  exists. **These are owner-reported, not measured-and-recorded, and must not be treated as
  evidence:** approximately 150 ft total run; exit via the existing AT&T fiber entry penetration
  (drywall over brick, exterior box present, so `Drilling required: no`); route runs router -> wall
  -> down the side of the house inside a fence -> across the yard; surface conduit rather than
  burial, which **avoids the 811 locate** under the form's own rule. Still unrecorded: the spot
  marker and landmark reference, the outlet inspection, the sealing method, and a measured (not
  estimated) run length. Verdict trends `FEASIBLE` on all three criteria but is not set.
- **Confirm the Wonderjune B0GSSQVJD7 shelf is removable** before that box is bought. A fixed
  mid-height shelf makes lifting the handset off the cradle physically impossible — a hard fail.
- **PoE must be 802.3at (30W) or better**, with a splitter that outputs 5V/5A over USB-C PD. The Pi 5
  needs 27W; 802.3af tops out at 15.4W. Undersized supply presents in December as random mid-call
  audio dropouts.
- **Cat6 must be solid bare copper, not CCA.** Copper-clad aluminium raises resistance and voltage
  drop across a ~150 ft PoE run, and much of the cheap "direct burial Cat6" on the market is CCA.
- **Unrecorded conflict: HW-06 admits an LTE dongle, ADMIN-01 requires the admin UI on the local home
  network.** A Pi on LTE is not on the home LAN, so the admin UI would be unreachable from a phone on
  home WiFi. Nothing in the planning documents addresses this. Moot if the ethernet branch is taken;
  becomes a real Phase 5 problem if the wireless branch is taken and WiFi fails the range bar.

### Blockers/Concerns

- **Phase 1 is time-critical.** Enclosure lead time is the longest in the project. If Phase 1 slips
  past 2026-08-25, revisit scope rather than compress later phases.

- **The POC does not port.** `poc/index.html` holds the entire control loop in browser JavaScript.
  Only the token-broker role and the `SANTA_INSTRUCTIONS` persona transfer. Phase 2 is a headless
  re-implementation, not a deployment.

- **Privacy guardrail is easy to break silently.** No audio, no transcripts, ever — including debug
  logging of Realtime data-channel events during Phase 2 development.

- **Safety is under-specified upstream.** The source PRD gives a zero-tolerance criterion with no
  verification method. Phase 4 must produce both a mechanism and a passing test run.

- **Cost exposure.** Realtime API bills per audio-minute against a 12h/day, 7d/week unattended
  schedule with unsupervised children. Spend ceiling is a Phase 1 item.

- **Undocumented codebase** at `voice/my-project/` (27 tracked files, nested duplicate). Resolve in
  Phase 1 before it confuses later work.

## Deferred Items

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| Feature | Peak concurrent wait indicator / outdoor queue light | v2 | 2026-08-11 |
| Feature | Multi-language support | Out of scope v1 | 2026-08-11 |
| Architecture | Modular voice stack (Whisper + Claude + ElevenLabs) | v2 fallback only if Realtime voice quality disappoints in the field | 2026-08-11 |

## Session Continuity

Last session: 2026-09-02T02:04:26.525Z
Stopped at: Compute locked (DECISION pi-5). Enclosure deprioritized off the critical path (D-28); mount now removable (D-27); deployment is seasonal (D-26). 3 checkpoints remain open: 01-03, 01-05, 01-06
Resume file: None
