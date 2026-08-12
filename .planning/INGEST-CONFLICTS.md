## Conflict Detection Report

Mode: new (net-new bootstrap, no pre-existing .planning context)
Precedence applied: ADR > SPEC > PRD > DOC
Ingest set: 2 docs — 1 PRD, 1 DOC. Zero ADRs, zero SPECs, zero locked decisions.

### BLOCKERS (0)

No blockers. Checks run and their results:

- LOCKED-vs-LOCKED ADR contradiction: not applicable — zero ADRs in the ingest set.
- Ingest decision vs existing locked CONTEXT.md decision: not applicable — mode is `new`, no
  pre-existing .planning files.
- UNKNOWN type with low confidence: none — both classifications are high confidence
  (call-santa-pre-prd.md → PRD, poc/README.md → DOC).
- Cross-ref cycle detection: clean. Graph is poc/README.md → call-santa-pre-prd.md,
  poc/README.md → server.py, poc/README.md → index.html. Max depth 1, no back edges,
  well under the 50-hop cap.
- Contradiction of a binding architecture requirement by the as-built POC: none. The POC README
  explicitly declares booth, GPIO hook switch, scheduling/admin UI, PIN override,
  Grafana/Prometheus, weatherproofing and OFF-state recording out of its own scope. That is a
  declared scope boundary, not a contradiction of the PRD's Raspberry Pi architecture.

### WARNINGS (6)

[WARNING] Voice pipeline choice is unresolved while working code already commits to one option
  Found: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 5.1 presents Option A (OpenAI Realtime API) and Option B (Whisper + Claude + ElevenLabs) with only "Recommendation: Prototype with Option A"; Section 8 still lists "Voice pipeline: OpenAI Realtime vs. modular (Claude + ElevenLabs)" as an open question at High priority. Meanwhile /Users/cj.holler/Desktop/calling_santa/poc/README.md documents a built, working Option A implementation, and /Users/cj.holler/Desktop/calling_santa/poc/server.py hard-codes the Realtime session shape (model gpt-realtime, server_vad turn detection, end_call tool).
  Impact: The single highest-leverage architectural fork in the project has no recorded decision. A DOC (lowest precedence) cannot settle it, and synthesis will not promote a POC into a decision. Downstream planning of the agent, observability, and cost model all branch here. The PRD's own switch condition ("switch to Option B if voice quality is unsatisfactory") has no recorded evaluation result.
  → Record an ADR selecting Option A or Option B, with the voice-quality evaluation that justifies it, before routing. See .planning/intel/decisions.md CD-01.

[WARNING] Observability metric catalog presupposes a modular pipeline that Option A cannot expose
  Found: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 7 requires `santa_stt_latency_ms`, `santa_llm_latency_ms`, `santa_tts_latency_ms`, and `santa_api_errors_total{service="stt|llm|tts"}` — four metrics that assume separately observable STT, LLM and TTS stages. Section 5.1 Option A describes the OpenAI Realtime API as a "single API handles STT + LLM + TTS in one low-latency loop", and /Users/cj.holler/Desktop/calling_santa/poc/index.html confirms the as-built integration is one WebRTC session with no per-stage boundaries.
  Impact: If Option A is selected, three of the four voice-pipeline metrics and the `service` label set are unimplementable as written. Success criterion "Owner can see system health in Grafana" and the "High turn latency p95 > 3s" alert would be built against a metric contract the runtime cannot satisfy. Planning would produce tasks that cannot be completed.
  → Resolve alongside CD-01. If Option A wins, redefine the voice-pipeline metrics around what the Realtime API actually emits (`santa_total_turn_latency_ms`, response/session events, connection errors) and drop the per-stage label set. See .planning/intel/constraints.md CON-metric-catalog.

[WARNING] Camera is simultaneously out of scope and in the v1 budget
  Found: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 9 "Out of Scope (v1)" lists "Camera / video component". The same document, Section 5.3, describes an optional wide-angle camera mount that "could feed a simple local MJPEG stream viewable in the admin UI"; Section 6.5 builds physical traffic-awareness on it; Section 11 item 7 prices two specific cameras; and the Budget Summary publishes a "Total (with camera) ~$900–1,120" line.
  Impact: Intra-document contradiction with no precedence tiebreaker — both statements sit in the same PRD at the same authority level, so synthesis cannot auto-resolve it. The roadmapper would have to guess whether to plan a camera feature, an admin UI video surface, and a $50–70 line item.
  → Decide camera in-or-out for v1 and make Sections 9, 5.3, 6.5 and 11 agree. Section 5.3's "Not required for v1 but worth roughing in a mount point" is a plausible middle position (physical mount yes, software no) but is not what Section 9 says. See .planning/intel/decisions.md CD-05.

