# Phase 1 — Session Handoff

**Paused:** 2026-08-27, mid `/gsd:execute-phase 1`
**Reason:** All agent-completable work is done. Four blocking human checkpoints are open.

> Supersedes the 2026-08-13 planning handoff (resolved 2026-08-18; preserved in git history at `5cc91f2`).

---

## Where things stand

| | |
|---|---|
| Plans complete | **2 / 10** — `01-01`, `01-02` (both have SUMMARY.md) |
| Plans at a blocking human gate | **4** — `01-03`, `01-04`, `01-05`, `01-06` |
| Plans blocked behind those | **4** — `01-07`, `01-08`, `01-09`, `01-10` |
| Validation gate | `verify.sh` → `passed=4 failed=0 pending=43 not-yet=3`, **exit 0** |
| Repo | on `main`, tree clean, no worktrees, no stray branches |

Phase verification was **not** run and the phase is **not** marked complete — correctly, since 8 plans remain.

**Resume with `/gsd:execute-phase 1`.** Completed plans are skipped via their SUMMARY.md. Each open
checkpoint resumes through a fresh continuation agent that verifies prior commits first.

---

## The four open gates

Answer any subset — each resumes independently. Ordered by what unblocks the most.

### 1. `01-06` — OpenAI dashboard (~20 min) → reply `configured`

Nothing committed yet; this plan's first task *is* the checkpoint.

1. `platform.openai.com/settings/` → create project **`call-santa-prod`**, issue a key scoped to it.
   Store in a password manager. **Never** into this repo, a commit, or chat.
2. Project → Limits → spend limit **$150** → **toggle "Enforce a hard limit" ON**.
   *A dollar amount with the toggle OFF is an alert, not a cap* — the most common way this gets
   marked done while providing zero protection. → `project-hard-limit.png`
3. Org limits → **$175** → **toggle ON** (must exceed the project limit; catches a future second
   key or project). → `org-hard-limit.png`
4. Alerts at 50/75/90% = **$75 / $112.50 / $135**. Alerts do not enforce. → `spend-alerts.png`
5. Billing → confirm **auto-recharge OFF** (D-19). → `auto-recharge-off.png`
6. **Revoke the `VITE_OPENAI_API_KEY`** from `voice/my-project/.env`. Record **name, last four,
   date** — never the value.
7. **POC key: migrate into `call-santa-prod`, do not revoke.** It is an exported shell var; there is
   no `poc/.env`. A migration gets prose, not a token.

PNGs go in `evidence/spend-controls/`. **Screenshot hygiene (D-24):** these land in a public repo and
cannot be un-pushed from forks. No key value, org ID, account number, or card in frame.

**Before you type the limit —** `$150` is a *loss-tolerance* figure, not a capacity figure:

| Model | $150/mo buys | ≈ calls/day |
|---|---|---|
| `gpt-realtime-2.1` | ~312 four-minute calls | **≈10/day** |
| `gpt-realtime-2.1-mini` | ~937 four-minute calls | **≈30/day** |

At a busy 30 calls/day the full model exhausts the cap **around December 10th — and OpenAI monthly
limits do not reset until January 1st**, after the season. Input transcription bills separately
(~$5–31/mo at 30/day) and is not in the numbers above. D-18 locks $150 and pricing has not moved, so
that is the planned figure; raise it if you choose and the deviation gets recorded.

### 2. `01-05` — Long-lead orders → reply `ordered`

Task 1 committed at `7a7e06d`. Buy against the spec qualifiers in
`evidence/orders/PROCUREMENT-LIST.md`, not against product titles.

- **Enclosure** — Ilyapa outdoor library box 16×14×22, ASIN `B0CPN4K6LP`, ~$150–230. Needs: solid
  wood/weatherproof composite · interior ≥15×13×20 · outdoor-rated · 4×4-post mountable. Over ~$280
  or unavailable → substitute on those four criteria and note which forced it.
  **Copy the vendor's outdoor-rating wording verbatim even if inconvenient** — the PRD claimed full
  weatherproofing for a unit both retailers label "For Indoor or Covered Use Only!", and Phase 3's
  weatherproofing scope is sized against whichever is true. Not the $2,195 mahogany booth.
