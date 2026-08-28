# Compute path comparison — Raspberry Pi 5 vs. existing laptop

**Plan:** 01-04 (wave 2), task 1
**Decision reference:** D-10, D-11, D-12, D-13, D-14, D-16
**Requirement:** HW-01 (with HW-02, HW-03, HW-04 defining what the compute path must physically support)
**Prices fetched:** 2026-08-27 (headline lines re-verified the same day; the full pass ran 2026-08-25 to 2026-08-27)
**Sources:** pishop.us and canakit.com only — both official Raspberry Pi resellers

**This document does not decide anything.** It informs the checkpoint in task 2. The owner chooses.

---

## Sourcing rule and what was excluded

Every price below was fetched from a product page at **pishop.us** or **canakit.com**. Both are
official Raspberry Pi resellers, which is the whole reason they were used: research recorded
third-party Amazon marketplace listings for the bare Pi 5 8GB board running as high as $218 against
a $175 official-reseller price — a 25% markup with no authenticity guarantee on a SKU that has been
counterfeited. No price on this page comes from an Amazon marketplace listing, and none should.

Where a part is not carried by either named vendor, the line says **UNVERIFIED** and gives no
invented number. Per D-16, actual-at-checkout is authoritative in every case.

---

## Fetched price table (2026-08-27)

### pishop.us

| Item | SKU | Price | Stock | Research (2026-08-13) | Delta |
|------|-----|-------|-------|-----------------------|-------|
| Raspberry Pi 5 8GB | SC1112 | $175.00 | In stock | $175 | none |
| Raspberry Pi 5 4GB | SC1111 | $110.00 | In stock | $110 | none |
| Raspberry Pi 5 2GB | SC1110 | $65.00 | In stock | not priced | — |
| Raspberry Pi 27W USB-C PD supply, black, US plug | SC1158 | $12.95 | In stock | ~$15 | −$2.05 |
| Raspberry Pi 27W USB-C PD supply, white, US plug | SC1153 | $12.95 | In stock | ~$15 | −$2.05 |
| Raspberry Pi Active Cooler | SC1148 | $10.95 | In stock | not priced | — |
| USB Audio Adapter — Works with Raspberry Pi | — | $4.95 | In stock | $4.95 | none |
| Raspberry Pi Case for Pi 5, black/grey | — | $10.95 | In stock | not priced | — |
| SanDisk Ultra microSDHC 32GB, blank | — | $14.95 | In stock | ~$12 | +$2.95 |
| SanDisk microSD 32GB, pre-loaded Pi OS 64-bit | — | $19.95 | In stock | not priced | — |
| SanDisk High Endurance microSDHC 32GB, blank | — | $29.95 | In stock | not priced | — |
| Official Raspberry Pi microSD A2/V30 32GB, blank | — | $19.95 | **OUT OF STOCK** | not priced | — |
| Raspberry Pi Pico (non-wireless) | SC0915 | $3.95 | **OUT OF STOCK** | ~$4 | stock, not price |
| Raspberry Pi Pico H (pre-soldered headers) | — | $5.00 | In stock | ~$4–6 | in range |
| Raspberry Pi Pico W | SC0918 | $6.00 | In stock | not priced | — |
| USB A-male to Micro-B cable, 6 inch | — | $2.95 | In stock | not priced | — |
| Arduino Leonardo with headers | A000057 | $26.95 | In stock | ~$10 assumed | **+$16.95** |

### canakit.com

| Item | SKU | Price | Stock |
|------|-----|-------|-------|
| Raspberry Pi 5 8GB, board only | — | $175.00 | In Stock |
| Raspberry Pi 5 4GB, board only | — | $110.00 | In Stock |
| Raspberry Pi 5 Active Cooler | — | $11.95 | In Stock |
| CanaKit Pi 5 Starter Kit — Turbine Black, 8GB | PI5-8GB-STR128-C4-BLK | $269.95 | listed |
| CanaKit Pi 5 Starter Kit — Turbine Black, 4GB | PI5-4GB-STR128-C4-BLK | $204.95 | listed |
| CanaKit Pi 5 Starter Kit — Turbine Black, 2GB | PI5-2GB-STR128-C4-BLK | $159.95 | listed |

