# Phase 1: Procurement, Site Survey & Repo Cleanup - Research

**Researched:** 2026-08-13
**Domain:** Physical procurement, RF site survey methodology, SaaS cost governance, repo hygiene
**Confidence:** MEDIUM-HIGH (repo findings HIGH; OpenAI spend controls HIGH; hardware prices HIGH but volatile; Realtime API pricing MEDIUM)

---

## Summary

This phase has one finding that outranks everything else: **the enclosure budget in the source PRD is wrong by roughly 3x, and the phase cannot succeed as written without an explicit user decision.** The King's Bay solid-mahogany full-size booth — the exact vendor and product the PRD prices at "$600–800" — is listed at **$2,195.00** (sale, marked down from $2,795.00) as of 2026-08-13, is 200 lbs, and is explicitly labeled *"For Indoor or Covered Use Only."* [VERIFIED: thekingsbay.com product page, fetched 2026-08-13]. Every other mahogany booth from that vendor is the same $2,195; a second retailer lists the identical product at $3,475.95. There is no version of "buy the mahogany booth" that lands inside the ~$850–1,050 budget. Success criteria 1 and 2 are in direct conflict and the plan must force a costed choice rather than paper over it.

The second-largest finding is that **Raspberry Pi hardware costs have moved sharply since the PRD was written.** Raspberry Pi raised prices twice — 8GB from $80 to $95 on 2025-12-01, then a further +$30 to $125 list on 2026-02-02, both driven by LPDDR4 memory scarcity from AI datacenter buildout [VERIFIED: raspberrypi.com news posts]. Street prices at official US resellers are higher still: PiShop and CanaKit both list the 8GB board at **$175**, and the CanaKit Starter Kit at **$269.95** against the PRD's assumed $130. The non-enclosure bill of materials is roughly **$433** as priced today, not the PRD's ~$251.

The third finding is a **spend-exposure asymmetry the roadmap does not yet reflect.** The hardware budget argument is over hundreds of dollars; the OpenAI Realtime bill for a 12h/day, 7-day season is plausibly **$200–550/month** at observed real-world per-minute rates. OPS-03 is therefore not a hygiene task — it is the largest single financial risk in the project, and the $5 prepaid balance the user has already funded is a real hard ceiling *today* but an accidental one that evaporates the moment credits are topped up for the season. OpenAI restored genuine hard spend limits in July 2026; that feature, not the credit balance, is the correct control [VERIFIED: developers.openai.com/api/docs/guides/spend-limits].

Finally, the repo question is settled by evidence, not judgement. `voice/my-project/` is a pre-POC Vite scaffold that predates `poc/` in git history, is referenced by nothing, contains an untouched duplicate of the Vite starter template, and — materially — ships a **standing OpenAI API key into browser JavaScript** via `import.meta.env['VITE_OPENAI_API_KEY']`, the exact pattern OPS-02 forbids. A `.env` file exists on disk in that directory right now. Delete it, and check that key.

**Primary recommendation:** Structure the plan around four independent tracks that can run in parallel, with a `checkpoint:human-decision` gate at the front of the procurement track presenting three costed enclosure options. Do not let the enclosure decision block the Pi order, the site survey, the spend ceiling, or the repo cleanup — none of those depend on it.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| **HW-01** | Booth enclosure and phone hardware ordered and received; mahogany preferred over MDF; full corded/rotary phone preferred over standalone handset. Resolves CD-06, CD-07. | `## The Enclosure Problem` (verified vendor pricing, three costed options, budget reconciliation table); `## Phone Hardware` (rotary vs. handset tradeoff, RJ9 vs. 3.5mm audio-path gotcha, hook-switch internals) |
| **HW-06** | Connectivity path chosen on the basis of a physical range test at the actual front-yard install location. Resolves CD-04a. | `## Site Survey Method` (derived bandwidth target from Realtime PCM16/24kHz, RSSI/SNR/jitter/loss thresholds, sampling protocol, exact commands, LTE equivalent with RSRP/RSRQ/SINR and data-volume sizing) |
| **OPS-01** | `voice/my-project/` deleted or documented; repo has exactly one authoritative implementation path. | `## Repo Cleanup — Evidence` (git archaeology, file-by-file contents, zero inbound references, browser-key security finding, README gap, recommended disposition) |
| **OPS-03** | Hard spend ceiling on the OpenAI account with budget alerting, before any unattended runtime. | `## OpenAI Spend Controls` (hard limit vs. alert mechanics from official docs, error codes, dashboard paths, assessment of the existing $5 balance, defense-in-depth configuration, season cost model) |
</phase_requirements>

---

## Upstream Constraints

> No `CONTEXT.md` exists for this phase — the user elected to plan without a discuss-phase pass.
> These constraints are lifted from `.planning/PROJECT.md` and `.planning/ROADMAP.md` and the planner
> must honor them identically to locked CONTEXT.md decisions.

### Locked (from PROJECT.md `<decisions>`)

- **CD-01** — Voice pipeline is the OpenAI Realtime API (Option A). No modular Whisper/Claude/ElevenLabs branch, no evaluation phase.
- **CD-05** — Camera fully out of v1. No camera, no mount point, no MJPEG stream, no admin video surface, no PRD 6.5 traffic-awareness. **Budget line removed** — the plan must not reintroduce a camera line item.
- Per-stage STT/LLM/TTS metrics are dropped as unimplementable; latency alert fires at p95 > 2s.

### Forced in this phase (must be resolved, not deferred)

- **CD-04a** — WiFi vs. LTE dongle, decided on physical range-test evidence.
- **CD-06** — Final phone purchase. Stated preference: full rotary phone (cradle and hook switch built in).
- **CD-07** — Final enclosure purchase, vendor and material. Stated preference: mahogany over MDF.
- `voice/my-project/` — delete or keep.

### Hard constraints inherited