- **Phone** — ECVISION rotary repro, ASIN `B00A8BOTWQ`, ~$70 *(price assumed; Amazon blocked
  automated checking)*. Must be **full body with intact cradle**. Not a bare handset; not a "USB
  retro handset".
- **Site hardware** — 4×4 PT post · fast-setting concrete · post cap + brackets · **IP68 compression
  gland** multi-pack · exterior **polyurethane** sealant **and** **100% silicone** (both) · breather
  vent + silica gel · handset anchor (D-04) · black UV zip ties. Order now: the footing needs cure
  time before the Phase 3 window.

Per line item report: vendor, SKU/ASIN, qty, actual price paid, order #, order date, delivery ETA,
spec qualifier confirmed. Plus the enclosure's stated outdoor rating + listed interior dimensions,
and yes/no on the phone's cradle. **Prices and order numbers only — no card, CVV, address, password.**

**Enclosure ETA is the field that matters:** anything after **2026-10-06** trips `LEAD TIME RISK`
against the Phase 3 build window.

> The three order files are deliberately **not** pre-created. `verify.sh` scores a missing order file
> as 4 PENDING but an empty one as 1 PASS + 3 FAIL — three blank forms would inject 9 FAILs and hold
> the gate red through waves 2–4. They get written once, with real values, at resume.

### 3. `01-04` — Compute decision → reply `pi-5` or `laptop`

`COMPUTE-COMPARISON.md` committed at `0395b8d` (305 lines, pishop.us + canakit.com, no marketplace).

| | `pi-5` (8GB board-only) | `laptop` |
|---|---|---|
| All-in today | **$239.75** | **$7.95** verified (+ unpriced hub) |
| Hook-switch | GPIO header, $0.00, one pin read | Pico H $5.00 + cable $2.95, USB serial + firmware |
| HW-04 LEDs | native, 3 pins | none on host — move to the Pico |
| Cold rating vs 20–50°F | 0–50°C | typically 10–35°C |
| Mid-season replacement | $175, in stock, re-image spare card | used-market hunt |
| Precedent | every documented rotary conversion | none found |

4GB saves exactly $65. The CanaKit kit costs $45.15 more than board-only and doesn't state its PSU wattage.

**The enclosure fit check decides it.** Cavity ≈14.5×12.5×20.5"; D-03 wants a sealed inner box ~2"
larger per horizontal axis. Pi in case → ~6×5×3.5", fits easily. 15.6" laptop → 16.2" wide, **1.7"
over**. 14" → 14.8", **0.3" over**. Only a **13"-or-smaller** laptop can be sealed per D-03 — anything
larger lies flat and unsealed on the cabinet floor, the exact arrangement D-03 forbids. And the 13"
that fits is still fan-cooled inside a box that must be sealed.

**Agent recommendation: `pi-5`, 8GB, board-only.** Keep 8GB over 4GB — CD-03 is open and may put
Grafana on this box; running out of headroom in November inside a sealed enclosure beats saving $65.

If `pi-5`: state 8GB/4GB and board-only/kit. If `laptop`: state make, model, RAM, CPU, screen size —
and note the four obligations: battery physically removed (D-12, not optional), BIOS
restore-on-AC-power-loss, sleep disabled, lid-close does nothing. No AC-power-loss setting in BIOS →
path not viable unattended.

*48-hour time box would expire 2026-08-29. Not triggered — this is the owner's first sight of it.
Do not write the `DECISION: OVERDUE` branch without confirming the box actually ran.*

### 4. `01-03` — Yard visit → reply `scoped`

Form on disk at `evidence/site-survey/ETHERNET-SCOPING.md` (committed `0c7ed68`) — fill it in place
on a phone. Carry a measuring wheel, one stake/paver/flag.

1. **Mark the spot first** — every later measurement, including plan 07's survey, references it.
2. Landmark reference only ("9 ft due south of the porch post"). **No street address, no GPS** — committed to the repo.
3. Walk the route the cable would actually take, not the straight line.
4. Assess the exit point and name a sealing method.
5. **Inspect the outdoor outlet on the same trip.** GFCI = TEST/RESET on the face; can't confirm in
   two minutes → write `unknown` (carries identically to `no`). In-use cover = **bubble** clamshell
   that closes **with a plug inserted**; a flat lid that shuts only when empty is `no`.
