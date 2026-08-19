# Phase 1 Procurement List (non-compute, long-lead)

**Owner:** the human placing the orders
**Plan:** 01-05 (wave 2)
**Requirement:** HW-01
**Written:** 2026-08-18
**Phase 1 must complete by:** 2026-08-25. The enclosure is the longest-lead item in the project.

## How to use this list

Every line carries a **spec qualifier** — the property that makes it the right part. Buy against the
qualifier, not against the product title. "Sealant", "cable gland" and "retro phone" each describe
both a working choice and a failing one, and the failing one is usually cheaper and better reviewed.

Prices below are **research-date estimates** (2026-08-13). Per D-16, **actual-at-checkout is
authoritative** — confirm the live price before buying and record what you actually paid in the
matching order file. Do not treat a number on this page as a budget commitment.

Nothing on this list depends on the compute comparison (D-13). Do not wait for it.

Record each purchase in:

- `evidence/orders/enclosure-order.md`
- `evidence/orders/phone-order.md`
- `evidence/orders/site-hardware-order.md`

---

## Enclosure

**Decision reference:** D-01.

**Reference product:** Ilyapa Outdoor Library Book Box — 16" x 14" x 22", solid wood, all-weather
finish, plexiglass front door, magnetic latch, 4x4 post mount. Amazon ASIN `B0CPN4K6LP`.
Expected roughly **$150-230** (approximately $226 seen on eBay at research time; live price to be
confirmed at checkout).

**Required field at checkout — copy the vendor's own words verbatim:**

`Outdoor rating as stated by vendor:`

This field exists because of RESEARCH "Common Pitfalls" pitfall 4. The source PRD asserted that the
originally-specified booth "provides full weatherproofing for the internal electronics"; both
retailers selling that product state "For Indoor or Covered Use Only!". Phase 3's weatherproofing
scope (HW-05) is sized against whichever claim is believed, so the vendor's wording is recorded as
evidence rather than inferred from a product description. Copy it even if it says something
inconvenient. **An unrecorded rating is the same as an unverified one.**

**Acceptance criteria an equivalent cabinet must meet** (if the reference item is unavailable, or if
its live price exceeds roughly $280 — substitute rather than escalating, and record which criterion
drove the substitution):

