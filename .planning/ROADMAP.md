# Roadmap: Call Santa

## Overview

Seven phases carry Call Santa from a laptop proof of concept to a working phone box in the front yard
by the first week of December 2026. The shape is dictated by two forces. First, the season does not
move — so the longest-lead item (a mahogany phone box) is ordered in Phase 1, in the first two weeks,
before a single line of production code is written. Second, the POC does not port — the entire control
loop lives in browser JavaScript, so Phase 2 is a substantial headless re-implementation on the Pi,
not a deployment task.

After that the work splits cleanly: give the software a body (Phase 3), prove it is safe for the
children who will actually use it (Phase 4), give the owner control over when it runs (Phase 5), make
it observable and self-healing so it survives unattended outdoors (Phase 6), and finally put it in the
yard and run a dress rehearsal before the neighborhood arrives (Phase 7).

**Granularity:** standard (no `config.json` present; 7 phases sized for ~16 weeks of part-time
evenings and weekends by one person).

### Timeline anchors

Today is 2026-08-11. Target live date: **first week of December 2026** (~16 weeks). These are
back-pressure dates, not estimates — if a phase slips past its anchor, something downstream has to
be cut rather than compressed.

| Phase | Complete by | Week |
|-------|-------------|------|
| 1. Procurement, Site Survey & Repo Cleanup | 2026-08-25 | 2 |
| 2. Headless Session Core | 2026-10-06 | 8 |
| 3. Physical Build & Hardware Integration | 2026-10-27 | 11 |
| 4. Safety Guardrail & Verification | 2026-11-03 | 12 |
| 5. Scheduling, Admin Control & System States | 2026-11-17 | 14 |
| 6. Observability & Unattended Operations | 2026-11-24 | 15 |
| 7. Outdoor Install & Season Readiness | 2026-12-01 | 16 |

Phase 4 touches prompts, classifiers and test corpora; Phase 3 touches solder, sealant and GPIO.
They can overlap in practice if the booth is late.

**The one non-negotiable date is Phase 1.** A late enclosure order is the single most likely way this
project misses Christmas 2026.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Procurement, Site Survey & Repo Cleanup** - Money spent and questions answered before lead times can hurt us
- [ ] **Phase 2: Headless Session Core** - The whole conversation loop runs on a Pi with no browser
- [ ] **Phase 3: Physical Build & Hardware Integration** - The software gets a body: handset, hook switch, LEDs, sealed booth
- [ ] **Phase 4: Safety Guardrail & Verification** - The zero-inappropriate-content criterion stops being a hope and becomes a tested claim
- [ ] **Phase 5: Scheduling, Admin Control & System States** - The owner controls when Santa is awake, from their phone
- [ ] **Phase 6: Observability & Unattended Operations** - The box tells you when it is sick and heals itself when it can
- [ ] **Phase 7: Outdoor Install & Season Readiness** - It is in the yard, and a child can use it alone

## Phase Details

### Phase 1: Procurement, Site Survey & Repo Cleanup

**Goal**: Every long-lead purchase is placed and every question that could invalidate the build plan
is answered, within two weeks — so that shipping time runs in parallel with software work instead of
after it.
**Depends on**: Nothing (first phase)
**Requirements**: HW-01, HW-06, OPS-01, OPS-03
**Success Criteria** (what must be TRUE):

  1. The booth enclosure and the phone are ordered, with order confirmations and delivery dates on
     record — mahogany over MDF, full corded/rotary phone over a standalone handset (CD-06, CD-07
     resolved by purchase).

  2. The Pi 5 (8GB), USB audio adapter, lever-arm microswitch, LEDs, weatherproof cord and sealant
     are ordered and the total lands inside the ~$850–1,050 budget with no camera line item.

  3. A physical signal-strength test has been run at the exact front-yard install spot, and the
     connectivity path is chosen on that evidence — home WiFi or LTE dongle (CD-04a resolved).

  4. `voice/my-project/` is either deleted from the repo or documented in the README with a stated
     reason to keep it; the repo has exactly one authoritative implementation path.

  5. A hard spend ceiling with budget alerting is active on the OpenAI account, so no unattended run
     can produce a surprise bill.
