# Decisions (ADR-derived)

Ingest mode: new. Precedence: ADR > SPEC > PRD > DOC.

## Status: NO ADRs IN INGEST SET

The ingest set contained 1 PRD and 1 DOC. **Zero ADRs. Zero locked decisions.**

Nothing in this project's ingested documentation is binding. The pre-PRD is explicitly
`Status: Pre-PRD / Concept Definition` with `Author: TBD`, and the POC README documents
as-built behavior, not commitments.

Downstream consumers must treat every item below as **not yet decided**.

---

## Candidate decisions that need an ADR before build planning

These are recorded so the roadmapper can schedule decision work. They are NOT decisions.

### CD-01 — Voice pipeline: unified Realtime vs modular stack
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 5.1, Section 8 item "Voice pipeline", priority High)
- status: OPEN (author-labeled TBD)
- Option A: OpenAI Realtime API (single API for STT + LLM + TTS, lowest latency, less voice control)
- Option B: Modular — Whisper STT + Claude LLM + ElevenLabs TTS (more control, higher voice quality, higher latency/complexity)
- PRD stance: "Prototype with Option A. Switch to Option B if voice quality is unsatisfactory." — a recommendation, not a decision.
- Evidence postdating the PRD: a working POC on Option A exists.
  - source: /Users/cj.holler/Desktop/calling_santa/poc/README.md
- scope: entire software architecture, observability metric design, cost model
- Blocks: CD-02, CON-metric-catalog applicability

### CD-02 — Vulgarity detection: in-LLM vs separate classifier
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 8 item 4, priority Medium; Section 5.2 hard guardrail)
- status: OPEN
- Evidence postdating the PRD: POC implements in-LLM only — persona prompt plus an `end_call`
  function tool with `reason: "inappropriate"`. No independent classifier, no deterministic filter.
  - source: /Users/cj.holler/Desktop/calling_santa/poc/server.py (SANTA_TOOLS), /Users/cj.holler/Desktop/calling_santa/poc/index.html (response.function_call_arguments.done handler)
- scope: safety-critical; gates success criterion "Zero inappropriate content delivered to a child"

### CD-03 — Admin UI and observability hosting: on-Pi vs separate home server
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 8 item 8, priority Medium; Section 7 "run alongside the session manager on the Pi or on a home server")
- status: OPEN
- scope: deployment topology, Pi 5 resource budget, failure isolation

### CD-04 — Connectivity: home WiFi vs LTE dongle
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 3, Section 5.3, Section 8 item 3, priority Medium)
- status: OPEN (site survey required)
- scope: bill of materials, offline-degradation behavior

### CD-05 — Camera in or out of v1
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 5.3 "not required for v1", Section 6.5, Section 9 out of scope, Section 11 item 7 + budget line)
- status: CONTRADICTORY within the single source document — see INGEST-CONFLICTS.md WARNING
- scope: v1 feature set, admin UI surface, budget

### CD-06 — Handset hardware form: full corded phone vs standalone handset
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 11 item 2)
- status: OPEN, with a stated preference ("Option 1 (full rotary phone) is recommended — cradle and hook switch are already built in")
- scope: hook-switch wiring approach, weatherproofing

### CD-07 — Enclosure sourcing
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 11 item 1)
- status: OPEN, with stated preference for mahogany over MDF for outdoor durability; two concrete vendor options priced ~$500–800
- scope: dominant line item in the ~$850–1,050 budget

---

## Locked decisions

None. No source in the ingest set asserts a locked or accepted decision.