**Three deltas worth naming before the decision is made:**

1. **The Pi has not moved since research.** 8GB is $175.00 at both official resellers, 4GB is
   $110.00 at both, and the 8GB starter kit is still $269.95. The two 2026 price rises appear to
   have settled for now. This does *not* mean the price is stable — Raspberry Pi stated in February
   that LPDDR4 pressure is expected to continue through 2026 — but nothing rose in the last fortnight.
2. **The bare Pico is out of stock; the Pico H is not.** The $3.95 headerless Pico that research
   assumed for the laptop path cannot be ordered today. The **Pico H at $5.00 is in stock**, and it
   is the better part anyway: pre-soldered headers mean no soldering iron between the decision and a
   working hook switch.
3. **An Arduino is not the ~$10 part the plan assumed.** The cheapest Arduino at pishop.us with
   native USB HID is the Leonardo at **$26.95** — more than five times the Pico H. If the laptop path
   is chosen, the microcontroller is a Pico H, not an Arduino.

---

## Path A — Raspberry Pi 5

### A1. Board-only, 8GB (recommended configuration of this path)

| Item | Vendor | Qty | Unit | Line |
|------|--------|-----|------|------|
| Raspberry Pi 5 8GB (SC1112) | pishop.us | 1 | $175.00 | $175.00 |
| Raspberry Pi 27W USB-C PD supply, US (SC1158/SC1153) | pishop.us | 1 | $12.95 | $12.95 |
| Raspberry Pi Active Cooler (SC1148) | pishop.us | 1 | $10.95 | $10.95 |
| SanDisk Ultra microSDHC 32GB, blank | pishop.us | 2 | $14.95 | $29.90 |
| Raspberry Pi Case for Pi 5, black/grey | pishop.us | 1 | $10.95 | $10.95 |
| **All-in subtotal** | | | | **$239.75** |

Single vendor, single shipment, everything in stock today.

### A2. Board-only, 4GB — the memory lever

Identical to A1 with SC1111 substituted for SC1112: **$174.75 all-in**. The delta is exactly
**$65.00**, unchanged from research.

Research recommends **8GB**, and the reasoning survives contact with today's prices. The v1 workload
— a Python session manager holding one WebSocket, a small admin web service, node_exporter — is not
memory-bound at 4GB. But **CD-03 is still open**, and one of its two candidate outcomes puts
Prometheus and Grafana on this same box. Discovering in November that the box is out of headroom, in
a sealed enclosure, outdoors, is a materially worse outcome than $65. The lever exists and is
recorded here so the owner can pull it; the recommendation is not to.

### A3. CanaKit Starter Kit, 8GB — the bundled alternative

| Item | Vendor | Qty | Unit | Line |
|------|--------|-----|------|------|
| CanaKit Pi 5 Starter Kit Turbine Black 8GB (PI5-8GB-STR128-C4-BLK) | canakit.com | 1 | $269.95 | $269.95 |
| Spare microSD (the kit ships one card; a spare is not optional — see below) | pishop.us | 1 | $14.95 | $14.95 |
| **All-in subtotal** | | | | **$284.90** |

The kit bundles the Turbine case, a MEGA heat sink, a low-noise PWM fan, a CanaKit USB-C PD supply,
a 128GB microSD pre-loaded with Raspberry Pi OS, and two micro-HDMI cables. It costs **$45.15 more**
than A1 and arrives from a second vendor.

**One thing to confirm at checkout if this option is chosen:** the kit's listing says "CanaKit USB-C
PD Power Supply" without stating wattage on the page fetched. Research pitfall 8 is that an
undersized supply causes USB current-limit throttling, which presents in December as random mid-call
audio dropouts — the hardest class of bug to diagnose in a sealed cold box. **Verify the bundled
supply is 5V/5A / 27W before relying on it.** If it is not, this option needs the $12.95 official
supply added and loses its remaining appeal against A1.

### Why two microSD cards, on every Pi variant

A corrupted card in late November with no spare is a season-ending event: the installation is dead
until a replacement card ships and is re-imaged, and the season does not wait. At $14.95 the second
card is the cheapest insurance in the entire BOM. It is a required line, not an optional extra.