[WARNING] Vulgarity detection mechanism is undecided but gates a zero-tolerance success criterion
  Found: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 8 item 4 leaves "Vulgarity detection: in-LLM (prompt-based) vs. separate classifier" open at Medium priority, while Section 10 sets the success criterion "Zero inappropriate content delivered to a child" and Section 5.2 calls it a "Hard guardrail". The as-built POC implements the prompt-based path only: guardrails live in the `SANTA_INSTRUCTIONS` string and termination depends on the model choosing to call `end_call` with `reason: "inappropriate"` (/Users/cj.holler/Desktop/calling_santa/poc/server.py, /Users/cj.holler/Desktop/calling_santa/poc/index.html).
  Impact: A zero-tolerance safety criterion for an unattended installation used by unsupervised children currently rests on a mechanism the PRD itself has not accepted, with no deterministic backstop and no independent check. The priority label (Medium) understates the exposure relative to the success criterion it gates.
  → Decide the detection mechanism and define how "zero inappropriate content" will be verified before launch. See .planning/intel/decisions.md CD-02.

[WARNING] Admin UI and observability hosting location is undecided, and the Pi's load budget depends on it
  Found: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 8 item 8 asks "Admin UI hosting: run on Pi itself (Flask/FastAPI) or separate home server?"; Section 7 hedges identically ("Lightweight enough to run alongside the session manager on the Pi or on a home server"); yet Section 5.3 and Section 11 both assert the Pi "runs session manager, admin web server, and Prometheus exporter" as settled fact.
  Impact: Deployment topology is a structural planning input — it determines whether Grafana/Prometheus provisioning is a Pi task or a separate-host task, whether the Pi's thermal and CPU alerts (>85°C) are sized correctly for an outdoor cold-weather enclosure, and whether an observability outage takes the phone down with it.
  → Choose the topology, then reconcile Sections 5.3/7/8/11. See .planning/intel/decisions.md CD-03.

[WARNING] POC session-control logic is browser-resident and does not port to the target device
  Found: /Users/cj.holler/Desktop/calling_santa/poc/index.html holds the entire control loop in browser JavaScript — WebRTC handshake via `RTCPeerConnection` and `POST https://api.openai.com/v1/realtime/calls`, mic capture via `getUserMedia`, the 300s cap, the 255s wrap nudge, the 15s/28s silence ladder, LED state, and the `end_call` teardown. /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 5.4 places that same loop in a headless session manager on a Raspberry Pi driven by a GPIO hook switch and a USB audio adapter, with no browser and no screen.
  Impact: Not a contradiction — the POC declares hardware out of scope — but the proven code is not reusable as-is on the target. Only `server.py`'s token-broker role and the `SANTA_INSTRUCTIONS` persona transfer directly. If the roadmapper assumes the POC is "the app minus hardware", it will materially underestimate the port: transport, audio I/O, timers, guardrail teardown and state machine all need headless re-implementation.
  → Scope a "port POC control loop to headless Pi session manager" work item explicitly, and confirm whether the Realtime WebRTC transport or a WebSocket transport is used on the Pi. See .planning/intel/constraints.md CON-realtime-transport.

### INFO (11)

[INFO] No precedence-based auto-resolutions were required
  Note: With zero ADRs and zero SPECs, the PRD (/Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md) is the highest-authority source in the set and the POC README (/Users/cj.holler/Desktop/calling_santa/poc/README.md) is the lowest. No cross-tier content contradiction was found, so nothing landed in the auto-resolved bucket by precedence. Every disagreement surfaced above is either intra-document or an author-labeled open question.

[INFO] Cross-reference graph is acyclic
  Note: Three edges from /Users/cj.holler/Desktop/calling_santa/poc/README.md — to ../call-santa-pre-prd.md, server.py and index.html. The PRD has no outbound doc refs; its markdown links are all external vendor URLs (thekingsbay.com, ebay.com, amazon.com, raspberrypi.com) and its "Section 6.5" pointers are self-references. Depth 1, no cycles.

