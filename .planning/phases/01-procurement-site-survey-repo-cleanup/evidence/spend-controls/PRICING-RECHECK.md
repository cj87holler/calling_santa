# Realtime API Pricing Re-Check

**Fetch date:** 2026-08-24 (UTC 2026-08-25T01:33:01Z)
**Plan:** 01-02, Task 2
**Requirement:** OPS-03
**Governing decisions:** D-18 ($150/month hard limit, enforcement on, alerts at 50/75/90),
D-19 (the $5 balance is not the ceiling), D-20 (re-verify before setting the figure)
**Closes:** Assumptions A2 and A3 from `01-RESEARCH.md` — both rated **High** risk because the
official pricing page 404'd during research and the whole cost model rested on three secondary blogs.

> This document contains no API key, no account identifier and no organization ID.

## Source resolution

Fetched in the order the plan specifies, until one resolved:

| Order | URL | Result |
|-------|-----|--------|
| 1 | `https://openai.com/api/pricing/` | **HTTP 403** — no redirect, bot-blocked. (Research recorded a 404 here; either way it does not resolve.) |
| 2 | `https://platform.openai.com/docs/pricing` | **HTTP 200** — redirects to `https://developers.openai.com/api/docs/pricing`. **This is the source used below.** |
| 3 | `https://developers.openai.com/api/docs/guides/realtime-conversations` | HTTP 200 — fetched, but the rate table lives at the pricing URL above. |

One additional official page was fetched because it settles the token-per-minute derivation that A3
depends on:

| URL | Result | Why |
|-----|--------|-----|
| `https://developers.openai.com/api/docs/guides/realtime-costs` | **HTTP 200** | Official statement of Realtime billing mechanics, audio tokenization rate, caching and truncation behavior |

**A2 and A3 are now closed against a primary source.** The secondary-blog caveat that
`01-RESEARCH.md` attached to the entire cost model can be lifted.

## Verified rates — `developers.openai.com/api/docs/pricing`, fetched 2026-08-24

Section heading on the page: *"Realtime and audio generation models — Prices per 1M tokens unless
noted."*

### gpt-realtime-2.1 (full)

| Modality | Input | Cached input | Output |
|----------|-------|--------------|--------|
| **Audio** | **$32.00** per 1M audio input tokens | **$0.40** | **$64.00** per 1M audio output tokens |
| Text | $4.00 | $0.40 | $24.00 |
| Image | $5.00 | $0.50 | — |

### gpt-realtime-2.1-mini

| Modality | Input | Cached input | Output |
|----------|-------|--------------|--------|
| **Audio** | **$10.00** per 1M audio input tokens | **$0.30** | **$20.00** per 1M audio output tokens |
| Text | $0.60 | $0.06 | $2.40 |
| Image | $0.80 | $0.08 | — |

### What changed since research: nothing

**The rates are identical to the figures A2 recorded** ($32 / $64 per 1M audio in/out for the full
model; the mini "roughly ⅓" is exactly $10 / $20, which is 0.3125×). Three independent secondary
blogs were correct. **Assumption A2 is CLOSED — verified, unchanged, no price movement.**

**The new and materially useful number is the cached-input rate: $0.40 per 1M audio input tokens for
the full model — 80× cheaper than uncached input.** Research knew Realtime re-bills conversation
context on every turn but had no cached rate to price it with, which is the entire reason its
real-world estimate spanned the 4× band $0.06–0.46/min. That band can now be narrowed.

## Tokenization — verified, not assumed

From `developers.openai.com/api/docs/guides/realtime-costs` (fetched 2026-08-24), verbatim:

> *"Audio tokens in user messages are 1 token per 100 ms of audio, while audio tokens in assistant
> messages are 1 token per 50ms of audio."*

This is the official confirmation of the derivation `01-RESEARCH.md` used:

- 1 token / 100 ms heard → **600 audio tokens per minute heard**
- 1 token / 50 ms spoken → **1,200 audio tokens per minute spoken**

Two further mechanics from the same page that the model below depends on:

- **Billing is per Response, and the whole conversation so far is re-sent as input on every turn.**
- **Prompt caching is automatic and applies when a Response's input tokens match a previous
  Response's** — "best-effort and not guaranteed." Cache is busted by changing history; the largest
  documented cache-buster is **truncation**, which fires only when the conversation exceeds the
  context window (a 32k model with 4,096 max output tokens holds 28,224 input tokens).

## Arithmetic

### Step 1 — raw audio rate per minute

| | Heard (600 tok/min) | Spoken (1,200 tok/min) |
|---|---|---|
| **Full** | 600 × $32/1M = **$0.0192/min** | 1,200 × $64/1M = **$0.0768/min** |
| **Mini** | 600 × $10/1M = **$0.0060/min** | 1,200 × $20/1M = **$0.0240/min** |

