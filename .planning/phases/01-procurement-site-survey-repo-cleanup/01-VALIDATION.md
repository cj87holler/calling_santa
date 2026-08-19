---
phase: 1
slug: procurement-site-survey-repo-cleanup
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-13
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> **This is a procurement and operations phase — no application code is produced.** The
> validation surface is committed evidence artefacts and recorded measurements. A claim is
> "tested" when a file in the repo contains the raw numbers or the confirmation that proves it.
> Derived from `01-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — artefact-existence and content assertions via shell (`bash` + `git`) |
| **Config file** | none — Wave 0 authors `verify.sh` |
| **Quick run command** | `bash .planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh` |
| **Full suite command** | same — the script is the suite |
| **Gate command** | `bash .../verify.sh --gate` — upgrades `PENDING` and `NOT-YET` to `FAIL` |
| **Estimated runtime** | ~2 seconds (measured: 0.05 s) |

**Evidence root:** `.planning/phases/01-procurement-site-survey-repo-cleanup/evidence/`

```
evidence/
├── orders/           PROCUREMENT-LIST.md · enclosure-order.md · phone-order.md ·
│                     site-hardware-order.md · COMPUTE-COMPARISON.md · COMPUTE-DECISION.md ·
│                     pi-and-electronics-order.md · connectivity-order.md · budget-actual.md
├── site-survey/      survey-protocol.md · ETHERNET-SCOPING.md · CONNECTIVITY-BRANCH ·
│                     wifi-samples-*.csv · mtr-*.json · iperf3-*.txt · CONNECTIVITY-DECISION.md
├── spend-controls/   CREDENTIAL-INVENTORY.md · PRICING-RECHECK.md · SPEND-CEILING.md ·
│                     org-hard-limit.png · project-hard-limit.png · spend-alerts.png ·
│                     auto-recharge-off.png
└── repo-cleanup/     (no artefact — asserted directly against git state)
```

---

## Sampling Rate

- **After every task commit:** Run `bash .../verify.sh`
- **After every plan wave:** Run `bash .../verify.sh` (same script)
- **Before `/gsd:verify-work`:** `bash .../verify.sh --gate` must exit 0
- **Max feedback latency:** 2 seconds

### Result states

`verify.sh` reports four states, and three of them are **not** the same thing:

| State | Meaning | Affects exit code? |
|-------|---------|--------------------|
| `PASS` | The assertion is true | — |
| `PENDING` | The artefact does not exist yet because the task that produces it has not run | No in default mode; **yes** under `--gate` |
| `NOT-YET` | The assertion checks state a **later wave deliberately removes**, so it is correctly false right now; the label names the gating plan | No in default mode; **yes** under `--gate` |
| `FAIL` | The assertion is false and nothing in the plan explains why | Always |

Collapsing `NOT-YET` into `FAIL` would leave the gate red for three of five waves, which trains
everyone to ignore it. Collapsing `PENDING` into `PASS` would let the phase close over unspent money.

---

## Per-Task Verification Map

> Rows below are the **required assertion set** — every row is owned by exactly one task, and
> `verify.sh` encodes every row. Task ID convention: `P{plan}-T{n}`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| P01-T1 | 01 | 1 | — | — | N/A | infra | `test -d evidence/orders -a -d evidence/site-survey -a -d evidence/spend-controls` | ✅ | ✅ green |
| P01-T1 | 01 | 1 | — | — | N/A | infra | `test -x verify.sh` | ✅ | ✅ green |
| P05-T2 | 05 | 2 | HW-01 | T-1-40 | Gate tests a filled value, not a printed label | artefact | `test -f evidence/orders/enclosure-order.md` and `grep -qE 'Order #: *[A-Za-z0-9-]{4,}'`, `grep -qE 'Delivery ETA: *[0-9A-Za-z]'`, `grep -qE 'Actual price paid \(USD\): *\$?[0-9]'` against it | ❌ | ⬜ pending |
| P05-T2 | 05 | 2 | HW-01 | T-1-40 | Gate tests a filled value, not a printed label | artefact | `test -f evidence/orders/phone-order.md` and the same three value greps | ❌ | ⬜ pending |
| P08-T1 | 08 | 3 | HW-01 | T-1-40 | Gate tests a filled value, not a printed label | artefact | `test -f evidence/orders/pi-and-electronics-order.md` and the same three value greps | ❌ | ⬜ pending |
| P10-T1 | 10 | 5 | HW-01 | — | N/A | artefact | `test -f evidence/orders/budget-actual.md && ! grep -qi camera evidence/orders/budget-actual.md` | ❌ | ⬜ pending |
| P07-T2 | 07 | 3 | HW-06 | — | N/A | measurement | `test "$(ls evidence/site-survey/wifi-samples-*.csv \| wc -l)" -ge 3` | ❌ | ⬜ pending |
| P07-T2 | 07 | 3 | HW-06 | — | N/A | measurement | `for f in evidence/site-survey/wifi-samples-*.csv; do test "$(wc -l < "$f")" -ge 200; done` | ❌ | ⬜ pending |
| P07-T2 | 07 | 3 | HW-06 | — | N/A | measurement | `ls evidence/site-survey/mtr-*.json && ls evidence/site-survey/iperf3-*.txt` | ❌ | ⬜ pending |
| P07-T3 | 07 | 3 | HW-06 | — | N/A | artefact | `grep -qE 'WiFi\|LTE' evidence/site-survey/CONNECTIVITY-DECISION.md && grep -q 'dBm' evidence/site-survey/CONNECTIVITY-DECISION.md` | ❌ | ⬜ pending |
| P09-T1 | 09 | 4 | OPS-01 | T-1-01 | Client-side key code removed from repo | git state | `test -z "$(git ls-files voice)"` | ❌ | 🕓 not-yet |
| P09-T2 | 09 | 4 | OPS-01 | T-1-01 | No stale references remain | git grep | `! git grep -q -i 'my-project' -- . ':!.planning/'` | ❌ | 🕓 not-yet |
| P01-T2 | 01 | 1 | OPS-01 | — | N/A | artefact | `test -f README.md && grep -q 'poc/' README.md` | ✅ | ✅ green |
| P09-T1 | 09 | 4 | OPS-01 | T-1-02 | Orphaned `.env` removed from disk | filesystem | `test ! -d voice` | ❌ | 🕓 not-yet |
| P06-T1 | 06 | 3 | OPS-03 | T-1-03 | Hard limit enforcing, not merely alerting | artefact + human | `test -f evidence/spend-controls/org-hard-limit.png && test -f evidence/spend-controls/project-hard-limit.png` | ❌ | ⬜ pending |
| P06-T1 | 06 | 3 | OPS-03 | T-1-03 | Alerting configured | artefact | `test -f evidence/spend-controls/spend-alerts.png` | ❌ | ⬜ pending |
| P06-T2 | 06 | 3 | OPS-03 | T-1-03 | Auto-recharge off; monthly figure recorded | artefact | `test -f evidence/spend-controls/auto-recharge-off.png && grep -qE '\$[0-9]' evidence/spend-controls/SPEND-CEILING.md` | ❌ | ⬜ pending |
| P06-T2 | 06 | 3 | OPS-03 | T-1-02 | Browser-destined key revoked | artefact | `grep -qE 'KEY REVOKED: .+ last-four [0-9A-Za-z]{4} on 20[0-9]{2}-' evidence/spend-controls/SPEND-CEILING.md` | ❌ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · 🕓 not-yet · ⚠️ flaky*

**Correspondence note.** `verify.sh` expands several rows above into more than one printed assertion
line. Per its **global missing-file rule**, a row whose target file is absent reports `PENDING` and
its greps are not run — so each content row is emitted as a file-existence guard followed by one line
per grep. Row 15 (org and project hard-limit PNGs) is likewise emitted as two lines, one per PNG.
The set of assertions is identical; only the line granularity differs.

---

### Ethernet branch (D-07) - evaluated only when CONNECTIVITY-BRANCH is ethernet

These five rows **replace rows 7 through 9** of the map above when
`evidence/site-survey/CONNECTIVITY-BRANCH` reads `ethernet`. Under that branch no RF measurement
windows are run at all, so the wireless rows are not merely pending — they are inapplicable.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| P03-T1 | 03 | 2 | HW-06 | — | N/A | artefact | `test -f evidence/site-survey/ETHERNET-SCOPING.md && grep -qE '^VERDICT: FEASIBLE *$' evidence/site-survey/ETHERNET-SCOPING.md` | ❌ | ⬜ pending |
| P03-T1 | 03 | 2 | HW-06 | — | N/A | measurement | `grep -qE 'Measured cable run length \(ft\): *[0-9]+' evidence/site-survey/ETHERNET-SCOPING.md` | ❌ | ⬜ pending |
| P03-T1 | 03 | 2 | HW-06 | — | N/A | measurement | `grep -qE '^Spot marker placed: *yes *$' evidence/site-survey/ETHERNET-SCOPING.md` | ❌ | ⬜ pending |
| P07-T2 | 07 | 3 | HW-06 | — | N/A | measurement | `ls evidence/site-survey/mtr-*.json && ls evidence/site-survey/iperf3-*.txt` | ❌ | ⬜ pending |
| P07-T3 | 07 | 3 | HW-06 | — | N/A | artefact | `grep -q 'Ethernet' evidence/site-survey/CONNECTIVITY-DECISION.md && grep -qE 'Mbps' evidence/site-survey/CONNECTIVITY-DECISION.md` | ❌ | ⬜ pending |

**Why the two numeric rows exist.** D-09 says a decision without a cited number does not satisfy
HW-06. Without the cable-run and spot-marker assertions, the cheapest way to pass the ethernet branch
is to hand-write `VERDICT: FEASIBLE` and never go outside.

**Why the two string assertions are line-anchored (`^...*$`).** The phase-wide template convention
prints allowed values inline, so plan 03's rendered blank form contains the literal lines
`VERDICT: FEASIBLE | NOT FEASIBLE` and `Spot marker placed: yes | no`. An unanchored
`grep -q 'VERDICT: FEASIBLE'` matches the blank template from indoors — the same label-versus-value
defect the order-file assertions were strengthened to close. Anchoring forces the human to delete the
unchosen alternative.

**Branch split provenance.** This split is required by CONTEXT.md **D-06 through D-09**, which
postdate this validation document. `verify.sh` selects the assertion set at runtime by reading
`evidence/site-survey/CONNECTIVITY-BRANCH`. If that file is absent, every HW-06 assertion for both
branches reports `PENDING` with the label prefix `HW-06 (branch undetermined)`. If it contains any
string other than exactly `ethernet` or `wireless`, the script reports a hard `FAIL`.

---

### Amendments - assertion strengthening

Assertions `verify.sh` encodes that this document did not originally specify. Recorded here so the
map and the script stay in correspondence.

| Task ID | Plan | Wave | Requirement | Threat Ref | Assertion | Reason |
|---------|------|------|-------------|------------|-----------|--------|
| P05-T2 | 05 | 2 | HW-01 | T-1-40 | `enclosure-order.md`: `grep -qE 'Order #: *[A-Za-z0-9-]{4,}'`, `grep -qE 'Delivery ETA: *[0-9A-Za-z]'`, `grep -qE 'Actual price paid \(USD\): *\$?[0-9]'` | Replaces `grep -qE 'Order #\|Confirmation'`, which matched the printed label on the empty form the agent creates before the human buys — greening the HW-01 gate over unspent money |
| P05-T2 | 05 | 2 | HW-01 | T-1-40 | `phone-order.md`: the same three value greps | Same defect, same fix |
| P05-T2 | 05 | 2 | HW-01 | T-1-40 | `site-hardware-order.md`: existence plus the same three value greps | This file was **not asserted at all**, despite carrying the D-02 post and concrete line ordered in Phase 1 specifically for footing cure time |
| P08-T1 | 08 | 3 | HW-01 | T-1-40 | `pi-and-electronics-order.md`: the same three value greps | Existence alone did not prove a purchase |
| P07-T4 | 07 | 3 | HW-01 | T-1-40 | `connectivity-order.md`: existence plus the same three value greps | **No assertion existed against the connectivity purchase at all.** Plans 05 and 08 both exclude these items, so the order was orphaned. Shape by P07-T3, values by P07-T4 |
| P10-T1 | 10 | 5 | HW-01 | — | `budget-actual.md`: `grep -qE '^BUDGET STATUS: (WITHIN CEILING\|OVERRUN \$[0-9])'` | An overrun was previously visible only to a human reading reconciliation prose. The `BUDGET STATUS` line makes it visible at the gate |
| P06-T2 | 06 | 3 | OPS-03 | T-1-02 | `SPEND-CEILING.md`: `grep -qE 'KEY REVOKED: .+ last-four [0-9A-Za-z]{4} on 20[0-9]{2}-'` | Replaces `grep -qi 'revok\|rotat'`. Plan 06 writes the heading `## Key rotation record` unconditionally, so the loose pattern matched with **no revocation performed** — and plan 09 gates an irreversible `rm -rf voice/` on it. Per D-24 the token carries the key **name and last four characters only**; a key value must never appear |
| P09-T1 · P09-T2 | 09 | 4 | OPS-01 | T-1-41 | The `NOT-YET` state for the three OPS-01 rows (`git ls-files voice`, the `my-project` stale-reference grep, `test ! -d voice`), each labelled *(gated on plan 09 deletion, wave 4)* | Those three assertions are **correctly false during waves 1 through 3**. Reporting them as `FAIL` made the gate permanently red and therefore ignorable. They are upgraded to `FAIL` under `--gate` |
| P03-T2 | 03 | 2 | HW-06 | — | `CONNECTIVITY-BRANCH` reads exactly `ethernet` or `wireless`; any other string is a hard `FAIL` | The branch selector is itself an assertion. A typo'd or free-text branch file would otherwise silently skip the entire HW-06 assertion set |