**Hook-switch input path:** **GPIO header, a normally-closed lever-arm microswitch wired to a GPIO
pin with an internal pull-up, pin number to be assigned in Phase 3.** The 40-pin header is already
on the board — this costs $0.00 in additional hardware and adds no protocol, no firmware and no
second device to the system. The same header carries the three HW-04 status LEDs.

---

## Path B — Existing laptop with battery removed

### B1. Costed lines

| Item | Vendor | Qty | Unit | Line |
|------|--------|-----|------|------|
| The laptop itself (already owned) | — | 1 | $0.00 | $0.00 |
| **Raspberry Pi Pico H (pre-soldered headers)** — reads the hook switch, presents state over USB | pishop.us | 1 | $5.00 | $5.00 |
| USB A-male to Micro-B cable, 6 inch — the Pico H uses micro-USB, not USB-C | pishop.us | 1 | $2.95 | $2.95 |
| **All-in subtotal (new hardware)** | | | | **$7.95** |

**Conditional, and UNVERIFIED:** if the machine's USB-A port count is tight — the build needs one
port for the audio adapter and one for the Pico H, minimum — a powered USB hub or a USB-A extension
is required. **Neither named vendor stocks a plain powered USB hub**, so no price is quoted here
rather than invented. Budget for it as an unpriced line and source it at checkout time.

Two alternatives that were fetched and rejected: the bare **Pico** at $3.95 is **out of stock**, and
the cheapest **Arduino** with native USB HID (Leonardo, $26.95) costs more than three times the
whole rest of this path. The Pico H is the part.

**Hook-switch input path:** **a Raspberry Pi Pico H (pishop.us, $5.00, in stock) reading the
normally-closed lever-arm microswitch on one of its GPIO pins with an internal pull-up, and
presenting on-hook/off-hook state to the laptop over USB serial (CDC-ACM) — driverless on Linux via
the standard `cdc_acm` driver, appearing as `/dev/ttyACM0`.** USB HID is the alternative host-side
interface; USB serial is preferred here because it is trivially debuggable from a terminal and does
not require the host to consume raw HID reports.

Two consequences of this path that the Pi path does not have:

- **Firmware becomes a Phase 3 deliverable.** MicroPython or C on the Pico, plus debounce logic on
  the microcontroller side, plus a host-side serial reader — three moving parts where the Pi path has
  one GPIO read. HW-02 requires no bounce-induced false sessions; the debounce moves onto the Pico.
- **The three HW-04 status LEDs also land on the Pico.** A laptop has no GPIO. The LEDs must be
  driven from the Pico's pins, which means the host has to *push* state changes down the same serial
  link — a bidirectional protocol where the Pi path has three direct pin writes.

### B2. PRE-INSTALL OBLIGATIONS — non-monetary, and owed to Phase 3

- [ ] **Battery physically removed from the laptop before installation. Not optional (D-12).** A
      lithium cell held at full charge through 20–50°F outdoor swings, sealed in a wooden box,
      unattended, near children, is a real hazard and not a hypothetical one. Removal must happen
      before the machine goes in the cabinet, not after.
- [ ] **BIOS: "restore on AC power loss" enabled** (may be labelled "power on after power failure"
      or "AC power recovery"). Without it, the first outage in December leaves the installation dark
      until someone walks outside and presses a button.
- [ ] **Sleep disabled** — both the OS suspend timers and any BIOS-level sleep.
- [ ] **Lid-close action set to do nothing.** The lid will be closed the entire time it is installed.

If any of these four cannot be satisfied on the specific machine — some consumer BIOSes do not
expose an AC-power-loss setting at all — the laptop path is not viable for an unattended outdoor
installation, and that is worth checking *before* choosing it rather than after.

### B3. Physical drawbacks against the D-01 cabinet

The reference cabinet gives a usable cavity of roughly **14.5" × 12.5" × 20.5"**, of which a full
rotary desk set occupies roughly **9" × 9" × 5.5"**. See the fit check below — the arithmetic does
not favour this path, and for machines 14" and larger it rules it out.

