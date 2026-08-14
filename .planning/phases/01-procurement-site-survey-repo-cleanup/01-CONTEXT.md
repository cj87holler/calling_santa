# Phase 1: Procurement, Site Survey & Repo Cleanup - Context

**Gathered:** 2026-08-13
**Status:** Ready for planning
**Source:** Interactive decisions captured during `/gsd:plan-phase 1` (user declined a separate discuss-phase pass, then supplied direction in response to research findings)

<domain>
## Phase Boundary

Place every long-lead purchase and answer every question that could invalidate the build plan,
within two weeks, so shipping time runs in parallel with software work instead of after it.

**In scope:** enclosure + phone + electronics procurement, connectivity path determination,
OpenAI spend ceiling, repo cleanup and credential rotation.

**Out of scope:** any physical assembly, mounting, or installation; any application code;
audio tuning; theming/decoration. Those belong to later phases.

**Material change from ROADMAP.md:** research proved the roadmap's enclosure spec and its budget
are mutually exclusive (the cited mahogany booth is $2,195, not $600–800, and is rated
"Indoor or Covered Use Only"). D-01 below resolves this by changing the enclosure form factor.
ROADMAP.md success criterion 1 should be read as superseded by D-01.

</domain>

<decisions>
## Implementation Decisions

### Enclosure (supersedes ROADMAP CD-07)

- **D-01 —** The enclosure is a **post-mounted outdoor library-box style wooden cabinet**
  (reference: Ilyapa 16" × 14" × 22" solid wood, all-weather finish, plexiglass front door,
  magnetic latch, 4×4 post mount — ASIN B0CPN4K6LP, ~$150–230), **not** a walk-in mahogany
  phone booth. Rationale: the mahogany booth is $2,195 (3× the entire remaining budget), is
  explicitly indoor-rated, and puts 200 lbs in a front yard used by unsupervised children.
  The library box is genuinely outdoor-rated, ships in days, and mounts at child height.
  An equivalent cabinet from another vendor is acceptable if it meets the same criteria:
  solid wood or weatherproof composite, ≥15" × 13" × 20" interior-capable, outdoor-rated,
  4×4 post mountable.
- **D-02 —** Post-mount hardware (4×4 post, concrete, post cap) is a **Phase 1 order line
  item**, not deferred to the install phase — the footing needs cure time before install.
- **D-03 —** Electronics mount in a **sealed inner enclosure** positioned high and to the rear
  of the cabinet. The plexiglass door protects only when closed; the interior is open every
  time a child uses the phone. Nothing critical sits loose on the cabinet floor.
- **D-04 —** The handset requires an **anchor point inside the cabinet**. There is no booth
  hook to hang it on.
- **D-05 —** Cable entry through the cabinet floor or back panel uses a gland/grommet plus
  sealant. Drilling a finished weatherproof box means the penetration must be resealed.

### Connectivity (CD-04a — NOT yet resolved; branch pending)

- **D-06 —** **Wired ethernet is the preferred path** and must be scoped before the wireless
  survey is run. A scoping task walks the route from house to install spot, measures cable
  length, identifies the wall/soffit exit point, and determines whether it can be sealed.
- **D-07 —** If the ethernet run is feasible: use **outdoor-rated or direct-burial Cat6**
  (never indoor PVC-jacket — UV and moisture destroy it within a season), and prefer **PoE**
  so one cable carries power and network, eliminating the separate weatherproof extension
  cord from the BOM.
- **D-08 —** If the ethernet run is **not** feasible: fall back to the full wireless site
  survey as specified in RESEARCH.md — ≥3 × 20-minute measurement windows, raw sample series
  committed, WiFi vs. LTE chosen on measured numbers against the pass bar (≥2 Mbps sustained,
  RSSI ≥ −67 dBm, SNR ≥ 25 dB, loss < 0.5%, jitter < 30 ms).
- **D-09 —** The connectivity decision is recorded with the measurement or the scoping
  evidence that justifies it. A decision without a cited number does not satisfy HW-06.

### Compute (largest BOM line — decide before ordering)

- **D-10 —** The Pi-vs-laptop choice is **not pre-committed**. A short comparison task runs
  first, evaluating: Raspberry Pi 5 8GB (~$125–175, GPIO for the hook switch, no battery,
  cheap to replace) against an existing old laptop with the **battery physically removed**
  (~$10 for a Pico to read the hook switch, saves the largest line item, but bulkier, fan
  draws outdoor air through it, and needs BIOS "restore on AC power loss" plus sleep and
  lid-close disabled).
- **D-11 —** Whichever is chosen, the hook-switch input path must be concrete: GPIO header
  on the Pi, or a USB microcontroller (Pico/Arduino) on the laptop. "Figure it out later"
  is not an acceptable output of the comparison.
- **D-12 —** A laptop permanently installed outdoors **must** have its battery removed.
  A lithium cell held at full charge through outdoor temperature swings, sealed in a wooden
  box, unattended, near children, is a real hazard — not a hypothetical one.
- **D-13 —** The comparison task is time-boxed and must not block the non-compute orders.
  Enclosure, phone, post hardware, cabling and sundries are ordered in parallel with it.

### Budget

- **D-14 —** The ~$850–1,050 ceiling **stands**, made achievable by D-01. Reference math:
  ~$200 enclosure + ~$433 non-enclosure BOM ≈ $633, leaving headroom for post, concrete,
  cable and sealant.
