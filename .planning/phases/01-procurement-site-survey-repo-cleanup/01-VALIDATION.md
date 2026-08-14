---
phase: 1
slug: procurement-site-survey-repo-cleanup
status: draft
nyquist_compliant: false
wave_0_complete: false
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
| **Estimated runtime** | ~2 seconds |

**Evidence root:** `.planning/phases/01-procurement-site-survey-repo-cleanup/evidence/`

```
evidence/
├── orders/           enclosure-order.md · phone-order.md · pi-and-electronics-order.md · budget-actual.md
├── site-survey/      survey-protocol.md · wifi-samples-*.csv · mtr-*.json · iperf3-*.txt · CONNECTIVITY-DECISION.md
├── spend-controls/   org-hard-limit.png · project-hard-limit.png · spend-alerts.png · auto-recharge-off.png · SPEND-CEILING.md
└── repo-cleanup/     (no artefact — asserted directly against git state)
```

---

## Sampling Rate

- **After every task commit:** Run `bash .../verify.sh`
- **After every plan wave:** Run `bash .../verify.sh` (same script)
- **Before `/gsd:verify-work`:** `verify.sh` must exit 0 with every assertion passing
- **Max feedback latency:** 2 seconds

---

## Per-Task Verification Map

> Task IDs are assigned by the planner. Rows below are the **required assertion set** — every
> row must be owned by exactly one task, and `verify.sh` must encode every row.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | 0 | — | — | N/A | infra | `test -d evidence/orders -a -d evidence/site-survey -a -d evidence/spend-controls` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0 | — | — | N/A | infra | `test -x verify.sh` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-01 | — | N/A | artefact | `test -f evidence/orders/enclosure-order.md && grep -qE 'Order #\|Confirmation' evidence/orders/enclosure-order.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-01 | — | N/A | artefact | `test -f evidence/orders/phone-order.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-01 | — | N/A | artefact | `test -f evidence/orders/pi-and-electronics-order.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-01 | — | N/A | artefact | `test -f evidence/orders/budget-actual.md && ! grep -qi camera evidence/orders/budget-actual.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-06 | — | N/A | measurement | `test "$(ls evidence/site-survey/wifi-samples-*.csv \| wc -l)" -ge 3` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-06 | — | N/A | measurement | `for f in evidence/site-survey/wifi-samples-*.csv; do test "$(wc -l < "$f")" -ge 200; done` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-06 | — | N/A | measurement | `ls evidence/site-survey/mtr-*.json && ls evidence/site-survey/iperf3-*.txt` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | HW-06 | — | N/A | artefact | `grep -qE 'WiFi\|LTE' evidence/site-survey/CONNECTIVITY-DECISION.md && grep -q 'dBm' evidence/site-survey/CONNECTIVITY-DECISION.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-01 | T-1-01 | Client-side key code removed from repo | git state | `test -z "$(git ls-files voice)"` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-01 | T-1-01 | No stale references remain | git grep | `! git grep -q -i 'my-project' -- . ':!.planning/'` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-01 | — | N/A | artefact | `test -f README.md && grep -q 'poc/' README.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-01 | T-1-02 | Orphaned `.env` removed from disk | filesystem | `test ! -d voice` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-03 | T-1-03 | Hard limit enforcing, not merely alerting | artefact + human | `test -f evidence/spend-controls/org-hard-limit.png && test -f evidence/spend-controls/project-hard-limit.png` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-03 | T-1-03 | Alerting configured | artefact | `test -f evidence/spend-controls/spend-alerts.png` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-03 | T-1-03 | Auto-recharge off; monthly figure recorded | artefact | `test -f evidence/spend-controls/auto-recharge-off.png && grep -qE '\$[0-9]' evidence/spend-controls/SPEND-CEILING.md` | ❌ W0 | ⬜ pending |
| TBD | TBD | — | OPS-03 | T-1-02 | Browser-destined key revoked | artefact | `grep -qi 'revok\|rotat' evidence/spend-controls/SPEND-CEILING.md` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `evidence/` directory tree (`orders/`, `site-survey/`, `spend-controls/`) — created before any evidence-producing task runs
- [ ] `verify.sh` — assertion script encoding **every row** of the map above; authored **first** so downstream tasks know exactly what artefact shape they owe
- [ ] `README.md` at repo root — does not currently exist; required by OPS-01's "exactly one authoritative implementation path" clause
- [ ] `evidence/site-survey/survey-protocol.md` template — pre-filled with spot / height / orientation / device / date / weather fields so the human fills blanks in the yard

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| "Enforce a hard limit" toggle is visibly **ON** in the screenshot | OPS-03 | An agent cannot read toggle state out of a PNG. File existence is the automated half only. | Human opens the PNG, confirms the toggle renders as enabled, and types confirmation at a `checkpoint:human-verify` |
| Purchase actually placed (money moved) | HW-01 | Requires a human at a checkout page with a payment method | Human places the order and pastes the order number + delivery ETA into the corresponding `evidence/orders/*.md` |
| Physical signal-strength readings taken at the real install spot | HW-06 | Requires a human standing in the front yard with the survey device | Human follows `survey-protocol.md`, runs ≥3 × 20-min windows, commits raw CSV/JSON/txt |
| Enclosure selection (CD-07) | HW-01 | ~$1,700 cost swing; a scope decision, not an implementation detail | `checkpoint:human-decision` before any enclosure purchase task runs |
| Outdoor outlet has GFCI + in-use cover | HW-01 (downstream) | Physical inspection | Human checks while in the yard for the site survey; records result in `survey-protocol.md` |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
