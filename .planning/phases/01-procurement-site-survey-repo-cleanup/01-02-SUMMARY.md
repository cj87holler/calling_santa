---
phase: 01-procurement-site-survey-repo-cleanup
plan: 02
subsystem: ops
tags: [openai, spend-controls, credentials, pricing, cost-model, security, evidence]

# Dependency graph
requires:
  - "01-01 — the evidence/spend-controls/ tree and verify.sh"
provides:
  - "evidence/spend-controls/CREDENTIAL-INVENTORY.md — shape-only record of the orphaned .env plus the REVOCATION REQUIRED obligation that gates plan 09's deletion"
  - "evidence/spend-controls/PRICING-RECHECK.md — official Realtime rates verified 2026-08-24, a recomputed season model, and the RECOMMENDED MONTHLY LIMIT figure plan 06 enters"
  - "Assumptions A2 and A3 closed against primary sources; the secondary-blog caveat on the whole cost model is lifted"
  - "The $0.40/1M cached-audio-input rate — the number that explains the blogs' 4x cost spread"
affects: [01-06, 01-09, 01-10]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Shape-only credential inspection: test -f, wc -l and grep -c are the complete permitted toolset against a .env (D-24)"
    - "Cost models are stated as a function of an explicitly-named assumption (cache-hit rate h), not as a single opaque per-minute guess"
    - "Cross-wave obligation tokens: an evidence file states the action a later plan must discharge, and the gate tests for the discharge record"

key-files:
  created:
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/spend-controls/CREDENTIAL-INVENTORY.md
    - .planning/phases/01-procurement-site-survey-repo-cleanup/evidence/spend-controls/PRICING-RECHECK.md
  modified: []

key-decisions:
  - "Measure the on-disk .env facts against the main working tree, not the worktree — a git worktree contains tracked files only, and the gitignored .env does not exist inside it. Measuring in the worktree would have recorded 'no credential on disk' and silently voided the revocation obligation"
  - "Adopt h = 0.55 (caching only half effective) for the season model even though the structural evidence says h should be 0.8-1.0 — sizing a spend ceiling against the optimistic end is the wrong error to make"
  - "Do not raise PRICING MOVED - OWNER DECISION NEEDED: the rates did not move at all, and the -20% shift in the monthly figure comes from replacing a guessed $0.15/min with a cached-rate-aware $0.12/min"
  - "Flag the audio/pcmu cost lever as unverified rather than carrying it forward as fact — the official tokenization statement prices audio by duration with no codec qualifier"
  - "Leave REQUIREMENTS.md untouched: OPS-03 is not satisfied by evidence documents, it is satisfied by dashboard configuration in plan 06 and its screenshots"

patterns-established:
  - "Assumption closure table: every High-risk assumption this plan targeted gets a was/now row naming the primary source that closed it"

requirements-completed: []
requirements-advanced: [OPS-03]

# Metrics
duration: ~25min
completed: 2026-08-25
---

# Phase 01 Plan 02: Credential Inventory & Pricing Re-Check Summary

**The two facts plan 06 needs before a human touches the OpenAI dashboard: a one-line orphaned `.env` inventoried by shape without ever being read, carrying an unconditional revocation obligation; and Realtime rates re-verified against the official page — unchanged at $32/$64 per 1M audio in/out — with a season model rebuilt on the newly-found $0.40/1M cached-input rate that closes both of the phase's High-risk assumptions.**

## Performance

- **Duration:** ~25 min of execution
- **Tasks:** 2 of 2
- **Files created:** 2
- **Checkpoints:** none (plan is fully autonomous)

## Accomplishments

- **The orphaned credential is inventoried and its contents were never read.** `voice/my-project/.env`
  exists, is **1 line** long and contains **1** API_KEY-shaped line — so the entire file is a single
  `VITE_OPENAI_API_KEY=` assignment. It is **untracked**, and `git log --all --full-history -- '*.env'`
  returns **0** commits, so nothing ever reached GitHub. Only `test -f`, `wc -l` and `grep -c` were
  run against it (D-24).
- **The revocation obligation is written down with the exact dashboard URL and is now gated.**
  `src/main.ts` references `VITE_OPENAI_API_KEY` exactly once, and Vite inlines `VITE_`-prefixed
  variables into the browser bundle at build time — so the key was authored to be shipped to a client
  and must be treated as compromised by design. `CREDENTIAL-INVENTORY.md` states the check → revoke →
  delete order (D-23) and names plan 06 and plan 09 as the discharging steps.