### Step 2 — fresh audio in one 4-minute call

Assume a 4-minute call splits wall-clock roughly 50/50 between the child speaking and Santa speaking
— 2 min heard, 2 min spoken.

- **Full:** (2 × $0.0192) + (2 × $0.0768) = $0.0384 + $0.1536 = **$0.1920 per call**
- **Mini:** (2 × $0.0060) + (2 × $0.0240) = $0.0120 + $0.0480 = **$0.0600 per call**

### Step 3 — re-billed conversation context (the part that dominates)

Model the call as **12 turns of 20 s** (10 s child + 10 s Santa). Each turn appends
100 + 200 = **300 audio tokens** to the history. Turn *k* re-sends everything from turns 1..*k*−1, so
the total re-sent across the call is:

```
300 × (0 + 1 + 2 + ... + 11) = 300 × 66 = 19,800 audio input tokens
```

Priced at cache-hit rate *h* on those re-sent tokens, full model:

| Cache hit rate | Blended rate per 1M | Context cost per call | Total per call | Effective $/min |
|---|---|---|---|---|
| **h = 1.00** (caching fully effective) | $0.40 | $0.0079 | $0.200 | **$0.050** |
| **h = 0.70** | $9.88 | $0.196 | $0.388 | **$0.097** |
| **h = 0.55** | $14.62 | $0.290 | $0.482 | **$0.120** |
| **h = 0.00** (cache never hits) | $32.00 | $0.634 | $0.826 | **$0.206** |

**This reproduces the measured ranges research cited** — $0.06–0.11/min with caching working
(h ≈ 0.7–1.0) and $0.18–0.46/min without (h ≈ 0) — from first principles and official rates. The
secondary sources were measuring the cache-hit spectrum. **Assumption A3 is CLOSED**, with the
mid-range refined from $0.15/min to $0.12/min.

Session instructions (~300 text tokens) add roughly $0.0025 per call at $4.00/1M first-send plus
$0.40/1M cached re-sends. That is rounding noise here, but see COST LEVERS — a long prompt is not.

### Step 4 — mid-range figures adopted, and the caching assumption behind them

**Caching assumption: h ≈ 0.55 — caching only about half effective.** This is deliberately
pessimistic, and here is why the true figure is probably better:

The documented primary cache-buster is truncation, and **a capped Santa call never truncates.** A
5-minute call at the turn model above accumulates roughly 4,500 audio tokens plus instructions —
under 5,000 against a 28,224-token ceiling. The session's history is strictly append-only: no tool
calls, no mid-session instruction edits, no history rewriting. Those are exactly the conditions the
official guide names for maximizing cache rate. Realistically h should sit at 0.8–1.0, putting the
true cost near **$0.05–0.07/min**.

Sizing a spend ceiling against the optimistic end would be the wrong error to make, so the season
table below uses h ≈ 0.55 and carries roughly 2× headroom over the likely outcome.

- **Full model mid-range: $0.12/min → $0.48 per 4-minute call**
- **Mini model mid-range: $0.04/min → $0.16 per 4-minute call** (computed $0.038, rounded up)

## Season cost model at today's verified rates

4-minute calls, 30-day month.

| Load | Model | Cost/day | Cost/month |
|------|-------|---------:|-----------:|
| **10 calls/day** | gpt-realtime-2.1 | $4.80 | **$144** |
| **10 calls/day** | gpt-realtime-2.1-mini | $1.60 | **$48** |
| **30 calls/day** | gpt-realtime-2.1 | $14.40 | **$432** |
| **30 calls/day** | gpt-realtime-2.1-mini | $4.80 | **$144** |
| **60 calls/day** | gpt-realtime-2.1 | $28.80 | **$864** |
| **60 calls/day** | gpt-realtime-2.1-mini | $9.60 | **$288** |

**Comparison against the research baseline:** research put 30 calls/day at **≈ $540/month**; the
recomputed figure is **$432/month**, a change of **−20.0%**. That is **within** the ±30% band, and
the underlying rates did not move at all — the difference comes entirely from replacing the
$0.15/min guess with a cached-rate-aware $0.12/min. **No owner decision is triggered on this
ground; D-18's $150 stands.**

The headline from research survives intact: **at the full model and a busy neighborhood, the API
bill can exceed the entire hardware budget.** SESS-04 (5-minute cap), SESS-05 (silence ladder) and
ADMIN-02 (schedule) remain the primary cost controls; the hard limit is the backstop behind them.

## RECOMMENDED MONTHLY LIMIT