Beyond volume: **a laptop fan draws outdoor air, with its dust and moisture, through the machine
continuously**, for the entire season, and it is the one component in the design that cannot be
sealed. This collides directly with D-03, which requires the electronics to live in a sealed inner
enclosure. A sealed box around a fan-cooled laptop suffocates it; an unsealed laptop in a cabinet
whose door opens every time a child uses the phone is exposed to the weather. There is no
configuration that satisfies both, and the plan has to pick one.

---

## Head to head

| Criterion | Path A — Pi 5 8GB (A1) | Path B — laptop |
|-----------|------------------------|-----------------|
| All-in cost, today | **$239.75** ($174.75 at 4GB; $284.90 as a CanaKit kit) | **$7.95** verified, plus an unpriced hub if ports are tight |
| Cost delta | +$231.80 vs. Path B | baseline |
| Physical volume required | Pi in official case ≈ 3.7" × 2.4" × 1.2"; inside a sealed IP65 inner box ≈ 6" × 5" × 3.5" | 13" laptop ≈ 11.9" × 8.4" × 0.6"; 15.6" ≈ 14.2" × 9.8" × 0.9" — sealed box adds 2" to each horizontal axis |
| Cold-weather tolerance, 20–50°F | Rated 0–50°C (32–122°F) ambient. **20°F is below the bottom of that rating**; the active cooler plus self-heating inside a sealed inner box is the mitigation, and it is a Phase 3 concern | Consumer laptops are typically rated 10–35°C (50–95°F) — **a narrower window than the Pi and further from the operating range**. UNVERIFIED until the specific machine is named; check its datasheet |
| Replacement if it dies mid-season | $175.00, in stock at two official resellers today, same-week ship, re-image the spare microSD and go | Not a same-week order. A used-market hunt for a comparable machine with a removable battery, then a fresh OS install. The $5.00 Pico H survives the failure; nothing else does |
| GPIO for the three HW-04 status LEDs | Native. 40-pin header, three pins, three resistors, no protocol | None on the host. LEDs hang off the Pico H, driven over a bidirectional serial protocol the Pi path does not need |
| Hook-switch complexity | One GPIO read with an internal pull-up. Zero added hardware, zero firmware | Pico H + micro-USB cable + MicroPython/C firmware + debounce on-device + host-side serial reader |
| Vendor/authenticity risk | Two official resellers, both in stock, no marketplace exposure | None — the machine is already owned |
| Precedent | Every documented rotary-phone conversion found in research used exactly this | None found in research |

---

## Fit check against the enclosure

**D-01 cabinet usable cavity: roughly 14.5" × 12.5" × 20.5".** Occupied by the phone: roughly
9" × 9" × 5.5". **D-03 requires the electronics in a sealed inner enclosure mounted high and to the
rear** — nothing critical sits loose on the cabinet floor. Research guidance for that inner box is at
least 1 inch of internal clearance on every axis, i.e. roughly 2 inches added to each external
dimension.

**Path A fits with room to spare.** A Pi 5 in its official case is roughly 3.7" × 2.4" × 1.2". Its
sealed inner enclosure lands near 6" × 5" × 3.5" — under half the cavity width, and light enough to
bracket-mount high on the rear panel exactly as D-03 asks. The phone, the USB audio adapter, the
sealed box and the wiring all coexist comfortably.

**Path A on the CanaKit Turbine case** is slightly larger than the official case but well inside the
same envelope.

**Path B does not fit for a 14" or larger machine.** The arithmetic, using the cavity width of 14.5":