- **D-15 —** **No camera line item.** (ROADMAP constraint — unchanged.)
- **D-16 —** Every order records vendor, SKU, actual price paid, order number and delivery
  ETA. Prices in RESEARCH.md are research-date estimates; actual-at-checkout is authoritative,
  and Pi 5 pricing in particular has moved twice since the PRD ($80 → $95 → $125 list).

### Phone

- **D-17 —** A **full corded/rotary phone** (ROADMAP CD-06 — unchanged), not a standalone
  handset. Sourced to be gutted; the hook switch is retrofitted with a lever-arm microswitch.

### OpenAI spend controls

- **D-18 —** Configure a **$150/month hard spend limit** with **enforcement enabled** (not
  alert-only), and alerts at **50% / 75% / 90%**. Auto-recharge stays **off**.
- **D-19 —** The existing $5 balance is **not** accepted as the ceiling. It is an accidental
  cap that disappears on the first top-up and fails closed mid-call.
- **D-20 —** Re-verify current Realtime pricing against openai.com **before** setting the
  figure — the official pricing page 404'd during research, so the cost model rests on
  secondary sources. If pricing has moved materially, surface it rather than silently
  applying $150.
- **D-21 —** Issue the device key inside a **dedicated OpenAI project** so the spend limit
  can be project-scoped and the credential is least-privileged.

### Repo cleanup

- **D-22 —** **Delete** `voice/my-project/`. Evidence: added in the first commit, referenced
  by zero code and zero docs, an untouched duplicate Vite scaffold, and its `src/main.ts`
  inlines a standing API key into browser code via `VITE_OPENAI_API_KEY` — the exact pattern
  OPS-02 forbids. The "document it in the README" branch is rejected.
- **D-23 —** **Order of operations is mandatory: check `.env` → rotate/revoke the key →
  then delete.** An untracked `.env` exists on disk there now. Deleting first orphans a live
  credential.
- **D-24 —** Never `cat` the `.env` or echo its contents into a transcript, log, or commit.
  Assert shape and existence only. Screenshots of the OpenAI dashboard must not show a key value.
- **D-25 —** Author a **root `README.md`** — none exists today. OPS-01's "exactly one
  authoritative implementation path" clause cannot be satisfied without it. It must name
  `poc/` as the authoritative path and must not embed any key.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase research and validation
- `.planning/phases/01-procurement-site-survey-repo-cleanup/01-RESEARCH.md` — costed enclosure
  options, current Pi 5 pricing, USB audio chipset guidance, site-survey protocol and pass bar,
  OpenAI spend-control mechanics, repo-cleanup evidence, Validation Architecture, Security Domain,
  and an Assumptions Log (A1–A6) naming what is unverified
- `.planning/phases/01-procurement-site-survey-repo-cleanup/01-VALIDATION.md` — the required
  assertion set, evidence tree layout, Wave 0 gaps, and manual-only verifications

### Project scope and requirements
- `.planning/REQUIREMENTS.md` — HW-01, HW-06, OPS-01, OPS-03 (and OPS-02, which D-22 relates to)
- `.planning/ROADMAP.md` — Phase 1 section; note success criterion 1 is superseded by D-01
- `.planning/PROJECT.md` — project overview and constraints
- `.planning/INGEST-CONFLICTS.md` — carried-forward unresolved decisions (CD-04a, CD-06, CD-07)

### Existing implementation
- `poc/` — the authoritative implementation path (server-side ephemeral token broker pattern)
- `voice/my-project/` — to be deleted per D-22; do not build on it

</canonical_refs>

<specifics>
## Specific Ideas

- Reference enclosure: Ilyapa Outdoor Library Book Box, 16" × 14" × 22", ASIN `B0CPN4K6LP`
  (~$226 seen on eBay; live Amazon price to be confirmed at checkout).
- Interior fit check: a full rotary desk set is roughly 9" × 9" × 5.5" in a ~14.5" × 12.5" × 20.5"
  usable cavity — comfortable, with room for compute, USB audio adapter and wiring.
- Theming direction (deferred to a later phase, noted so it isn't lost): the cabinet reads as a
  "Direct Line to the North Pole" call box rather than a generic phone booth. Easier to decorate
  than a walk-in structure.
- Site-survey pass bar derived in research: ≥2 Mbps sustained per direction, RSSI ≥ −67 dBm,
  SNR ≥ 25 dB, loss < 0.5%, jitter < 30 ms. Report p95, not mean.
- LTE fallback data volume: ~12 GB/month — rules out small IoT data plans.

</specifics>

<deferred>
## Deferred Ideas

- **Acoustic/echo treatment** — a small hard-walled cavity with a plexiglass face is an echo
  chamber. Largely moot if audio runs through the handset earpiece and mic as designed, but a
  problem for anything open-air. Defer to the audio phase; do not solve here.
- **Theming and decoration** of the cabinet — later phase.
- **Physical mounting, post setting, anchoring and wind load** — install phase. Phase 1 only
  *orders* the post hardware (D-02).
- **GFCI / in-use outlet cover verification** — free to check while standing in the yard during
  the connectivity scoping task; record the finding, but remediation is an install-phase task.
- **Spare 3.5 mm handset (~$30) as insurance** against the unproven RJ9 audio path — research
  suggested it; not adopted as a Phase 1 purchase. Revisit if the audio phase hits trouble.

</deferred>

---

*Phase: 01-procurement-site-survey-repo-cleanup*
*Context gathered: 2026-08-13 during /gsd:plan-phase 1*