- **Deadline** — Phase 1 complete by 2026-08-25. Live installation by ~2026-12-01. STATE.md: *"a late enclosure order is the top risk to the season."*
- **Budget** — ~$850–1,050 total hardware, camera line removed. **This research shows the constraint is not simultaneously satisfiable with the mahogany preference. See `## The Enclosure Problem`.**
- **Privacy** — no audio, no transcripts, ever. Applies to this phase only insofar as survey logs must not capture call content (they won't — no calls exist yet).
- **Environmental** — outdoor, unattended, 20°F–50°F.

### Deferred (do not research or plan here)

CD-02 (Phase 4), CD-03 (Phase 5/6), CD-04b handset weatherproofing (Phase 3), CD-04c attract music (Phase 5), CD-04d signage (Phase 7), CD-04e PIN complexity (Phase 5), WebRTC-vs-WebSocket transport (Phase 2).

---

## Project Constraints (from CLAUDE.md)

**No `./CLAUDE.md` exists in this repository** [VERIFIED: `cat CLAUDE.md` returned exit 1, 2026-08-13].
**No `.claude/skills/` or `.agents/skills/` directory exists** [VERIFIED: `ls` returned no matches].

There are therefore no project-specific coding conventions, forbidden patterns, or tooling mandates to enforce beyond the constraints in PROJECT.md above. The planner should treat the absence of a CLAUDE.md as a gap worth closing later, but not in this phase.

---

## Architectural Responsibility Map

This is a procurement and operations phase, so the "tiers" are not software layers. They are the four
independent systems this phase touches. The value of mapping them is that **none of the four blocks
any other** — they should be planned as parallel tracks, not a sequence.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Enclosure selection and purchase | Human decision (checkpoint) | External vendor | Money + aesthetics + a budget conflict only the owner can resolve. Agent cannot and must not pick. |
| Phone / Pi / electronics purchase | External vendor | Human checkout | Specs are researchable; the card swipe is human. Independent of enclosure choice. |
| Front-yard RF measurement | Physical world | Local device (laptop or Pi) | Cannot be simulated, cannot be inferred from the router's admin page. Requires a person standing in the yard. |
| Connectivity decision (WiFi vs LTE) | Recorded evidence | Human decision | Decision is mechanical *given* the measurement log — thresholds are objective. |
| OpenAI spend ceiling | Vendor dashboard (SaaS control plane) | — | Configured in a browser at platform.openai.com. Not code, not repo state. No public write API documented. |
| Repo cleanup | Local git working tree | GitHub remote | Pure `git` operation, fully agent-executable, fully verifiable. |
| Credential hygiene (found `.env`) | Local filesystem + vendor dashboard | — | Discovered during repo inspection; belongs with OPS-03 because a stray key *is* a spend-ceiling hole. |

**Planner takeaway:** four plans, not one. The enclosure checkpoint is the only long-pole item; everything else can complete while the owner is deciding.

---

## The Enclosure Problem

> This is the single most important section of this research. Read it before writing any task.

### What the PRD assumed vs. what exists

| | PRD (rev 2, 2026-03-30) | Verified 2026-08-13 |
|---|---|---|
| The King's Bay full-size mahogany booth | "~$600–800" | **$2,195.00** (sale, was $2,795.00), 3 in stock, ships in 5–10 days, 200 lbs, 89.5"H × 32"W × 29.5"D, arrives fully assembled |
| Same booth via eBay | "~$500–700 (often cheaper)" | Vendor's own site now cheaper than the third-party listings found; eBay listing 401339285238 did not resolve (request timeout) |
| Outdoor rating | *"Provides full weatherproofing for the internal electronics"* | **"For Indoor or Covered Use Only!"** — stated by both retailers |

[VERIFIED: thekingsbay.com/product/red-british-wood-telephone-booth-replica-like-old-cast-iron-style/, fetched 2026-08-13]
[VERIFIED: thekingsbay.com/product-category/english-charm/phone-booths/ — all eight booth SKUs listed; the cheapest wooden option of any colour is $2,195; aluminum versions are $2,995 and $5,995]
[VERIFIED: centerlinedynamics.com lists the identical 200 lb mahogany product at $3,475.95, also "For Indoor or Covered Use Only!"]

The PRD's price was either a stale figure or a different (much smaller) product. Every solid-wood full-size booth found in this research sits between **$2,195 and $3,476**. There is no mahogany walk-in booth at $600–800 in the current US market.

### Budget reconciliation (verified prices, 2026-08-13)

Non-enclosure bill of materials:

| Line | PRD estimate | Verified today | Source | Delta |
|------|-------------|----------------|--------|-------|
| Rotary phone (ECVISION 1960s repro, red) | $35 | **~$70** | Amazon listing B00A8BOTWQ, price surfaced via search 2026-08-13 | +$35 |
| Raspberry Pi 5 8GB — CanaKit Starter Kit | $130 | **$269.95** | canakit.com, fetched 2026-08-13 | +$140 |
| *(alt)* Pi 5 8GB board only | $80 | **$175.00** | pishop.us and canakit.com both, fetched 2026-08-13 | +$95 |
| *(alt)* Pi 5 4GB board only | — | **$110.00** | pishop.us, fetched 2026-08-13 | — |
| USB audio adapter | $12 | **$4.95** | pishop.us "USB Audio Adapter — Works with Raspberry Pi", in stock | −$7 |
| Microswitch kit + jumper wiring | $20 | ~$20 | commodity, unchanged | 0 |
| Status LEDs + resistors | $8 | ~$8 | commodity, unchanged | 0 |
| Misc (weatherproof cord, sealant, 3.5mm cables, zip ties) | $46 | ~$60 | see `## Outdoor Electrical` — cord + in-use cover + gland cost more than the PRD's line | +$14 |
| **Non-enclosure subtotal (Pi kit path)** | **$251** | **≈ $433** | | **+$182** |
| **Non-enclosure subtotal (4GB board + own PSU/SD ≈ $45)** | — | **≈ $318** | | |

**Therefore:** inside the $1,050 ceiling, the money available for an enclosure is **$617 (Pi kit path)** or **$732 (lean 4GB path)**. The mahogany booth at $2,195 is **3.0–3.6× that remaining budget**, and total spend would land at **≈ $2,630**, roughly **2.5× the stated ceiling**.

**Stated plainly, as requested: the ~$850–1,050 budget is not achievable if a solid-mahogany walk-in booth is purchased. Not close. The gap is about $1,600.**

### Three costed options — this is a human decision, not an agent one

| # | Option | All-in cost | Lead time | Satisfies HW-01 as written? | Risks |
|---|--------|------------|-----------|------------------------------|-------|
| **A** | Buy The King's Bay mahogany booth | **≈ $2,630** | Ships 5–10 days, but 200 lbs → freight/liftgate handling likely | Yes — mahogany, full booth | Budget blown 2.5×. Indoor-rated, so weatherproofing work is *still* required. 200 lbs and 7.5 ft tall in a front yard is a real wind-load and child-safety anchoring problem. Only 3 in stock. |
| **B** | Buy a cheaper full-size prop (MDF/plywood/fabric-frame), weatherproof it | **≈ $750–1,050** | Unknown — Etsy/eBay sellers, varies | No — reverses the "mahogany over MDF" preference | Pricing not verifiable from this session (Etsy/eBay/Amazon all blocked automated fetches). Outdoor durability of MDF over a wet December is the exact thing HW-01 was written to avoid. |
| **C** | Build a smaller enclosure — a waist-high or wall-mounted "Santa Call Station" kiosk in cedar/exterior ply, red-painted, phone-box styling | **≈ $600–750** (materials $250–450 + the $318–433 BOM) | Materials same-week from a big-box store | No — not a walk-in booth | Costs *build hours*, which is the scarcest resource in a 16-week part-time schedule. Aesthetic ambition is reduced. |
| — | Build a full-size K2 booth from plans | materials only, but **months of labour** | — | Partially | **Not viable.** The best-documented free plan set (BuildEazy K2) requires a circular saw, planer, router, jigsaw, angle grinder, drill press, mitre saw, fibreglass cloth, epoxy resin, hypertufa and *"months of casual work"*. Phase 3's entire hardware window is ~3 weeks. [VERIFIED: buildeazy.com/red-english-telephone-box/] |

**The functional insight the planner should surface at the checkpoint:** nothing in the requirements needs a walk-in booth. HW-01/02/03/04/05 need a weatherproof box that holds a Pi, a cradle, a handset and three LEDs, mounted at child height, that a child can walk up to. The walk-in booth is entirely an aesthetic goal — a legitimate one, but the *only* line item capable of consuming both the budget and the schedule. That tradeoff belongs in front of the owner, explicitly.

**Recommended default if the owner does not want to decide (state the reasoning, do not assume silently):** Option C. Rationale: the binding constraint on this project is the 2026-12-01 date, and Option C is the only one whose cost, lead time and outdoor-suitability are all simultaneously under the owner's control. Option A is defensible if the owner is willing to say "the booth is the point, and $2,600 is fine" — that is a perfectly reasonable answer, it just has to be said out loud and written down, because every later phase inherits it.

**Whatever is chosen, the plan must also capture:** the booth is indoor-rated even in Option A, so Phase 3's weatherproofing scope (HW-05) does not shrink. Budget sealant, a drip edge, and a raised/levelled base regardless.

---

## Phone Hardware

### The recommendation holds, but for a different reason than the PRD gives

The PRD recommends the **full rotary phone over the standalone handset** because "cradle and hook switch are already built in." That reasoning is correct and this research confirms it — but it understates a second, larger benefit and hides one real cost.

**Why the full phone still wins:**

1. **The cradle mechanism is the hard part.** A phone body gives you a moulded cradle, a hook plunger with the right travel, and a handset that physically sits in it. Fabricating a cradle that reliably actuates a microswitch — with enough travel, no rattle, and correct rest position — is fiddly woodwork that would otherwise land in Phase 3's critical path.
2. **It looks right.** A bare handset dangling in a booth reads as broken. A whole phone reads as an invitation.
3. **The hook switch is genuinely reusable.** In every documented rotary-phone-to-Pi conversion, the hook is treated as *"a simple switch"* wired to a GPIO pin that gets pulled low when the handset is on the cradle [CITED: stavros.io — "I converted a rotary phone into a meeting handset"]. Raspberry Pi forum consensus is identical: the hook switch opens when the receiver is on the hook and closes when lifted (or the inverse, depending on which contact set you tap), and it wires to a GPIO with a pull resistor.

**The cost the PRD does not mention — the audio path.**

A full retro phone connects its handset to the base with an **RJ9/RJ22 (4P4C) modular plug**, carrying a mic pair and a receiver pair at telephone levels. A USB audio adapter expects **3.5mm jacks at computer levels**. These do not connect without intervention. You must either:

- cut the handset cord and terminate the two pairs into 3.5mm plugs (or solder them onto the adapter's pads, as the documented conversion did — the author removed the 3.5mm connectors from a $1.69 USB sound card and soldered pins in their place), **or**
- buy an RJ9-to-3.5mm breakout, **or**
- replace the phone's internal handset with a 3.5mm handset (which defeats the point).

The documented conversion reports this worked without special impedance or bias-voltage handling — *"the computer recognized the sound card, and audio worked fine with the handset"* [CITED: stavros.io]. That is one data point, not a guarantee. Handset receivers are typically low-impedance and handset mics in modern reproductions are usually electret (which the CM108-class mic input biases correctly), but a carbon-mic-era original would not work.

**Planner action:** this is a Phase 3 integration risk, but it is a **Phase 1 procurement decision** because it determines what you buy. Two mitigations, both cheap:

- **Buy both.** The full rotary phone (~$70) *and* a 3.5mm handset (~$30). $30 of insurance against a hardware dead-end discovered in October. Use the rotary phone's body and cradle; if the RJ9 audio path fights back, swap the 3.5mm handset into the cradle. Total added cost is under 3% of the project budget and it removes a schedule risk entirely.
- **Buy a spare RJ9-to-3.5mm breakout / RJ9 crimp connectors and a crimper** so the cord can be re-terminated without destroying the phone on the first attempt.

**Do not buy a "USB retro handset."** Several exist and they are plug-and-play, but they enumerate as their own USB audio device and they have no cradle — you would be buying back the exact problem the full phone solves.

### Verified availability

| Item | Price | Status | Source |
|------|-------|--------|--------|
| ECVISION 1960s Style Rotary Retro Phone, red (Amazon B00A8BOTWQ) | **~$70** (PRD said $35) | Listing active | Search result, 2026-08-13. **Amazon blocks automated fetch — price must be human-confirmed at purchase.** `[ASSUMED]` |
| Alternative red rotary repros (Sangyn, Mcheeta, generic "1960s style") | not verified | Multiple active listings | Search result, 2026-08-13 `[ASSUMED]` |
| Opis Technology 60s Micro Retro Handset, red, 3.5mm (B0087PQGXU) | ~$30 per PRD | not re-verified | PRD Section 11 `[ASSUMED]` |

---

## Raspberry Pi 5 and Audio

### Pi 5 pricing has moved — twice — and the plan must reflect it

| Date | Event | 8GB list price |
|------|-------|----------------|
| 2023 launch | — | $80 |
| **2025-12-01** | Raspberry Pi announces 1GB model at $45 and memory-driven price rises: *"the recent unprecedented rise in the cost of LPDDR4 memory"* driven by *"competition from the AI infrastructure roll-out."* 2GB $50→$55, 4GB $60→$70, 8GB $80→**$95**, 16GB $120→$145. | **$95** |
| **2026-02-02** | Second rise: *"The cost of some parts has more than doubled over the last quarter."* 1GB unchanged, 2GB +$10, 4GB +$15, 8GB **+$30**, 16GB +$60. Raspberry Pi states they *"look forward to unwinding these price increases once it abates"* but anticipate continued pressure through 2026. | **$125** |
| **2026-08-13 (today)** | Official US resellers are above list: PiShop **$175**, CanaKit **$175** board-only, CanaKit Starter Kit (8GB, 128GB SD, case, fan, PSU, cables) **$269.95**. Both show in stock. Amazon third-party markups observed as high as $218 for the bare board. | street $175 |

[VERIFIED: raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/ and raspberrypi.com/news/more-memory-driven-price-rises/, both fetched 2026-08-13]
[VERIFIED: pishop.us and canakit.com product pages, fetched 2026-08-13]

**Two consequences for the plan:**

1. **Buy from an official reseller, not a third-party Amazon marketplace seller.** PiShop and CanaKit are both official Raspberry Pi resellers with stock today. Amazon marketplace pricing on this SKU is 25–75% above reseller price.
2. **8GB is a preference, not a requirement — and it costs $65.** The Pi 5 4GB is $110 vs. $175. The v1 workload is a Python session manager holding one WebSocket, a small admin web service, node_exporter, and (possibly, pending CD-03) Prometheus + Grafana. None of that is memory-bound at 4GB. **Recommendation: keep 8GB.** Reasoning: the $65 delta is small relative to the enclosure decision, CD-03 is still open and might put Grafana on this box, and running out of headroom in November on an outdoor sealed device is a far worse failure than $65. But the planner should note the 4GB option in the checkpoint so the owner sees the lever exists if Option A (mahogany) is chosen and every dollar matters.

**Pi 5 gotchas that affect what you order:**

- **No 3.5mm audio jack.** The Pi 5 removed it entirely. USB audio is mandatory, not optional. (PRD already states this correctly.)
- **Requires a 5V/5A USB-C PD supply (27W).** Undersized supplies cause brownouts and USB current-limit throttling — which would present as random audio-device dropouts, a miserable thing to debug in a cold booth in December. If buying board-only, budget ~$15 for the *official* 27W PSU specifically, not a generic charger. [VERIFIED: reseller product pages both state the 5V/5A requirement]
- **Active cooling recommended.** The starter kit includes it. In a sealed outdoor enclosure at 20–50°F, thermal is unlikely to be the problem — but the fan also prevents the *condensation-on-a-cold-board* problem from stagnant air. Buy the cooler either way.
- **Buy two microSD cards.** A corrupted card in late November with no spare is a season-ending event. ~$12 each.

### USB audio adapter — buy the boring one, and buy two

**Recommendation: the reseller-vetted adapter, at $4.95 from PiShop** — "USB Audio Adapter — Works with Raspberry Pi," in stock, described as *"Fully compatible with Raspberry Pi 5 and earlier models"* and *"tested successfully with Raspberry Pi OS."* [VERIFIED: pishop.us, fetched 2026-08-13]. A Pi reseller that sells a part branded "works with Raspberry Pi" and has tested it on Pi OS is a materially better signal than an Amazon listing that claims Linux compatibility.

**Chipset guidance:**

- **Known-good family: C-Media CM108 / CM119.** These are the default chips in nearly every cheap USB audio dongle, they are driverless via the USB Audio Class driver, and they are heavily used in the amateur-radio community on Raspberry Pi specifically because they work. Adafruit's guide identifies a compatible card by looking for *"C-Media Electronics, Inc. CM108 Audio Adapter"* or *"Texas Instruments PCM2902 Audio Codec"* in `lsusb` output. [CITED: learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/]
- **Also known-good: TI PCM2902.** Same guide.
- **UGREEN adapters work on Pi 5** — a Raspberry Pi forum thread confirms plug-and-play operation, 24-bit/96kHz, no workarounds needed. **Caveat carried by that same thread: UGREEN uses different DACs across models with the same product family name, so a good review of one SKU does not transfer to another.** [CITED: forums.raspberrypi.com/viewtopic.php?t=365923]
- **The real risk is not the chip, it's the jack layout.** Many modern adapters (including the widely-recommended UGREEN B087T5H3MQ) expose a **single combined TRRS jack** for headsets. A telephone handset gives you a separate mic pair and a separate receiver pair. You want an adapter with **two separate 3.5mm jacks — one pink mic-in, one green line-out.** Confirm this from the product photo before ordering. Getting a TRRS-only adapter means adding a splitter and a failure point.
- **Mic input is the part that historically breaks.** Some Pi tutorials for CM108 adapters cover output only and note they have no instructions for the mic port. Plan for `alsamixer` work in Phase 3 (unmuting `Mic`, enabling `Auto Gain Control` or disabling it, setting capture level) — this is normal, not a defect.

**Buy 2–3 adapters at $5 each, ideally from two different vendors/chipsets.** At this price, carrying a spare and an alternative is free insurance against discovering in Phase 3 that the mic input on your one adapter is unusable.

**Do not buy an audio HAT for v1.** A HAT (e.g. an I2S codec board) gives better audio quality and avoids USB entirely, but it costs more, occupies the GPIO header you need for the hook switch and LEDs, needs device-tree overlay configuration, and — critically — is not driverless. The requirement (HW-03) explicitly says *"driverless USB audio adapter."* Honour it. A HAT is a Phase 3 fallback if and only if USB audio quality proves unacceptable through a telephone handset.

---

## Outdoor Electrical

### Power path — this is where a code violation could quietly become a fire

| Item | Spec to buy | Why |
|------|------------|-----|
| Outdoor extension cord | **SJTW or SJEOW jacket, 12/3 or 14/3, "W" (wet-location) rated**, length measured *after* the booth position is fixed | Temporary cords must be listed for outdoor use. 16/3 "light duty holiday" cords are fine for LED strings and marginal for a continuous-duty appliance. [CITED: nassaunationalcable.com NEC rules for outdoor wiring] |
| Receptacle protection | **GFCI.** If the outdoor outlet is not already GFCI, add an in-line GFCI adapter or a GFCI extension cord. | All 15A/20A 125V outdoor receptacles require GFCI protection. [CITED: NEC 210.8 via expertce.com / nassaunationalcable.com] |
| Receptacle cover | **"In-use" / bubble cover** (weatherproof *with the plug inserted*) | NEC 406.9(B): receptacles in wet locations require an enclosure that is weatherproof *whether or not the attachment plug cap is inserted.* A flip-lid cover that only closes when empty does not satisfy this. [CITED: NEC 406.9(B)] |
| Cord-to-booth entry | **IP68 compression cable gland** (PG or M-series), sized to the cord OD, entering the enclosure from **underneath or a downward-facing face** | A gland gives a sealed, strain-relieved penetration. Entering from the top or a vertical face invites water tracking down the cord into the box. |
| Drip loop | Free, costs nothing, forgotten by everyone | Route the cord so it dips *below* the entry point before rising into the gland. Water runs off the low point instead of into the enclosure. |
| Sealant, wood joints | **Exterior polyurethane sealant** (paintable) | Polyurethane adheres to wood far better than silicone and takes paint; silicone does not accept paint and performs poorly on porous substrates. [CITED: finepowertools.com, hunker.com, siliconedepot.com — multiple concurring sources] |
| Sealant, glass/acrylic panes and exposed weather edges | **100% silicone** | Superior UV and long-term weather durability, up to ~4× the service life of polyurethane in direct sun. The professional hybrid approach — fill with polyurethane, cap the exposed bead with silicone — applies well here. [CITED: same sources] |

**Lead times:** none of the electrical items are long-lead. Cords, GFCI adapters, in-use covers and sealant are same-day big-box stock. **Cable glands are the one item plausibly not stocked locally** — order online, ~3–5 days, ~$10 for a multi-pack. Order them in Phase 1 anyway; they cost nothing and their absence would stall Phase 3.

**One thing to add that the PRD does not list — a vent, and desiccant.**

A fully sealed wooden box that heats from a Pi during the day and drops to 20°F overnight will condense water on the coldest interior surface, which will be the electronics. The correct fix is a **breather/pressure-equalisation vent** (a Gore-style vented plug, ~$5–10, or at minimum a downward-facing louvre with a bug screen) plus **silica gel desiccant packs**. This is an HW-05 (Phase 3) concern, but it is a **Phase 1 purchase** because it is easy to forget and trivially cheap. Add ~$15 to the misc line.

---

## Site Survey Method

> HW-06 is the only requirement in this phase whose evidence cannot be produced by an agent. Design
> the tasks so the human's job is mechanical: stand here, run this command, paste the output into
> this file.

### First, derive the actual target — do not survey against "does the internet work"

The OpenAI Realtime API's audio format is **PCM16 at 24,000 Hz** for input, with output as PCM or `audio/pcmu` (mu-law) [VERIFIED: developers.openai.com/api/docs/guides/realtime-conversations — input example shows `"type": "audio/pcm", "rate": 24000`; output examples show `audio/pcm` and `audio/pcmu`]. Over WebSocket, audio moves as **base64-encoded chunks** [VERIFIED: developers.openai.com/api/docs/guides/realtime-websocket].

Computed bandwidth (arithmetic, not a citation — mark as derived):

| Path | Raw | Base64 over WebSocket (+~33%) |
|------|-----|-------------------------------|
| Child → API, PCM16 @ 24 kHz mono | 24000 × 2 bytes = 384 kbps | **≈ 512 kbps sustained upstream** |
| API → Child, PCM16 @ 24 kHz mono | 384 kbps | **≈ 512 kbps sustained downstream** |
| API → Child, if `audio/pcmu` (8 kHz mu-law) | 64 kbps | ≈ 85 kbps downstream |

**Survey pass bar: ≥ 2 Mbps sustained in each direction at the install spot, with headroom.** Roughly 1 Mbps is the actual requirement in the worst (all-PCM16 WebSocket) case; 2 Mbps is the number to test against so that a shared home connection under evening load still has room.

Note for the planner: the official docs state that for server-to-server integrations, **WebSocket is the recommended transport**, while WebRTC is recommended for browsers/mobile clients [VERIFIED: developers.openai.com/api/docs/guides/realtime-websocket]. That is an input to the Phase 2 transport decision, not a Phase 1 decision — but it is the reason the survey should be sized for the uncompressed PCM16 case rather than an Opus-compressed WebRTC case.

### Thresholds to measure against

| Metric | Pass | Marginal | Fail | Basis |
|--------|------|----------|------|-------|
| WiFi RSSI | **≥ −67 dBm** | −67 to −72 dBm | < −72 dBm | −67 dBm is the long-standing industry baseline for reliable voice. The −65 to −72 dBm band is where WebRTC packet loss begins exceeding FEC correction capacity. [CITED: purple.ai WiFi signal strength guide; corroborated by NHS England Digital Wi-Fi metrics guidance] |
| WiFi SNR | **≥ 25 dB** | 20–25 dB | < 20 dB | Below 25 dB, 5 GHz links fall back from QAM256 to QAM64, halving PHY rate. [CITED: same] |
| Packet loss (to `api.openai.com`) | **< 0.5%** | 0.5–1% | > 1% | Realtime audio has no retransmission budget; loss becomes audible dropout. |
| Jitter | **< 30 ms** | 30–60 ms | > 60 ms | Conservative relative to the general VoIP guidance; the 2s p95 turn-latency target (SESS-03) leaves little slack. |
| RTT to `api.openai.com` | **< 100 ms** | 100–150 ms | > 150 ms | Network RTT is pure additive latency inside the 2s p95 budget. |
| Sustained throughput | **≥ 2 Mbps each way** | 1–2 Mbps | < 1 Mbps | Derived above. |

### Sampling protocol — what makes the result defensible rather than a one-off

A single RSSI reading is worthless. The protocol below is what makes this a *measurement* rather than an anecdote, and it is what should be written into the task:

1. **Exact spot, exact height.** Mark the install location physically (a stake, a paver). Measure at **handset height, ~48 inches**, not on the ground and not at chest height while holding a laptop overhead. RF at 4 ft differs measurably from RF at 5.5 ft.
2. **Exact orientation.** Note and hold the device orientation; record it. The Pi 5's antenna is directional enough to matter across 5–10 dB.
3. **Use the actual radio if possible.** The single best survey device is the Pi 5 itself, because its antenna is the one that will be there in December. If the Pi has not arrived, use a Linux laptop and record that the reading is a proxy — then **re-run the survey once the Pi arrives**, before Phase 3 seals it in a box. Add that as an explicit follow-up task.
4. **Three windows, ≥ 20 minutes each, at different times of day**, one of which must be a weekday evening (peak neighbourhood WiFi contention, peak ISP contention, and the actual operating hours of the installation). One quiet-Sunday-morning reading will pass and then fail in December.
5. **Log continuously, not once.** Capture a sample every 5 seconds and keep the raw series. Report min / median / p95, not the average — the p5 RSSI and the p95 jitter are what break calls.
6. **Test the failure mode you care about.** A 60-second bidirectional `iperf3` run is closer to a Realtime session than a speed-test website is.
7. **Record the weather.** Leaf cover in August is a *best case* for a signal path that has to work in December — but rain and wet foliage are worse. Note conditions so the December reality can be reasoned about.
8. **Note whether the booth material will attenuate.** Wood: minor (1–3 dB, ignorable). Metal or foil-backed: severe — if Option A's aluminium variant or any metal booth is ever considered, the antenna must be external and this survey must be redone with the box closed.

### Commands (WiFi)

```bash
# One-time setup on the survey device (Raspberry Pi OS / Debian)
sudo apt update && sudo apt install -y iw wavemon iperf3 mtr-tiny

# Interface name — Pi OS Bookworm+ uses NetworkManager; wlan0 is still typical
iw dev

# --- Instantaneous link quality ---
iw dev wlan0 link
#   → reports SSID, signal (dBm), tx bitrate. This is your RSSI.

# --- Neighbourhood scan: what else is on the channel (contention is invisible in RSSI) ---
sudo iw dev wlan0 scan dump | grep -E 'SSID|signal|freq|DS Parameter'

# --- Interactive view with a signal-over-time histogram (press F2 for the graph) ---
wavemon -i wlan0

# --- Continuous logged sampling: RSSI every 5s for 20 minutes, to CSV ---
END=$(( $(date +%s) + 1200 ))
echo "timestamp,rssi_dbm,tx_bitrate_mbps" > survey-wifi-$(date +%Y%m%d-%H%M).csv
while [ "$(date +%s)" -lt "$END" ]; do
  L=$(iw dev wlan0 link)
  RSSI=$(echo "$L" | awk '/signal:/ {print $2}')
  RATE=$(echo "$L" | awk '/tx bitrate:/ {print $3}')
  echo "$(date -Is),${RSSI:-NA},${RATE:-NA}" >> survey-wifi-*.csv
  sleep 5
done

# --- Loss + jitter to the actual endpoint, 300 probes (~5 min) ---
mtr -r -c 300 --json api.openai.com > survey-mtr-$(date +%Y%m%d-%H%M).json
# Read: Loss% and StDev on the final hop.

# --- Sustained throughput. Run iperf3 -s on a WIRED machine on the LAN first. ---
iperf3 -c <lan-server-ip> -t 60            # upstream from booth
iperf3 -c <lan-server-ip> -t 60 -R         # downstream to booth
# Pass bar: >= 2 Mbps each direction, and no zero-throughput seconds in the per-second output.
```

**Gotcha to warn the human about:** run `iperf3 -s` on a machine that is **wired** to the router. If the iperf server is itself on WiFi, you are measuring two wireless hops and the result is meaningless.

**Gotcha 2:** disable WiFi power save on the survey device before measuring, or you will record artificially poor latency: `sudo iw dev wlan0 set power_save off`. Note that this must *also* be set on the production device — Pi WiFi power save is a classic cause of intermittent multi-hundred-millisecond latency spikes on an idle-then-active connection, which is exactly this workload's profile.

### Commands (LTE fallback evaluation)

Only run this if the WiFi survey fails or is marginal. Requires purchasing a dongle first — so the plan should structure this as: survey WiFi → **if marginal or failing, that triggers the LTE dongle purchase** as a second, conditional order.

```bash
sudo apt install -y modemmanager
mmcli -L                          # list modems
mmcli -m 0                        # full modem status incl. registration, operator, tech
mmcli -m 0 --signal-setup=5       # poll extended signal info every 5 seconds
mmcli -m 0 --signal-get           # RSSI / RSRP / RSRQ / SNR per access technology
```

[CITED: mmcli usage confirmed across raspberry.tips and Raspberry Pi forum threads. Note: the specific RSRP/RSRQ/SINR field availability via `--signal-get` was **not** verified against official ModemManager documentation in this session — mark `[ASSUMED]` and confirm during execution.]

| LTE metric | Good | Marginal | Poor |
|-----------|------|----------|------|
| RSRP | ≥ −90 dBm | −90 to −105 dBm | < −110 dBm |
| RSRQ | ≥ −10 dB | −10 to −15 dB | < −15 dB |
| SINR | ≥ 15 dB | 5–15 dB | < 5 dB |

`[ASSUMED]` — these are conventional LTE quality bands from general industry practice, not verified against a cited authority in this session. They are directionally correct and adequate for a go/no-go, but should not be presented as sourced.

**Dongle selection:** buy a **4G/LTE** dongle, not 3G — 3G/UMTS networks have been shut down by major carriers in North America and Europe. Huawei MS2372h-class dongles are documented working with ModemManager on Raspberry Pi. Verify carrier band support against the carrier you intend to use before buying. [CITED: raspberry.tips LTE tutorial; Raspberry Pi forums]

**Data volume sizing — the number nobody computes until the overage bill:**

At ~3.4 MB per minute of active conversation (derived from the ~450 kbps combined figure above), a season at 30 calls/day × 4 min ≈ 120 call-minutes/day:

- **≈ 400 MB/day → ≈ 12 GB/month.**

That rules out a 1–2 GB IoT data plan. Size any LTE plan at **20 GB/month minimum** with a hard data cap, and note that using `audio/pcmu` for the output path roughly halves it. Idle/attract state should generate negligible traffic (an idle WebSocket, or no connection at all when on-hook) — confirm that in Phase 2 and re-check this estimate then.

---

## OpenAI Spend Controls

### The mechanics, verified against official documentation

OpenAI's spend controls were in flux through 2026 and training-data knowledge of them is unreliable. Current state, from the official guide:

| Control | What it actually does | Hard cap? |
|---------|----------------------|-----------|
| **Hard spend limit (organization)** | Set a monthly dollar cap at Organization limits, click "Edit spend limit," enter the amount, **toggle "Enforce a hard limit."** When crossed, requests fail. | **YES** — returns `429` with `organization_spend_limit_exceeded` |
| **Hard spend limit (project)** | Same, per-project: Project settings → Limits → "Edit spend limit" → "Enforce a hard limit." | **YES** — returns `429` with `project_spend_limit_exceeded` |
| **Spend alerts** | Email/dashboard notification at a threshold. *"Spend alerts do not enforce a cap. They remain active when you add a hard spend limit, so you can use alerts for notification before a hard limit interrupts traffic."* | **NO** — notification only |
| **Prepaid credit balance exhaustion** | When purchased credits run out, requests fail. | **YES, incidentally** — returns `credit_balance_exhausted` |
| **Usage tier limit** | OpenAI's own approved tier ceiling. | Returns `organization_usage_limit_exceeded` |

[VERIFIED: developers.openai.com/api/docs/guides/spend-limits, fetched 2026-08-13]

**Two behaviours the plan must account for:**

1. **Enforcement is not instantaneous.** The official docs state: *"Enforcement is not instantaneous. The API Platform can process a small amount of extra usage while the limit state propagates, so recorded spend can slightly exceed the configured amount."* Set the cap slightly below the true pain threshold; do not treat it as a precise fence.
2. **Hard limits are monthly and reset with the billing cycle.** A cap hit on December 18th unblocks on January 1st — which is after the season. Sizing matters more than existence.

**Dashboard paths (for the verification step in the plan):**

- Organization limits: `platform.openai.com/settings/organization/limits`
- Project limits: `platform.openai.com/settings/` → select project → Limits
- Usage: `platform.openai.com/settings/organization/usage`
- Billing / credits / auto-recharge: `platform.openai.com/settings/organization/billing`

### Assessment: is the existing $5 + auto-recharge-off a hard ceiling?

**Yes — but it is the wrong kind of ceiling, and it will not survive contact with the season.**

It genuinely caps exposure at $5 today, because credit exhaustion returns `credit_balance_exhausted` and requests stop. Four problems:

1. **It is a ceiling by accident of being underfunded, not by policy.** The moment credits are topped up to a season-sized balance — which they must be — the ceiling rises to that balance. A $400 top-up creates a $400 ceiling with no per-month structure.
2. **It fails closed mid-call, silently, with no warning.** A child is mid-conversation with Santa and Santa stops existing. That is a worse user-facing failure than an amber LED and a "Santa is resting" message.
3. **It is one toggle away from not existing.** Turning auto-recharge on — which is a natural thing to do when a call fails and you're troubleshooting at 9pm — removes the ceiling entirely and permanently.
4. **It does not scope to the Santa key.** Any other use of the same org's credits (a laptop experiment, a different project) draws down the same pool.

### Recommended configuration — defense in depth

The plan should implement all five, in this order:

1. **Create a dedicated project** for this installation (e.g. `call-santa-prod`) and issue the device's API key scoped **only** to that project. This is also the OPS-02 groundwork and it makes step 3 possible.
2. **Set a project-level hard spend limit** on that project, with "Enforce a hard limit" toggled on, sized to the monthly season budget the owner is willing to lose. This is the control that actually stops a runaway.
3. **Set an organization-level hard spend limit** slightly above the project limit, as a backstop against a second key or project appearing.
4. **Add spend alerts** at 50% / 75% / 90% of the project limit — so the owner learns about a problem before Santa goes silent.
5. **Confirm auto-recharge remains OFF** and keep the credit balance as a third, outermost fence.

**Also — and this belongs in this phase because it was discovered here — there is a `.env` file on disk at `voice/my-project/.env` that was written to hold `VITE_OPENAI_API_KEY`, a key intended to be shipped to a browser.** It is correctly gitignored and was never committed, but it is a standing credential attached to a dead project. Any key in it must be treated as an unaccounted-for spend vector and **rotated or revoked** as part of OPS-03. Do not print its contents into any log or transcript.

### Season cost model — size the cap against this, not against a guess

`[CONFIDENCE: MEDIUM — pricing figures below are from secondary sources; the official pricing page did not resolve during this session and MUST be re-verified during execution.]`

Reported rates (July 2026): **gpt-realtime-2.1 at $32/1M audio input tokens and $64/1M audio output tokens.** Audio tokenises at roughly 1 token per 100 ms of user speech and 1 token per 50 ms of assistant speech, giving ~600 tokens per minute heard and ~1,200 per minute spoken → **≈ $0.019/min heard, ≈ $0.077/min spoken** for the audio alone. Because Realtime re-bills conversation context on each turn unless prompt caching is effective, measured real-world costs run **$0.06–0.11/min with caching working and $0.18–0.46/min without**. **gpt-realtime-2.1-mini** is reported at roughly a third of the price ($10/$20 per 1M audio in/out).

[CITED: hackernoon.com "OpenAI Realtime API Pricing in 2026: Real-World Data From 4,000 Measured Sessions"; tokenmix.ai; eesel.ai — three independent secondary sources broadly agreeing. **Not** confirmed against openai.com pricing.]

Scenario at $0.15/min (mid-range, conservative):

| Load | Cost/day | Cost/month |
|------|---------|-----------|
| 10 calls/day × 4 min | $6 | ≈ $180 |
| 30 calls/day × 4 min | $18 | ≈ $540 |
| 60 calls/day × 4 min (a good night in a busy neighbourhood) | $36 | ≈ $1,080 |

**This is the headline: the API bill can plausibly exceed the entire hardware budget.** The 5-minute session cap (SESS-04), the 15s/28s silence ladder (SESS-05) and the schedule (ADMIN-02) are not just UX features — they are the primary cost controls, and the hard spend limit is the backstop behind them. The planner should carry this into the Phase 1 checkpoint: the owner needs to name a monthly figure they are willing to lose, because that figure *is* the hard limit value.

**Cost levers worth surfacing now** (decisions belong to Phase 2, but the owner should know they exist): using `gpt-realtime-mini` (≈ ⅓ cost), using `audio/pcmu` output, and keeping the session prompt short so cached-context billing stays small.

---

## Repo Cleanup — Evidence

> The roadmap asks for a delete-vs-document call. The evidence supports **delete**, decisively.

### What `voice/my-project/` actually is

**27 tracked files** [VERIFIED: `git ls-files voice | wc -l`], comprising two things:

**(a) `voice/my-project/` — a Vite + TypeScript starter with a 12-line Realtime demo bolted on.**

`src/agent.ts` is six lines:

```typescript
import { RealtimeAgent } from '@openai/agents/realtime';

export const agent = new RealtimeAgent({
  name: 'Santa',
  instructions: 'You are a jolly old Saint Nick. You will listen to childer, repeat back their name, and ask what they want for Christmas.',
});
```

(Note the typo — "childer". This is a first-sketch artefact, not a maintained asset.)

`src/main.ts` is twelve lines: a button click handler that creates a `RealtimeSession` and calls `session.connect({ apiKey: import.meta.env['VITE_OPENAI_API_KEY'] })`.

Everything else in the directory is unmodified Vite scaffold: `counter.ts`, `style.css`, `vite.svg`, `typescript.svg`, `hero.png`, `favicon.svg`, `icons.svg`, `tsconfig.json`.

**(b) `voice/my-project/my-project/` — a second, completely untouched copy of the Vite starter.** Its `package.json` has no `@openai/agents` dependency at all; its `main.ts` is the stock "Edit src/main.ts and save to test HMR" hero page. This is the residue of running the scaffolder twice in the wrong directory. It has zero project value under any interpretation.

### Git archaeology — it predates the POC

```
1361b16 docs: ingest 2 docs from repo root (#2387)
a0d272a Add laptop POC: real-time voice "Call Santa" over OpenAI Realtime API
ef37f70 initial commit          <-- voice/ was added here
d5dc1ef initial commit with read me
```

`git log --oneline -- voice` returns exactly one commit: `ef37f70 initial commit`. **`voice/` has never been touched since the repo's first commit, and the working POC was added in a *later* commit.** It is chronologically and functionally superseded by `poc/`. [VERIFIED: `git log`]

### Nothing references it

```
git grep -n -i -e "my-project" -e "voice/" -- . ':!voice/'
```

returns **only `.planning/*` files**, and every one of those hits is a planning document describing it as *unresolved*. No source file, no config, no README, no build script, and neither ingested document references it. [VERIFIED, 2026-08-13]

### The security finding — this is the argument that settles it

`voice/my-project/src/main.ts` passes a **standing OpenAI API key read from a Vite environment variable directly into browser-side code**. Vite inlines `VITE_`-prefixed variables into the client bundle at build time. Any build of this project ships a live, long-lived OpenAI key into JavaScript served to the browser.

This is the exact inverse of the pattern the project has already adopted: `poc/server.py` is a token broker whose README states *"Your secret key never reaches the browser."* And it directly contradicts **OPS-02** (*"The OpenAI API key lives only in the device environment... credentials scoped as narrowly as the chosen transport allows"*).

Leaving this in the repo means leaving a worked example of the forbidden pattern where a future agent — or the owner at 11pm in November — could copy it.

**Additionally: `voice/my-project/.env` exists on disk** [VERIFIED: `find` located it; contents deliberately not read]. It is gitignored and was never committed, so nothing leaked to GitHub. But it was created to hold a browser-destined key. Treat any key in it as compromised-by-design and rotate it.

### Disk

`voice/` occupies **123 MB**, of which **87 MB is untracked `node_modules/`** [VERIFIED: `du -sh`]. The tracked payload is small (27 mostly-tiny files plus a `hero.png`), so deletion is a repo-hygiene win rather than a repo-size win — but it does reclaim 123 MB of local disk.

### The README gap the success criterion assumes away

ROADMAP success criterion 4 offers the alternative *"documented in the README with a stated reason to keep it."* **There is no top-level README in this repository** [VERIFIED: `ls README*` → no matches]. Only `poc/README.md` exists. So the "document it" branch is not a one-line change — it requires authoring a root README first.

That README should be written **regardless of which branch is taken**, because criterion 4's second clause — *"exactly one authoritative implementation path"* — is a documentation claim, and there is currently no document in the repo that makes it. A root README stating "`poc/` is the reference implementation; the production system will live in `<path>`; see `.planning/` for the roadmap" is what actually satisfies that clause.

### Recommended disposition

**Delete, and document the deletion.** Specifically:

1. `git rm -r voice/` — removes all 27 tracked files.
2. `rm -rf voice/` — removes the untracked `node_modules/` (87 MB) and the `.env`.
3. **Before step 2**, check whether `voice/my-project/.env` contains a live key; if so, revoke it at `platform.openai.com/settings/organization/api-keys`. Do not echo its contents.
4. Author a root `README.md` naming `poc/` as the single reference implementation and recording, in two sentences, what `voice/my-project/` was and why it was removed — so this is not re-litigated in three months.
5. Note the deletion in `.planning/STATE.md` under Accumulated Context, closing the open decision.

Git history preserves everything; nothing is truly lost.

**Counter-argument, stated fairly:** the only thing of value in `voice/my-project/` is the demonstration that `@openai/agents` has a `RealtimeAgent`/`RealtimeSession` abstraction. If the Phase 2 transport decision ends up favouring a Node/TypeScript session manager over Python, that SDK is worth knowing about. **That knowledge should be captured as one line in the root README or in Phase 2's research, not as 123 MB of scaffolding.**

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Stopping runaway API spend | A custom token-counting wrapper, a cron job that greps usage, or "we'll just watch the dashboard" | OpenAI's **hard spend limit** with "Enforce a hard limit" toggled at project scope | It is the only control that actually returns `429` and stops requests. Anything you build runs *inside* the thing that's running away. |
| Off-hook detection mechanism | A fabricated cradle + custom lever geometry | The **hook switch already inside a full corded/rotary phone** | It is a solved mechanical problem with correct travel, rest position and detents, for $70. |
| WiFi signal measurement | Reading the router's admin page, or a phone's signal bars | `iw dev wlan0 link` + `wavemon` + `iperf3` + `mtr` on the actual device | Bars are a 4-level quantisation of a value you need to 1 dBm. The router's page reports *its* view, not the yard's. |
| Handset audio interface | A custom amplifier/impedance-matching circuit | A **$5 CM108-class USB audio adapter** and, if needed, an `alsamixer` gain adjustment | Documented conversions report this works directly. Build the circuit only if measurement proves you need it. |
| Weatherproof cable entry | Drilled hole + a blob of caulk | An **IP68 compression cable gland** | A gland provides sealing *and* strain relief and survives thermal cycling. Caulk on a moving cord fails in one season. |
| Detecting hallucinated packages in later phases | Manual eyeballing of package names | `slopcheck` (installed and available at `~/Library/Python/3.9/bin/slopcheck`) | Already installed during this research. Note it for Phase 2. |
| A "one authoritative implementation path" claim | An argument in a planning doc | A **root README.md** that states it | Criterion 4 is a documentation requirement; only a document in the repo can satisfy it. |

**Key insight:** every one of this phase's success criteria is satisfied by *evidence*, not by artefacts. The temptation in a procurement phase is to build tracking spreadsheets, cost calculators and survey tooling. Don't. Record raw numbers in flat files, use the vendor's own controls, and spend the saved time on the enclosure decision — which is the only thing in this phase that can actually cost the season.

---

## Runtime State Inventory

> Included because OPS-01 is a deletion/refactor operation, and because this phase changes state in
> systems outside the repository.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| **Stored data** | None. No database, no vector store, no persisted state anywhere in this project yet. The POC is stateless by design and writes nothing to disk. [VERIFIED: `poc/` contains only `server.py`, `index.html`, `README.md`] | None |
| **Live service config** | **OpenAI platform account** — spend limits, spend alerts, projects, and auto-recharge all live in the OpenAI dashboard, **not in git**. Nothing in this repo records or asserts their state. This is the only external service in play. | Configure per `## OpenAI Spend Controls`; capture evidence in-repo (see `## Validation Architecture`) since the settings themselves cannot be version-controlled |
| **OS-registered state** | None. No systemd units, no launchd plists, no cron entries, no pm2 processes. The POC is run manually via `python3 server.py`. [VERIFIED: no service definitions in the repo] | None |
| **Secrets / env vars** | **`voice/my-project/.env` EXISTS on disk** (untracked, gitignored). Written to hold `VITE_OPENAI_API_KEY` — a key intended for browser-side use. Also expect an `.env` or exported `OPENAI_API_KEY` for `poc/server.py`. No secrets are tracked in git. [VERIFIED: `find` located `voice/my-project/.env`; `git ls-files \| grep -i env` returned nothing] | **Check and rotate/revoke** the key in `voice/my-project/.env` before deleting the directory. Do not read its value into any transcript or log. The `poc/` key should be migrated to the new scoped project created for OPS-03. |
| **Build artifacts** | **`voice/my-project/node_modules/` — 87 MB, untracked.** Will not be removed by `git rm`; requires an explicit `rm -rf`. No compiled binaries, no egg-info, no dist directories, no published packages, no Docker images. [VERIFIED: `du -sh`] | `rm -rf voice/` after `git rm -r voice/` |
| **Remote state** | Repo is pushed to GitHub on `main`. Deleting `voice/` locally requires a push to take effect remotely; git history retains the files either way. | Commit and push; no history rewrite needed or recommended |

---

## Common Pitfalls

### Pitfall 1: Treating the budget conflict as a rounding error
**What goes wrong:** The plan writes "order the mahogany booth" and "stay inside $850–1,050" as two separate tasks, the executor orders the booth, and the budget criterion silently fails — or worse, the executor picks a cheaper booth unilaterally and the owner discovers in October that their walk-in mahogany phone box is a $180 MDF prop.
**Why it happens:** Success criteria 1 and 2 read as independent bullets. They are not; they are mutually exclusive at current prices.
**How to avoid:** Put a `checkpoint:human-decision` **before** any purchase task, presenting the three costed options from `## The Enclosure Problem` with real numbers. Record the answer in STATE.md as a locked decision (CD-07) before the order is placed.
**Warning signs:** Any task that says "order the enclosure" without a preceding decision gate.

### Pitfall 2: Sequencing everything behind the enclosure decision
**What goes wrong:** The owner takes six days to think about spending $2,600 instead of $900, and the site survey, the spend ceiling and the repo cleanup all sit idle. Phase 1 blows its 2026-08-25 date over a decision that blocked nothing.
**Why it happens:** Procurement *feels* like one linear task list.
**How to avoid:** Four parallel plans. The Pi/electronics order, the site survey, the OpenAI spend ceiling and the repo cleanup have **zero** dependency on the enclosure choice.
**Warning signs:** A single plan file containing all of Phase 1.

### Pitfall 3: A one-shot site survey reading
**What goes wrong:** Someone stands in the yard on a Sunday morning, sees "−58 dBm, looks great," writes "WiFi" in the doc, and the installation drops calls every evening in December when the street's networks are loaded and the leaves are gone but the rain isn't.
**Why it happens:** RSSI is trivially easy to read once and genuinely hard to characterise.
**How to avoid:** Enforce the sampling protocol — three ≥20-minute windows, one on a weekday evening, logged every 5 seconds, reported as min/median/p95, with throughput and loss tested separately against the real endpoint.
**Warning signs:** A survey artefact containing a single number instead of a time series.

### Pitfall 4: Believing an "outdoor" product description
**What goes wrong:** The PRD asserts the booth *"provides full weatherproofing for the internal electronics."* Both retailers say **"For Indoor or Covered Use Only!"** If Phase 3's weatherproofing scope was sized against the PRD's claim, it is undersized.
**Why it happens:** The PRD's hardware section was written from search results, not product pages.
**How to avoid:** Verify the outdoor rating on the actual product page at purchase time, and record it in the order-confirmation artefact. Budget sealant, a drip edge and a raised base regardless of what the listing says.
**Warning signs:** Any plan task that treats HW-05 as smaller because "the booth is weatherproof."

### Pitfall 5: Confusing a spend *alert* with a spend *limit*
**What goes wrong:** Someone sets a $50 budget alert, sees it in the dashboard, marks OPS-03 done. In December an unattended box bills $600 and every dollar of it was accompanied by an email nobody read.
**Why it happens:** OpenAI's own history — hard caps existed, were removed in early 2026 leaving alerts only, then were restored in July 2026. Training data and most blog posts describe one of the two obsolete states.
**How to avoid:** The verification step must confirm the **"Enforce a hard limit" toggle is on**, at project scope, not merely that an alert exists. Official docs are explicit: *"Spend alerts do not enforce a cap."*
**Warning signs:** Evidence for OPS-03 that shows a threshold but not the enforcement toggle.

### Pitfall 6: Deleting `voice/` without checking its `.env`
**What goes wrong:** `rm -rf voice/` removes the directory and the untracked `.env` inside it, along with any record that a browser-destined API key ever existed. The key remains live on the OpenAI account, unaccounted for, drawing on the same credit balance the spend ceiling is protecting.
**Why it happens:** The cleanup task and the spend-ceiling task look unrelated.
**How to avoid:** Order the tasks: check `.env` → revoke key if present → `git rm -r voice/` → `rm -rf voice/`. And never read the file's contents into a transcript.
**Warning signs:** A cleanup plan whose first action is a delete.

### Pitfall 7: Ordering a TRRS-only USB audio adapter
**What goes wrong:** A well-reviewed adapter arrives with one combined headset jack. The handset's separate mic and receiver pairs cannot connect without a splitter, discovered in Phase 3.
**Why it happens:** "USB audio adapter with mic support" describes both jack layouts.
**How to avoid:** Require **two separate 3.5mm jacks** (pink mic-in, green line-out) and confirm from the product photo. Buy 2–3 at ~$5 each from different vendors.
**Warning signs:** A BOM line reading "USB audio adapter" with no jack-layout qualifier.

### Pitfall 8: Under-powering the Pi 5
**What goes wrong:** A generic USB-C charger is used instead of a 5V/5A PD supply. The Pi throttles USB current, the audio adapter intermittently disappears, and the symptom presents in December as random mid-call audio failure — the hardest possible class of bug to diagnose in a sealed cold box.
**How to avoid:** Buy the official 27W supply, or buy the CanaKit Starter Kit which bundles a correct one.
**Warning signs:** A BOM with a board-only Pi and no explicit PSU line item.

---

## Code Examples

### Verify the repo cleanup happened (git-state assertion)

```bash
# Assert: no tracked files remain under voice/
test -z "$(git ls-files voice)" && echo "PASS: voice/ untracked" || echo "FAIL"

# Assert: nothing outside .planning/ references it
git grep -q -i -e "my-project" -- . ':!.planning/' && echo "FAIL: stale reference" || echo "PASS: no references"

# Assert: directory is gone from disk (including node_modules and .env)
test ! -d voice && echo "PASS: voice/ removed from disk" || echo "FAIL"

# Assert: a root README exists and names the authoritative path
test -f README.md && grep -q "poc/" README.md && echo "PASS: README names implementation path" || echo "FAIL"
```

### Check for a stray credential before deleting (without exposing it)

```bash
# Existence and shape only — never print the value
if [ -f voice/my-project/.env ]; then
  echo "FOUND: voice/my-project/.env"
  grep -c 'API_KEY' voice/my-project/.env    # count of key-shaped lines, not values
  echo "ACTION: revoke this key at platform.openai.com/settings/organization/api-keys before deleting"
fi
```

### Site survey — a single logged sample (see `## Site Survey Method` for the full protocol)

```bash
# Source: Raspberry Pi Spy / Adafruit / iw man page — standard Linux wireless tooling
iw dev wlan0 link | awk '/signal:/ {print "RSSI:", $2, "dBm"}'
mtr -r -c 300 --json api.openai.com | jq '.report.hubs[-1] | {loss: .Loss, jitter_stdev: .StDev, avg_rtt: .Avg}'
iperf3 -c <wired-lan-host> -t 60 -J | jq '.end.sum_sent.bits_per_second / 1e6'
```

### Verify the OpenAI hard limit is actually enforcing

There is **no documented public API for reading spend limits** [VERIFIED: the official spend-limits guide documents no endpoints]. Verification is therefore a dashboard action:

1. Navigate to `platform.openai.com/settings/organization/limits` → confirm a dollar amount is set **and** "Enforce a hard limit" is toggled on.
2. Navigate to the `call-santa-prod` project → Limits → confirm the same.
3. Navigate to `platform.openai.com/settings/organization/billing` → confirm auto-recharge is **off**.
4. Capture screenshots of all three and commit them (see `## Validation Architecture`).

`[ASSUMED]` — an organization costs/usage endpoint may exist under `/v1/organization/costs` that could provide a programmatic cross-check of *spend*, though not of *limit configuration*. This was **not verified** in this session. If the planner wants an automated check, verify that endpoint's existence first.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| OpenAI "soft limit / hard limit" usage settings | Removed, leaving **alerts only** — a runaway key could bill thousands unnoticed | early 2026 | Any guidance written before mid-2026 is wrong |
| Alerts-only | **Hard spend limits restored**, org + project scope, `429 insufficient_quota` with `organization_spend_limit_exceeded` / `project_spend_limit_exceeded` | rolled out to all accounts week of **2026-07-22** | This is the control OPS-03 must use. It is ~3 weeks old at time of writing — expect docs and UI to still be settling |
| Raspberry Pi 5 8GB at $80 | **$125 list, ~$175 street** | 2025-12-01 (+$15) and 2026-02-02 (+$30), LPDDR4 scarcity from AI datacenter demand | The PRD's $130 "Pi kit" line is now $270. Raspberry Pi says the rises are temporary but expects pressure through 2026 |
| 3G/UMTS USB dongles | **4G/LTE only** — 3G networks shut down by major NA/EU carriers | 2022–2024 | Do not buy a 3G dongle at any price |
| Realtime API billed as a per-minute service | Billed **per audio token**, with conversation context re-billed each turn unless prompt caching applies | ongoing | Per-minute cost is a derived, load-dependent figure ($0.06–0.46/min observed), not a rate card number |

**Deprecated / outdated in the source PRD:**
- Booth price band ($600–800) — off by ~3x
- Booth outdoor rating ("provides full weatherproofing") — vendors say indoor/covered only
- Pi 5 kit price ($130) — now $270
- Phone price ($35) — now ~$70
- Camera section entirely — CD-05 locked it out; do not reintroduce

---

## Package Legitimacy Audit

**Not applicable to this phase's deliverables.** Phase 1 installs no language-registry (npm / PyPI / crates.io) packages. Its outputs are purchase orders, a measurement log, a dashboard configuration and a `git rm`.

Two adjacent notes for the planner:

1. **Survey tooling is Debian system packages, not registry packages.** `iw`, `wavemon`, `iperf3`, `mtr-tiny` and `modemmanager` are all long-standing Debian/Raspberry Pi OS packages installed via `apt`. slopcheck does not cover the apt ecosystem, and these are not a slopsquatting surface. `[VERIFIED: standard Debian packages, referenced across Adafruit, Raspberry Pi Spy and raspberrypi.com documentation]`
2. **slopcheck was installed during this research and is available for later phases** at `~/Library/Python/3.9/bin/slopcheck` (not on the default PATH — the harness will need `export PATH="$HOME/Library/Python/3.9/bin:$PATH"` or the absolute path). Phase 2, which will install real dependencies, should use it.

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| — | — | — | — | — | — | No registry packages installed in this phase |

**Packages removed due to slopcheck [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

---

## Environment Availability

The survey and cleanup work happens on the owner's macOS machine (this one) plus, eventually, the Pi.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `git` | OPS-01 repo cleanup | ✓ | in use this session | — |
| `python3` | POC, future tooling | ✓ | 3.9 (`/usr/bin/python3`) | — |
| `pip3` | tooling installs | ✓ | 21.2.4 (old; `--break-system-packages` unsupported) | plain `pip3 install` works |
| `slopcheck` | future package vetting | ✓ (installed this session) | at `~/Library/Python/3.9/bin/` | not on PATH by default |
| `iw` | WiFi RSSI measurement | ✗ (macOS) | — | **Survey must run on Linux.** Use the Pi once delivered, or a Linux laptop. macOS alternative: `wdutil info` (requires sudo) or the Wireless Diagnostics app — **less precise and not the production radio** |
| `wavemon` | WiFi signal-over-time | ✗ (macOS) | — | same as above |
| `iperf3` | throughput | ✗ | — | `brew install iperf3` on macOS; `apt install iperf3` on Pi. Needs a **wired** server host on the LAN |
| `mtr` | loss / jitter | ✗ | — | `brew install mtr` / `apt install mtr-tiny` |
| `nmcli`, `mmcli` | LTE evaluation | ✗ (macOS) | — | Pi only; only needed if WiFi survey fails |
| Raspberry Pi 5 | the production radio for a definitive survey | ✗ — not yet ordered | — | Survey with a Linux laptop as a proxy and **re-survey with the Pi on arrival**. Record the proxy caveat in the log |
| Wired LAN host for `iperf3 -s` | throughput measurement | ? unknown | — | If no wired host exists, use a public iperf3 server and note the added WAN variance, or fall back to a speed test with the caveat recorded |

**Missing dependencies with no fallback:** none — every gap has a viable path.

**Missing dependencies with fallback (planner must handle):**
- No Linux machine for the survey → the plan needs an explicit "survey device" decision task before the survey task.
- No wired LAN host for `iperf3 -s` → the plan needs a fallback throughput method with the caveat recorded in the log.
- Pi not yet delivered → plan a **re-survey task in Phase 3**, before the box is sealed, using the production radio.

---

## Validation Architecture

This is a procurement and operations phase. There is no code and therefore no test suite. The
validation surface is **committed evidence artefacts and recorded measurements** — a claim is
"tested" when a file in the repo contains the raw numbers or the confirmation that proves it.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | None (no code produced this phase). Verification is artefact-existence + content assertions via shell. |
| Config file | none — see Wave 0 |
| Quick run command | `bash .planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh` (to be created in Wave 0) |
| Full suite command | same — the script is the suite |
| Phase gate | All five success criteria have a committed evidence artefact and `verify.sh` exits 0 |

### Evidence Location Convention

Create `.planning/phases/01-procurement-site-survey-repo-cleanup/evidence/` and commit:

```
evidence/
├── orders/
│   ├── enclosure-order.md          # vendor, SKU, price paid, order #, delivery ETA, outdoor rating as stated
│   ├── phone-order.md
│   ├── pi-and-electronics-order.md
│   └── budget-actual.md            # line-by-line actual vs. the $850–1,050 ceiling, with the variance explained
├── site-survey/
│   ├── survey-protocol.md          # spot, height, orientation, device, dates/times, weather
│   ├── wifi-samples-*.csv          # raw 5s RSSI series, one file per window (>=3 windows)
│   ├── mtr-*.json                  # raw loss/jitter
│   ├── iperf3-*.txt                # raw throughput, both directions
│   └── CONNECTIVITY-DECISION.md    # WiFi or LTE, with the numbers that justify it
├── spend-controls/
│   ├── org-hard-limit.png          # "Enforce a hard limit" toggle visibly ON
│   ├── project-hard-limit.png
│   ├── spend-alerts.png
│   ├── auto-recharge-off.png
│   └── SPEND-CEILING.md            # the dollar figures chosen and why; key rotation record
└── repo-cleanup/
    └── (no artefact — asserted directly against git state)
```

### Phase Requirements → Evidence Map

| Req ID | Behavior proven | Evidence type | Automated assertion | Exists? |
|--------|-----------------|---------------|---------------------|---------|
| **HW-01** | Enclosure ordered, decision recorded | order confirmation file | `test -f evidence/orders/enclosure-order.md && grep -qE 'Order #\|Confirmation' evidence/orders/enclosure-order.md` | ❌ Wave 0 |
| **HW-01** | Phone ordered (full corded/rotary, resolving CD-06) | order confirmation file | `test -f evidence/orders/phone-order.md` | ❌ Wave 0 |
| **HW-01 / budget** | Pi + electronics ordered, total reconciled against the ceiling, **no camera line** | budget file | `test -f evidence/orders/budget-actual.md && ! grep -qi camera evidence/orders/budget-actual.md` | ❌ Wave 0 |
| **HW-06** | ≥3 survey windows of raw samples exist | measurement logs | `test "$(ls evidence/site-survey/wifi-samples-*.csv \| wc -l)" -ge 3` | ❌ Wave 0 |
| **HW-06** | Each window is a real time series, not one reading | measurement logs | `for f in evidence/site-survey/wifi-samples-*.csv; do test "$(wc -l < "$f")" -ge 200; done` (20 min @ 5s ≈ 240 rows) | ❌ Wave 0 |
| **HW-06** | Loss/jitter and throughput measured against the real endpoint | raw tool output | `test -f evidence/site-survey/mtr-*.json && test -f evidence/site-survey/iperf3-*.txt` | ❌ Wave 0 |
| **HW-06** | Connectivity path chosen **on that evidence** (CD-04a) | decision doc | `grep -qE 'WiFi\|LTE' evidence/site-survey/CONNECTIVITY-DECISION.md && grep -q 'dBm' evidence/site-survey/CONNECTIVITY-DECISION.md` — the decision must cite a measured number | ❌ Wave 0 |
| **OPS-01** | No tracked files under `voice/` | git state | `test -z "$(git ls-files voice)"` | ❌ Wave 0 |
| **OPS-01** | No stale references outside `.planning/` | git grep | `! git grep -q -i 'my-project' -- . ':!.planning/'` | ❌ Wave 0 |
| **OPS-01** | Exactly one authoritative implementation path is *documented* | root README | `test -f README.md && grep -q 'poc/' README.md` | ❌ Wave 0 |
| **OPS-01** | Directory gone from disk incl. `node_modules` and `.env` | filesystem | `test ! -d voice` | ❌ Wave 0 |
| **OPS-03** | Hard limit **enforcing**, not just alerting | screenshot + written record | `test -f evidence/spend-controls/org-hard-limit.png && test -f evidence/spend-controls/project-hard-limit.png` + human confirms the toggle is visibly ON | ❌ Wave 0 |
| **OPS-03** | Alerting configured | screenshot | `test -f evidence/spend-controls/spend-alerts.png` | ❌ Wave 0 |
| **OPS-03** | Auto-recharge off; monthly figure recorded | screenshot + doc | `test -f evidence/spend-controls/auto-recharge-off.png && grep -qE '\$[0-9]' evidence/spend-controls/SPEND-CEILING.md` | ❌ Wave 0 |
| **OPS-03** | Stray browser-key from `voice/my-project/.env` revoked | written record | `grep -qi 'revok\|rotat' evidence/spend-controls/SPEND-CEILING.md` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `bash verify.sh` — it is fast (file existence + git assertions, < 2 seconds)
- **Per wave merge:** same
- **Phase gate:** `verify.sh` exits 0 with all assertions passing, before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `evidence/` directory tree — created before any evidence-producing task runs
- [ ] `verify.sh` — the assertion script encoding every row of the table above; must be authored **first** so tasks know exactly what artefact shape they owe
- [ ] `README.md` at repo root — required by OPS-01's "exactly one authoritative implementation path" clause; does not currently exist
- [ ] `evidence/site-survey/survey-protocol.md` template — pre-filled with the spot/height/orientation/device/weather fields so the human just fills blanks in the yard

**Note on screenshot evidence:** an agent cannot verify that a toggle is visibly ON inside a PNG. The plan should pair each screenshot task with a `checkpoint:human-verify` in which the human explicitly confirms the toggle state. File existence is the automated half; the human confirmation is the other half.

---

## Security Domain

`security_enforcement` is not disabled in config (no `.planning/config.json` exists), so this section is required.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth surface created this phase (PIN/admin auth is Phase 5) |
| V3 Session Management | no | No sessions this phase |
| V4 Access Control | **yes** | **API key scoping.** Create a dedicated OpenAI project and issue the device key scoped to it — least privilege for the credential, and the precondition for a project-scoped spend limit |
| V5 Input Validation | no | No inputs processed this phase |
| V6 Cryptography | no | No crypto implemented this phase |
| **V7 Error Handling & Logging** | **yes** | The `.env` check must **not** echo secret values into any transcript, log or commit. Assert shape/count, never content |
| **V14 Configuration** | **yes** | `.gitignore` already covers `.env`, `.env.*`, `*.key` and no secrets are tracked [VERIFIED]. Preserve this. The root README added for OPS-01 must not embed any key |
| **V1 Architecture (Secrets Management)** | **yes** | **Rotate the browser-destined key in `voice/my-project/.env`.** It was authored to be inlined into a client bundle; treat it as compromised by design |

### Known Threat Patterns for this phase

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Client-side API key exposure (`VITE_OPENAI_API_KEY` inlined into a browser bundle by Vite) — **present in the repo today** at `voice/my-project/src/main.ts` | Information Disclosure / Elevation of Privilege | Delete the code. Rotate the key. The correct pattern already exists in `poc/server.py`: a server-side token broker minting short-lived ephemeral tokens |
| Orphaned live credential on disk (`voice/my-project/.env`) surviving a directory deletion | Information Disclosure | Check-then-revoke-then-delete, in that order |
| Unbounded API spend from an unattended device with children as the load generator | Denial of Service (financial) | Project-scoped **hard** spend limit with enforcement toggled on, layered alerts, auto-recharge off, plus the session cap and schedule as primary controls |
| Secret leakage into planning artefacts or agent transcripts during the cleanup | Information Disclosure | Never `cat` a `.env`. Use existence/count assertions only. Screenshots of the OpenAI dashboard must not include a visible key value |
| Supply-chain risk from survey tooling | Tampering | Survey tools are Debian-official apt packages; no registry packages installed this phase |
| Physical safety (adjacent, worth flagging): a 200 lb, 7.5 ft enclosure in a front yard used by unsupervised children | Physical / Tampering | If Option A is chosen, the plan must add anchoring and wind-load tasks to Phase 3 or 7. Not a software control, but a real hazard the roadmap does not currently name |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | ECVISION rotary phone is ~$70 | Phone Hardware | Low — Amazon blocked automated fetch; price must be confirmed by the human at checkout. Off by ±$40 at worst |
| A2 | Realtime pricing is $32/$64 per 1M audio in/out (gpt-realtime-2.1) and mini is ~⅓ | OpenAI Spend Controls | **High** — the entire season cost model and the hard-limit sizing rest on it. Sourced from three concurring secondary blogs; the official pricing page 404'd during this session. **Must be re-verified against openai.com before setting the cap** |
| A3 | ~$0.15/min is a fair mid-range real-world cost estimate | OpenAI Spend Controls | High — a 3× error changes the monthly figure from $180 to $540. Mitigated by the hard cap itself: the cap fails safe |
| A4 | ~3.4 MB/min of call traffic, ≈12 GB/month on LTE | Site Survey Method | Medium — sizes the LTE data plan. Derived arithmetic from the verified PCM16/24kHz format, but real overhead (framing, keepalives, reconnects) is unmeasured |
| A5 | LTE RSRP/RSRQ/SINR quality bands (−90/−105/−110 etc.) | Site Survey Method | Low — conventional industry bands, adequate for go/no-go, not verified against a cited authority |
| A6 | `mmcli --signal-get` reports RSRP/RSRQ/SINR | Site Survey Method | Low — command existence verified; specific field availability not confirmed against ModemManager docs |
| A7 | An `/v1/organization/costs` endpoint exists for programmatic spend verification | Code Examples | Low — flagged as unverified; the plan should use dashboard screenshots regardless |
| A8 | Etsy/eBay mid-band booth props exist at $300–600 (Option B) | The Enclosure Problem | **Medium** — Etsy, eBay and Amazon all blocked automated fetch. Option B's price band is the least verified of the three options. A human must price it before the checkpoint, or Option B should be dropped from the choice set |
| A9 | Cedar/exterior-ply materials for a kiosk run $250–450 (Option C) | The Enclosure Problem | Medium — lumber pricing not verified this session; regionally variable |
| A10 | Opis 3.5mm handset is ~$30 | Phone Hardware | Low — carried forward from the PRD, not re-verified |
| A11 | 8GB vs 4GB Pi makes no functional difference for the v1 workload | Raspberry Pi 5 and Audio | Low — recommendation is to buy 8GB anyway, so the assumption is not load-bearing |
| A12 | The key in `voice/my-project/.env` is a live OpenAI key | Repo Cleanup / Security | Low — file contents deliberately not read. The plan's check-then-revoke sequence handles both outcomes |

---

## Open Questions

1. **Which enclosure option? (CD-07)**
   - *What we know:* Mahogany walk-in booths are $2,195–$3,476 and indoor-rated. The $850–1,050 budget cannot accommodate one. Non-enclosure BOM is ~$433.
   - *What's unclear:* Whether the owner values the walk-in mahogany booth enough to spend ~$2,630, or would rather protect the budget and the schedule.
   - *Recommendation:* **`checkpoint:human-decision` as the first task in the procurement plan.** Present the three costed options verbatim. Do not let an agent choose. Record the answer as a locked decision in PROJECT.md and STATE.md before ordering.

2. **What monthly dollar figure should the hard spend limit be set to? (OPS-03)**
   - *What we know:* The mechanism (project-scoped hard limit with enforcement toggled on). Plausible season spend $180–1,080/month depending on traffic.
   - *What's unclear:* The owner's actual risk appetite. This is a values question, not a research question.
   - *Recommendation:* Second `checkpoint:human-decision`. Suggest a starting point of **$150/month** with alerts at 50/75/90% — high enough not to kill a busy December evening, low enough that the worst case is survivable, and adjustable upward from the dashboard in seconds if alerts start firing early. Frame it explicitly as "the amount you would be annoyed but not upset to lose."

3. **What device runs the site survey, and when?**
   - *What we know:* macOS lacks `iw`/`wavemon`. The Pi is the ideal survey radio but has not been ordered.
   - *What's unclear:* Whether a Linux laptop is available, and whether the Pi can arrive inside the two-week window (PiShop/CanaKit show in stock, so probably yes).
   - *Recommendation:* Order the Pi on day 1 of the phase — it is in stock and cheap relative to the enclosure. Survey with whatever Linux device is available first to get an early read; add a mandatory **re-survey with the production Pi** task in Phase 3 before the enclosure is sealed.

4. **Is there a wired host on the LAN to run `iperf3 -s`?**
   - *What we know:* Measuring WiFi-to-WiFi produces meaningless throughput numbers.
   - *Recommendation:* Ask in the survey plan. If no wired host, fall back to a public iperf3 server and record the WAN-variance caveat in the log rather than silently reporting a worse number.

5. **Does the front-yard outdoor outlet already have GFCI and an in-use cover?**
   - *What we know:* NEC requires both for a wet-location outdoor receptacle; older homes frequently have neither.
   - *Recommendation:* Add a one-line inspection task to the site-survey visit — the person is already standing there. If missing, it is a ~$25 in-line GFCI + in-use cover purchase, not a project risk, but only if discovered in August rather than November.

6. **Should a spare 3.5mm handset be bought alongside the rotary phone?**
   - *What we know:* The RJ9-to-3.5mm audio path is the one unproven link in the hardware chain, and it is discovered in Phase 3 — too late to reorder.
   - *Recommendation:* **Yes.** ~$30 to eliminate a schedule risk. Include it in the BOM and note the reason so it does not look like scope creep.

---

## Sources

### Primary (HIGH confidence)

- **developers.openai.com/api/docs/guides/spend-limits** — hard spend limits (org + project), "Enforce a hard limit" toggle, spend alerts vs. caps, error codes (`organization_spend_limit_exceeded`, `project_spend_limit_exceeded`, `credit_balance_exhausted`, `organization_usage_limit_exceeded`), non-instantaneous enforcement, dashboard paths. Fetched 2026-08-13.
- **developers.openai.com/api/docs/guides/realtime-websocket** — base64 audio chunks over the socket; WebSocket recommended for server-to-server, WebRTC for browsers/mobile. Fetched 2026-08-13.
- **developers.openai.com/api/docs/guides/realtime-conversations** — audio format `"type": "audio/pcm", "rate": 24000`; output `audio/pcm` and `audio/pcmu`. Fetched 2026-08-13.
- **raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/** — 2025-12-01, full before/after price table, LPDDR4 rationale. Fetched 2026-08-13.
- **raspberrypi.com/news/more-memory-driven-price-rises/** — 2026-02-02, second rise, +$30 on 8GB. Fetched 2026-08-13.
- **thekingsbay.com** (product page + phone-booths category) — $2,195 sale price, 3 in stock, 200 lbs, 89.5"×32"×29.5", ships 5–10 days, "For Indoor or Covered Use Only!", full eight-SKU price list. Fetched 2026-08-13.
- **centerlinedynamics.com** — same product at $3,475.95, same indoor-only rating. Fetched 2026-08-13.
- **pishop.us** — Pi 5 8GB $175 in stock; Pi 5 4GB $110 in stock; USB Audio Adapter $4.95 in stock, "Fully compatible with Raspberry Pi 5," tested on Raspberry Pi OS. Fetched 2026-08-13.
- **canakit.com** — Pi 5 8GB board $175, Starter Kit $269.95, 5V/5A PD requirement, active cooling recommendation. Fetched 2026-08-13.
- **buildeazy.com/red-english-telephone-box/** — K2 build plans: full materials list, tool list, "months of casual work," outdoor-suitable via fibreglass/epoxy. Fetched 2026-08-13.
- **Local repository inspection** — `git ls-files`, `git log`, `git grep`, `du`, `find`, and direct reads of `voice/my-project/{package.json,src/agent.ts,src/main.ts}` and `voice/my-project/my-project/*`. 2026-08-13.
- **`.planning/` corpus** — PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, INGEST-CONFLICTS.md; `call-santa-pre-prd.md` Sections 3, 5.3, 5.4, 11.

### Secondary (MEDIUM confidence)

- **learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/** — CM108 / TI PCM2902 identification via `lsusb`; ALSA configuration. Authoritative for the ecosystem but the fetched page did not cover mic-input specifics.
- **forums.raspberrypi.com/viewtopic.php?t=365923** — UGREEN USB audio on Pi 5 confirmed plug-and-play; warning that UGREEN DACs vary across same-family SKUs.
- **stavros.io — "I converted a rotary phone into a meeting handset"** — handset wired directly to a cheap USB sound card, worked without impedance/bias intervention; hook switch as a plain GPIO-pulled-low switch.
- **purple.ai WiFi signal strength guide** + **NHS England Digital Wi-Fi metrics guidance** — −67 dBm voice baseline, −65 to −72 dBm WebRTC jitter cliff, SNR ≥ 25 dB for QAM256 retention.
- **nassaunationalcable.com NEC outdoor wiring** / **expertce.com NEC 406.9** — SJTW/SJEOW outdoor listing, GFCI on outdoor receptacles, in-use weatherproof covers.
- **finepowertools.com, hunker.com, siliconedepot.com** — three concurring sources on polyurethane-for-wood vs. silicone-for-weather, and the hybrid fill-and-cap approach.
- **raspberry.tips LTE tutorial** + Raspberry Pi forum threads — `mmcli` usage, Huawei MS2372h working with ModemManager, 3G shutdown.
- **Raspberry Pi Spy — wavemon guide** — F2 signal histogram, sampling over time rather than single readings.

### Tertiary (LOW confidence — flagged for validation)

- **hackernoon.com, tokenmix.ai, eesel.ai, layer3labs.io** — Realtime API per-token pricing and observed per-minute costs. Three-way agreement raises confidence, but **the official OpenAI pricing page did not resolve during this session (404 on `developers.openai.com/api/pricing`)**. Assumption A2/A3. Re-verify before setting the spend cap.
- **ai-tldr.dev, blog.alephant.io, satgate.io** — hard spend limit rollout "week of 22 July 2026" and the earlier removal of caps. The *mechanism* is confirmed by official docs; only the rollout date and the historical sequence rest on these.
- **Amazon product listings** (ECVISION B00A8BOTWQ, Opis B0087PQGXU, UGREEN B087T5H3MQ) — Amazon returned 403/500 to automated fetch throughout. All Amazon prices are from search-result snippets and must be human-confirmed at purchase.
- **Etsy / eBay listings** — all blocked automated fetch. Option B's $300–600 band is the weakest number in this document.

---

## Metadata

**Confidence breakdown:**
- **Repo cleanup (OPS-01): HIGH** — every claim verified by direct command output in this session. Nothing rests on inference.
- **OpenAI spend-limit mechanics (OPS-03): HIGH** — official documentation fetched and quoted directly.
- **OpenAI cost model (OPS-03 sizing): MEDIUM-LOW** — three concurring secondary sources, official pricing page unreachable. Flagged as A2/A3.
- **Enclosure pricing and outdoor rating (HW-01): HIGH for the mahogany path** (two independent retailers, both fetched directly); **LOW for the mid-band alternative** (marketplaces blocked automated fetch).
- **Pi 5 pricing and availability (HW-01): HIGH** — official Raspberry Pi price announcements plus two official resellers, all fetched today. Note this is a volatile line; re-check at purchase.
- **USB audio guidance (HW-01/HW-03): MEDIUM-HIGH** — Adafruit is the ecosystem authority and a Pi reseller sells a tested part; the TRRS-vs-dual-jack warning is inference from product descriptions and is the weakest link.
- **Site survey methodology (HW-06): MEDIUM-HIGH** — the tooling and commands are standard and well-documented; the bandwidth target is derived arithmetic from a verified audio format; the thresholds come from concurring industry sources. The LTE quality bands are conventional rather than cited (A5).
- **Outdoor electrical (adjacent): MEDIUM-HIGH** — NEC citations are second-hand through electrical-trade sites rather than the code text itself. Directionally reliable; a licensed electrician trumps this document.

**Research date:** 2026-08-13
**Valid until:** **2026-08-27** — 14 days. This is a short window deliberately: Raspberry Pi pricing has moved twice in eight months and resellers are above list; the King's Bay booth has **3 units in stock** and is on sale; and OpenAI's hard spend limit feature is roughly three weeks old. Every price in this document must be re-confirmed at the moment of purchase, and the OpenAI dashboard UI may have shifted since the docs were written.
