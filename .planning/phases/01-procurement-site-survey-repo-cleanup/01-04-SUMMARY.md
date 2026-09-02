---
phase: 01-procurement-site-survey-repo-cleanup
plan: 04
subsystem: infra
tags: [procurement, raspberry-pi, hardware-bom, gpio, budget]

# Dependency graph
requires:
  - phase: 01-procurement-site-survey-repo-cleanup
    provides: "01-01's evidence tree layout and PROCUREMENT-LIST.md scaffolding under evidence/orders/"
provides:
  - "COMPUTE-COMPARISON.md: both compute paths costed at today's reseller prices with a named hook-switch input for each"
  - "COMPUTE-DECISION.md: locked DECISION: pi-5 (8GB, board-only, pishop.us configuration A1) with an exact, spec-qualified ORDER LINES section plan 08 purchases verbatim"
  - "Concrete hook-switch input path (GPIO header + pull-up pin, assigned in Phase 3) satisfying D-11"
  - "Power-draw basis (5V/5A/27W envelope) for plan 07's PoE splitter sizing"
affects: [01-07, 01-08, 01-10]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Decision-lock document with a machine-checkable DECISION: line consumed by downstream plans (07, 08, 10)"]

key-files:
  created:
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/orders/COMPUTE-COMPARISON.md
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/orders/COMPUTE-DECISION.md
  modified: []

key-decisions:
  - "DECISION: pi-5 — Raspberry Pi 5 chosen over an existing laptop for the installation's compute"
  - "8GB (SC1112), not 4GB — the $65 memory lever is deliberately not pulled because CD-03 may still place Prometheus/Grafana on this board"
  - "Board-only from pishop.us (configuration A1, $239.75 all-in), not the CanaKit 8GB starter kit (A3, $284.90, unverified bundled-PSU wattage)"
  - "Hook-switch input path is the GPIO header with a normally-closed lever-arm microswitch on a pull-up pin; pin number deferred to Phase 3; no Pico/Arduino/USB microcontroller needed"

patterns-established: []

requirements-completed: []  # HW-01 not yet complete — this plan settles the compute decision, but pi-and-electronics-order.md (plan 08) still gates HW-01

# Metrics
duration: 25min
completed: 2026-09-01
---

# Phase 1 Plan 4: Compute Decision (Pi 5 vs. Laptop) Summary

**Locked the largest BOM line item to a Raspberry Pi 5 8GB board-only order ($239.75 all-in) with a GPIO-header hook-switch path, unblocking plan 08's electronics order and plan 07's PoE splitter sizing.**

## Performance

- **Duration:** ~25 min (this session — task 3 only; tasks 1-2 ran in a prior session and are unchanged)
- **Completed:** 2026-09-01
- **Tasks:** 3 total (1 auto, 1 checkpoint:decision, 1 auto) — 1 and 2 previously complete, 3 executed this session
- **Files modified:** 1 created this session (`COMPUTE-DECISION.md`); `COMPUTE-COMPARISON.md` unchanged from prior session

## Accomplishments
- Verified prior-session artifact `COMPUTE-COMPARISON.md` (commit `0395b8d`) is intact on disk and unmodified — no price re-fetch performed
- Recorded the owner's checkpoint answer (`pi-5`, 8GB, board-only from pishop.us) into `COMPUTE-DECISION.md` with a dated rationale
- Named the concrete hook-switch input path (GPIO header + pull-up pin) as required by D-11
- Emitted a fully spec-qualified `## ORDER LINES` section — six lines priced today ($239.75 subtotal), four lines named with spec qualifiers but no invented price (second USB audio adapter, microswitch kit, LED/resistor set, sealed inner enclosure), consistent with D-16
- Guarded pitfall 7 (TRRS-only adapter) and pitfall 8 (undersized PSU) explicitly in the order lines
- Added a power-draw note (5V/5A/27W envelope) so plan 07 can size the PoE splitter off this file without re-deriving it

## Task Commits

Task 1 and 2 ran in a prior session (verified intact, not redone):

1. **Task 1: Cost both compute paths and name the hook-switch input for each** - `0395b8d` (docs) — prior session, verified present
2. **Task 2: Owner selects the compute path** - checkpoint, no commit (decision captured directly in this session's prompt: `pi-5`, 8GB, board-only/pishop.us)

This session:

3. **Task 3: Lock the decision and emit the exact order lines** - `ffba297` (docs)

**Plan metadata:** pending (this summary + STATE.md update)

## Files Created/Modified
- `.planning/phases/01-procurement-site-survey-repo-cleanup/evidence/orders/COMPUTE-DECISION.md` - `DECISION: pi-5`, sub-choices, hook-switch input path, power-draw note, and the six-line-priced/four-line-unpriced `## ORDER LINES` section plan 08 purchases verbatim

## Decisions Made
- **DECISION: pi-5, 8GB, board-only (configuration A1)** — see key-decisions above for full rationale. This is the owner's decision, captured verbatim from the executor's launch prompt per the resume context; no independent judgment was applied to the choice itself.
- The sealed inner enclosure line is now sized to the Pi 5's known footprint rather than the oversized laptop-class footprint the `OVERDUE` branch would have required — a small optimization available only because a real decision landed.

## Deviations from Plan

None - plan executed exactly as written for task 3. Tasks 1-2 (prior session) are outside this session's scope per the resume instructions and were only verified, not re-executed.

## Issues Encountered

`verify.sh` carries no direct assertions against `COMPUTE-COMPARISON.md` or `COMPUTE-DECISION.md` — it only asserts against the order files (`pi-and-electronics-order.md`, etc.) that plan 08 will create. Confirmed via `grep -n "COMPUTE\|orders/" verify.sh`. As a result, the verify.sh pass/fail/pending/not-yet counts were identical before and after this task (`passed=4 failed=0 pending=43 not-yet=3`). This is expected — this plan's own acceptance criteria (file existence, `DECISION:` line, `Hook-switch input path:`, `## ORDER LINES`, chipset/TRRS/microswitch guards, no-camera exclusion, 27W presence) were verified directly via targeted `grep` checks per the plan's `<acceptance_criteria>`, all of which passed. No gap requiring a fix.

## User Setup Required

None - no external service configuration required. This plan's checkpoint (task 2) was answered by the owner directly in the launch instructions for this session; no further owner action is needed for this plan.

## Next Phase Readiness

- `COMPUTE-DECISION.md` is ready for plan 07 (PoE splitter sizing, reads the `DECISION:` line and the power-draw note) and plan 08 (electronics order, purchases `## ORDER LINES` verbatim)
- HW-01 remains incomplete — this plan settles the compute decision only; the actual purchase and the `pi-and-electronics-order.md` evidence file are plan 08's job
- Three other Phase 1 checkpoints remain open and untouched by this session: 01-03 (yard visit/ethernet scoping), 01-05 (enclosure/phone/site-hardware orders), 01-06 (OpenAI dashboard + key revocation) — none were started or modified, per this plan's explicit scope boundary
- Phase 1 is not complete; 7 plans remain (03, 05, 06, 07, 08, 09, 10). Phase-level verification was not run and the phase was not marked complete, per instructions

---
*Phase: 01-procurement-site-survey-repo-cleanup*
*Completed: 2026-09-01*

## Self-Check: PASSED

- FOUND: `.planning/phases/01-procurement-site-survey-repo-cleanup/evidence/orders/COMPUTE-DECISION.md`
- FOUND: `.planning/phases/01-procurement-site-survey-repo-cleanup/01-04-SUMMARY.md`
- FOUND commit: `0395b8d` (task 1, prior session)
- FOUND commit: `ffba297` (task 3, this session)
