# Spend Ceiling — OpenAI controls for `call-santa-prod`

Configured by the owner on 2026-11-02. Values below are as reported by the owner.

## Configured limits

| Control | Value | Enforcement | Where it lives |
|---|---|---|---|
| Project hard limit (`call-santa-prod`) | **$200 / month** | "Enforce a hard limit" **ON** | Project settings → Limits |
| Organization hard limit | **$120 / month** (maximum the account's usage tier allows today) | "Enforce a hard limit" **ON** | Settings → Organization → Limits |
| Spend alerts | **$60 / $90 / $110** (50% / 75% / ~90% of the binding $120 org cap) | Email only — alerts do not enforce | Organization → Limits → alerts |
| Auto-recharge | **OFF** (D-19) | — | Organization → Billing |
| Prepaid credit balance | $5 at time of writing — the outermost fence | Requests fail at $0 | Organization → Billing |
| Service tier | Standard | — | Project settings |

**The binding ceiling is the $120 org limit, not the $200 project limit.** The org cap is enforced
first, so the project limit cannot be reached until the account's usage tier rises. OpenAI raises the
tier automatically with cumulative payment and account age; the org limit can then be raised from the
dashboard. Today, with $5 of credit and auto-recharge off, the credit balance binds before either.

### OWNER ATTESTATION (deviation from plan 01-06)

OWNER ATTESTATION: limits configured and enforcement toggles confirmed ON at project and org scope on 2026-11-02

The owner chose not to capture the four screenshots plan 01-06 called for, and attested to the
configuration directly. This replaces the PNG evidence; `verify.sh` accepts this line in place of the
images. Recorded as decision D-29 for this phase.

## Why this figure

`PRICING-RECHECK.md` recommended $150 (D-18), framed as "the amount you would be annoyed but not
upset to lose." The owner raised the project limit to $200; the account tier capped the org at $120.
At the re-verified rates (4-minute calls, 31-day December):

| Model | ≈ Calls/day at $120 | ≈ Calls/day at $200 |
|---|---:|---:|
| `gpt-realtime-2.1` | ≈ 8 | ≈ 13 |
| `gpt-realtime-2.1-mini` | ≈ 25 | ≈ 40 |

Input transcription bills separately and is not in these numbers. The figure is adjustable upward
from the dashboard in seconds if alerts start firing early — once the tier allows.

**Action before the season:** add season credit early in November so the usage tier has time to rise
before go-live; otherwise the $120 cap holds through December.

## Key rotation record

KEY RETAINED: owner decision, single key moved into call-santa-prod, not revoked, on 2026-11-02

The account has exactly one API key. It is the same key formerly held in the removed scaffold's
`voice/my-project/.env`, and the owner has moved it into `call-santa-prod`, so it now sits under the
project and org hard limits. The owner chose to keep it rather than revoke it (D-29).

Why the risk was accepted: plan 01-02 treated the key as compromised by design because
`voice/my-project/src/main.ts` read it through a `VITE_`-prefixed variable, which Vite inlines into a
client bundle at build time. On 2026-11-02 the repository was re-checked without printing any value:
zero key-shaped strings in any commit on any branch (local and `origin`), the `.env` was gitignored
and never committed, and no built `dist/` bundle exists on disk. The key was never exposed through the
repository. The residual risk — exposure through some build or copy outside the repo — is the owner's
to accept, and is capped by the limits above.

**Plan 09 gate change:** `rm -rf voice/` no longer gates on revocation. It gates on the key being saved
somewhere other than `voice/my-project/.env`, because that file may be the only on-disk copy:

KEY BACKED UP: pending

Plan 09 must not delete `voice/` until the line above reads `KEY BACKED UP: yes on <YYYY-MM-DD>`.

## Known limits of this control

- **Enforcement is not instantaneous.** The platform can process a small amount of extra usage while
  the limit state propagates, so recorded spend can slightly exceed the configured amount.
- **Hard limits are monthly and reset with the billing cycle.** A cap hit on December 18th does not
  unblock until January 1st, after the season.
- This ceiling is a backstop, not the primary control. The 5-minute session cap (SESS-04), the
  silence ladder (SESS-05) and the schedule (ADMIN-02) are what actually keep spend down.

## Carried to Phase 2

The `call-santa-prod` project and its key are the OPS-02 groundwork. The device key must live only in
the device environment, never in the repo.
