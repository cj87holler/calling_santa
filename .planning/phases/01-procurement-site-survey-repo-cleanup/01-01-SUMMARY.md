---
phase: 01-procurement-site-survey-repo-cleanup
plan: 01
subsystem: testing
tags: [bash, git, verification-harness, evidence-scaffolding, procurement, site-survey]

# Dependency graph
requires: []
provides:
  - "verify.sh — the Phase 1 gate: a four-state (PASS/FAIL/PENDING/NOT-YET) bash assertion harness with a --gate mode, runtime 0.05s"
  - "evidence/ tree (orders/, site-survey/, spend-controls/) — the committed artefact surface every other Phase 1 plan writes into"
  - "Root README.md naming poc/ as the single authoritative implementation path (OPS-01 documentation clause)"
  - "evidence/site-survey/survey-protocol.md — the fill-in-the-blank yard form for the wireless survey and the outlet inspection"
  - "01-VALIDATION.md with a fully-populated Per-Task Verification Map, the ethernet-branch row set, and the assertion-amendment record"
  - "ROADMAP.md Phase 1 success criteria 1, 2 and 3 corrected to match the CONTEXT.md decisions that superseded them"
  - "REQUIREMENTS.md HW-06 wired-path evidence note"
affects: [01-02, 01-03, 01-04, 01-05, 01-06, 01-07, 01-08, 01-09, 01-10]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Value-shaped assertions: gates grep for a filled value, never a printed field label"
    - "Four-state verification: PENDING (task has not run) and NOT-YET (a later wave deliberately falsifies this) are semantically distinct from FAIL"
    - "Branch-aware gating: verify.sh reads evidence/site-survey/CONNECTIVITY-BRANCH to select the wireless or ethernet HW-06 assertion set"
    - "Blank-form convention: ____ placeholder plus an inline (allowed: a | b) hint, so a rendered template cannot pre-satisfy its own assertion"

key-files:
  created:
    - .planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/orders/.gitkeep
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/site-survey/.gitkeep
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/spend-controls/.gitkeep
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/site-survey/survey-protocol.md
    - README.md
  modified:
    - .planning/phases/01-procurement-site-survey-repo-cleanup/01-VALIDATION.md
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md

key-decisions:
  - "The HW-01 order gate tests filled values (Order #, Delivery ETA, Actual price paid), never the printed label — every order file exists as a blank form before money moves"
  - "NOT-YET is a first-class result state so the gate is quiet during waves 1-3 rather than permanently red, and both PENDING and NOT-YET upgrade to FAIL under --gate"
  - "Both ethernet string assertions are line-anchored (^...*$) so a blank template line 'VERDICT: FEASIBLE | NOT FEASIBLE' cannot green the branch from indoors"
  - "survey-protocol.md constrained fields use ____ with an inline (allowed: ...) hint rather than a bare inline 'yes | no', so the blank form cannot pre-satisfy plan 07's value assertion"
  - "ROADMAP criterion 2 is branch-neutral: it reads the compute path out of COMPUTE-DECISION.md and makes the weatherproof cord conditional on the connectivity branch (D-07, D-10)"

patterns-established:
  - "Global missing-file rule: any assertion whose target file is absent reports PENDING and its greps are not run — this closes the inverted-grep false PASS (! grep on a missing file exits 2)"
  - "Amendment record: every assertion verify.sh encodes beyond the original validation map is logged in 01-VALIDATION.md with an owner, a wave and a reason"
  - "Task ID convention P{plan}-T{n} used across the whole phase"

requirements-completed: [OPS-01, HW-06]

# Metrics
duration: 12min
completed: 2026-08-18
---

# Phase 01 Plan 01: Evidence Scaffolding & Verification Harness Summary

**A four-state bash gate (`verify.sh`, 50 assertions, 0.05s) that tests filled order values rather than printed labels, plus the evidence tree, the root README, the yard survey form, and the ROADMAP corrections that make the phase's success criteria describe the plan the project actually adopted.**

## Performance

