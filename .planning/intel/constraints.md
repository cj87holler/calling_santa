# Constraints

No SPEC-type documents were present in the ingest set. The constraints below are extracted from
two lower-authority sources and are labelled accordingly:

- `derived-from: PRD (proposal-stage)` — SPEC-grade material embedded in the pre-PRD. Binding intent,
  but the document is concept-stage; treat as target, not contract.
- `derived-from: POC (as-built)` — proven implementation facts from working code that postdates the PRD.
  These are evidence, not requirements. Per precedence (PRD > DOC) they never override a PRD requirement.

---

## CON-schedule-schema
- type: schema
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 6.2)
- Config file written by the admin UI, read by the session manager:

```json
{
  "schedule": {
    "monday":    { "enabled": true, "start": "09:00", "end": "21:00" },
    "tuesday":   { "enabled": true, "start": "09:00", "end": "21:00" },
    "wednesday": { "enabled": true, "start": "09:00", "end": "21:00" },
    "thursday":  { "enabled": true, "start": "09:00", "end": "21:00" },
    "friday":    { "enabled": true, "start": "09:00", "end": "21:00" },
    "saturday":  { "enabled": true, "start": "09:00", "end": "21:00" },
    "sunday":    { "enabled": true, "start": "09:00", "end": "21:00" }
  },
  "override": {
    "active": false,
    "state": null,
    "expires_at": null
  }
}
```

- Default windows: MON–SUN 09:00–21:00 ON; outside these windows OFF.
- Override semantics: Force ON = active regardless of schedule; Force OFF = inactive regardless of schedule; none = schedule governs.

## CON-metric-catalog
- type: protocol
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 7 + appended rev-2 fragment)

Session metrics:
- `santa_sessions_total` — total sessions started
- `santa_sessions_completed` — sessions ended normally (hang-up or timeout)
- `santa_sessions_terminated_early` — sessions ended due to vulgarity
- `santa_session_duration_seconds` — histogram of session lengths
- `santa_idle_duration_seconds` — time between sessions

Voice pipeline metrics (CONTESTED under a unified Realtime pipeline — see INGEST-CONFLICTS.md):
- `santa_stt_latency_ms`
- `santa_llm_latency_ms`
- `santa_tts_latency_ms`
- `santa_total_turn_latency_ms` — full turn latency (child speaks → Santa responds)

API / error metrics:
- `santa_api_errors_total{service="stt|llm|tts"}` — CONTESTED label set under a unified pipeline
- `santa_api_retries_total`
- `santa_hook_events_total{type="pickup|hangup"}`

Admin metrics (from the appended rev-2 fragment below the Section 7 horizontal rule):
- `santa_schedule_state{state="on|off|override"}` — current system state
- `santa_override_active` — boolean, 1 when a PIN override is in effect

System metrics via node_exporter: CPU, memory, temperature, WiFi signal strength / connectivity.

## CON-alert-rules
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 7)
- API failure spike: > 3 errors in 5 min — Critical
- High turn latency: p95 turn latency > 3s — Warning
- Device offline: no metrics for 5 min — Critical
- Session stuck: session open > 6 min — Warning
- High CPU/temp: Pi CPU > 85°C — Warning

## CON-latency-budget
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Sections 2, 10)
- Target: turn latency < 2s p95. Long pauses break immersion for children.
- Note: the alert rule only fires above 3s p95, leaving a 2–3s unmonitored band.

## CON-privacy-and-retention
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Sections 6.4, 7, 9)
- No audio stored. No transcripts stored. Children's privacy.
- Structured JSON logs per session only: session ID, duration, states visited, errors.
- Logs rotated daily, retained 7 days.
- Recording or replaying calls is out of scope for v1.

## CON-network-exposure
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Sections 6.1, 9)
- Admin UI is local-network only. Remote / internet-facing admin access is out of scope for v1.
- PIN stored hashed on device.

## CON-concurrency
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 4)
- Exactly 1 concurrent session (single handset).

## CON-environmental
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 5.3)
- Operating temperature range: 20°F–50°F typical for the holiday season.
- Outdoor, unattended, powered from an outdoor outlet.
- Booth door latch required to prevent wind-driven swing.