6. Set `VERDICT:`.

`FEASIBLE` requires **all three**: measured run **≤300 ft** (Cat6 limit 328; last 28 are margin) ·
sealable exit point with a named method · no trenching under a driveway and no 811 locate you won't
schedule. **A run that is technically possible only via a route you don't want to cut is still NOT
FEASIBLE** — a technical yes that never gets executed sends the project down the wrong branch.

FEASIBLE → `ethernet` (plan 07 skips three RF windows; BOM gains direct-burial Cat6 + PoE, loses the
extension cord). NOT FEASIBLE → `wireless` (full three-window survey; cord stays).

**Fill `survey-protocol.md` on the same trip** — same directory, same marker, 48 in height fixed in
both. Use *identical* landmark wording in both files, or every distance in the project is measured
from a different point than the one that gets dug.

**Three line-anchored grep traps** that fail the gate despite a real visit:
`Spot marker placed: yes` (col 0, nothing after) · `VERDICT: FEASIBLE` (col 0, one space, uppercase,
nothing after) · `Measured cable run length (ft):` **digits only** — not `~74`, not a range, not `74 ft`.

Do **not** create `CONNECTIVITY-BRANCH` yourself; the agent writes it. `verify.sh` hard-fails on any
word other than `ethernet`/`wireless`.

---

## Findings from this session worth carrying

**A worktree trap that would have defeated the revocation chain.** `test -f voice/my-project/.env`
**fails inside a git worktree** — worktrees materialize only tracked files and the `.env` is
gitignored. Read naively that records "no credential on disk," dissolving the D-23 revocation
obligation and clearing plan 09 to `rm -rf voice/` **while a live browser-destined key stays valid**.
Plan `01-02` caught it and measured against the main tree.
→ **Plan 09 must run on the main working tree, never in worktree isolation.** So must any plan that
inspects untracked on-disk state.

**Pricing assumption A2 is closed.** Official page resolves at `developers.openai.com/api/docs/pricing`
(200; the old URL 403s, which research misread as a 404). `gpt-realtime-2.1` $32/$64 per 1M audio
in/out, mini $10/$20 — matching research exactly. **No `PRICING MOVED` flag; $150 stands per D-18.**
New: **cached audio input is $0.40/1M, 80× cheaper than uncached** — which explains the 4× cost spread
across secondary blogs as a cache-hit spectrum rather than disagreement.

**The key is compromised by design regardless of deployment.** `voice/my-project/src/main.ts` reads it
via a `VITE_`-prefixed variable, and Vite inlines those into the client bundle at build time. It was
authored to be shipped to a browser. It appears in **0 commits** in full history, so `.env` is the only
on-disk trace — which is exactly why revocation must precede deletion.

**`audio/pcmu` is not a confirmed cost lever.** The official guide prices audio purely by duration with
no codec qualifier, so it likely saves bandwidth, not tokens. Don't bank it until a real
`response.done` usage payload confirms.

**Plan 01-06 prose undercounts its own gate.** It says "all six OPS-03 assertions"; `verify.sh` emits
**seven** (4 PNGs + 3 SPEND-CEILING). The harness is correct and stricter. Not a defect to fix —
`verify.sh` is not in that plan's `files_modified`.

**HW-06 and OPS-01 were wrongly marked Complete** by `requirements mark-complete` during plan 01-01 and
were reverted to In Progress with the completing plans named. **Plan 10 should mark them complete after
`verify.sh --gate` exits 0**, not before.

---

## Loose ends

- `.planning/config.json` is untracked — an orchestrator artifact
  (`{"workflow":{"_auto_chain_active":false}}`). Left alone deliberately. Commit it or gitignore it,
  owner's call.
- The **2026-08-25 Phase 1 target has passed.** Both remaining critical-path items are human-only:
  the enclosure order (lead time) and the dashboard (its revocation token gates plan 09's
  irreversible `rm -rf voice/`).
