# Spike 01 — Analog phone + ATA → OpenAI Realtime over SIP

**Started:** 2026-11-02 · **Time box:** 2 evenings once hardware arrives · **Owner:** C.J.

## The question

Can a plain corded phone, plugged into a Grandstream HT801 ATA on the home network, reach Santa
(OpenAI Realtime) the moment the handset is lifted — with **no hook-switch wiring and no computer in
the yard**?

If yes: the Pi, GPIO hook switch, PoE run and sealed compute box leave the plan. Only a phone cord
runs to the yard. Phases 2–3 shrink substantially (a decision gets recorded and the roadmap is redone).
If no: the phone is still needed on the Pi path, so the only sunk cost is the ATA (~$50).

## How it would work

```
 [rotary phone] --phone cord--> [HT801 ATA] --ethernet--> [home router] --internet--> OpenAI SIP
   lift handset                 auto-dials on lift                                      |
                                                                                        v
                                                  [webhook program] <-- "call incoming, answer?"
                                                  accepts with Santa's instructions + voice
```

The webhook program is the new `server.py`: instead of handing a token to a browser, it answers
OpenAI's "incoming call" message with Santa's instructions, voice and tools.

---

## Shopping list (Amazon)

ASINs are deliberately not listed for the ATA: search the name and check the spec line before buying.
Prices are estimates, not verified.

| # | Item | Search Amazon for | Must have | ≈ Price |
|---|------|-------------------|-----------|--------:|
| 1 | **ATA** | `Grandstream HT801` (V2 is fine) | **1 FXS port**, sold by Grandstream or a reputable seller; includes power adapter | $45–60 |
| 2 | **Phone** | ECVISION rotary phone — ASIN `B00A8BOTWQ` | **Full phone with cradle**, standard RJ11 cord. *Not* a bare handset, *not* "USB retro handset" | ~$70 |
| 3 | Phone cord (test) | `RJ11 telephone cord 25 ft` | RJ11 both ends | ~$8 |
| 4 | Ethernet cable (if ATA doesn't include one) | `Cat6 ethernet cable 6 ft` | Any | ~$7 |

**Total ≈ $130–145.** Not needed for the test: the Pi, PoE gear, the 150 ft outdoor run. Hold those.

The ECVISION phone has no keypad, which doesn't matter here — the ATA dials automatically on lift.

---

## Test plan

### Part A — before the hardware arrives (no cost beyond a few test calls)

Proves the OpenAI half works, using a free softphone app on the laptop in place of the ATA.

1. **OpenAI webhook.** platform.openai.com → `call-santa-prod` → Settings → **Webhooks** → add one for
   the `realtime.call.incoming` event. Save the **webhook secret** in your password manager (not in
   the repo). Note the **project ID** (`proj_...`) — this is what the phone will dial.
2. **Host on Vercel (D-30).** The call handler lives in `santa-line/` and deploys to Vercel, so
   OpenAI can always reach it and no laptop tunnel is needed. Vercel's free-plan 300-second function
   limit sets Santa's hard cap at **4:30** (was 5:00).
3. **The `santa-line` webhook** (`/api/webhook`): verifies the webhook signature,
   **rejects any call not coming from your own phone/ATA** (see the safety note), then accepts with
   `SANTA_INSTRUCTIONS`, the voice, and the `end_call` tool.
4. **Install a softphone** (Linphone is free, Mac) and call
   `sip:<project-id>@sip.api.openai.com;transport=tls`.
5. **Pass:** Santa answers in his voice and runs the normal call through to his goodbye.
   Record: did it work **directly** from the softphone, or did it need a SIP provider (Twilio) in
   between? This answers the biggest open question before the ATA is even unboxed.

### Part B — hardware arrives

6. Plug in: phone → ATA **Phone** port; ATA → router; power on.
7. **Find the ATA:** the rotary phone can't dial the ATA's menu codes, so check the router's
   connected-devices list for "Grandstream" and open its IP in a browser. (On a keypad
   phone: `***` then `02` reads the IP aloud.) Default login is printed on the box label.
8. In the ATA web page, set the account to call OpenAI's SIP address (TLS), and set
   **Offhook Auto-Dial** (FXS Port page) to the Santa address, delay **0**. Claude will give exact
   field values once Part A shows which connection works.
9. **Pass/fail tests, kitchen table:**

| # | Test | Pass looks like |
|---|------|-----------------|
| B1 | Lift handset | Santa greets you within **~3 seconds**, no dialing |
| B2 | Full call | Name → wish → goodbye, all heard clearly in the handset |
| B3 | Santa hangs up | After his goodbye the line goes dead on its own (end_call works over SIP) |
| B4 | Child hangs up mid-call | Hang up → OpenAI session ends (check usage stops; no lingering cost) |
| B5 | Pick up again | Brand-new call; Santa doesn't remember your name |
| B6 | Sound quality | Voice is warm, not tinny/robotic over a phone line (phone audio is narrower than the laptop) |
| B7 | Stranger test | A call to the project from anything other than your ATA is **rejected** |

### Part C — what carries over from the POC (to check, not to build yet)

| POC feature | Over SIP? |
|---|---|
| Santa persona, voice, guardrails | ✅ same instructions |
| Santa hangs up himself | Webhook program calls the **hangup** endpoint |
| 5-minute cap | Webhook program runs a timer → hangup |
| Silence checks | Needs the program to watch the call over a WebSocket — doable, more work |
| Jingle on pickup / sparkle at end | **Open.** Browser can't play into a phone line. Options: Santa's first audio, the ATA, or drop it |
| No transcripts saved | ✅ unchanged — the program must not log call content |

---

## Safety note — read before Part A

Anyone who learns the project's SIP address can call it, and **each call bills your account**. The
webhook must **reject** every call that isn't from your own ATA/softphone (checked against something
only your devices send). Test B7 proves it. The $120 hard limit is the backstop, not the defense.

## Decision this spike feeds

- **Pass (B1–B7):** record "ATA + SIP replaces Pi + GPIO", re-plan Phases 2–3, cancel the Pi order,
  outdoor run becomes a phone cord.
- **Fail:** record why, keep the Pi path; the phone carries over.

## Sources

- OpenAI Realtime API with SIP — https://developers.openai.com/api/docs/guides/realtime-sip
- Grandstream Offhook Auto-Dial — https://support.8x8.com/devices-accessories/phones/ata-adapters/How_to_Set_Up_Offhook_Auto-Dial_on_Grandstream_ATAs
