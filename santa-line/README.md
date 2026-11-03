# santa-line

Answers phone calls to Santa. A corded phone → Grandstream HT801 ATA → OpenAI Realtime (SIP) →
OpenAI calls `POST /api/webhook` here → we answer as Santa and watch the call until it ends.
Spike 01 (`.planning/spikes/01-ata-sip/TEST-PLAN.md`), decision D-30 (provisional).

- `api/webhook.js` — verifies OpenAI's signature, rejects any caller whose SIP `From` doesn't contain
  `ALLOWED_CALLER` (fails closed if unset), accepts with Santa's session, then runs the call in the
  background.
- `lib/call.js` — per-call rules: Santa hangs up via `end_call`, 4:30 hard cap (Vercel Hobby's
  300s function limit), silence ladder at 15s / 28s.
- `lib/santa.js` — persona copied from `poc/server.py`. Tune in the POC, then re-copy.

**Env vars (Vercel only, never in git):** `OPENAI_API_KEY`, `OPENAI_WEBHOOK_SECRET`,
`ALLOWED_CALLER`, optional `SANTA_VOICE`, `SANTA_MODEL`.

**Privacy:** logs call id, duration and end reason only. Never audio, never transcripts.

**Known limits (spike):** the `From` check stops casual strangers but can be spoofed by someone who
knows both the project ID and the caller name — the $120 hard limit is the backstop. No
one-call-at-a-time lock yet (needs storage). No pickup/hang-up jingles over the phone line yet.
