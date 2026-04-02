# Pre-PRD: "Call Santa" — Neighborhood Phone Installation
**Status:** Pre-PRD / Concept Definition  
**Last Updated:** 2026-03-30 (rev 2)  
**Author:** TBD  

---

## 1. Concept Summary

An outdoor, unattended interactive installation placed in front of a home during the holiday season. Neighborhood children walk up, pick up a vintage-style telephone handset, and are connected directly to "Santa Claus" — a real-time AI voice agent. Santa greets them by name (after asking), engages in warm holiday conversation, asks what they'd like for Christmas, and closes with an encouraging message.

---

## 2. Target Experience

### User Journey
```
[IDLE STATE]
  Soft Christmas music plays / light blinks invitingly
  ↓
[CHILD PICKS UP HANDSET]
  Session begins
  Santa: "Ho ho ho! You've reached the North Pole! Who do I have the pleasure of speaking with today?"
  ↓
[CHILD GIVES NAME]
  Santa uses their name throughout the conversation
  Santa: "What a wonderful name! Now [Name], have you been good this year?"
  ↓
[CONVERSATION]
  Santa asks what they want for Christmas
  Santa listens, responds warmly, shows excitement about their wishes
  ↓
[CLOSING MESSAGE]
  Santa delivers an encouraging, values-based send-off
  E.g. "Keep being kind to others and a wonderful friend — that's what makes Christmas truly special."
  ↓
[CHILD HANGS UP]
  Session ends → reset to IDLE
```

### System OFF State (Outside Scheduled Hours)
```
[CHILD PICKS UP HANDSET while system is OFF]
  Indicator light is off (no attract state)
  Pre-recorded audio plays: "Ho ho ho! Santa is resting right now.
  Come back and call me soon — I can't wait to hear from you!"
  Handset goes silent → child hangs up
  No session is started, no API calls made
```

### Key Experience Qualities
- **Magical**: Santa feels present and real, not robotic
- **Warm and safe**: Content is always age-appropriate and kind
- **Snappy**: Low latency — long pauses break immersion for kids
- **Self-contained**: No parent setup required; any child can walk up

---

## 3. Deployment Context

| Attribute | Detail |
|---|---|
| Location | Outdoor, front of home |
| Audience | Neighborhood children (unattended, self-service) |
| Power | Outdoor power outlet available |
| Connectivity | WiFi (primary) or LTE dongle (fallback — TBD) |
| Season | Christmas / holiday season |
| Supervision | None — fully unattended |

---

## 4. Session Rules

| Rule | Detail |
|---|---|
| Max session length | 5 minutes — Santa gracefully wraps up and says goodbye |
| Inactivity timeout | ~15 seconds of silence → Santa prompts once, then closes session |
| Vulgar / inappropriate language | Santa responds: *"That isn't very nice. I'll have to say goodbye for now — Ho ho ho."* → session ends immediately |
| Session reset | On hang-up or session end → return to IDLE state, clean all session state |
| Concurrent sessions | 1 (single handset) |

---

## 5. System Architecture

### 5.1 Voice Pipeline

```
Handset mic → STT → LLM (Santa Agent) → TTS → Handset speaker
```

**Option A — OpenAI Realtime API**
- Single API handles STT + LLM + TTS in one low-latency loop
- Easiest to implement, lowest latency
- Less control over voice character

**Option B — Modular Stack**
- STT: Whisper (local on-device or API)
- LLM: Claude (Anthropic API) with Santa system prompt
- TTS: ElevenLabs — custom "Santa" voice with warmth and depth
- More control, higher quality voice, slightly higher latency and complexity

> **Recommendation:** Prototype with Option A. Switch to Option B if voice quality is unsatisfactory.

---

### 5.2 Santa AI Agent

