#!/usr/bin/env python3
"""Santa call report: sessions, cost, errors, latency and connectivity from ~/santa-logs.

Usage:
  python3 calls.py          today, last 7 days, connectivity, and today's calls
  python3 calls.py --live   also check right now whether the Pi can reach OpenAI

Reads the JSON lines call.py writes. Numbers only; the logs hold no audio or words.
Cost is an estimate from token counts; the OpenAI usage dashboard is the real bill.
"""

import glob
import json
import os
import socket
import sys
import time
from collections import Counter
from datetime import date

LOG_DIR = os.path.expanduser("~/santa-logs")
LATENCY_TARGET_S = 2.0  # SESS-03 / alert threshold: p95 turn latency under 2s


def load():
    records = []
    for path in sorted(glob.glob(os.path.join(LOG_DIR, "*.jsonl"))):
        with open(path) as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except ValueError:
                    pass
    return records


def p95(values):
    if not values:
        return None
    values = sorted(values)
    return values[min(len(values) - 1, int(round(0.95 * (len(values) - 1))))]


def fmt_s(v):
    return "-" if v is None else f"{v:.1f}s"


def summarize(title, calls):
    print(f"== {title} ==")
    if not calls:
        print("  no calls\n")
        return
    connected = [c for c in calls if c.get("end") not in ("auth", "session", "connect")]
    minutes = sum(c.get("seconds", 0) for c in calls) / 60
    cost = sum(c.get("cost_usd", 0) for c in calls)
    lat = [c["turn_latency_avg_s"] for c in calls if c.get("turn_latency_avg_s") is not None]
    worst = [c["turn_latency_max_s"] for c in calls if c.get("turn_latency_max_s") is not None]
    api_errors = sum(len(c.get("api_errors") or []) for c in calls)
    failed = len(calls) - len(connected)
    print(f"  calls           {len(calls)}  ({failed} failed to connect)")
    print(f"  talk time       {minutes:.1f} min   (avg {fmt_s(minutes * 60 / len(calls))} per call)")
    print(f"  est. cost       ${cost:.2f}   (avg ${cost / len(calls):.3f} per call)")
    if lat:
        flag = "  <-- over the 2s target" if p95(worst) > LATENCY_TARGET_S else ""
        print(f"  reply speed     avg {fmt_s(sum(lat) / len(lat))}, worst-turn p95 {fmt_s(p95(worst))}{flag}")
    print(f"  API errors      {api_errors}")
    ends = Counter(c.get("end", "?") for c in calls)
    print("  how calls ended " + ", ".join(f"{k} {v}" for k, v in ends.most_common()))
    print()


def connectivity(records, today):
    checks = [r for r in records if r.get("kind") == "health"]
    print("== Connectivity (checked every 5 min while call.py runs) ==")
    if not checks:
        print("  no checks logged yet\n")
        return
    last = checks[-1]
    sig = last.get("wifi_dbm")
    sig_txt = "-" if sig is None else f"{sig:.0f} dBm ({wifi_word(sig)})"
    ms = f", {last['openai_ms']} ms" if last.get("openai_ms") is not None else ""
    print(f"  last check      {last['time'][11:16]}: OpenAI {last.get('openai')}{ms}, WiFi {sig_txt}, CPU {last.get('cpu_c', '-')}°C")
    todays = [r for r in checks if r["time"].startswith(today)]
    bad = [r for r in todays if r.get("openai") != "ok"]
    print(f"  today           {len(todays)} checks, {len(bad)} failed")
    for r in bad[-5:]:
        print(f"    {r['time'][11:16]}  {r.get('openai')}")
    sigs = [r["wifi_dbm"] for r in todays if r.get("wifi_dbm") is not None]
    if sigs:
        print(f"  WiFi today      best {max(sigs):.0f} dBm, worst {min(sigs):.0f} dBm")
    print()


def wifi_word(dbm):
    if dbm >= -60:
        return "good"
    if dbm >= -70:
        return "ok"
    if dbm >= -80:
        return "weak"
    return "very weak"


def live_check():
    print("== Live check ==")
    t0 = time.monotonic()
    try:
        socket.create_connection(("api.openai.com", 443), timeout=5).close()
        print(f"  OpenAI reachable ({(time.monotonic() - t0) * 1000:.0f} ms)")
    except OSError as e:
        print(f"  OpenAI NOT reachable: {type(e).__name__}")
    print()


def main():
    records = load()
    today = date.today().isoformat()
    calls = [r for r in records if r.get("kind") == "call"]
    todays = [c for c in calls if c["time"].startswith(today)]

    summarize(f"Today ({today})", todays)
    summarize("Last 7 days", calls)
    connectivity(records, today)
    if "--live" in sys.argv:
        live_check()

    if todays:
        print("== Today's calls ==")
        print("  time   length  turns  reply  cost     ended")
        for c in todays:
            print(f"  {c['time'][11:16]}  {fmt_s(c.get('seconds')):>6}  {c.get('child_turns', 0):>5}"
                  f"  {fmt_s(c.get('turn_latency_avg_s')):>5}  ${c.get('cost_usd', 0):.3f}   {c.get('end')}")
        print()
    print("Cost is an estimate. The real bill: platform.openai.com > Usage.")


if __name__ == "__main__":
    main()