**Plans**: 10 plans across 5 waves

Plans:
**Wave 1**

- [ ] 01-01-PLAN.md — Evidence tree, verify.sh assertion harness, root README, survey-protocol template (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 01-02-PLAN.md — Credential inventory of the orphaned .env and Realtime pricing re-verification (wave 2)
- [ ] 01-03-PLAN.md — Ethernet route scoping, install-spot marking, outlet inspection, branch selection (wave 2)
- [ ] 01-04-PLAN.md — Pi-5-versus-laptop compute comparison and time-boxed owner decision (wave 2)
- [ ] 01-05-PLAN.md — Enclosure, phone, post hardware and weatherproofing sundries procurement (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 01-06-PLAN.md — OpenAI project-scoped hard spend ceiling, alerts, and browser-key revocation (wave 3)
- [ ] 01-07-PLAN.md — Site-survey measurement, connectivity decision, and cabling or dongle order (wave 3)
- [ ] 01-08-PLAN.md — Compute and electronics procurement against the plan 04 decision (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 01-09-PLAN.md — Delete voice/, gated on the key revocation record (wave 4)

**Wave 5** *(blocked on Wave 4 completion)*

- [ ] 01-10-PLAN.md — Budget reconciliation, phase gate run, STATE.md and ROADMAP closeout (wave 5)

**Note on success criterion 1**: superseded by CONTEXT.md D-01. Plan 01 rewrites it during execution
to the post-mounted outdoor cabinet form factor. Research verified the cited mahogany booth at
$2,195, 200 lbs, and rated "For Indoor or Covered Use Only".

### Phase 2: Headless Session Core

**Goal**: The complete Santa conversation — pick up, greeting, conversation, wrap-up, hang-up — runs
end to end on a bench Raspberry Pi through a real handset, with no browser and no screen anywhere in
the loop.
**Depends on**: Phase 1
**Requirements**: SESS-01, SESS-02, SESS-03, SESS-04, SESS-05, SESS-06, SESS-07, EXP-01, EXP-02, OPS-02
**Success Criteria** (what must be TRUE):

  1. Closing the microswitch by hand starts a session on the Pi and opening it ends the session
     immediately, with audio flowing both ways through the USB adapter — no browser, no
     `getUserMedia`, no screen.

  2. Santa greets, asks the child's name, uses that name throughout, talks warmly about Christmas
     wishes, redirects off-topic questions back to Christmas themes, and closes with a positive
     values-based send-off.

  3. A session that runs long is wrapped up in spoken words before the 5-minute cap rather than cut
     off, and a session that goes quiet gets exactly one "still there?" prompt before Santa says a
     brief goodbye and hangs up.

  4. Measured turn latency from the child ceasing to speak to Santa's first audio is under 2 seconds
     at p95 across a run of at least 20 turns.

  5. After any ending — hang-up, timeout, silence, error — the next pickup starts completely fresh:
     no name, no timers, no leftover connection, and a second concurrent session is impossible.

  6. Nothing in the running system writes audio or transcript text to disk or to any log stream,
     including debug output of Realtime data-channel events, and the API key exists only in the
     device environment.
**Plans**: TBD

**Decision forced here**: WebRTC vs WebSocket transport for the Realtime API on the Pi. The POC's
browser WebRTC path has no free headless equivalent; settle this before writing the transport layer.

**Scoping note**: Only `poc/server.py`'s token-broker role and the `SANTA_INSTRUCTIONS` persona string
transfer directly from the POC. Transport, audio I/O, the 300s cap, the 255s wrap nudge, the 15s/28s
silence ladder, LED state and `end_call` teardown all need headless re-implementation. This is the
largest phase in the project — plan it accordingly.

### Phase 3: Physical Build & Hardware Integration

**Goal**: The session core moves out of the bench rig and into the real booth — real handset, real
cradle switch, real LEDs, sealed against weather and ready to sit outside in the cold.
**Depends on**: Phase 2 (and delivery of Phase 1 orders)
**Requirements**: HW-02, HW-03, HW-04, HW-05, EXP-05
**Success Criteria** (what must be TRUE):

  1. Lifting the real handset from the real cradle starts a session and replacing it ends one, every
     time, with no bounce-induced double-triggers or phantom sessions across 20 consecutive lifts.

  2. A person speaking into the handset is understood, and Santa's voice comes out of the handset
     earpiece clearly enough for a child to follow without straining.

  3. The status LED reads green during an active session, amber when idle and ready, and off when the
     system is off — visible through the internal panel from outside the booth.

  4. The Pi and all electronics are sealed inside the booth, the handset cord entry at the cradle is
     sealed, and the door latches shut against wind (CD-04b resolved).

  5. The assembled unit runs a complete conversation after a cold soak at holiday-season temperatures
     (20°F–50°F range).
**Plans**: TBD

### Phase 4: Safety Guardrail & Verification

**Goal**: "Zero inappropriate content delivered to a child" stops being an aspiration in a concept
document and becomes a claim backed by a decided mechanism and a test run that passed.
**Depends on**: Phase 2
**Requirements**: SAFE-01, SAFE-02, SAFE-03
**Success Criteria** (what must be TRUE):

  1. The detection mechanism is decided and written down — prompt-based in-LLM judgement, a separate
     classifier, or both in layers — with the reasoning recorded (CD-02 resolved).

  2. Saying something vulgar to the handset produces exactly "That isn't very nice. I'll have to say
     goodbye for now — Ho ho ho." followed by immediate termination, with no further conversational
     turns and no negotiation.

  3. A written adversarial test corpus exists with a stated pass bar, covering profanity, sexual
     content, violence, prompt injection ("ignore your instructions"), and children pushing
     boundaries in the ordinary ways children do.

  4. The corpus has been executed against the real installed system and passed, with the result and
     date recorded — the criterion is not resting on prompt text alone.

  5. Early terminations are counted in a way that will show up in the season's traffic figures.

**Plans**: TBD

**Escalation note**: The source PRD rates this Medium priority. That understates it — this gates a
zero-tolerance criterion for an unattended installation used by unsupervised children, with no adult
in the loop. It is treated as a first-class phase here for that reason.

### Phase 5: Scheduling, Admin Control & System States

**Goal**: The owner decides when Santa is awake, changes it from their phone in seconds, and the box
behaves correctly in all three states — inviting when on, resting when off, talking when in use.
**Depends on**: Phase 2
**Requirements**: ADMIN-01, ADMIN-02, ADMIN-03, ADMIN-04, ADMIN-05, ADMIN-06, EXP-03, EXP-04
**Success Criteria** (what must be TRUE):

  1. From a phone on the home network, the owner reaches all five screens — Dashboard, Schedule
     Editor, Override Panel, Session Log, System Health — with the Dashboard showing current ON/OFF
     status, sessions today, and the next schedule change.

  2. Editing a day's ON/OFF window in the UI changes the box's behavior without restarting anything,
     and the whole round trip from phone in hand to change applied takes under 30 seconds.

  3. A PIN-protected Force ON or Force OFF takes effect within 5 seconds, overrides the schedule,
     and expires on its own timer or on manual clear.

  4. During scheduled hours with the handset down, soft Christmas music plays and the light blinks
     invitingly (CD-04c resolved); outside those hours, picking up plays the pre-recorded "Santa is
     resting" message with the light off and zero outbound API calls.

  5. The Session Log lists today's sessions by time, duration and completion status, and contains no
     audio and no transcript text anywhere; traffic figures show sessions today/week/season, a
     busiest-hours heatmap, average duration, and early-termination count.
**Plans**: TBD
**UI hint**: yes

**Decision surfaced here**: CD-03, admin UI and observability hosting — on the Pi itself or a separate
home server. Surface the tradeoff while building the admin service; settle it in Phase 6 when the
observability stack lands and the Pi's real CPU and thermal headroom are measurable.

### Phase 6: Observability & Unattended Operations

**Goal**: The box reports its own health in a form the owner can read from the couch, alerts when
something is actually wrong, and recovers from the ordinary outdoor failures — power blips, network
drops, crashes — without anyone walking outside.
**Depends on**: Phase 5
**Requirements**: OBS-01, OBS-02, OBS-03, OBS-04, OPS-04
**Success Criteria** (what must be TRUE):

  1. A Prometheus endpoint serves the full metric contract in REQUIREMENTS.md — session counts and
     duration histogram, total turn latency, Realtime session/response counts, billable audio
     seconds, typed API errors, connection drops, hook events, schedule state and override state,
     plus node_exporter system metrics.

  2. Grafana dashboards render all of it, and all five alerts fire on their conditions — API failure
     spike, turn latency p95 above **2s**, device offline, session stuck, Pi above 85°C.

  3. The owner can diagnose an outage entirely from Grafana and the admin UI, without SSH-ing into
     the device.

  4. Structured JSON session logs rotate daily and retain 7 days, carrying session ID, duration,
     states visited and errors — and a search of the device finds no audio file and no transcript
     text anywhere.

  5. Pulling the power and restoring it brings the box back to correct scheduled behavior with no
     manual intervention; the same is true after a network drop and after a forced crash of the
     session manager.
**Plans**: TBD

**Decision settled here**: CD-03. Measure the Pi's actual CPU and thermal headroom with the session
manager, admin service and metrics stack all running in a cold sealed enclosure, then decide whether
Grafana and Prometheus stay on the Pi or move to a home server. An observability outage must not be
able to take the phone down with it.

### Phase 7: Outdoor Install & Season Readiness

**Goal**: The booth is standing in the front yard, powered and connected, and a child who has never
seen it before can walk up and have a complete Santa conversation with nobody helping.
**Depends on**: Phase 3, Phase 4, Phase 6
**Requirements**: HW-07, EXP-06
**Success Criteria** (what must be TRUE):

  1. The booth is installed in the front yard, powered from the outdoor outlet through a weatherproof
     cord, and holds power and connectivity through a full scheduled day with no dropouts.

  2. A dress rehearsal runs a full scheduled day end to end — attract state, real conversations, the
     OFF-hours resting message at the boundary — and the metrics and session log afterward show what
     actually happened.

  3. A child who has not been coached walks up, picks up the handset, and completes a conversation
     with zero adult intervention and zero setup.

  4. The Phase 4 safety corpus has been re-run against the final installed system and passed.
  5. Signage or decoration makes it obvious what the box is and that it is meant to be picked up
     (CD-04d resolved).
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Procurement, Site Survey & Repo Cleanup | 0/10 | Planned | - |
| 2. Headless Session Core | 0/TBD | Not started | - |
| 3. Physical Build & Hardware Integration | 0/TBD | Not started | - |
| 4. Safety Guardrail & Verification | 0/TBD | Not started | - |
| 5. Scheduling, Admin Control & System States | 0/TBD | Not started | - |
| 6. Observability & Unattended Operations | 0/TBD | Not started | - |
| 7. Outdoor Install & Season Readiness | 0/TBD | Not started | - |

## Coverage

All 37 v1 requirements map to exactly one phase. No orphans, no duplicates.
See `.planning/REQUIREMENTS.md` Traceability.

**Note on Phase 6 and UI**: Phase 6 builds Grafana dashboards, which are provisioned configuration in
a third-party tool rather than a designed UI surface. Only Phase 5 carries a UI hint.
