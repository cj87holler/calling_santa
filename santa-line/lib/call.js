// Runs one Santa phone call after it has been accepted: opens the "sideband" WebSocket to the
// live OpenAI session and enforces the call rules the POC browser used to enforce —
// Santa hangs up himself, a hard time cap, and the silence ladder.
//
// PRIVACY: this file must never log or store what anyone said. It logs call metadata only
// (call id, duration, how the call ended).

import WebSocket from "ws";

const API = "https://api.openai.com/v1/realtime/calls";

// Vercel Hobby functions stop at 300s, so the call must end comfortably before that.
export const MAX_SECONDS = 4 * 60 + 30;        // 4:30 hard cap
const WRAP_NUDGE_AT = MAX_SECONDS - 45;        // ~3:45 — nudge Santa to start his goodbye
const SILENCE_CHECK_AT = 15;                   // s of dead air before "are you still there?"
const SILENCE_HANGUP_AT = 28;                  // s of dead air before Santa says goodbye
const CHARS_PER_SECOND = 13;                   // rough speaking rate, to estimate goodbye length

export async function hangup(callId, apiKey) {
  const r = await fetch(`${API}/${callId}/hangup`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  return r.status;
}

export function runCall(callId, apiKey) {
  return new Promise((resolve) => {
    const started = Date.now();
    const elapsed = () => Math.floor((Date.now() - started) / 1000);
    let lastActivity = 0, silencePrompted = false, wrapNudged = false;
    let endReason = null, pendingReason = null, finished = false;
    let santaText = "", santaAudioStartedAt = 0;

    const ws = new WebSocket(`wss://api.openai.com/v1/realtime?call_id=${callId}`, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });

    const send = (obj) => { if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(obj)); };
    const nudge = (note) => {
      if (pendingReason || endReason) return;
      send({ type: "conversation.item.create",
             item: { type: "message", role: "system", content: [{ type: "input_text", text: note }] } });
      send({ type: "response.create" });
      lastActivity = elapsed();
    };

    const finish = async (reason) => {
      if (finished) return;
      finished = true;
      clearInterval(tick);
      let status = "skipped";
      if (reason !== "caller_hung_up") {
        try { status = await hangup(callId, apiKey); } catch { status = "error"; }
      }
      try { ws.close(); } catch {}
      console.log(JSON.stringify({ event: "call_ended", call_id: callId, seconds: elapsed(), reason, hangup_status: status }));
      resolve({ seconds: elapsed(), reason });
    };

    // Hang up only after Santa's goodbye has had time to actually play down the phone line.
    // The text finishes generating long before the audio finishes playing.
    const hangupAfterSpeech = (reason) => {
      const spokenFor = santaAudioStartedAt ? (Date.now() - santaAudioStartedAt) / 1000 : 0;
      const remaining = Math.max(1, santaText.length / CHARS_PER_SECOND - spokenFor);
      setTimeout(() => finish(reason), (remaining + 0.8) * 1000);
    };

    ws.on("open", () => {
      console.log(JSON.stringify({ event: "call_connected", call_id: callId }));
      send({ type: "response.create" });            // Santa speaks first: "Ho... ho... ho!"
    });

    ws.on("message", (raw) => {
      let msg; try { msg = JSON.parse(raw); } catch { return; }
      switch (msg.type) {
        case "input_audio_buffer.speech_started":
          lastActivity = elapsed(); silencePrompted = false;
          break;
        case "response.created":
          lastActivity = elapsed(); santaText = ""; santaAudioStartedAt = 0;
          break;
        case "response.output_audio_transcript.delta":
          // used only to estimate how long the audio will take to play; never logged
          if (!santaAudioStartedAt) santaAudioStartedAt = Date.now();
          santaText += msg.delta || "";
          break;
        case "response.function_call_arguments.done":
          if (msg.name === "end_call") {
            try { pendingReason = JSON.parse(msg.arguments || "{}").reason || "goodbye"; }
            catch { pendingReason = "goodbye"; }
          }
          break;
        case "response.done":
          if (pendingReason && !endReason) { endReason = pendingReason; hangupAfterSpeech(endReason); }
          break;
        case "error":
          console.log(JSON.stringify({ event: "realtime_error", call_id: callId, code: msg.error?.code, type: msg.error?.type }));
          break;
      }
    });

    ws.on("close", () => finish(endReason || "caller_hung_up"));
    ws.on("error", (e) => {
      console.log(JSON.stringify({ event: "sideband_error", call_id: callId, message: String(e.message || e) }));
      finish("sideband_error");
    });

    const tick = setInterval(() => {
      const t = elapsed();
      if (t >= MAX_SECONDS) return finish("time_cap");
      if (endReason) return;
      if (!wrapNudged && t >= WRAP_NUDGE_AT) {
        wrapNudged = true;
        nudge("(The call is almost out of time. Warmly begin your goodbye now: give your encouraging send-off, then end the call.)");
      }
      const quiet = t - lastActivity;
      if (!silencePrompted && quiet >= SILENCE_CHECK_AT) {
        silencePrompted = true;
        nudge("(The child has gone quiet for a little while. Warmly check if they're still there.)");
      } else if (silencePrompted && quiet >= SILENCE_HANGUP_AT) {
        nudge("(Still no response from the child. Give a brief cheerful goodbye, then end the call with reason no_response.)");
      }
    }, 1000);
  });
}
