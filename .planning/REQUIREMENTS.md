# Requirements: Call Santa

**Defined:** 2026-08-11
**Core Value:** A child picks up the handset and talks to a Santa who feels real — warm, fast, and
never says anything a parent would object to.

**Baseline provenance:** 28 requirements derived from `call-santa-pre-prd.md` (rev 2, 2026-03-30,
Pre-PRD / Concept Definition, Author TBD). That document is **PRD-derived, not locked** — it is
explicitly concept-stage and zero ADRs existed at ingest. Requirements added or rewritten during
roadmapping are tagged `[added]` or `[revised]` with a reason.

---

## v1 Requirements

### Hardware & Enclosure (HW)

- [ ] **HW-01**: Booth enclosure and phone hardware are ordered and received, with mahogany preferred
  over MDF for outdoor durability and a full corded/rotary phone preferred over a standalone handset
  (cradle and hook switch already built in). *(PRD 5.3, 11; resolves CD-06, CD-07)*
- [ ] **HW-02**: A normally-closed lever-arm microswitch on the phone cradle reports off-hook and
  on-hook to a Pi GPIO pin reliably, with no bounce-induced false sessions. *(PRD 5.3, 5.4)*
- [ ] **HW-03**: A driverless USB audio adapter carries handset mic input and handset speaker output
  at a quality that makes Santa intelligible to a child. *(PRD 5.3, 11)*
- [ ] **HW-04**: Three-state status LEDs are wired to GPIO and visible through the internal panel.
  *(PRD 5.3)*
- [ ] **HW-05**: Electronics are sealed inside the booth, the handset cord entry at the cradle is
  sealed, joints and glass panes are sealed, and a door latch prevents wind swing — the assembly
  stays dry and operable across 20°F–50°F. *(PRD 5.3, 11; resolves CD-04b)*
- [ ] **HW-06**: The connectivity path is chosen on the basis of a physical range test at the actual
  front-yard install location — home WiFi if signal holds, LTE dongle if it does not. *(PRD 3, 5.3;
  resolves CD-04a)*
  - *Note (Phase 1): decisions D-06 through D-09 admit a wired ethernet run as a third outcome.
    Under that branch the physical evidence required by this requirement is the measured cable run
    at the marked install spot plus wired-path `mtr` and `iperf3` results, in place of an RF range
    test. A decision without a cited number satisfies neither branch (D-09).*
- [ ] **HW-07**: The booth is installed in the front yard, powered from an outdoor outlet through a
  weatherproof cord, and holds connectivity and power through a full scheduled day. *(PRD 3, 5.3)*

### Session Core (SESS)

- [ ] **SESS-01**: Lifting the handset starts a session with no other input; returning it to the
  cradle tears the session down immediately and returns to IDLE. *(PRD 2, 5.3, 5.4)*
- [ ] **SESS-02**: A headless session manager on the Pi runs the full voice loop — handset mic →
  OpenAI Realtime API → handset speaker — with no browser, no screen, and no `getUserMedia`.
  *(PRD 5.1, 5.4; [revised] Option A locked per CD-01, and re-scoped as a full headless
  re-implementation rather than a port of `poc/index.html`)*
- [ ] **SESS-03**: Turn latency from the child ceasing to speak to Santa's first audio is under 2
  seconds at p95. *(PRD 10)*
- [ ] **SESS-04**: No session exceeds 5 minutes, and the ending is a spoken graceful wrap-up rather
  than an abrupt cut. *(PRD 4; POC reference: 300s cap, 255s wrap nudge)*
- [ ] **SESS-05**: About 15 seconds of dead air triggers exactly one re-engagement prompt from Santa;
  continued silence closes the session with a brief goodbye. *(PRD 4; POC reference: 15s check /
  28s hang-up)*
- [ ] **SESS-06**: On hang-up or session end, no state survives into the next session — name,
  transcript buffer, timers, and the Realtime connection are all cleared. *(PRD 4)*