**System Prompt Design Goals:**
- Persona: Jolly, warm, patient, age-appropriate
- Always refers to the child by name after learning it
- Stays on topic (Christmas, kindness, family, gifts)
- Deflects off-topic questions gently back to Christmas themes
- Closes every session with a positive, values-based message
- Hard guardrail: detects vulgarity → deliver closing line → terminate session

**Conversation Flow States:**
1. `GREETING` → Ask for name
2. `ENGAGED` → Warm conversation, ask about Christmas wishes
3. `CLOSING` → Encouraging send-off message
4. `TERMINATED` → Inappropriate language detected, graceful exit

---

### 5.3 Hardware — Reference Design

A real-world example of this concept has been identified and used as the target design reference.

**Enclosure: British Red Telephone Box Prop**
- A wood/MDF British-style red phone box sold as a Christmas display prop
- Provides full weatherproofing for the internal electronics
- Aesthetic is immediately recognizable and on-brand for the experience
- Search terms: *"red British telephone box Christmas prop"*, *"red phone booth outdoor Christmas decor"*
- Likely flat-pack or pre-assembled; may need minor sealing for moisture protection

**Handset: Red Corded Novelty Handset**
- Standard red analog-style handset with coiled cord, mounted inside the booth
- Hook/cradle mounted to the booth wall — lifting the handset is the session trigger
- Search terms: *"red retro telephone handset prop"*, *"novelty telephone handset corded"*
- Hook switch wired to Raspberry Pi GPIO pin for off-hook/on-hook detection

**Internal Panel**
- A custom-printed acrylic or foamboard "North Pole" facade panel mounts inside the booth
- Houses the Raspberry Pi, status LEDs, speaker, and USB audio adapter behind branding
- LEDs visible through panel: recommend 3-state indicator (green = active, amber = idle, off = system off)

**Optional: Camera Mount**
- Reference design includes a small wide-angle camera above the booth door
- Useful for owner's physical traffic monitoring (maps to Section 6.5)
- Could feed a simple local MJPEG stream viewable in the admin UI
- Not required for v1 but worth roughing in a mount point during construction

**Raspberry Pi Role:**
- GPIO pin monitors hook switch (off-hook → session start, on-hook → session end)
- USB audio adapter handles handset mic and speaker I/O
- Runs session manager, admin web server, and Prometheus exporter
- Controls status LEDs via GPIO
- Handles WiFi connectivity (LTE dongle as fallback TBD)

**Weatherproofing Requirements:**
- Pi and electronics housed inside sealed booth enclosure
- Handset cradle sealed around entry point for cord
- Operating temp range: 20°F–50°F typical for holiday season
- Booth door latch to prevent wind from swinging open

---

### 5.4 Session Manager (Software)

Core process running on device:

```
loop:
  wait for OFF-HOOK signal
  → initialize session (start timer, open audio stream)
  → begin voice pipeline
  → monitor: 
      - vulgarity detection → terminate
      - 5-min timer → graceful close
      - inactivity timeout → prompt or close
      - ON-HOOK signal → end session
  → teardown session, reset state
  → return to IDLE
```

---

## 6. Admin Control & Scheduling

### 6.1 Overview

The owner controls system availability via a **web-based admin UI** accessible from any browser on the local network (phone or desktop). The UI writes schedule config to a file on the device, which the session manager reads to determine active/inactive state. A PIN-protected override allows forcing the system ON or OFF outside of the defined schedule.

---

### 6.2 Schedule Configuration

**Default schedule (example):**
```
MON–FRI:  09:00–21:00  (ON)
SAT–SUN:  09:00–21:00  (ON)
Outside these windows: OFF
```

The admin UI allows:
- Setting per-day ON/OFF windows (e.g. different hours on weekends)
- Enabling/disabling specific days entirely
- Viewing the current active/inactive state at a glance

**Config file format (written by UI, read by session manager):**
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

---

### 6.3 PIN-Protected Override

The admin UI provides a **Force ON / Force OFF** toggle, protected by a PIN. This allows the owner to:
- Start the system early for a special event
- Shut it down immediately if there's an issue outside
- Set a time-limited override (e.g. "Force ON for 2 hours")

