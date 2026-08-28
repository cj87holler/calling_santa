# Ethernet Scoping — Field Form

**This is a form, not a document.** Every line below ending in `____` is a blank you fill in
**while standing in the front yard with a tape measure**. Nothing in this file can be answered
from indoors. D-09: a connectivity decision without a cited number does not satisfy HW-06.

Work top to bottom. The form is ordered so you walk the yard once, not three times.

---

## Before you go outside — what to carry

- Tape measure **or** measuring wheel (a wheel is far easier for a 60–100 ft cable route)
- One stake, paver, or garden flag — the physical spot marker
- Phone (to fill this form) and a pen for the paper fallback
- Optional: a length of string or a spare extension cord to lay along the route if a wheel
  is not available — you can measure the string indoors afterwards

---

## Formatting rules — read these once, they matter

The phase gate (`verify.sh`) greps this file with **line-anchored** patterns. Three lines must be
formatted exactly, or a genuine yard visit will still fail the gate:

1. `Spot marker placed: yes` — starts at column 0 (no leading spaces), **nothing after the value**.
2. The `Measured cable run length (ft):` line must carry a **bare number in whole feet, digits
   only** — no tilde, no approximation, no range, no unit suffix, no words. If you measured a
   range, record the longer end. (No worked example is printed here on purpose: a sample number
   next to that label would satisfy the gate from indoors, which is the one thing this assertion
   exists to prevent.)
3. `VERDICT: FEASIBLE` or `VERDICT: NOT FEASIBLE` — column 0, **exactly one space** after the colon,
   uppercase, **nothing after the value** (the rationale goes on its own line below it).

For every other field, replace `____` with your answer and leave the surrounding text alone.
Do not leave a placeholder standing in for an answer — an unanswered field is a failed gate.
If a field genuinely does not apply, write `n/a` and say why in the rationale.

**Privacy (T-1-12):** this file is committed to the repository. Use **landmark-relative**
references only — "9 ft due south of the porch post". Never record a street address, a full
postal address, or GPS coordinates.

---

## A. Install spot

This is the exact point the cabinet post gets set in. **Every later measurement in this project
references it**, including plan 07's wireless survey, so mark it physically before measuring
anything. Measurement height is fixed at **48 in** by `survey-protocol.md` — do not change it.

The next line must read `Spot marker placed: yes` or `Spot marker placed: no`, with nothing
after the value:

Spot marker placed: ____

    Spot marker used:                            ____   (stake, paver or flag actually placed)
    Landmark reference:                          ____   (distance and bearing from a fixed
                                                         feature, e.g. "9 ft due south of the
                                                         porch post" — no street address)
    Distance from house wall to spot (ft):       ____
    Measurement height:                          48 in  (fixed by protocol — do not change)

> Record the identical marker and landmark reference in `survey-protocol.md`'s **Install spot**
> group while you are out here. If the two files ever disagree about where the spot is, every
> distance in the project is measured from a different point than the one that gets dug.

---

## B. Ethernet route

Walk the route the cable would actually take — around the corner, along the soffit, down the wall,
across the yard. Do **not** measure the straight line through the house; you cannot lay cable
through a foundation.

    Interior termination point:                  ____   (where the router or switch physically is,
                                                         e.g. "office closet, north wall")
    Route description:                           ____   (the path in order, e.g. "office wall ->
                                                         attic -> front soffit -> down downspout ->
                                                         along bed edge -> spot")

The next line must carry a bare number in whole feet, digits only:

Measured cable run length (ft): ____

    Length to order (ft):                        ____   (measured length + 20% slack, rounded UP
                                                         to a stock length: 75 / 100 / 150 / 200)
    Proposed exit point location:                ____   (where the cable leaves the house)
    Exit point construction:                     ____   (allowed: soffit | rim joist | wall cavity |
                                                         existing penetration | other)
    Can the exit point be sealed:                ____   (allowed: yes | no)
    Sealing method:                              ____   (compression gland, cable boot, exterior
                                                         sealant, or "none identified")
    Drilling required:                           ____   (allowed: yes | no)
    Drilling material:                           ____   (siding, brick, rim joist, soffit panel,
                                                         or "n/a")
    Obstacles on the route:                      ____   (driveway, walkway, planting bed, tree
                                                         roots, buried utilities, or "none")
    Buried-utility locate needed (811 call):     ____   (allowed: yes | no)
    PoE source available:                        ____   (allowed: PoE switch | PoE injector needed |
                                                         none)

> **811 rule of thumb:** you need a locate if the route is buried at any depth across open ground,
> or bored under a walkway or driveway. A cable run stapled along a fence line, tucked under bed
> mulch, or laid in a surface conduit does not require one. The call is free and takes a few
> business days — its cost is schedule, not money.

---

## C. Outdoor outlet inspection

**Do this on the same trip.** It is free while you are already standing in the yard, and it is
the last chance before November. Remediation is deferred to the install phase — recording the
finding now is the entire deliverable (T-1-09, NEC 210.8 and 406.9(B)).

    Outlet present at intended power point:      ____   (allowed: yes | no)
    GFCI protection present:                     ____   (allowed: yes | no | unknown)
    In-use (bubble) weatherproof cover present:  ____   (allowed: yes | no)
    Distance from outlet to install spot (ft):   ____

> **How to tell.** *GFCI:* look for **TEST** and **RESET** buttons on the outlet face. If they are
> absent, the outlet may still be protected by a GFCI upstream — another outlet on the same circuit,
> or a GFCI breaker in the panel. If you cannot confirm it in under two minutes, write `unknown`;
> that is an honest answer and it carries forward exactly the same as `no`.
>
> *In-use cover:* a **bubble** cover is a deep clamshell that closes **with a plug still inserted**.
> A flat flip lid that only shuts when the outlet is empty is **not** an in-use cover — answer `no`.

---

## D. Verdict

**Decision rule.** Mark `FEASIBLE` only when **all three** are true:

1. `Measured cable run length (ft)` is **at or under 300**. The Cat6 limit is 328 ft / 100 m;
   the last 28 ft are margin for slack, terminations and route error.
2. An exit point exists that **can be sealed** — `Can the exit point be sealed: yes` with a named
   method. An unsealed penetration admits water into the wall cavity, not just the enclosure (T-1-10).
3. No route obstacle requires trenching under a driveway, **and** no buried-utility locate is needed
   that you are unwilling to schedule.

Mark `NOT FEASIBLE` otherwise. **If the run is technically possible but only via a route you do not
want to cut, that is still `NOT FEASIBLE`.** Record the real reason. A technical yes that never gets
executed sends the whole project down the wrong branch and costs a weekend of RF measurements you
skipped.

Do not fill this line until `Measured cable run length (ft)` above holds a real number.

The next line must be `VERDICT: FEASIBLE` or `VERDICT: NOT FEASIBLE` — column 0, one space after
the colon, nothing after the value:

VERDICT: ____

    Rationale (one line, citing the measured
    length and the exit-point assessment):      ____

---

## E. What happens next

Once this form is complete, one word gets written to `CONNECTIVITY-BRANCH` in this directory and
every downstream plan reads it:

| This verdict | Branch word | Consequence |
|---|---|---|
| `VERDICT: FEASIBLE` | `ethernet` | Plan 07 skips the three 20-minute wireless windows; the BOM gains outdoor-rated Cat6 and PoE and loses the weatherproof extension cord |
| `VERDICT: NOT FEASIBLE` | `wireless` | Plan 07 runs the full three-window RF survey; the weatherproof extension cord stays in the BOM |

The `## Downstream consequences` section is appended to this file by the agent after the branch is
set. Do not write it by hand.
