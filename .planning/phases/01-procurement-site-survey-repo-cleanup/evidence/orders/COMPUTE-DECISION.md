DECISION: pi-5

**Date:** 2026-09-01
**Rationale:** The owner selected the Raspberry Pi 5 — purpose-built for this job, the GPIO header
handles the hook switch and the three HW-04 status LEDs with zero added hardware, no lithium battery
sits in a sealed outdoor box near children, and every documented rotary-phone conversion in research
used exactly this path. The 4GB-vs-8GB memory lever ($65) was priced but deliberately not pulled,
because CD-03 is still open and one of its candidate outcomes puts Prometheus and Grafana on this
same board.

**Plan:** 01-04 (wave 2), task 3
**Decision reference:** D-10, D-11, D-13, D-14, D-16
**Source:** `evidence/orders/COMPUTE-COMPARISON.md`, configuration A1 (board-only, 8GB)
**Requirement:** HW-01 (order lines satisfy HW-02, HW-03, HW-04 downstream in Phase 3)

---

## Sub-choices confirmed by the owner

- **Memory: 8GB (part SC1112), not 4GB.** The recommendation's reasoning was accepted as-is: CD-03
  remains open, and a candidate outcome of that decision places Prometheus and Grafana on this same
  board. The $65 memory-saving lever is deliberately not pulled.
- **Configuration: board-only from pishop.us (comparison configuration A1), not the CanaKit starter
  kit (A3).** A1 is a single vendor, single shipment, all-in **$239.75**, everything in stock today.
  A3 costs $45.15 more, ships from a second vendor, and its bundled PSU's wattage could not be
  confirmed from the product page at fetch time — an unnecessary re-introduction of the pitfall-8
  under-powering risk that A1 avoids by ordering the official 27W supply explicitly.

**Hook-switch input path:** **GPIO header, a normally-closed lever-arm microswitch wired to a GPIO
pin with an internal pull-up, pin number to be assigned in Phase 3.** The 40-pin header is already
present on the board — this costs $0.00 in additional hardware, requires no firmware, no protocol
and no second device. The same header also carries the three HW-04 status LEDs. No Pico, no Arduino
and no USB microcontroller is needed or ordered on this path.

**Power draw, for plan 07's PoE splitter sizing:** the Raspberry Pi 5 is powered by the official 27W
(5V/5A) USB-C PD supply ordered below. Typical board draw under this workload (Python session
manager, one WebSocket, a small admin web service, node_exporter, USB audio adapter, active cooler
fan) is well under the 27W ceiling, but the supply — and therefore the PoE splitter output plan 07
must size to — must support the full 5V/5A (25W) envelope so the active cooler and USB peripherals
never hit the current-limit throttling described in pitfall 8 below.

---

## ORDER LINES

Plan 08 purchases these lines verbatim. Prices are those fetched 2026-08-27 in
`COMPUTE-COMPARISON.md`; per D-16, actual-at-checkout is authoritative.

| Item | Required spec | Vendor | SKU | Qty | Unit price | Line |
|------|---------------|--------|-----|-----|------------|------|
| Raspberry Pi 5, 8GB, board only | 8GB LPDDR4X, board only (no case/PSU bundled) | pishop.us | SC1112 | 1 | $175.00 | $175.00 |
| Raspberry Pi 27W USB-C PD supply, US plug | **5V/5A, 27W official supply — never a generic charger.** An undersized supply causes USB current-limit throttling that presents in December as random mid-call audio dropouts, the hardest class of bug to diagnose in a sealed cold box. | pishop.us | SC1158 (black) or SC1153 (white) | 1 | $12.95 | $12.95 |
| Raspberry Pi Active Cooler | Official active cooler for Pi 5 — the board's 0-50°C rated ambient plus self-heating inside a sealed inner enclosure needs active cooling | pishop.us | SC1148 | 1 | $10.95 | $10.95 |
| SanDisk Ultra microSDHC 32GB, blank | 32GB or larger. **Two cards, not one** — a corrupted card in late November with no spare is a season-ending event; at $14.95 each this is the cheapest insurance in the entire BOM | pishop.us | — | 2 | $14.95 | $29.90 |
| Raspberry Pi Case for Pi 5, black/grey | Official case for the bare board | pishop.us | — | 1 | $10.95 | $10.95 |
| USB audio adapter, unit 1 | **Two separate 3.5mm jacks — one pink mic-in, one green line-out — not a single combined TRRS headset jack.** Driverless via the standard USB Audio Class driver, satisfying HW-03. Known-good chipsets: C-Media CM108 or CM119, or TI PCM2902. Confirm the jack layout from the product photo before ordering | pishop.us ("USB Audio Adapter — Works with Raspberry Pi") | — | 1 | $4.95 | $4.95 |
| USB audio adapter, unit 2 | Same spec as unit 1 — two separate 3.5mm jacks, not TRRS — from a **different vendor or chipset** than unit 1, so a dead mic input discovered in Phase 3 is a swap and not a re-order. Neither named reseller stocks a second distinct SKU; price at checkout | second vendor, UNVERIFIED | — | 1 | UNVERIFIED (~$5 class) | UNVERIFIED |
| Normally-closed lever-arm microswitch kit, with jumper wiring | Normally-closed, lever-arm, reporting off-hook and on-hook with no bounce-induced false sessions, satisfying HW-02. Not stocked by pishop.us or canakit.com; price at checkout | UNVERIFIED vendor | — | 1 | UNVERIFIED | UNVERIFIED |
| Status LEDs and resistors | Three discrete LEDs plus current-limiting resistors for the HW-04 three-state indicator, GPIO-driven. Not stocked as a matched kit by either named reseller; price at checkout | UNVERIFIED vendor | — | 1 set | UNVERIFIED | UNVERIFIED |
| Sealed inner enclosure, with standoffs or mounting bracket | **IP65 or better**, ABS or polycarbonate project box, gasketed lid, internal dimensions at least 1 inch larger than the Pi 5 in its case on every axis, bracket-mountable high and to the rear of the D-01 cabinet (D-03). Sized to the Pi 5 footprint (roughly 3.7" x 2.4" x 1.2" boarded, ~6" x 5" x 3.5" sealed) now that the compute path is locked — not the oversized laptop-class footprint the overdue branch would have required. Not stocked by either named reseller; price at checkout | UNVERIFIED vendor | — | 1 | UNVERIFIED | UNVERIFIED |
| **Priced subtotal (compute path, A1)** | | | | | | **$239.75** |

Six lines above are fully priced today at $239.75 all-in for the compute itself. Four remaining
lines (second audio adapter, microswitch kit, LED/resistor set, sealed inner enclosure) are not
carried by pishop.us or canakit.com and are named with their spec qualifiers rather than an invented
price, per D-16.

---

## Exclusions carried forward from every branch

No video or imaging component of any kind is included — CD-05 and D-15 lock it out of v1.

No spare 3.5mm handset is included — CONTEXT.md defers it explicitly; the rotary phone's RJ9 audio
path is Phase 3's risk to carry.

No outer cabinet, phone body, post-mount hardware, sealant, gland, vent or desiccant appears above —
plan 05 owns those. No ethernet cable, PoE injector or LTE dongle appears above — plan 07 owns those,
selected by the connectivity branch.

---

*Written by plan 01-04 task 3, 2026-09-01. Owner decision recorded at the task 2 checkpoint.*
*Per D-16, actual-at-checkout is authoritative. Per D-13, this decision did not hold plan 05's orders.*