- **Duration:** ~12 min
- **Started:** 2026-08-19T01:20:00Z
- **Completed:** 2026-08-19T01:32:00Z
- **Tasks:** 3 of 3
- **Files created/modified:** 9

## Accomplishments

- **`verify.sh` is the phase gate and it cannot green over unspent money.** All five order files
  (`enclosure`, `phone`, `site-hardware`, `pi-and-electronics`, `connectivity`) are asserted on
  filled values — `Order #: *[A-Za-z0-9-]{4,}`, a non-empty `Delivery ETA:` and a numeric
  `Actual price paid (USD):`. The prior `grep -qE 'Order #|Confirmation'` matched the label on the
  blank form the agent writes *before* the human buys (T-1-40).
- **The gate is quiet mid-phase and red only for real defects.** Four result states. `PENDING` means
  the producing task has not run; `NOT-YET` means a later wave deliberately falsifies the assertion
  and carries the gating reason in its label; `FAIL` means something is actually wrong. Today:
  `passed=4 failed=0 pending=43 not-yet=3`, exit 0. Under `--gate` both non-terminal states upgrade
  to `FAIL` and the script exits 1.
- **HW-06 is branch-aware.** `verify.sh` reads `evidence/site-survey/CONNECTIVITY-BRANCH` and selects
  the wireless or the ethernet assertion set; an absent file yields 13 `PENDING` lines prefixed
  `HW-06 (branch undetermined)`, and any string other than exactly `ethernet` or `wireless` is a hard
  `FAIL`. Both branches were exercised end to end during verification.
- **Every downstream plan can read the exact artefact shape it owes** — the `evidence/` tree exists,
  the mandatory nine-field order-record set is fixed, and the Per-Task Verification Map now carries a
  real Task ID, Plan and Wave on all 18 rows plus 5 ethernet-branch rows.
- **The repo root finally makes the OPS-01 claim.** `README.md` names `poc/` as the single
  authoritative implementation path, records the `voice/` scaffold removal and its
  browser-inlined-key rationale, and salvages the one useful fact (`@openai/agents` exposes
  `RealtimeAgent` / `RealtimeSession`).
- **Three ROADMAP success criteria now describe the project that exists.** Criterion 1 reads against
  the post-mounted cabinet (D-01) instead of a $2,195 indoor-rated mahogany booth; criterion 2 is
  branch-neutral on compute and cabling (D-07, D-10); criterion 3 admits a wired ethernet run as a
  third outcome and requires a cited number (D-06, D-09). Two of those three would have made
  correctly-delivered work read as unmet at `/gsd:verify-work` time.

## Task Commits

1. **Task 1: Create the evidence tree and author verify.sh** — `e607420` (feat)
2. **Task 2: Author root README.md and correct the superseded ROADMAP criteria** — `b4dc356` (docs)
3. **Task 3: Author the survey-protocol template and complete the Per-Task Verification Map** — `8829475` (docs)

## Files Created/Modified

- `.planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh` — the phase gate. 50 assertions across WAVE 0, HW-01 orders, HW-01 budget, HW-06 (branch-aware), OPS-01 and OPS-03. `set -u` only, no `set -e`, coreutils and `git` only, 0.05 s.
- `.../evidence/{orders,site-survey,spend-controls}/.gitkeep` — the committable empty evidence tree.
- `.../evidence/site-survey/survey-protocol.md` — the yard form: install spot (with the fixed `48 in` measurement height), survey device, throughput reference host, three W1/W2/W3 measurement windows, the GFCI and in-use-cover outlet inspection, and the pass bar.
- `README.md` — repo root. Repository layout naming `poc/`, the "Removed code" record for `voice/`, and a pointer to `poc/README.md`. Contains no `my-project` reference and no key material.
- `.../01-VALIDATION.md` — map filled (zero `TBD`), ethernet-branch sub-section, amendment record, branch-qualified Manual-Only HW-06 row, `wave_0_complete: true`, `nyquist_compliant: true`.
- `.planning/ROADMAP.md` — Phase 1 success criteria 1, 2 and 3 rewritten; the standing supersession note now names all three.
- `.planning/REQUIREMENTS.md` — HW-06 gains the wired-path evidence note citing D-06.

