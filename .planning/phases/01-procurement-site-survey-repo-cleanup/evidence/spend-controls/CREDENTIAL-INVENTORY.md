# Credential Inventory — On-Disk Shape Only

**Inventory date:** 2026-08-18 (UTC 2026-08-19T02:38:41Z)
**Plan:** 01-02, Task 1
**Requirement:** OPS-03
**Governing decisions:** D-23 (check → rotate/revoke → delete, in that order), D-24 (never read or
echo the value)

> **This document records existence, counts and variable names only.** The contents of
> `voice/my-project/.env` were never read. No `cat`, `head`, `tail`, `less`, `sed -n p` or `awk`
> print-form was run against it at any point. The only operations performed on that file were
> `test -f`, `wc -l` and `grep -c` — the first two emit no line of the file, and `grep -c` emits a
> count rather than a match. No key value, key prefix, partial key or key-shaped placeholder appears
> anywhere below.

## Where these measurements were taken

Plan 01-02 executes inside a git worktree, and a worktree contains **tracked files only**. The
`.env` is gitignored and therefore does not exist inside the worktree. All on-disk facts below were
therefore measured against the **main working tree** at `/Users/cj.holler/Desktop/calling_santa`,
which is the checkout the owner actually uses and the one plan 09 will delete from. Git facts
(`git ls-files`, `git log`) are repository-wide and identical from either checkout.

## Facts

| # | Fact | Measured value | Command |
|---|------|----------------|---------|
| 1 | `voice/my-project/.env` exists on disk | **Yes** (exit 0) | `test -f voice/my-project/.env` |
| 2 | Count of API_KEY-shaped lines in that file | **1** | `grep -c 'API_KEY' voice/my-project/.env` |
| 3 | Total line count of that file | **1** | `wc -l < voice/my-project/.env` |
| 4 | Is that file tracked by git? | **No** — `error: pathspec ... did not match any file(s) known to git` (exit 1) | `git ls-files --error-unmatch voice/my-project/.env` |
| 5 | Commits in all history touching any `.env` | **0** | `git log --all --full-history --oneline -- '*.env' \| wc -l` |
| 6 | Tracked files under `voice/` | **27** | `git ls-files voice \| wc -l` |
| 7 | `VITE_OPENAI_API_KEY` occurrences in `voice/my-project/src/main.ts` | **1** | `grep -c 'VITE_OPENAI_API_KEY' voice/my-project/src/main.ts` |
| 8 | Same, in the nested duplicate `voice/my-project/my-project/src/main.ts` | **0** | `grep -c 'VITE_OPENAI_API_KEY' voice/my-project/my-project/src/main.ts` |
| 9 | `poc/.env` exists on disk | **No** (exit 1) | `test -f poc/.env` |
| 10 | Total `.env*` files anywhere in the repo (excluding `node_modules/`) | **1** — only `voice/my-project/.env` | `find . -maxdepth 3 -name '.env*' -not -path '*/node_modules/*' -type f` |

### What the shape means

- **One file, one line, one `API_KEY`-shaped line.** Facts 2 and 3 agree at 1, so the entire file is
  a single `VITE_OPENAI_API_KEY=...` assignment. There is exactly one credential to deal with here,
  not a set. This matches what RESEARCH.md's Runtime State Inventory observed.
- **Nothing leaked to GitHub.** Fact 4 confirms the file is untracked and fact 5 confirms no `.env`
  has ever appeared in any commit on any branch in the full history. `.gitignore` covers `.env`,
  `.env.*` and `*.key`, which is why. The credential's exposure is local-disk only — but see the
  revocation section: local-only is not the same as safe.
- **Fact 6 (27) matches research exactly**, so `voice/` has not drifted since the survey and plan
  09's deletion scope is unchanged.
- **Fact 7 is the finding that settles the disposition.** `src/main.ts` reads the key through Vite's
  `VITE_` prefix, which is the mechanism by which Vite **inlines the value into the browser bundle at
  build time**. Any key ever placed in this file was authored to be shipped to a client. The nested
  duplicate scaffold (fact 8) does not reference it.
- **Fact 9 corrects a research expectation.** RESEARCH.md anticipated "an `.env` or exported
  `OPENAI_API_KEY`" for `poc/server.py`; there is no `poc/.env` on disk, so the POC key is supplied
  as an exported shell environment variable, not a file. There is nothing under `poc/` to inventory
  and nothing there for plan 09 to orphan.

## REVOCATION REQUIRED

**The API key held in `voice/my-project/.env` must be revoked at
`platform.openai.com/settings/organization/api-keys` before `voice/` is deleted.**

This obligation is unconditional and does not depend on whether the key was ever used, whether it
has ever been billed, or whether it appears in any git history (it does not — fact 5).

**Why revoke rather than merely delete the file:** `voice/my-project/src/main.ts` was authored to
read this credential through `VITE_OPENAI_API_KEY` (fact 7). Vite substitutes `VITE_`-prefixed
variables directly into the emitted client bundle, so the key was written for a code path whose
entire purpose is to hand it to a browser. **It must therefore be treated as compromised by design.**
Deleting the file removes the copy on disk while leaving a live, billable, browser-destined
credential valid on the OpenAI account — which is precisely the unaccounted-for spend vector that
OPS-03 exists to close, and precisely the failure mode D-23 orders the operations to prevent.

**Sequencing (D-23 — mandatory, spans wave boundaries):**

1. **Check** — this document. Complete.
2. **Rotate / revoke** — plan 06 (wave 3). Revoke the key at the URL above, then record the outcome
   in `SPEND-CEILING.md` as the structured token
   `KEY REVOKED: <key name> last-four <XXXX> on <YYYY-MM-DD>`. Per D-24 that token carries the key's
   **name and last four characters only** — never the value, and never a prefix.
3. **Delete** — plan 09 (wave 4). `git rm -r voice/` followed by `rm -rf voice/` (the latter is
   required because `voice/my-project/node_modules/` is untracked). **This step is gated on step 2
   having been recorded.** Do not delete `voice/` while the revocation token is absent.

**Two adjacent actions for plan 06, which are not revocations and must not be confused with one:**

- The **POC key** (an exported `OPENAI_API_KEY`, no file on disk — fact 9) should be **migrated** to
  the dedicated project created per D-21, not revoked. It is a working credential for the codebase
  the project is keeping.
- **Auto-recharge stays off** and the $5 balance is **not** accepted as the ceiling (D-19). The hard
  spend limit is the control that matters; see `PRICING-RECHECK.md` for the figure to enter.

## Handling constraints observed

- The file's contents were never read, printed, copied, redirected or paraphrased.
- No key value, prefix, suffix, length, character class or redacted-but-shaped placeholder is
  recorded in this document, in the commit that adds it, or in the execution transcript.
- Only the variable **name** (`VITE_OPENAI_API_KEY`) is recorded. A variable name is not a
  credential, and it is required evidence for the browser-inlining finding above.
- This document is committed to a public-facing GitHub repository (T-1-04). Everything above is
  counts, variable names, public dashboard URLs and local file paths.