- [ ] **SESS-07**: Exactly one session can exist at a time, by construction. *(PRD 4)*

### Santa Experience (EXP)

- [ ] **EXP-01**: Santa runs the four-state conversation — GREETING (asks the child's name), ENGAGED
  (warm conversation about Christmas wishes), CLOSING (values-based send-off), TERMINATED (graceful
  exit) — using the child's name throughout and ending every normal session on a positive note.
  *(PRD 2, 5.2)*
- [ ] **EXP-02**: Santa stays jolly, warm, patient and age-appropriate, keeps to Christmas, kindness,
  family and gifts, and gently redirects off-topic questions instead of answering them as a general
  assistant. *(PRD 5.2)*
- [ ] **EXP-03**: While the system is ON with the handset on-hook, soft Christmas music plays and the
  indicator light blinks invitingly. *(PRD 2; requires resolving CD-04c, the music source and speaker)*
- [ ] **EXP-04**: Outside scheduled hours, picking up the handset plays a pre-recorded "Santa is
  resting" message — indicator light off, no session started, zero outbound API calls. *(PRD 2)*
- [ ] **EXP-05**: LED state matches system state in all three cases — green for an active session,
  amber for idle/ready, off for system off. *(PRD 5.3)*
- [ ] **EXP-06**: A child can walk up, pick up the phone, and complete a magical Santa conversation
  with zero adult intervention and zero parent setup. *(PRD 2, 10)*

### Safety (SAFE)

- [ ] **SAFE-01**: On vulgar or inappropriate language, Santa delivers exactly "That isn't very nice.
  I'll have to say goodbye for now — Ho ho ho." and the session terminates with no further
  conversational turns. *(PRD 4, 5.2)*
- [ ] **SAFE-02**: Zero inappropriate content is delivered to a child across the season. *(PRD 10, 5.2)*
- [ ] **SAFE-03**: The vulgarity detection mechanism is explicitly decided between prompt-based
  in-LLM judgement and a separate classifier, implemented, and paired with a written verification
  protocol — an adversarial test corpus with a pass bar — that is executed and passes before public
  launch. *(PRD 8 item 4 + 5.2; [added] because SAFE-02 is a zero-tolerance criterion with no
  verification method specified anywhere in the source PRD, currently resting on prompt text alone.
  Resolves CD-02.)*

### Admin & Scheduling (ADMIN)

- [ ] **ADMIN-01**: A web admin UI reachable from any browser on the local home network exposes five
  screens — Dashboard, Schedule Editor, Override Panel, Session Log, System Health — with the
  Dashboard showing current ON/OFF status, sessions today, and the next schedule change. Local
  network only. *(PRD 6.1, 6.4, 9)*
- [ ] **ADMIN-02**: Per-day ON/OFF windows with individual day enable/disable are edited in the UI,
  written to a config file matching the documented JSON schema, and take effect in the session
  manager without a restart. *(PRD 6.2)*
- [ ] **ADMIN-03**: A PIN-protected Force ON / Force OFF toggle with optional time-limited expiry
  overrides the schedule, takes effect within 5 seconds of submission, expires on schedule or on
  manual clear, and stores the PIN hashed on device. *(PRD 6.3, 10; PIN complexity per CD-04e)*
- [ ] **ADMIN-04**: A Session Log screen lists today's sessions with time, duration and completion
  status — and no audio and no transcript text appears anywhere in it. *(PRD 6.4)*
- [ ] **ADMIN-05**: Traffic metrics render for live season data — sessions today / this week / total
  season, a busiest-hours heatmap (hour of day × day of week), average session duration, and
  early-termination count. *(PRD 6.5; [revised] camera-based physical traffic-awareness removed per
  the CD-05 lock)*
- [ ] **ADMIN-06**: The owner can go from phone in hand to a schedule change or override applied in
  under 30 seconds. *(PRD 10)*

### Observability (OBS)

- [ ] **OBS-01**: The session manager exposes a Prometheus metrics endpoint covering the full
  Realtime-compatible catalog below. *(PRD 7; [revised] per-stage STT/LLM/TTS metrics and the
  `service` label set removed as unimplementable under a unified Realtime loop — see Metric Contract)*
- [ ] **OBS-02**: Self-hosted Grafana dashboards over Prometheus, with all five alert rules configured
  and firing on their conditions. *(PRD 7; [revised] high-turn-latency threshold aligned to the 2s
  p95 target; hosting location per CD-03)*
- [ ] **OBS-03**: The owner can see every health signal needed to diagnose an outage without SSH-ing
  into the device. *(PRD 10)*
- [ ] **OBS-04**: Structured JSON logs are written per session — session ID, duration, states visited,
  errors — rotated daily and retained 7 days, with no audio file and no transcript text persisted
  anywhere on the device or in any log, including debug logging of Realtime data-channel events.
  *(PRD 7; hard privacy requirement, non-negotiable)*

### Operations (OPS)

- [ ] **OPS-01**: The `voice/my-project/` codebase is either deleted or documented and kept, and the
  repo has exactly one authoritative implementation path. *([added] — 27 tracked Node/TypeScript
  files with a nested duplicate `my-project/my-project/`, referenced by no document; an ingest
  coverage gap that will confuse every later phase if left unresolved)*
- [ ] **OPS-02**: The OpenAI API key lives only in the device environment, never in the repo and
  never in a log, and the Realtime session is established with credentials scoped as narrowly as the
  chosen transport allows. *(POC as-built token-broker pattern; [added] as an explicit target-device
  requirement because the browser/ephemeral-token split does not carry over unchanged to a headless
  Pi)*
- [ ] **OPS-03**: A hard spend ceiling on the OpenAI account is in place with budget alerting, before
  any unattended runtime. *([added] — the Realtime API bills per audio-minute and the default schedule
  is 12 hours/day, 7 days/week, unattended, with unsupervised children as the load generator)*
- [ ] **OPS-04**: The system auto-starts on boot and returns to correct scheduled behavior after a
  power loss, a network drop, or a crash, with no manual intervention. *([added] — implied by the
  unattended-installation requirement but never stated in the source PRD)*

---

## Metric Contract (replaces PRD Section 7 voice-pipeline metrics)

CD-01 locks the OpenAI Realtime API: one unified STT+LLM+TTS loop with no per-stage boundaries.
`santa_stt_latency_ms`, `santa_llm_latency_ms`, `santa_tts_latency_ms` and the
`santa_api_errors_total{service="stt|llm|tts"}` label set are therefore **dropped** — the runtime
cannot emit them. The contract below is what the Realtime API can actually satisfy.

**Session metrics** (unchanged from PRD Section 7)
- `santa_sessions_total` — sessions started
- `santa_sessions_completed` — sessions ended normally (hang-up or timeout)
- `santa_sessions_terminated_early` — sessions ended due to vulgarity
- `santa_session_duration_seconds` — histogram of session lengths
- `santa_idle_duration_seconds` — time between sessions

**Voice pipeline metrics** (revised)
- `santa_total_turn_latency_ms` — histogram, child speech stop → first Santa audio frame
- `santa_realtime_sessions_total` — Realtime sessions successfully established
- `santa_realtime_responses_total` — completed model responses
- `santa_realtime_audio_seconds_total{direction="in|out"}` — billable audio, supports OPS-03

**API / error metrics** (revised label set)
- `santa_api_errors_total{type="auth|connect|session|response"}` — replaces the `service` labels
- `santa_connection_drops_total` — mid-session transport failures
- `santa_api_retries_total`
- `santa_hook_events_total{type="pickup|hangup"}`

**Admin metrics** (from the unmerged PRD rev-2 fragment)
- `santa_schedule_state{state="on|off|override"}`
- `santa_override_active` — 1 when a PIN override is in effect

**System metrics** — node_exporter: CPU, memory, temperature, WiFi signal strength / connectivity.

**Alert rules** (5)
| Alert | Condition | Severity |
|-------|-----------|----------|
| API failure spike | > 3 errors in 5 min | Critical |
| High turn latency | p95 turn latency > **2s** (aligned to the target; PRD said 3s) | Warning |
| Device offline | no metrics for 5 min | Critical |
| Session stuck | session open > 6 min | Warning |
| High CPU / temp | Pi CPU > 85°C | Warning |

---

## v2 Requirements

Deferred. Tracked, not in this roadmap.

- **Peak concurrent wait indicator** and an outdoor queue light — PRD 6.5 marks both future
- **Multi-language support**
- **Modular voice stack** (Whisper + Claude + ElevenLabs) — only if Realtime voice quality
  disappoints in the field; CD-01 locks Option A for v1

## Out of Scope

| Feature | Reason |
|---------|--------|
| Camera / video component | CD-05 locked out of v1 — no hardware, no mount point, no MJPEG stream, no admin video surface, budget line removed |
| Physical traffic-awareness (PRD 6.5) | Depends on the camera; falls with it |
| Recording or replaying calls | Direct conflict with the no-audio, no-transcript privacy rule |
| Multiple simultaneous callers | One handset, single by construction |
| Remote / internet-facing admin access | Local network only; keeps attack surface at zero for an unattended outdoor device |
| Option A vs Option B pipeline evaluation phase | CD-01 is locked; a working Option A POC already exists |
| Per-stage STT/LLM/TTS latency and error metrics | Unimplementable under a unified Realtime loop — see Metric Contract |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| HW-01 | Phase 1 | Pending |
| HW-06 | Phase 1 | Pending |
| OPS-01 | Phase 1 | Pending |
| OPS-03 | Phase 1 | Pending |
| SESS-01 | Phase 2 | Pending |
| SESS-02 | Phase 2 | Pending |
| SESS-03 | Phase 2 | Pending |
| SESS-04 | Phase 2 | Pending |
| SESS-05 | Phase 2 | Pending |
| SESS-06 | Phase 2 | Pending |
| SESS-07 | Phase 2 | Pending |
| EXP-01 | Phase 2 | Pending |
| EXP-02 | Phase 2 | Pending |
| OPS-02 | Phase 2 | Pending |
| HW-02 | Phase 3 | Pending |
| HW-03 | Phase 3 | Pending |
| HW-04 | Phase 3 | Pending |
| HW-05 | Phase 3 | Pending |
| EXP-05 | Phase 3 | Pending |
| SAFE-01 | Phase 4 | Pending |
| SAFE-02 | Phase 4 | Pending |
| SAFE-03 | Phase 4 | Pending |
| ADMIN-01 | Phase 5 | Pending |
| ADMIN-02 | Phase 5 | Pending |
| ADMIN-03 | Phase 5 | Pending |
| ADMIN-04 | Phase 5 | Pending |
| ADMIN-05 | Phase 5 | Pending |
| ADMIN-06 | Phase 5 | Pending |
| EXP-03 | Phase 5 | Pending |
| EXP-04 | Phase 5 | Pending |
| OBS-01 | Phase 6 | Pending |
| OBS-02 | Phase 6 | Pending |
| OBS-03 | Phase 6 | Pending |
| OBS-04 | Phase 6 | Pending |
| OPS-04 | Phase 6 | Pending |
| HW-07 | Phase 7 | Pending |
| EXP-06 | Phase 7 | Pending |

**Coverage:**
- v1 requirements: 37 total
- Mapped to phases: 37
- Unmapped: 0 ✓

---
*Requirements defined: 2026-08-11*
*Last updated: 2026-08-11 after document ingest and initial roadmap*
