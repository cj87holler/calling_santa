---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
stopped_at: "Paused 2026-11-26. SD card died after rewiring (LED 8/3-blink boot codes; loose COM wire + hard power pulls); re-flashed (password SSH), Santa reinstalled, OpenAI key OK. First hook switch defective (NC open at rest), replaced. Echo on fresh card fixed with --half-duplex in santa.service. santa.service INSTALLED + running. Next: cold-boot test with new switch, hang-up debounce, card power-loss protection, yard WiFi test, Pi-only API key."
last_updated: "2026-09-02T02:04:26.532Z"
last_activity: 2026-11-26
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
- [Phase 01] 2026-11-02: **D-29 — spend controls configured (01-06).** Project $200 / org $120 (tier-capped, binding) / alerts $60-$90-$110 / auto-recharge off, enforcement ON at both scopes by owner attestation (no screenshots). Single key kept in `call-santa-prod`, not revoked; plan 09 now gates on `KEY BACKED UP: yes`.
- [Phase 01] 2026-11-02: **D-30 (PROVISIONAL — pending spike 01) — analog phone + Grandstream HT801 ATA + OpenAI Realtime SIP, call handling hosted on Vercel.** Owner can't source a USB phone with cradle and won't wire a GPIO hook switch; the ATA detects hook state and auto-dials on lift, and only a phone cord runs to the yard. Webhook + per-call sideband run on Vercel (Hobby 300s function cap → Santa's hard cap drops to 4:30). Settles CD-03 (cloud admin/observability, needs a login) and moots the LTE-vs-ADMIN-01 conflict. **Pi order on hold.** Test plan: `.planning/spikes/01-ata-sip/TEST-PLAN.md`.
- [Phase 01] 2026-11-16: **D-31 — back to the Pi path, starting on a free Raspberry Pi 3 B (1GB).** Owner got the board free on 2026-11-04. Bring-up blocked for two sessions by undervoltage (a Philips 5V 2.5W = 0.5A brick); fixed with a 2A+ charger (`get_throttled=0x0`). The Pi is fully upgraded and joins WiFi `ATTPj8JP8V` (2.4GHz) on cold boot; `ssh cj@santa.local` works. The Pi 3 is the test bed. Whether it or a Pi 5 ships in the yard is decided after the first Pi call. **Spike 01 (D-30, ATA + SIP) parked, not cancelled.** `santa-line` stays deployed and has no Pi-path role yet. Headless shape agreed in principle: a Python program speaking Realtime over WebSocket (not headless Chromium; too heavy for 1GB). Order: USB audio sound check → hand-started call → port call rules (end_call, cap, silence) → systemd start on boot → trigger. **The no-wiring hook switch is still unsolved;** a USB button or foot pedal is the stopgap.
- [Phase 01] 2026-11-19: **D-32 — GPIO hook switch is back in.** The owner will now wire a hook switch, reversing the no-wiring premise behind D-30 and returning to D-10's design: an **LXW5-11N1** lever micro switch (SPDT) in the old cradle phone, **COM → GND (pin 9), NC → GPIO17 (pin 11)**, internal pull-up, no 3.3V wire. NC means a broken wire reads as on-hook (fail-safe: no runaway billed calls). Female dupont on the Pi header; Wago-style lever connectors at the switch tabs (no soldering). Lift = start Realtime call; hang up = close the socket. Max-length cap + silence hang-up stay mandatory (a phone left off the hook), and after either the program waits for a full hang-up before re-arming; debounce the switch. Audio: **lavalier mic hidden in the handset → USB adapter mic jack; Santa out of the adapter's 1/8\" jack to an external speaker** (not the earpiece). Echo plan: test full duplex first → `near_field` noise reduction + lower volume → half-duplex (mute mic while Santa speaks) as last resort.
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

Last session: 2026-11-22
**2026-11-22 UPDATE (read this first; it supersedes the 'Stopped at' / 'NEXT SESSION' notes from 11-21 below):**
- **Cradle built, red wire moved to NC.** Wiring now: green → Pi pin 9 (GND) → switch COM; red → Pi pin 11 (GPIO17)
  → switch **NC**. Handset resting presses the lever = idle; lift = off hook. No code change (closed-to-ground =
  off hook either way). `hooktest.py` passed with the real handset.
- **Full call with the real phone worked** (`python3 call.py`, started by hand over ssh): lift → jingle → Santa →
  hang up → sparkle. Owner: "worked pretty well." No gain or half-duplex tuning reported as needed.
- **`pi/santa.service` written and committed, NOT yet copied to or installed on the Pi.** Runs
  `/usr/bin/python3 -u /home/cj/call.py` as `cj` (groups audio + gpio), `Restart=always`, `RestartSec=5`, after
  `network-online.target` + `sound.target`. Install steps are in the file's header comment.
- **NEXT SESSION, in order:** (1) `scp santa.service` to the Pi → `sudo cp` to `/etc/systemd/system/` →
  `daemon-reload` → `enable --now santa`; (2) cold-boot test: unplug/replug power, wait ~1 min, lift handset
  with no ssh session, check `journalctl -u santa -f` (USB card found by name? GPIO OK as non-root?);
  remember `sudo systemctl stop santa` before running `call.py` by hand, or two copies fight over the mic;
  (3) yard WiFi test with `calls.py --live`; (4) separate Pi-only API key before the yard install;
  (5) compare `calls.py` cost estimates with the OpenAI usage dashboard.
- **Deadline:** yard install ~2026-12-01, 9 days from this pause. Software is close to done; the remaining risks are the
  enclosure/weatherproofing, power, and yard WiFi range.

Stopped at: **Hook switch proven; call program written but not yet run (no speaker).**
- **Switch wiring as built:** green dupont → Pi pin 9 (GND, 5th pin in on the odd row) → switch COM screw.
  Red dupont → Pi pin 11 (GPIO17, 6th pin in) → switch **NO** screw for the bench test (press lever = off the hook
  = call starts). **Move red to NC when the cradle is built** (handset resting = idle, lift = call). Switch is the
  screw-terminal kind (COM / NO / NC); wire goes under the washer, wrapped clockwise. No 3.3V wire.
- `pi/hooktest.py` passed: idle at rest, PICKED UP on press, HUNG UP on release, one line per press (50 ms debounce).
- `pi/call.py` written and on the Pi (not yet run): waits for off-hook, opens Realtime over WebSocket
  (`gpt-realtime`, voice `ash`, persona copied from `poc/server.py`), mic from USB card 2 via arecord with 3x
  software gain, Santa out card 2 via aplay, `near_field` noise reduction, no transcription requested, end_call
  hang-up, 5:00 cap with wrap nudge at 4:15, silence nudges at 15s/28s and hard stop at 45s, re-arms only after a
  full hang-up. Flags: `--now` (no switch), `--half-duplex` (mute mic while Santa talks), `--gain N`.
  `python3-websockets` 15.0.1 installed on the Pi.
- Mic in proven 11-19 (card 2, lavalier, quiet). **Playback through the adapter proven 2026-11-21** with a small
  powered speaker in the green jack (`speaker-test -D plughw:1,0 -c 2 -t wav -l 1`). **The USB card number shuffles
  between boots** (card 2 on 11-19, card 1 on 11-21; card 2 was HDMI, which gives "error 524" with no TV). Always
  check with `aplay -l | grep -i usb`; `call.py` finds the adapter by name, and `SANTA_CARD=N` overrides.
**FIRST TWO-WAY PI CALL WORKED (2026-11-21 20:44).** Bench switch press → "Off the hook: calling Santa." →
Santa talking within ~1s → child/Santa turns ×2 → Santa said goodbye + end_call → hung up after his audio
finished (43s call) → waited for the lever release → re-armed. Full duplex with the speaker; no self-interruption
in the log. Key now saved on the Pi in `~/.santa_key` (owner-only); `call.py` reads it when OPENAI_API_KEY is unset.
Before the yard install: make a separate Pi-only key so it can be revoked alone (the SD card is physically exposed).
**Logging proven on the Pi 2026-11-21 21:04:** first logged call 55s, 3 child turns, avg reply 1.1s (under the
2s SESS-03 target), est. cost $0.075, ended hung_up; health check OpenAI ok 36 ms, WiFi -32 dBm (indoors, near the
router; the yard will be weaker), CPU 45°C. Rough cost: ~$0.08/min of talk. Still to do: compare the estimate
against the OpenAI usage dashboard. **Logging added 2026-11-21 (OBS-04 shape):** `call.py` writes one JSON line per call
(end reason, seconds, turns, first-audio and turn latency, API errors, token counts, estimated cost) plus a
connectivity check every 5 min (OpenAI TCP reachability + ms, WiFi dBm, CPU °C) to `~/santa-logs/YYYY-MM-DD.jsonl`,
kept 7 days. No audio, no words. `pi/calls.py` prints the report (today / 7 days / connectivity / per call;
`--live` checks reachability now). Cost uses gpt-realtime prices checked 2026-11-21 ($32/$64 audio in/out,
$4/$16 text, $0.40 cached per 1M); the OpenAI usage dashboard is the real bill. **Prometheus + Grafana (OBS-01/02)
deferred:** too heavy for a 1GB Pi 3 and the Dec 1 timeline; the JSONL fields map onto the Metric Contract so an
exporter can be added later (or Grafana Cloud with the Pi pushing out, needing no DNS or open ports).
**Sounds added 2026-11-21 (owner approved by ear):** POC `pickup.mp3`/`hangup.mp3` trimmed to the POC clips
(6s/7s, same fades, 60% volume) as 24 kHz mono WAV in `pi/sounds/` → Pi `~/sounds/`. Jingle starts on pickup,
mic muted while it plays, Santa's greeting held until **3.5s** after pickup (`JINGLE_MIN_S`, env `SANTA_JINGLE_S`),
jingle fades on his first audio. Sparkle after every call, cut by a new pickup. Owner: "outro was great", intro
good at 3.5s.
**Files on the Pi (home dir `~`):** `call.py`, `calls.py`, `hooktest.py`, `soundcheck.sh`, `say.sh`,
`sounds/pickup.wav`, `sounds/hangup.wav`, `.santa_key` (chmod 600), logs in `santa-logs/`. All copied by scp from
`pi/` in the repo; the repo is the source of truth.
**NEXT SESSION: systemd start-on-boot.** A `santa.service` running `python3 /home/cj/call.py` as user `cj`,
`Restart=always`, after `network-online.target`; key from `~/.santa_key` (already supported); stdout to journald
(`journalctl -u santa -f`); confirm the USB card is found after a cold boot (number shuffles; found by name) and
that GPIO works for a non-root user (cj is in the gpio group by default on Pi OS). Then: cradle (red → NC), yard
WiFi test with `calls.py --live`, separate Pi-only API key before the yard install.
Next (updated 11-21): sound/latency feedback; systemd start-on-boot (so no ssh session is needed); cradle (red → NC).
Old next-session list, now done through step 3: (1) owner plugs a small powered speaker into the adapter's green out jack; (2) `ssh cj@santa.local`,
load key with `read -s`; (3) `python3 call.py`, hold the lever down, talk, let go; (4) tune: `--half-duplex` if Santa
interrupts himself (echo), `--gain` if he can't hear; (5) then systemd start-on-boot, then the cradle (red → NC).
Lessons: ship scripts with `scp`, run in a Mac terminal from `~/Desktop/calling_santa/pi` with short commands
(a pasted multi-line scp split into two commands). A Mac can't act as a speaker for the Pi.
**2026-11-22: cradle wired to NC** (green → pin 9 GND, red → pin 11 GPIO17, red on the switch's NC screw). `hooktest.py` passed with the handset: resting = idle, lift = PICKED UP, replace = HUNG UP. No code change needed (closed-to-ground = off hook either way). `pi/santa.service` written (not yet installed).
Resume file: none. Read D-31 and D-32 in this file.