## Decisions Made

- **Line-anchor the two ethernet string assertions** (`^VERDICT: FEASIBLE *$`,
  `^Spot marker placed: *yes *$`). Plan 03's rendered template will contain the literal lines
  `VERDICT: FEASIBLE | NOT FEASIBLE` and `Spot marker placed: yes | no` per the phase-wide
  print-allowed-values-inline convention. Unanchored, those blank template lines pass from indoors.
- **Emit 13 `PENDING` lines when `CONNECTIVITY-BRANCH` is absent** — the union of both branches'
  assertion sets, prefixed `HW-06 (branch undetermined)`. Before plan 03 selects a branch, neither
  set is knowably applicable, so both are shown as outstanding rather than silently skipped.
- **File-existence guards are emitted as their own assertion lines.** A map row expands into an
  existence guard plus one line per grep. Documented as a "Correspondence note" in 01-VALIDATION.md
  so the map and the script remain provably in correspondence at differing line granularity.
- **`verify.sh` stays under `.planning/`** (T-1-06, accepted). It contains the literal string
  `my-project` and is excluded from the OPS-01 stale-reference grep only by the `:!.planning/`
  pathspec. Relocating it would silently break the gate; a comment in the script header says so.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] survey-protocol.md constrained fields would have pre-satisfied plan 07's assertion**

- **Found during:** Task 3 (survey-protocol template)
- **Issue:** The plan specifies printing allowed values inline for constrained fields, and separately
  notes that plan 07 Task 1 asserts
  `grep -qE 'Is this the production radio \(Pi 5\)\?: *(yes|no)'`. Writing that field the literal
  inline way — `Is this the production radio (Pi 5)?: yes | no` — makes the **blank** form match that
  assertion immediately, because ` *` consumes the single space and `yes` follows. That recreates
  exactly the label-versus-value defect (T-1-40) this plan exists to close, in a new file, one wave
  before plan 07 relies on it.
- **Fix:** Adopted a form that satisfies both constraints: `____   (allowed: yes | no)`. Allowed
  values are still printed inline on the line, the trailing colon the plan warns about is preserved,
  and the blank template does **not** match `: *(yes|no)` — only a filled-in answer does. Applied
  consistently to every constrained field in the form.
- **Files modified:** `.../evidence/site-survey/survey-protocol.md`
- **Verification:** `grep -qE 'Is this the production radio \(Pi 5\)\?: *(yes|no)'` on the blank form
  returns no match; the literal label with its trailing colon is present.
- **Committed in:** `8829475`

**2. [Rule 1 - Bug] 01-VALIDATION.md map row 3 still carried the superseded label-match command**

- **Found during:** Task 3 (Per-Task Verification Map)
- **Issue:** Map row 3 read `grep -qE 'Order #|Confirmation'`. `verify.sh` does not encode that
  assertion — it encodes the value-shaped replacement. Leaving the old command in the map violates
  the plan's own acceptance criterion that every assertion in `verify.sh` appears in
  `01-VALIDATION.md` *and vice versa*, and leaves a future reader with two contradictory
  specifications of the same gate.
- **Fix:** Updated rows 3, 4, 5 and 18 to state the assertion `verify.sh` actually encodes, and added
  the T-1-40 threat ref and the "Gate tests a filled value, not a printed label" secure-behavior cell.
  The Amendments sub-section still records what changed and why.
- **Files modified:** `.../01-VALIDATION.md`
- **Verification:** Token-by-token cross-check of every assertion string in `verify.sh` against
  `01-VALIDATION.md` — full correspondence, no orphans in either direction.
- **Committed in:** `8829475`

**3. [Rule 2 - Missing critical functionality] The CONNECTIVITY-BRANCH selector itself was an unregistered assertion**

- **Found during:** Task 3 (Pass 2, ethernet-branch rows)
- **Issue:** `verify.sh` hard-`FAIL`s when `CONNECTIVITY-BRANCH` contains anything other than exactly
  `ethernet` or `wireless`, but no row in `01-VALIDATION.md` owned that assertion. An unowned
  assertion has no task responsible for satisfying it, and a typo'd or free-text branch file would
  otherwise silently skip the entire HW-06 set.