---

## Wave 0 Requirements

- [x] `evidence/` directory tree (`orders/`, `site-survey/`, `spend-controls/`) — created before any evidence-producing task runs *(P01-T1)*
- [x] `verify.sh` — assertion script encoding **every row** of the map above; authored **first** so downstream tasks know exactly what artefact shape they owe *(P01-T1)*
- [x] `README.md` at repo root — did not previously exist; required by OPS-01's "exactly one authoritative implementation path" clause *(P01-T2)*
- [x] `evidence/site-survey/survey-protocol.md` template — fill-in-the-blank spot / height / orientation / device / date / weather / outlet fields so the human fills blanks in the yard *(P01-T3)*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| "Enforce a hard limit" toggle is visibly **ON** in the screenshot | OPS-03 | An agent cannot read toggle state out of a PNG. File existence is the automated half only. | Human opens the PNG, confirms the toggle renders as enabled, and types confirmation at a `checkpoint:human-verify` |
| Purchase actually placed (money moved) | HW-01 | Requires a human at a checkout page with a payment method | Human places the order and pastes the order number, delivery ETA and actual price paid into the corresponding `evidence/orders/*.md` |
| Physical evidence gathered at the real install spot | HW-06 | Requires a human standing in the front yard | **Branch-dependent.** Under `wireless`: the human follows `survey-protocol.md` and runs at least three 20-minute measurement windows, committing the raw CSV/JSON/txt. Under `ethernet`: the human measures and records the cable run at the marked spot in `ETHERNET-SCOPING.md`, and runs wired-path `mtr` and `iperf3` from the exit-point end — **no CSV measurement windows are required** |
| Enclosure selection (CD-07) | HW-01 | ~$1,700 cost swing; a scope decision, not an implementation detail | `checkpoint:human-decision` before any enclosure purchase task runs |
| Outdoor outlet has GFCI + in-use cover | HW-01 (downstream) | Physical inspection | Human checks while in the yard; records the finding in `ETHERNET-SCOPING.md` (authoritative) and optionally in `survey-protocol.md`. Remediation is deferred to the install phase |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 2s (measured: 0.05 s)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