- **A2 is closed and pricing did not move.** The official page resolved and lists
  **gpt-realtime-2.1 at $32.00 / $64.00 per 1M audio input/output tokens** and
  **gpt-realtime-2.1-mini at $10.00 / $20.00** — matching research's secondary-blog figures exactly,
  with "roughly ⅓" turning out to be precisely 0.3125×. The caveat that hung over the entire cost
  model can be lifted.
- **A3 is closed, and the blogs' 4× cost spread is now explained rather than averaged over.** The
  official cost guide confirms the tokenization rate verbatim (1 token/100 ms heard, 1 token/50 ms
  spoken), and the pricing page exposes a **cached audio input rate of $0.40 per 1M — 80× cheaper
  than uncached**. Rebuilding the model as a function of cache-hit rate reproduces the reported
  $0.06–0.11/min (caching working) and $0.18–0.46/min (not working) from first principles. Those were
  never disagreeing measurements; they were two ends of one spectrum.
- **The season model is recomputed with its arithmetic shown**, at 10 / 30 / 60 calls per day for both
  models. At 30 calls/day the full model lands at **$432/month** against research's $540 baseline —
  a −20% move, **within** the 30% band, so `$150` stands per D-18 and no owner-decision flag is
  raised.
- **A structural finding that makes the cap cheaper than assumed.** The 5-minute session cap (SESS-04)
  keeps a conversation around 4,800 tokens against a 28,224-token truncation threshold. Truncation is
  the primary documented cache-buster, so it never fires in a capped Santa call — the session cap is
  not only a UX and cost control, it is what keeps prompt caching working.

## Task Commits

1. **Task 1: Inventory on-disk credential material without reading any value** — `e5c1a01` (docs)
2. **Task 2: Re-verify Realtime pricing and recompute the season cost model** — `de1a45a` (docs)

## Files Created

- `.../evidence/spend-controls/CREDENTIAL-INVENTORY.md` — 10 measured facts, each paired with the
  exact command that produced it; a "what the shape means" reading of those facts; and the
  `REVOCATION REQUIRED` section naming
  `platform.openai.com/settings/organization/api-keys` and the three-step D-23 sequence.
- `.../evidence/spend-controls/PRICING-RECHECK.md` — source-resolution table (which URLs 403'd,
  which resolved, fetch date), both verified rate tables, the four-step arithmetic derivation, a
  cache-hit sensitivity table, the six-row season table, `RECOMMENDED MONTHLY LIMIT`, `COST LEVERS`,
  and an assumption-closure table for A2 and A3.

## Decisions Made

- **Measure the `.env` against the main working tree, not the worktree.** This plan runs in a git
  worktree, which materializes **tracked files only**. The `.env` is gitignored, so it is genuinely
  absent from the worktree — `test -f` inside it returns 1. Running the inventory against the
  worktree would have produced "no credential on disk," dissolved the revocation obligation, and let
  plan 09 delete `voice/` while leaving a live browser-destined key valid. The document records where
  each fact was measured and why.
- **Use h ≈ 0.55 for the season model.** The evidence says caching should work well here (static
  append-only history, no truncation, no tool calls) and the true cost is likely $0.05–0.07/min. The
  model deliberately assumes caching is only half effective, carrying ~2× headroom, because
  under-sizing a spend ceiling fails worse than over-sizing one.
- **No `PRICING MOVED - OWNER DECISION NEEDED` flag.** The flag's trigger is re-verified *rates*
  moving the monthly figure >30%. The rates are byte-identical to A2; the −20% comes from improving
  the per-minute estimate, which is the task working as designed rather than a market change.
  Raising the flag would have sent a false "prices changed" signal to the owner.
- **State what $150 buys, without changing it.** D-18 locked $150 and this plan does not relitigate
  it. But $150 is a loss-tolerance figure, not a capacity figure: it funds ~10 calls/day on the full
  model (Santa goes dark around December 10th at 30 calls/day, and monthly limits do not clear until
  January 1st) versus ~30 calls/day on mini. The document surfaces this arithmetic so plan 06's
  checkpoint presents a decision the owner can actually see the consequences of.
- **Recommend a $175 organization-level backstop** above the $150 project limit, implementing
  research's defense-in-depth step 3 with a concrete number.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] The `.env` the plan instructs me to inventory does not exist in the execution environment**

- **Found during:** Task 1
- **Issue:** The plan specifies `test -f voice/my-project/.env` and expects it to succeed. Executed
  inside the assigned worktree it **fails** — a worktree checks out tracked files only, and the
  `.env` is gitignored. Taken at face value this would have been recorded as "no credential on disk,"
  which is both false and the most dangerous possible error in this plan: it would have dissolved the
  D-23 revocation obligation and cleared plan 09 to delete `voice/` while a browser-destined key
  stayed live.