## CON-hardware-budget
- type: nfr
- derived-from: PRD (proposal-stage)
- source: /Users/cj.holler/Desktop/calling_santa/call-santa-pre-prd.md (Section 11)
- Subtotal without camera: ~$850–1,050. With optional camera: ~$900–1,120.
- Booth dominates cost ($600–800 mahogany; $150–300 smaller Etsy props noted as a budget fallback).
- Named components: Raspberry Pi 5 8GB (~$80–130), USB audio adapter (~$10–12), red corded phone with cradle hook switch (~$35), normally-closed lever-arm microswitch (~$10/20-pack), 5mm LED assortment (~$8), weatherproof extension cord, silicone sealant, 3.5mm cables, cable management (~$46 combined).

---

## As-built constraints from the working POC

These postdate the pre-PRD (POC built after 2026-03-30) and describe proven behavior of
/Users/cj.holler/Desktop/calling_santa/poc/. They constrain reuse, not the target design.

## CON-token-broker
- type: api-contract
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/server.py, /Users/cj.holler/Desktop/calling_santa/poc/README.md
- The OpenAI API key stays server-side. The browser only ever receives an ephemeral session token.
- Mint endpoint: `POST https://api.openai.com/v1/realtime/client_secrets`, Bearer `OPENAI_API_KEY`.
- Token TTL: `expires_after: { anchor: "created_at", seconds: 600 }` (~10 minutes).
- Local server exposes `GET /token` (mints, optional `?voice=` A/B override validated against an allow-list) and `GET /` (serves the client page).

## CON-realtime-session-config
- type: api-contract
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/server.py
- `session.type`: `realtime`; `output_modalities`: `["audio"]`
- Model: `gpt-realtime` default (`gpt-realtime-2` selectable via `SANTA_MODEL`)
- Voice: `ash` default; allow-list includes cedar, ballad, marin, verse, coral, alloy, echo, sage, shimmer (`SANTA_VOICE`)
- Input transcription: `gpt-4o-transcribe`, language `en`
- Turn detection: `server_vad`, threshold 0.5, prefix_padding_ms 300, silence_duration_ms 700 (deliberately generous so a child's pause does not cut them off), create_response true, interrupt_response true
- Persona and guardrails live in the `SANTA_INSTRUCTIONS` string in server.py

## CON-end-call-tool
- type: api-contract
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/server.py (SANTA_TOOLS), /Users/cj.holler/Desktop/calling_santa/poc/index.html
- Single function tool `end_call(reason)` with `reason` enum: `goodbye` | `inappropriate` | `no_response`.
- Contract: the model must speak its goodbye out loud in the same turn, then call the tool. The client waits ~2.6s after `response.done` before tearing down so the spoken goodbye completes.
- This is the sole mechanism by which the vulgarity guardrail terminates a call in the POC.

## CON-realtime-transport
- type: protocol
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/index.html
- Browser WebRTC: `RTCPeerConnection` + `getUserMedia({audio:true})`, SDP offer POSTed to `https://api.openai.com/v1/realtime/calls` with `Content-Type: application/sdp` and `Authorization: Bearer <ephemeral>`.
- A data channel carries events: `conversation.item.input_audio_transcription.delta|completed`, `response.output_audio_transcript.delta|done`, `response.created`, `response.function_call_arguments.done`, `response.done`.
- Mic capture works on `localhost` without HTTPS. Requires a modern browser (Chrome/Safari/Edge).
- IMPLICATION: all session control lives in browser JavaScript. The Pi target has no browser or handset UI; this transport and its control loop must be re-hosted headlessly.

## CON-poc-timers
- type: nfr
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/index.html
- `MAX_SECONDS` = 300 (5-minute hard cap, sourced from the PRD)
- `WRAP_NUDGE_AT` = 255 (~4:15 — hidden system nudge telling Santa to begin his goodbye)
- `SILENCE_CHECK_AT` = 15s of dead air → Santa checks "still there?"
- `SILENCE_HANGUP_AT` = 28s of dead air → Santa gives a brief goodbye and calls `end_call("no_response")`
- Timers reset on either child speech or Santa speech.
- Consistent with PRD Section 4 and a strict refinement of "~15 seconds of silence → prompt once, then close".

## CON-runtime-footprint
- type: nfr
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/README.md, server.py
- Zero third-party dependencies: Python 3 stdlib only, single HTML file.
- Env vars: `OPENAI_API_KEY` (required), `SANTA_VOICE`, `SANTA_MODEL`, `PORT` (default 8000).

## CON-cost-model
- type: nfr
- derived-from: POC (as-built)
- source: /Users/cj.holler/Desktop/calling_santa/poc/README.md
- The OpenAI Realtime API bills per minute of audio in and out. A few test calls cost cents.
- Explicit warning against leaving the system running unattended — directly relevant to an
  installation whose default schedule is 12 hours/day, 7 days/week, unattended.
