// OpenAI calls this when a phone call reaches the call-santa-prod project.
// It decides whether to answer, answers as Santa, then keeps watching the call in the
// background (waitUntil) until it ends.
//
// Environment variables (set in Vercel, never in this repo):
//   OPENAI_API_KEY         the call-santa-prod key
//   OPENAI_WEBHOOK_SECRET  from the webhook you create in the OpenAI dashboard
//   ALLOWED_CALLER         text that must appear in the caller's SIP "From" address
//                          (the username set on your ATA/softphone). Unset = reject every call.
//   SANTA_VOICE / SANTA_MODEL  optional, default ash / gpt-realtime

import OpenAI from "openai";
import { waitUntil } from "@vercel/functions";
import { SANTA_INSTRUCTIONS, SANTA_TOOLS } from "../lib/santa.js";
import { runCall } from "../lib/call.js";

const API = "https://api.openai.com/v1/realtime/calls";

function sessionConfig() {
  return {
    type: "realtime",
    model: process.env.SANTA_MODEL || "gpt-realtime",
    instructions: SANTA_INSTRUCTIONS,
    output_modalities: ["audio"],
    tools: SANTA_TOOLS,
    tool_choice: "auto",
    audio: {
      input: {
        turn_detection: {
          type: "server_vad",
          threshold: 0.5,
          prefix_padding_ms: 300,
          silence_duration_ms: 700,   // a little generous so a kid's pause doesn't cut them off
          create_response: true,
          interrupt_response: true,
        },
      },
      output: { voice: process.env.SANTA_VOICE || "ash" },
    },
  };
}

function header(event, name) {
  const h = (event.data?.sip_headers || []).find((x) => x.name.toLowerCase() === name.toLowerCase());
  return h ? h.value : "";
}

export function GET() {
  return Response.json({ ok: true, service: "santa-line" });
}

export async function POST(request) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey || !process.env.OPENAI_WEBHOOK_SECRET) {
    console.log(JSON.stringify({ event: "not_configured" }));
    return new Response("not configured", { status: 503 });
  }
  const client = new OpenAI({ apiKey, webhookSecret: process.env.OPENAI_WEBHOOK_SECRET });

  let event;
  try {
    event = await client.webhooks.unwrap(await request.text(), request.headers);
  } catch {
    return new Response("invalid signature", { status: 400 });
  }
  if (event.type !== "realtime.call.incoming") return new Response(null, { status: 200 });

  const callId = event.data.call_id;
  const from = header(event, "From");
  const allowed = process.env.ALLOWED_CALLER;

  // Only our own phone may reach Santa — every call bills the account. Fail closed.
  if (!allowed || !from.includes(allowed)) {
    await fetch(`${API}/${callId}/reject`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify({ status_code: 603 }),
    });
    console.log(JSON.stringify({ event: "call_rejected", call_id: callId, reason: allowed ? "caller_not_allowed" : "ALLOWED_CALLER_unset" }));
    return new Response(null, { status: 200 });
  }

  const r = await fetch(`${API}/${callId}/accept`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify(sessionConfig()),
  });
  console.log(JSON.stringify({ event: "call_accepted", call_id: callId, status: r.status }));
  if (!r.ok) return new Response(null, { status: 200 });

  waitUntil(runCall(callId, apiKey));
  return new Response(null, { status: 200 });
}