**Override behavior:**
| Override State | Behavior |
|---|---|
| Force ON | System active regardless of schedule |
| Force OFF | System inactive regardless of schedule |
| None (default) | Schedule governs |

Override expires at a set time or can be manually cleared. PIN is set during initial device setup; stored hashed on device.

---

### 6.4 Admin UI — Key Screens

| Screen | Purpose |
|---|---|
| **Dashboard** | Current status (ON/OFF), active sessions today, next schedule change |
| **Schedule Editor** | Per-day time windows, enable/disable days |
| **Override Panel** | Force ON/OFF with PIN, set expiry |
| **Session Log** | Today's sessions: time, duration, completion status (no audio/transcripts) |
| **System Health** | Link to Grafana dashboard, last heartbeat, API error count |

---

### 6.5 Traffic Monitoring (Digital + Physical)

The admin UI doubles as a lightweight **traffic dashboard** to help the owner monitor neighborhood usage:

**Digital metrics surfaced in UI:**
- Sessions today / this week / total season
- Busiest hours heatmap (hour of day × day of week)
- Average session duration
- Early terminations (vulgarity flag count)
- Peak concurrent wait indicator (future: queue light outside)

**Physical awareness hooks:**
- Grafana alert if sessions/hour exceeds a threshold (e.g. >10/hr) → owner knows it's busy outside
- Optional: admin UI shows a "🔴 Busy right now" indicator when a session is active

---

## 7. Observability Stack (Grafana / Prometheus)

**Philosophy:** Open source, free, self-hosted. Lightweight enough to run alongside the session manager on the Pi or on a home server.

### Stack
| Component | Tool | Purpose |
|---|---|---|
| Metrics collection | Prometheus | Scrapes metrics from the session manager |
| Dashboards | Grafana | Visualizes session activity, API latency, errors |
| Alerting | Grafana Alerting (built-in) | Notifies on failures or anomalies |

### Key Metrics to Instrument

**Session Metrics**
- `santa_sessions_total` — total sessions started
- `santa_sessions_completed` — sessions ended normally (hang-up or timeout)
- `santa_sessions_terminated_early` — sessions ended due to vulgarity
- `santa_session_duration_seconds` — histogram of session lengths
- `santa_idle_duration_seconds` — time between sessions

**Voice Pipeline Metrics**
- `santa_stt_latency_ms` — speech-to-text round-trip time
- `santa_llm_latency_ms` — LLM response time
- `santa_tts_latency_ms` — text-to-speech time
- `santa_total_turn_latency_ms` — full turn latency (child speaks → Santa responds)

**API / Error Metrics**
- `santa_api_errors_total{service="stt|llm|tts"}` — API failures by service
- `santa_api_retries_total` — retry count
- `santa_hook_events_total{type="pickup|hangup"}` — hardware events

**System Metrics (via node_exporter)**
- CPU, memory, temperature (Pi thermals matter outdoors in the cold)
- WiFi signal strength / connectivity

### Alerts to Configure
| Alert | Condition | Severity |
|---|---|---|
| API failure spike | >3 errors in 5 min | Critical |
| High turn latency | p95 turn latency > 3s | Warning |
| Device offline | No metrics for 5 min | Critical |
| Session stuck | Session open > 6 min | Warning |
| High CPU/temp | Pi CPU > 85°C | Warning |