- **Fix:** Added an Amendments row owned by `P03-T2 | 03 | 2` recording the branch-vocabulary
  assertion, alongside the existing branch-split provenance note.
- **Files modified:** `.../01-VALIDATION.md`
- **Verification:** `grep -q 'CONNECTIVITY-BRANCH' .../01-VALIDATION.md` succeeds; the branch
  selector was exercised with `ethernet`, `wireless` and a bogus value during Task 1 verification.
- **Committed in:** `8829475`

---

**Total deviations:** 3 auto-fixed (2 × Rule 2, 1 × Rule 1)
**Impact on plan:** All three protect the plan's own stated purpose — a gate that cannot green over
unspent or unmeasured work. No scope creep; no new files beyond the plan's `files_modified` list.

## Issues Encountered

- The plan's acceptance criterion greps for the literal heading `Amendments - assertion strengthening`
  with an ASCII hyphen. The first draft used an em dash and the check failed. Corrected both
  sub-section headings to the plan's literal text before committing Task 3.

## Known Stubs

The `evidence/` tree is intentionally empty apart from `.gitkeep` files, and `survey-protocol.md` is
intentionally a blank form. **Neither is a stub in the defect sense** — authoring empty, precisely
shaped artefact scaffolding *before* the tasks that fill it is this plan's entire stated purpose, and
`verify.sh` reports every unfilled artefact as `PENDING` rather than passing over it. Owners and
waves for every blank are recorded in the Per-Task Verification Map.

One temporal note for readers of the repo between now and wave 4: `README.md` records the `voice/`
scaffold as removed, but plan 09 performs the actual deletion in wave 4 (gated on the plan 06 key
revocation record, per D-23). This is the sequencing the plan specifies; `verify.sh` reports the
three affected OPS-01 assertions as `NOT-YET (gated on plan 09 deletion, wave 4)` until then.

## Threat Flags

None. No new network endpoints, auth paths, file access patterns or schema changes at trust
boundaries. `verify.sh` performs existence and shape assertions only, makes no network calls, and
reads no `.env` (D-24, T-1-04). No package installs (T-1-05).

## User Setup Required

None - no external service configuration required by this plan.

## Next Phase Readiness

**Wave 2 is unblocked.** Plans 02, 03, 04 and 05 can start: the evidence tree exists, the gate is
authored, and every artefact path and field shape those plans owe is written down in the
`<interfaces>` block of 01-01-PLAN.md and mirrored in the verification map.

Notes for downstream plan authors:

- **Plan 03** owns `CONNECTIVITY-BRANCH` (one line: `ethernet` or `wireless`, nothing else) and
  `ETHERNET-SCOPING.md`. The two string assertions against that file are **line-anchored** — the
  human must delete the unchosen alternative from `VERDICT: FEASIBLE | NOT FEASIBLE` and
  `Spot marker placed: yes | no`, not merely leave the template line intact.
- **Plans 05, 07, 08** must write *values* into the order files, not just render the field labels.
  The nine-field set is fixed; three of the nine are gated on filled content.
- **Plan 06** must write the structured token
  `KEY REVOKED: <key name> last-four <XXXX> on <YYYY-MM-DD>` into `SPEND-CEILING.md`. Plan 09's
  irreversible `rm -rf voice/` is gated on it. Per D-24 the token carries the key **name and last
  four characters only**.
- **Plan 10** must write a machine-readable `BUDGET STATUS: WITHIN CEILING` or
  `BUDGET STATUS: OVERRUN $<amount>` line at the start of a line in `budget-actual.md`, and must run
  `verify.sh --gate` (not the default mode) as the phase gate.

**Concern carried forward:** Phase 1 must complete by 2026-08-25. This plan consumed roughly 12
minutes of that budget and unblocks four parallel wave-2 plans, three of which (03, 04, 05) are on
the enclosure-lead-time critical path.

---
*Phase: 01-procurement-site-survey-repo-cleanup*
*Completed: 2026-08-18*