| Machine class | Closed footprint (typical) | Sealed inner box (+2" per horizontal axis) | Against a 14.5" cavity width |
|---------------|---------------------------|--------------------------------------------|------------------------------|
| 15.6" laptop | ≈ 14.2" × 9.8" × 0.9" | ≈ 16.2" × 11.8" × 2.9" | **Does not fit** — 1.7" over |
| 14" laptop | ≈ 12.8" × 8.9" × 0.8" | ≈ 14.8" × 10.9" × 2.8" | **Does not fit** — 0.3" over |
| 13" laptop | ≈ 11.9" × 8.4" × 0.6" | ≈ 13.9" × 10.4" × 2.6" | Fits, with 0.6" of width to spare |

The footprints above are typical class figures, not measurements of the owner's actual machine —
**they are indicative and must be replaced by a tape measure on the real laptop before this path is
chosen.** But the conclusion holds across the class: only a 13"-or-smaller machine can be sealed per
D-03 inside this cabinet, and even then with well under an inch of margin on the binding axis.

A 14"-or-larger laptop can only go in **unsealed**, lying flat, which puts the single most expensive
and least replaceable component of the installation loose on the cabinet floor — the exact
arrangement D-03 exists to forbid, in a box whose door a child opens in the weather.

**And the fan problem is not solved by any of these rows.** Even the 13" machine that fits
dimensionally is a fan-cooled device inside a sealed box. Sealing it is a thermal problem; not
sealing it is a weather problem.

---

## Path-independent lines

These are identical under both paths. They satisfy HW-02, HW-03 and HW-04, none of which depend on
the compute choice. **This is the set that can be ordered without the decision** — and it is the set
plan 08 orders if the decision goes overdue.

| Item | Required spec | Vendor | Qty | Unit |
|------|---------------|--------|-----|------|
| USB audio adapter | **Two separate 3.5mm jacks — one pink mic-in, one green line-out — not a single combined TRRS headset jack.** Driverless USB Audio Class. Known-good chipsets: C-Media CM108/CM119, TI PCM2902. Confirm the jack layout from the product photo | pishop.us ("USB Audio Adapter — Works with Raspberry Pi") | 1 | $4.95 |
| USB audio adapter, second unit | Same spec, **different vendor or chipset** — a spare and an alternative, so a dead mic input in Phase 3 is a swap and not a re-order | second source, UNVERIFIED price (~$5 class) | 1 | UNVERIFIED |
| Normally-closed lever-arm microswitch kit, with jumper wiring | Normally-closed, lever-arm, reporting off-hook and on-hook with no bounce-induced false sessions (HW-02) | **Not stocked by either named vendor — UNVERIFIED price** | 1 | UNVERIFIED |
| Status LEDs and resistors | Three-state indicator per HW-04; discrete LEDs with current-limiting resistors | **Not stocked as a matched kit by either named vendor — UNVERIFIED price** | 1 set | UNVERIFIED |
| Sealed inner enclosure with standoffs or mounting bracket | **IP65 or better**, ABS or polycarbonate, gasketed lid, internal dimensions at least 1 inch larger than the compute on every axis, bracket-mountable high and to the rear (D-03) | **Not stocked by either named vendor — UNVERIFIED price** | 1 | UNVERIFIED |

Four of the six lines above could not be priced at pishop.us or canakit.com. **No number has been
invented for them.** They are named with their spec qualifiers so they are orderable, and their
prices are recorded at checkout per D-16.

**Note on the sealed inner enclosure under an overdue decision:** its internal dimensions depend on
which compute it houses, and the two candidates differ by an order of magnitude in footprint. If it
is ordered before the decision, it must be specified against the **larger** of the two footprints so
it fits either outcome — and that means specifying against a laptop, which the fit check above shows
may not fit the cabinet at all. This line is the one path-independent item that is not cleanly
path-independent, and it should be said out loud rather than glossed.

### Path-*dependent* lines — deliberately NOT in the set above

1. **The compute itself** — the Pi 5 board or kit, or nothing at all on the laptop path.
2. **The 27W 5V/5A USB-C PD supply** — required on a board-only Pi, meaningless on a laptop.
3. **The microSD cards** (2×) — a Pi-only line.
4. **The USB microcontroller** (Pico H + micro-USB cable) — a laptop-only line.

---

## What this comparison does not settle

- **The specific laptop.** Path B is costed against "an existing old laptop" as a class. Its make,
  model, RAM, CPU, screen size, port count, BIOS capabilities and operating temperature range are all
  unknown, and four of those six materially affect whether the path is viable at all. If the owner
  leans toward Path B, the machine has to be named and measured.
- **CD-03.** Whether Prometheus and Grafana land on this box is still open, and it is the single
  strongest argument for 8GB over 4GB on Path A and the single strongest argument for Path B overall.
- **Phase 3 pin assignments.** Deliberately deferred on both paths.

---

*Written by plan 01-04 task 1. Prices fetched from pishop.us and canakit.com on 2026-08-27.*
*Per D-16, actual-at-checkout is authoritative. Per D-13, nothing on plan 05's list waits for this.*