**$150 per month**, project-scoped, with "Enforce a hard limit" toggled **on**, per D-18.

Alerts at 50% / 75% / 90% ($75 / $112.50 / $135). Auto-recharge stays **off**. Set an
organization-level hard limit slightly above the project limit — **$175** — as a backstop against a
second key or project appearing.

**What $150/month actually buys** (31-day December, 4-minute calls):

| Model | Calls/month at $150 | ≈ Calls/day |
|-------|--------------------:|------------:|
| gpt-realtime-2.1 | 312 | **≈ 10/day** |
| gpt-realtime-2.1-mini | 937 | **≈ 30/day** |

**Read this before entering the figure in plan 06.** $150 is a *loss-tolerance* figure — the amount
the owner is willing to lose — not a *capacity* figure. Two consequences follow, and neither is a
reason to change the number, but both must be understood when it is set:

1. **On the full model, $150 supports about 10 calls/day.** A genuinely busy December — 30 calls/day
   — hits the cap around the 10th and Santa goes dark. Hard limits are **monthly and reset with the
   billing cycle**, so a cap hit on December 18th does not clear until January 1st, which is after
   the season. There is no partial-month reprieve.
2. **The mini model is what makes $150 a season-sized budget rather than a ten-day one.** It moves
   capacity from ~10 to ~30 calls/day at the same spend. This is a Phase 2 model-selection decision,
   but the arithmetic says it is the single highest-leverage cost choice in the project.

Also note, from the official docs: **enforcement is not instantaneous.** The platform can process a
small amount of extra usage while the limit state propagates, so recorded spend can slightly exceed
the configured amount. Treat $150 as approximate, not as a precise fence.

## COST LEVERS

Three levers change the arithmetic above. All are Phase 2 decisions; the owner should know they
exist before the ceiling is set.

1. **Use `gpt-realtime-2.1-mini` — verified 0.3125× the full model's audio rates** ($10/$20 vs
   $32/$64 per 1M audio in/out). Roughly 3× the calls for the same spend. Confirmed against today's
   official rate table, not estimated. **This is the dominant lever.**
2. **Keep the session prompt short.** Instructions sit at the very beginning of the conversation and
   are re-sent on every turn. The official guide is explicit that editing instructions mid-session
   busts the cache for all subsequent turns. A short, static `SANTA_INSTRUCTIONS` keeps re-billing in
   the $0.40/1M cached band; a long or dynamically-edited prompt drags it toward $32/1M.
3. **Use `audio/pcmu` output rather than PCM16** — carried forward from research, **but flagged as
   unverified.** The official tokenization statement prices audio purely by duration (1 token/100 ms
   heard, 1 token/50 ms spoken) with no codec qualifier, which implies pcmu saves *bandwidth* rather
   than *tokens*. Do not bank a cost saving on this lever until it is measured against a real
   `response.done` usage payload in Phase 2.

**A fourth lever, structural and already decided:** the 5-minute session cap (SESS-04) keeps every
conversation far below the 28,224-token truncation threshold, which is the main documented
cache-buster. The cap is not only a UX and cost control — it is what keeps prompt caching working.

## Cost line not in the research model

**Input transcription is billed separately if enabled.** Realtime bills speech-to-speech
conversation and input transcription from different rate cards. Today's page lists
`gpt-4o-mini-transcribe` at $0.003/minute, `gpt-transcribe` at $0.0045/minute and
`gpt-realtime-whisper` at $0.017/minute.

This matters because **CD-02 (vulgarity detection) is unresolved**. If the safety backstop turns out
to need input transcripts, add $0.006–$0.034 per 4-minute call — roughly **$5–$31/month at 30
calls/day**. Not budget-breaking, but it should not appear as a surprise line when CD-02 is settled
in Phase 4. (Generating a transcript transiently for a guardrail is a separate question from the
privacy rule against *storing* transcripts; that question belongs to CD-02, not here.)

## Assumptions log status

| ID | Was | Now |
|----|-----|-----|
| **A2** — Realtime pricing is $32/$64 per 1M audio in/out and mini is ~⅓ | High risk, three secondary blogs, official page 404'd | **CLOSED — verified exactly against `developers.openai.com/api/docs/pricing`, 2026-08-24. Mini is precisely 0.3125×. No price movement.** |
| **A3** — ~$0.15/min is a fair mid-range real-world estimate | High risk, 3× error would move the monthly figure from $180 to $540 | **CLOSED — refined to $0.12/min at h ≈ 0.55, derived from official rates and the official 100 ms / 50 ms tokenization statement. The blogs' $0.06–0.46/min spread is explained as the cache-hit spectrum, not as measurement disagreement.** |