- **Fix:** Measured all on-disk facts against the main working tree at
  `/Users/cj.holler/Desktop/calling_santa` (an authorized additional working directory and the
  checkout plan 09 will actually delete from), using the same read-restricted command set. Git facts
  are repository-wide and identical from either checkout. `CREDENTIAL-INVENTORY.md` documents where
  each fact was measured and why, so the number is reproducible rather than mysterious.
- **Files modified:** `.../evidence/spend-controls/CREDENTIAL-INVENTORY.md`
- **Commit:** `e5c1a01`

**2. [Rule 1 - Bug] Task 1's `API_KEY-shaped lines` acceptance grep failed on the first draft**

- **Found during:** Task 1 verification
- **Issue:** The table row was written as ``Count of `API_KEY`-shaped lines`` with markdown backticks
  around the identifier, so the literal string `API_KEY-shaped lines` the acceptance criterion (and
  the plan's `must_haves.artifacts.contains`) greps for was not present.
- **Fix:** Dropped the backticks on that row. Re-ran every Task 1 acceptance grep; all pass.
- **Files modified:** `.../evidence/spend-controls/CREDENTIAL-INVENTORY.md`
- **Commit:** `e5c1a01` (caught before commit)

**3. [Rule 2 - Missing critical functionality] The `audio/pcmu` cost lever is not supported by the official documentation**

- **Found during:** Task 2
- **Issue:** The plan directs me to record `audio/pcmu` output as a cost lever, carried from research.
  The official cost guide prices audio purely by **duration** — 1 token/100 ms heard, 1 token/50 ms
  spoken — with no codec qualifier anywhere. If tokens are a function of duration, pcmu saves
  bandwidth, not tokens, and the claimed cost saving may be zero. Recording it as an established
  lever would seed a Phase 2 budget assumption the primary source does not support.
- **Fix:** Recorded the lever as instructed, explicitly flagged as **unverified**, with the reasoning
  and a concrete way to settle it (measure a real `response.done` usage payload in Phase 2). The two
  levers that *are* verified — the mini model and prompt length — are marked as such.
- **Files modified:** `.../evidence/spend-controls/PRICING-RECHECK.md`
- **Commit:** `de1a45a`

**4. [Rule 2 - Missing critical functionality] Input transcription is a real cost line absent from the research model**

- **Found during:** Task 2
- **Issue:** The official guide states Realtime bills input transcription from a **separate rate
  card** when enabled. Research's season model does not account for it. CD-02 (vulgarity detection)
  is unresolved and is a plausible consumer of input transcripts, so this could appear as an
  unbudgeted line in Phase 4.
- **Fix:** Added a "Cost line not in the research model" section quantifying it —
  $0.003–$0.017/minute depending on transcription model, roughly $5–$31/month at 30 calls/day — and
  pointed it at CD-02. Noted that transiently generating a transcript for a guardrail is a distinct
  question from the privacy rule against storing transcripts, and belongs to CD-02.
- **Files modified:** `.../evidence/spend-controls/PRICING-RECHECK.md`
- **Commit:** `de1a45a`

### Deliberate non-deviations

- **`poc/.env` does not exist.** Research anticipated "an `.env` or exported `OPENAI_API_KEY`" for
  `poc/server.py`; `test -f poc/.env` returns 1, so the POC key is supplied as a shell environment
  variable. Recorded as fact 9 rather than treated as a discrepancy — research offered both
  possibilities and the second is the true one. Nothing under `poc/` needs inventorying and plan 09
  orphans nothing there.
- **`REQUIREMENTS.md` was not touched.** OPS-03 is a dashboard-configuration requirement. These two
  documents are its inputs, not its satisfaction. Following plan 01-01's deviation #4 and its note to
  plan 10, no requirement is marked complete from an intermediate plan.

---

**Total deviations:** 4 auto-fixed (2 × Rule 2, 1 × Rule 1, 1 × Rule 3)
**Impact on plan:** No scope change and no files beyond the plan's `files_modified` list. Deviation 1
is the consequential one — it is the difference between recording a live orphaned credential and
recording its absence.

## Issues Encountered

- `https://openai.com/api/pricing/` returns **HTTP 403** (bot-blocked, no redirect), not the 404
  research recorded. Either way it does not resolve for an agent; the plan's second candidate URL
  worked, so no fallback to research figures was needed.
- The pricing page is a client-rendered Astro app; the rate table had to be recovered from the
  server-rendered HTML rather than read as text. The extracted figures were cross-checked against the
  page's own `Model / Modality / Input / Cached input / Output` column headers before use.

## Known Stubs

None. Both documents are complete and carry no placeholder, no TBD and no unfilled field.

`verify.sh` still reports the seven OPS-03 assertions as `PENDING` — this is correct and expected.
Every one of them tests plan 06's outputs (four dashboard screenshots and `SPEND-CEILING.md`), not
this plan's. There is no assertion in the harness that targets `CREDENTIAL-INVENTORY.md` or
`PRICING-RECHECK.md`; their acceptance criteria live in this plan and were verified directly.

## Threat Flags

None. No new network endpoints, auth paths or schema changes. The only outbound traffic was
read-only anonymous HTTPS GETs of public OpenAI documentation, presenting no credential (T-1-05
scope: no package was installed).

Threat register dispositions discharged by this plan:

- **T-1-02** (info disclosure via `.env` inspection) — mitigated. Only `test -f`, `wc -l` and
  `grep -c` were run against the file. `grep -cE 'sk-[A-Za-z0-9]{8}'` returns **0** on both artifacts,
  and a recursive scan of the whole `evidence/` tree returns no match.
- **T-1-04** (evidence committed to a public repo) — mitigated. Both documents contain only counts,
  variable names, public pricing figures, public dashboard URLs and local paths. No account or
  organization identifier.
- **T-1-03** (financial DoS via a wrong limit) — mitigated. The figure now rests on rates verified at
  execution time from the official source.
- **T-1-01** (live browser-destined key) — the revocation obligation is recorded with its URL and
  sequencing; plan 06 discharges it, plan 09 is gated behind it.

## User Setup Required

None from this plan. It produces the inputs for the human work in **plan 06**, which needs:

1. **Revoke** the key from `voice/my-project/.env` at
   `platform.openai.com/settings/organization/api-keys`, then record
   `KEY REVOKED: <key name> last-four <XXXX> on <YYYY-MM-DD>` in `SPEND-CEILING.md`. Name and last
   four only (D-24). **Plan 09's `rm -rf voice/` is gated on this record.**
2. **Set the hard limits** — $150/month project-scoped with "Enforce a hard limit" **on**, $175 at
   the organization level as a backstop, alerts at $75 / $112.50 / $135, auto-recharge **off**.
3. **Migrate** the POC key into the new dedicated project (D-21) rather than revoking it.

## Next Phase Readiness

**Plan 06 is unblocked and has everything it needs to run as a scripted human checkpoint** — the
dollar figure, the alert thresholds, the exact dashboard URLs, and the revocation token format.

Carried forward for the plan 06 checkpoint author: the $150 figure is locked by D-18 and this plan
does not challenge it, but the owner should see the capacity arithmetic when they set it — **$150
funds roughly 10 calls/day on `gpt-realtime-2.1` and roughly 30 on the mini**, and a monthly hard
limit hit mid-December does not reset until January 1st. If the owner expects a busy neighborhood,
the honest options are a higher ceiling or an early commitment to the mini model. The mini decision
is nominally Phase 2, but it is the single highest-leverage cost choice in the project and the
ceiling is being sized now.

**Concern carried forward:** Phase 1 must complete by 2026-08-25 and that date has now arrived. This
plan is done and blocks nothing, but plan 06 requires a human at the OpenAI dashboard, and plan 09
cannot run until plan 06's revocation record exists.

## Self-Check: PASSED

- `CREDENTIAL-INVENTORY.md` — exists on disk, tracked in git.
- `PRICING-RECHECK.md` — exists on disk, tracked in git.
- Commits `e5c1a01` and `de1a45a` both present in `git log`.
- `bash verify.sh` exits **0** (`passed=4 failed=0 pending=43 not-yet=3`) — unchanged from plan 01,
  as expected, since no OPS-03 assertion targets this plan's artifacts.
- `git log -p --all -- '*.env'` returns **0 lines**.
- `grep -rE 'sk-[A-Za-z0-9]{8}' evidence/` returns **no match**.
- All Task 1 acceptance greps pass (`REVOCATION REQUIRED`, `API_KEY-shaped lines`,
  `platform.openai.com/settings/organization/api-keys`, `contents were never read` ×1, `sk-` count 0,
  voice tracked-file count and `VITE_OPENAI_API_KEY` count each paired with their command).
- All Task 2 acceptance greps pass (`RECOMMENDED MONTHLY LIMIT` ×1, `per 1M audio` ×6, `COST LEVERS`
  ×2, dollar figures present, `sk-` count 0, season rows for 10/30/60 calls per day, resolved URL and
  fetch date named).
- Per-plan constraint honored: **`STATE.md` and `ROADMAP.md` were not modified.**

---
*Phase: 01-procurement-site-survey-repo-cleanup*
*Completed: 2026-08-25*