### Logging
- Structured JSON logs per session: session ID, duration, states visited, any errors
- **No audio or transcripts stored** (children's privacy)
- Logs rotated daily, retained 7 days

---

Also add two new admin-specific metrics to the observability stack:
- `santa_schedule_state{state="on|off|override"}` — current system state
- `santa_override_active` — boolean, 1 when a PIN override is in effect

---

## 8. Open Questions / TBD

| # | Question | Priority |
|---|---|---|
| 1 | Source red British phone box prop (wood/MDF, outdoor-suitable) | High |
| 2 | Source red corded novelty handset with hook switch access | High |
| 2 | Voice pipeline: OpenAI Realtime vs. modular (Claude + ElevenLabs) | High |
| 3 | Connectivity: home WiFi range sufficient, or need LTE dongle? | Medium |
| 4 | Vulgarity detection: in-LLM (prompt-based) vs. separate classifier | Medium |
| 5 | Weatherproofing solution for handset | Medium |
| 6 | Attract state: Christmas music source / speaker setup | Low |
| 7 | Physical signage / decoration around the installation | Low |
| 8 | Admin UI hosting: run on Pi itself (Flask/FastAPI) or separate home server? | Medium |
| 9 | PIN complexity / reset mechanism if forgotten | Low |

---

## 9. Out of Scope (v1)

- Multi-language support
- Recording or replaying calls
- Multiple simultaneous callers
- Camera / video component
- Remote (internet-facing) admin access — local network only

---

## 10. Success Criteria

- A child can walk up, pick up the phone, and have a complete magical Santa conversation with no adult intervention
- Turn latency feels natural (target: < 2 seconds p95)
- Zero inappropriate content delivered to a child
- Owner can see system health in Grafana without SSH-ing into the device
- Owner can update the schedule and toggle overrides from their phone in under 30 seconds
- System correctly enters OFF state (light off, Santa resting message) outside scheduled hours
- PIN override activates/deactivates within 5 seconds of submission

---

## 11. Hardware Shopping List

### 1. Phone Booth Enclosure
The star of the show. Real mahogany wood is strongly preferred over MDF for outdoor durability. Add weatherproof sealant to joints and silicone bead around glass panes before outdoor deployment.

| Option | Link | Est. Cost |
|---|---|---|
| The King's Bay Full-Size Mahogany Booth (ships assembled) | [thekingsbay.com](https://thekingsbay.com/product/red-british-wood-telephone-booth-replica-like-old-cast-iron-style/) | ~$600–800 |
| Same seller, eBay (often cheaper) | [ebay.com/itm/401339285238](https://www.ebay.com/itm/401339285238) | ~$500–700 |

---

### 2. Red Handset / Telephone
A full corded phone with a working cradle is easier to work with than a standalone handset — the cradle already has a physical hook switch you can tap into with two wires.

| Option | Link | Est. Cost |
|---|---|---|
| ECVISION 1960s Style Rotary Retro Phone (Red) — full phone + working cradle hook switch | [amazon.com](https://www.amazon.com/ECVISION-1960s-Rotary-fashioned-Telephone/dp/B00A8BOTWQ) | ~$35 |
| Opis Technology 60s Micro Retro Handset (Red, 3.5mm) — handset only, plugs directly into USB audio adapter | [amazon.com](https://www.amazon.com/Opis-Technology-60s-Micro-red/dp/B0087PQGXU) | ~$30 |

> 💡 Option 1 (full rotary phone) is recommended — cradle and hook switch are already built in.

---

### 3. Raspberry Pi 5 (Brain)
The Pi 5 handles the voice pipeline, session manager, admin web server, GPIO, and Prometheus exporter. 8GB RAM is the sweet spot.

| Option | Link | Est. Cost |
|---|---|---|
| CanaKit Raspberry Pi 5 Starter PRO Kit (8GB, 128GB SD, case, fan, power supply) | [amazon.com](https://www.amazon.com/CanaKit-Raspberry-Starter-Kit-PRO/dp/B0CRSNCJ6Y) | ~$130 |
| Raspberry Pi 5 8GB board only | [amazon.com](https://www.amazon.com/Raspberry-Pi-Quad-core-Cortex-A76-Processor/dp/B0CTQ3BQLS) | ~$80 |
| Official Raspberry Pi 5 page | [raspberrypi.com](https://www.raspberrypi.com/products/raspberry-pi-5/) | — |

---

### 4. USB Audio Adapter (Mic + Speaker)
The Pi 5 has no built-in audio jack. A USB adapter handles both mic input (from handset) and speaker output (to handset earpiece). Driverless/plug-and-play is essential.

| Option | Link | Est. Cost |
|---|---|---|
| Plugable USB Audio Adapter (3.5mm mic + headphone, Pi OS compatible) | [amazon.com](https://www.amazon.com/Plugable-Headphone-Microphone-Aluminum-Compatible/dp/B00NMXY2MO) | ~$12 |
| KiWiBiRD USB External Sound Card (Raspberry Pi compatible) | [amazon.com](https://www.amazon.com/Compatible-Headphone-Microphone-Converter-Raspberry/dp/B09MGD6ZQL) | ~$10 |

---

### 5. Hook Switch / Microswitch (Cradle Sensor)
A simple normally-closed lever-arm microswitch mounted under the handset cradle wires to a GPIO pin — this is the session start/stop trigger.

| Item | Link | Est. Cost |
|---|---|---|
| Micro limit switch kit (normally closed, lever arm) — search "micro limit switch normally closed" | [amazon.com](https://www.amazon.com/s?k=micro+limit+switch+normally+closed) | ~$10 (20-pack) |
| Breadboard + jumper wire kit (for GPIO wiring) | [amazon.com](https://www.amazon.com/s?k=breadboard+jumper+wire+kit+raspberry+pi) | ~$10 |

---

### 6. Status LEDs
Mounted on the internal "North Pole" panel, visible from outside the booth. 3-state: green = active session, amber = idle/ready, off = system off.

| Item | Link | Est. Cost |
|---|---|---|
| Elegoo 5mm LED assortment kit (multicolor, includes resistors) | [amazon.com](https://www.amazon.com/s?k=elegoo+5mm+led+assortment+kit) | ~$8 |

---

### 7. Optional: Outdoor Camera (Traffic Monitoring)
Mounts above the booth door, mirrors the reference design. Enables remote visual monitoring of foot traffic, maps to admin UI Section 6.5.

| Option | Link | Est. Cost |
|---|---|---|
| Blink Outdoor 4 (1-cam, battery powered, no wiring needed) | [amazon.com](https://www.amazon.com/s?k=blink+outdoor+4+1+camera) | ~$70 |
| Blink Mini 2K+ with Weather-Resistant Adapter (plug-in, compact) | [amazon.com](https://www.amazon.com/s?k=blink+mini+2k+plus) | ~$50 |

---

### 8. Miscellaneous / Supporting Components

| Item | Link | Est. Cost |
|---|---|---|
| Weatherproof outdoor extension cord | [amazon.com](https://www.amazon.com/s?k=weatherproof+outdoor+extension+cord) | ~$20 |
| Clear silicone sealant (booth weatherproofing) | [amazon.com](https://www.amazon.com/s?k=clear+silicone+sealant+outdoor) | ~$8 |
| Short 3.5mm audio cables (handset to USB adapter) | [amazon.com](https://www.amazon.com/s?k=3.5mm+audio+cable+short) | ~$8 |
| Zip ties + velcro mounts (internal cable management) | [amazon.com](https://www.amazon.com/s?k=zip+ties+velcro+cable+management) | ~$10 |

---

### Budget Summary

| Category | Est. Cost |
|---|---|
| Phone booth | $600–800 |
| Handset / phone | $35 |
| Raspberry Pi 5 kit | $130 |
| USB audio adapter | $12 |
| Hook switch + wiring | $20 |
| Status LEDs | $8 |
| Miscellaneous | $46 |
| **Subtotal (without camera)** | **~$850–1,050** |
| Camera (optional) | $50–70 |
| **Total (with camera)** | **~$900–1,120** |

> 💡 The booth is the dominant cost. Etsy has smaller wooden phone box props in the $150–300 range if budget is a concern — though size and outdoor durability will vary.