| # | Criterion | Why it is the qualifier |
|---|-----------|-------------------------|
| 1 | Solid wood **or** weatherproof composite | MDF and untreated ply do not survive a wet December outdoors |
| 2 | Interior-capable of at least 15" x 13" x 20" | See the fit check below — anything smaller will not take the phone plus the compute |
| 3 | Genuinely outdoor-rated (per the vendor's own wording) | See pitfall 4 above |
| 4 | 4x4-post mountable | D-02 mounts this on a set post at child height; a ground-standing box is not the plan |

**Interior fit check that justifies the size.** A full rotary desk set is roughly 9" x 9" x 5.5". The
reference cabinet gives a usable cavity of roughly 14.5" x 12.5" x 20.5". That leaves comfortable room
for the phone, the compute (whichever plan 04 selects), the USB audio adapter and the wiring, with the
electronics mounted high and to the rear in a sealed inner enclosure per D-03.

### This supersedes the roadmap's mahogany walk-in booth. Do not order that booth.

The originally-cited King's Bay red British mahogany booth replica was verified on 2026-08-13 at:

- **$2,195.00** (sale price; list $2,795.00) — three times the entire remaining project budget
- **200 lbs**, 89.5"H x 32"W x 29.5"D, arrives fully assembled (freight/liftgate handling likely)
- Rated **"For Indoor or Covered Use Only!"** by both retailers carrying it

The all-in project cost on that path lands near $2,630 against a $850-1,050 ceiling, and it puts a
200 lb, 7.5 ft indoor-rated structure in a front yard used by unsupervised children. Every solid-wood
full-size booth found in research sits between $2,195 and $3,476; there is no $600-800 mahogany
walk-in booth in the current US market. The price is recorded here so this decision is not
re-litigated later from memory.

Nothing in HW-01 through HW-05 requires a walk-in booth. What is required is a weatherproof box at
child height that holds the phone, the compute and the status LEDs.

---

## Phone

**Decision reference:** D-17, resolving CD-06 by purchase.

**Buy a full corded or rotary phone — not a standalone handset.** The moulded cradle, the hook plunger
with the correct travel, and a handset that physically sits in it are the hard mechanical parts.
Fabricating a cradle that reliably actuates a lever-arm microswitch, with enough travel, no rattle and
a correct rest position, is fiddly woodwork that would otherwise land on Phase 3's critical path.
Buying it assembled keeps it off that path. It also simply reads better: a bare handset dangling in a
box reads as broken; a whole phone reads as an invitation.

**Reference product:** ECVISION 1960s Style Rotary Retro Phone, red. Amazon ASIN `B00A8BOTWQ`.
Expected roughly **$70**.

**Price confidence: ASSUMED, not verified.** Amazon blocks automated fetch, so research could not
confirm the live price. The PRD said $35; the search result suggested about $70. Actual-at-checkout
governs (D-16).

**Acceptable equivalents:** any full-body corded or rotary reproduction with an intact cradle and a
working hook mechanism. Confirm from the product photos that the cradle is present.

**Explicit exclusion: do not buy a "USB retro handset."** Several exist, they are cheap, and they are
plug-and-play — which is exactly why they get recommended. They enumerate as their own USB audio
device and **they have no cradle**, so buying one buys back the precise problem the full phone was
chosen to solve.

**Carried to Phase 3 as a note, not as a purchase — the audio path.** A full retro phone connects its
handset to the base with an **RJ9/RJ22 (4P4C) modular plug**, carrying a mic pair and a receiver pair
at telephone levels. A USB audio adapter expects **3.5mm jacks at computer levels**. These do not
connect without intervention: the cord will need re-terminating into 3.5mm plugs, or an RJ9-to-3.5mm
breakout. One documented conversion reports this working without special impedance or bias handling,
but that is a single data point. Modern reproduction handsets normally use electret mics, which a
CM108-class input biases correctly; a carbon-mic-era original would not work.

A spare 3.5mm handset (~$30) was considered as insurance against this path and **explicitly deferred
by CONTEXT.md**. Do not add it to this order. Revisit only if the audio phase hits trouble.

---

## Post-mount hardware

**Decision reference:** D-02. Ordered **now**, in Phase 1, specifically so the concrete footing has
cure time before the Phase 3 install window opens. Do not defer these to the install phase.

| Item | Spec qualifier | Notes |
|------|----------------|-------|
| 4x4 post, pressure-treated | Pressure-treated for ground contact; untreated wood rots at the soil line within a season | Length chosen so the cabinet sits at child height once the below-grade portion is buried |
| Fast-setting concrete mix | Fast-setting, sized for **one** post hole | Fast-setting is the qualifier — standard mix extends the cure window this order exists to protect |
| 4x4 post cap | Sized to the actual post (a nominal 4x4 measures about 3.5") | An open end grain on top of a post wicks water straight down the post |
| Post-mount hardware / brackets | Must match the cabinet's own mounting provision | Confirm against the cabinet listing before ordering, not after it arrives |

---

## Weatherproofing and cable entry

**Decision reference:** D-05, plus RESEARCH "Outdoor Electrical".

- **IP68 compression cable gland**, PG or M-series, **sized to the cable outside diameter**, entering
  the enclosure from **underneath or a downward-facing face**. A top or vertical-face entry invites
  water to track down the cable and into the box. Buy a **multi-pack** — roughly $10, 3-5 day ship.
  This is the one item on this list plausibly not stocked locally, which is exactly why it is ordered
  in Phase 1: it costs nothing and its absence would stall Phase 3.

- **Exterior polyurethane sealant, paintable** — for the wood joints. Polyurethane adheres to wood far
  better than silicone and it takes paint. Silicone does neither, and performs poorly on porous
  substrates.

- **100% silicone sealant** — for the plexiglass pane and the exposed weather edges. Up to roughly
  four times the service life of polyurethane in direct sun. **Both types are needed**: the
  professional approach is to fill the joint with polyurethane and cap the exposed bead with silicone.
  A tube labelled "siliconized latex" or "silicone*ized*" is not 100% silicone.

- **Breather / pressure-equalisation vent** — a Gore-style vented plug, roughly $5-10, or at minimum a
  **downward-facing** louvre with a bug screen. A sealed wooden box that warms from the compute by day
  and drops to 20F overnight condenses water on the coldest interior surface, which is the
  electronics. This failure mode is the classic omission and the fix is trivially cheap.

- **Silica gel desiccant packs** — the second half of the condensation fix. Buy rechargeable
  (oven-dryable) packs if the option costs the same. Roughly $15 for the vent and desiccant together.

- **Handset anchor point** for inside the cabinet (D-04) — a hook, a clip or a short retention lanyard.
  There is no booth hook to hang the handset on; without this, the handset lies on the cabinet floor
  where water collects.

- **Zip ties and cable management** — commodity. The qualifier: UV-resistant (black) ties, not the
  clear/natural nylon that goes brittle in sunlight.

---

## Explicitly excluded from this list

Each line names why it is excluded and which plan owns it, so nothing here is re-decided by accident
and nothing is silently dropped.

| Excluded item | Reason | Owner |
|---------------|--------|-------|
| Camera, or any imaging line item | Out of v1 entirely — no hardware, no mount point, no budget line (CD-05, D-15) | Nobody. It does not get bought. |
| Compute (Raspberry Pi 5 or laptop retrofit) | The Pi-vs-laptop comparison is not pre-committed (D-10) | Plan 08 |
| USB audio adapter | Selection depends on the compute path | Plan 08 |
| Lever-arm microswitch, status LEDs, resistors, jumper wiring | Hook-switch input path depends on the compute path (D-11) | Plan 08 |
| Ethernet cable (outdoor-rated / direct-burial Cat6) | Only bought on the ethernet branch (D-06, D-07) | Plan 07 |
| PoE injector | Only bought on the ethernet branch (D-07) | Plan 07 |
| LTE dongle | Only bought if the wireless survey selects LTE (D-08) | Plan 07 |
| Weatherproof extension cord, in-line GFCI, in-use outlet cover | Removed from the BOM entirely under the ethernet-plus-PoE branch, where one cable carries power and network (D-07) | Plan 07 |
| Spare 3.5mm handset (~$30) | Considered as audio-path insurance and explicitly deferred by CONTEXT.md | Deferred; revisit in the audio phase |
| The King's Bay mahogany walk-in booth | $2,195, 200 lbs, indoor-rated — superseded by D-01 | Nobody. Do not order it. |

**The mahogany booth exclusion is not a budget deferral.** It is a scope decision (D-01) that also
resolves a child-safety and a weatherproofing problem. Re-adding it later reopens all three.

---

## Expected subtotal

Against the D-14 reference math:

| Group | Estimate |
|-------|----------|
| Enclosure | ~$150-230 (reference: ~$200) |
| Post, concrete, post cap, brackets | ~$60-90 |
| IP68 gland multi-pack | ~$10 |
| Polyurethane + 100% silicone sealant | ~$20 |
| Breather vent + silica gel desiccant | ~$15 |
| Handset anchor, UV zip ties, cable management | ~$15 |
| Phone (full corded/rotary) | ~$70 |
| **This list, subtotal** | **~$340-450** |

D-14's reference math is roughly $200 enclosure plus roughly $433 of non-enclosure BOM, or about
$633 in total, leaving headroom inside the **$850-1,050 ceiling** once plan 08's compute lines and
plan 07's connectivity lines land. This list stays comfortably inside that envelope.

Plan 10 reconciles every actual price paid against this ceiling in `budget-actual.md`. That
reconciliation reads the `Actual price paid (USD):` field out of the three order files, which is why
that field is mandatory and why an estimate must never be written into it.