[INFO] Deduplication was performed on source_path, not on classification filenames
  Note: The classification filename suffixes (`call-santa-pre-prd-c7a41e08.json`, `README-9f3c1a7d.json`) are placeholder uniqueness tokens generated without a shell tool, not verified SHA-256 prefixes. Both files carry distinct `source_path` values; no duplicate ingestion occurred.

[INFO] POC facts postdate the PRD and are recorded as evidence, not requirements
  Note: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md is dated 2026-03-30 (rev 2); the POC was built after it. Per precedence (PRD > DOC), as-built facts — token broker shape, ~10-minute ephemeral tokens, `gpt-realtime` default model, `ash` default voice, server_vad tuning, 15s/28s silence ladder, `end_call` tool — are captured in .planning/intel/constraints.md under `derived-from: POC (as-built)` and never override a PRD requirement.

[INFO] Section 11 (rev 2) materially answers two High-priority open questions that Section 8 still lists as open
  Note: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 8 items 1 and 2 ask how to source the phone box prop and the red corded handset. Section 11 answers both with priced vendor links and stated preferences (mahogany over MDF; "Option 1 (full rotary phone) is recommended — cradle and hook switch are already built in"). Section 8 was not updated when Section 11 was added. Sourcing is de-risked; final purchase selection remains open (see .planning/intel/decisions.md CD-06, CD-07).

[INFO] Latency alerting leaves the success criterion unguarded between 2s and 3s
  Note: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 10 targets turn latency < 2s p95, but the Section 7 alert rule "High turn latency" only fires above 3s p95. A system sitting steadily at 2.5s p95 would miss its stated success criterion while never alerting. Consider aligning the warning threshold to the target.

[INFO] Section 7 contains an unmerged rev-2 fragment below its horizontal rule
  Note: The text "Also add two new admin-specific metrics to the observability stack" and its two metrics (`santa_schedule_state{state="on|off|override"}`, `santa_override_active`) sit outside the Section 7 body, after the section's closing rule. Both metrics were captured into .planning/intel/constraints.md CON-metric-catalog. The document structure should be repaired so the fragment does not get lost in the next edit.

[INFO] Section 8 open-question numbering is malformed
  Note: The Open Questions table in /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md contains ten rows numbered 1, 2, 2, 3, 4, 5, 6, 7, 8, 9 — the handset sourcing row and the voice pipeline row are both numbered "2". Any downstream reference to "open question 2" is ambiguous. Renumber before citing these in a roadmap.

[INFO] Five open questions are deferred without blocking planning
  Note: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 8 items 3 (WiFi range vs LTE dongle, Medium), 5 (handset weatherproofing, Medium), 6 (attract-state Christmas music source/speaker, Low), 7 (physical signage/decoration, Low) and 9 (PIN complexity / reset if forgotten, Low). Each is resolvable during build without changing roadmap structure. Item 3 needs a physical site range test; item 6 is the only one attached to a stated experience requirement (the IDLE attract state) and still has no defined audio source. Tracked in .planning/intel/decisions.md CD-04 and inline in .planning/intel/requirements.md.

[INFO] POC transcript display is consistent with the privacy rule, but the port must stay that way
  Note: /Users/cj.holler/Desktop/calling_santa/poc/index.html renders a live two-sided transcript and enables `gpt-4o-transcribe` input transcription; nothing is written to disk. /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md Section 7 forbids storing audio or transcripts, and Section 6.4 forbids them in the session log. No conflict today. Flagging because a headless port that adds debug logging of those same data-channel events would silently violate a hard privacy requirement. See .planning/intel/constraints.md CON-privacy-and-retention.

[INFO] Ingest coverage gap: an undocumented second codebase exists in the repo
  Note: /Users/cj.holler/Desktop/calling_santa/voice/my-project/ is tracked in git (27 files, Node/TypeScript, `@openai` packages present, plus a nested duplicate `my-project/my-project/` directory). No document in the ingest set describes it and neither ingested doc references it. It was not classified and therefore contributed nothing to synthesis. `.env` is correctly gitignored; no committed secrets were observed. Decide whether this is dead scaffolding to delete or a second implementation that needs documenting and re-ingesting.
