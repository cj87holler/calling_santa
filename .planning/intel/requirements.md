# Requirements (PRD-derived)

All requirements below derive from a single PRD. No competing PRDs exist in the ingest set,
so there are no cross-PRD acceptance variants. Intra-document contradictions are flagged
per-requirement and mirrored in INGEST-CONFLICTS.md.

source (all entries unless noted): /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md
PRD status: Pre-PRD / Concept Definition, rev 2, dated 2026-03-30, Author TBD — proposal-stage, not binding.

---

## Core experience

### REQ-offhook-session-trigger
- source: pre-PRD Sections 2, 5.3, 5.4
- description: Lifting the handset off the cradle starts a session; returning it to the cradle ends the session immediately.
- acceptance: Off-hook GPIO signal starts a session with no other input. On-hook signal tears the session down and returns to IDLE.
- scope: hardware + session manager

### REQ-santa-conversation-flow
- source: pre-PRD Sections 2, 5.2
- description: Santa runs a four-state conversation: GREETING (asks the child's name), ENGAGED (warm conversation, asks about Christmas wishes), CLOSING (encouraging values-based send-off), TERMINATED (graceful exit on inappropriate language).
- acceptance: Santa asks for a name in the opening turn; uses that name throughout; every normal session ends with a positive values-based message.
- scope: agent prompt + session manager

### REQ-santa-persona-guardrails
- source: pre-PRD Section 5.2
- description: Persona is jolly, warm, patient, age-appropriate; stays on topic (Christmas, kindness, family, gifts); gently deflects off-topic questions back to Christmas themes.
- acceptance: Off-topic prompts are redirected, not answered as a general assistant. Content is age-appropriate in every turn.
- scope: agent prompt

### REQ-attract-idle-state
- source: pre-PRD Section 2 (IDLE STATE)
- description: While the system is ON and no session is active, soft Christmas music plays and an indicator light blinks invitingly.
- acceptance: With the handset on-hook during scheduled hours, the attract light is visible and music plays.
- scope: hardware + session manager
- note: music source / speaker setup is an open question (Section 8 item 6, Low)

### REQ-off-state-behavior
- source: pre-PRD Section 2 (System OFF State)
- description: Outside scheduled hours, picking up the handset plays a pre-recorded "Santa is resting" message, the indicator light stays off, no session starts, and no API calls are made.
- acceptance: Handset pickup during OFF hours produces the recorded message only; zero outbound API calls; zero session records.
- scope: session manager + audio asset

### REQ-status-leds
- source: pre-PRD Section 5.3
- description: Three-state LED indicator visible through the internal panel — green = active session, amber = idle/ready, off = system off.
- acceptance: LED state matches system state in all three cases.
- scope: hardware + GPIO

---

## Session rules

### REQ-session-max-duration
- source: pre-PRD Section 4
- description: Maximum session length is 5 minutes; Santa gracefully wraps up and says goodbye rather than being cut off.
- acceptance: No session exceeds 5 minutes. The wrap-up is spoken, not abrupt.
- scope: session manager
- as-built reference: POC caps at 300s and nudges Santa toward goodbye at 255s (see constraints.md CON-poc-timers)

### REQ-inactivity-timeout
- source: pre-PRD Section 4
- description: ~15 seconds of silence triggers one Santa prompt; continued silence closes the session.
- acceptance: One and only one re-engagement prompt is issued, then the session closes.
- scope: session manager
- as-built reference: POC uses 15s check / 28s hang-up (consistent refinement)

### REQ-vulgarity-termination
- source: pre-PRD Sections 4, 5.2
- description: On vulgar or inappropriate language, Santa says "That isn't very nice. I'll have to say goodbye for now — Ho ho ho." and the session ends immediately.
- acceptance: The specified line is delivered, then the session terminates without further conversational turns.
- scope: agent prompt + session manager
- open: detection mechanism undecided (Section 8 item 4) — see decisions.md CD-02

### REQ-session-reset
- source: pre-PRD Section 4
- description: On hang-up or session end, return to IDLE and clean all session state.
- acceptance: No state (name, transcript, timers, connection) survives into the next session.
- scope: session manager

### REQ-single-concurrent-session
- source: pre-PRD Section 4
- description: Exactly one concurrent session — single handset.
- acceptance: A second concurrent session is impossible by construction.
- scope: session manager

### REQ-zero-inappropriate-content
- source: pre-PRD Section 10 (Success Criteria), Section 5.2 (Hard guardrail)
- description: No inappropriate content is ever delivered to a child.
- acceptance: Zero inappropriate outputs across the season. Requires a defined verification method (none specified in the PRD).
- scope: system-level safety NFR
- open: detection mechanism undecided (decisions.md CD-02); the POC relies solely on prompt-based in-LLM judgement with no deterministic backstop. See INGEST-CONFLICTS.md WARNING.

---

## Voice pipeline

### REQ-voice-pipeline
- source: pre-PRD Section 5.1
- description: Handset mic → STT → LLM (Santa agent) → TTS → handset speaker.
- acceptance: Full-duplex-feeling spoken conversation through the handset with turn latency meeting REQ-turn-latency.
- scope: core software
- OPEN: implementation is undecided between Option A (OpenAI Realtime) and Option B (Whisper + Claude + ElevenLabs). Do not treat Option A as selected. See decisions.md CD-01 and INGEST-CONFLICTS.md.

### REQ-turn-latency
- source: pre-PRD Section 10
- description: Turn latency feels natural to a child.
- acceptance: < 2 seconds p95 (child stops speaking → Santa responds).
- scope: NFR
- note: PRD alerting only fires above 3s p95 — see INGEST-CONFLICTS.md INFO

---

## Admin control and scheduling

### REQ-admin-web-ui
- source: pre-PRD Sections 6.1, 6.4
- description: Web-based admin UI reachable from any browser on the local network (phone or desktop), with five screens: Dashboard, Schedule Editor, Override Panel, Session Log, System Health.
- acceptance: Owner can reach all five screens from a phone on the home network. Dashboard shows current ON/OFF status, sessions today, and next schedule change.
- scope: admin service
- constraint: local network only; internet-facing admin is out of scope (Section 9)

### REQ-schedule-config
- source: pre-PRD Section 6.2
- description: Per-day ON/OFF windows, individual days enable/disable, written by the admin UI to a config file the session manager reads.
- acceptance: Editing a day's window in the UI changes system active/inactive behavior without a restart. Config matches the documented JSON schema (constraints.md CON-schedule-schema).
- scope: admin service + session manager

### REQ-pin-override
- source: pre-PRD Section 6.3
- description: PIN-protected Force ON / Force OFF toggle with optional time-limited expiry, overriding the schedule. PIN set during initial device setup, stored hashed on device.
- acceptance: Force ON activates regardless of schedule; Force OFF deactivates regardless of schedule; override expires at its set time or is manually cleared; activation/deactivation takes effect within 5 seconds of submission (Section 10).
- scope: admin service
- open: PIN complexity and reset-if-forgotten mechanism undecided (Section 8 item 9, Low)

### REQ-session-log
- source: pre-PRD Section 6.4
- description: Session Log screen listing today's sessions — time, duration, completion status.
- acceptance: No audio and no transcripts appear anywhere in the log.
- scope: admin service

### REQ-traffic-dashboard
- source: pre-PRD Section 6.5
- description: Traffic metrics in the admin UI — sessions today/this week/total season, busiest-hours heatmap (hour of day x day of week), average session duration, early-termination (vulgarity) count.
- acceptance: All five figures render for a live season's data.
- scope: admin service
- deferred: "peak concurrent wait indicator" and outdoor queue light are marked future
- contested: "physical awareness hooks" reference a camera — see INGEST-CONFLICTS.md camera scope WARNING

### REQ-owner-schedule-speed
- source: pre-PRD Section 10
- description: The owner can update the schedule and toggle overrides from their phone quickly.
- acceptance: Under 30 seconds from phone in hand to change applied.
- scope: NFR / admin UX

---

## Observability

### REQ-observability-metrics
- source: pre-PRD Section 7 (including the appended rev-2 fragment)
- description: The session manager exposes a Prometheus metrics endpoint covering session, voice pipeline, API/error, admin-state, and system (node_exporter) metrics.
- acceptance: All metric names in constraints.md CON-metric-catalog are scrapeable.
- scope: session manager
- contested: the per-stage `santa_stt_latency_ms` / `santa_llm_latency_ms` / `santa_tts_latency_ms` and `santa_api_errors_total{service="stt|llm|tts"}` metrics presuppose a modular pipeline — see INGEST-CONFLICTS.md WARNING

### REQ-grafana-dashboards-alerts
- source: pre-PRD Section 7
- description: Self-hosted Grafana dashboards over Prometheus, with built-in Grafana Alerting configured for the five documented alert rules.
- acceptance: All five alerts in constraints.md CON-alert-rules are configured and fire on their conditions.
- scope: observability stack
- open: hosting location undecided (Pi vs home server) — see decisions.md CD-03

### REQ-health-without-ssh
- source: pre-PRD Section 10
- description: The owner can see system health without SSH-ing into the device.
- acceptance: All health signals needed to diagnose an outage are visible in Grafana / admin UI.
- scope: NFR

### REQ-structured-logging-privacy
- source: pre-PRD Section 7 (Logging)
- description: Structured JSON logs per session — session ID, duration, states visited, errors. No audio or transcripts stored, for children's privacy. Logs rotated daily, retained 7 days.
- acceptance: No audio file and no transcript text is persisted anywhere on the device or in logs. Log rotation and 7-day retention verified.
- scope: session manager
- note: hard privacy requirement; treat as non-negotiable in downstream planning

---

## Hardware and deployment

### REQ-weatherproof-enclosure
- source: pre-PRD Section 5.3, Section 11 item 1
- description: Pi and electronics housed inside a sealed booth enclosure; handset cradle sealed around the cord entry point; booth door latch to prevent wind swing; sealant on joints and silicone bead around glass panes.
- acceptance: Electronics stay dry and operable across 20°F–50°F typical holiday conditions.
- scope: hardware
- open: handset weatherproofing solution undecided (Section 8 item 5, Medium)

### REQ-hardware-platform
- source: pre-PRD Sections 5.3, 11
- description: Raspberry Pi 5 (8GB) runs the session manager, admin web server, Prometheus exporter, GPIO hook-switch monitoring, and LED control; a driverless USB audio adapter handles handset mic and speaker I/O; a normally-closed lever-arm microswitch on the cradle is the session trigger.
- acceptance: All listed roles run concurrently on the Pi within thermal limits (alert at CPU > 85°C).
- scope: hardware
- note: whether the admin/observability stack also runs on the Pi is undecided — decisions.md CD-03

### REQ-connectivity
- source: pre-PRD Sections 3, 5.3
- description: WiFi is the primary connectivity path; an LTE dongle is a possible fallback.
- acceptance: TBD — depends on a site range test.
- scope: hardware
- open: Section 8 item 3, Medium — see decisions.md CD-04

### REQ-unattended-self-service
- source: pre-PRD Sections 2, 10
- description: A child can walk up, pick up the phone, and have a complete magical Santa conversation with no adult intervention and no parent setup.
- acceptance: End-to-end session completes with zero human operator involvement.
- scope: system-level

---

## Explicitly out of scope (v1)

source: pre-PRD Section 9

- Multi-language support
- Recording or replaying calls
- Multiple simultaneous callers
- Camera / video component  — CONTESTED, contradicted by Sections 5.3, 6.5, and 11
- Remote (internet-facing) admin access — local network only
