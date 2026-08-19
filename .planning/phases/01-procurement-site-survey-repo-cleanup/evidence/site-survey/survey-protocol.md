# Site Survey — Field Form

**This is a form, not a document. Every line below with a `____` is a blank you fill in while
standing in the front yard.** Where a value is constrained, the allowed values are printed on the
line after `(allowed: ...)`. Replace the `____` with your answer; leave the `(allowed: ...)` hint
in place.

**Branch note (D-07):** if the ethernet run is feasible, complete only the **Install spot** and
**Outdoor outlet inspection** groups below and stop. The three measurement windows are skipped in
favour of `ETHERNET-SCOPING.md`. Under the wireless branch, complete every group.

**Before you start (two gotchas that silently ruin the numbers):**

1. Run `iperf3 -s` on a machine that is **wired** to the router. An iperf3 server on WiFi measures
   two wireless hops and the result is meaningless.
2. Disable WiFi power save on the survey device first:
   `sudo iw dev wlan0 set power_save off`. Without it you will record artificially poor latency.

---

## Install spot

    Spot marker:                                 ____   (stake, paver or flag actually used)
    Landmark reference:                          ____   (distance and bearing from a fixed feature,
                                                         e.g. "9 ft due south of the porch post")
    Measurement height:                          48 in  (fixed by protocol — do not change)
    Device orientation (compass heading):        ____   (degrees; note it and hold it)
    Straight-line distance to router (ft):       ____
    Obstructions between router and spot:        ____   (wall count and material, e.g.
                                                         "2 walls: exterior brick + interior drywall")

---

## Survey device

    Make/model:                                  ____
    OS and version:                              ____
    Wireless chipset (from lsusb or lspci):      ____
    Is this the production radio (Pi 5)?:        ____   (allowed: yes | no)
    If no - proxy caveat acknowledged:           ____   (allowed: yes | no)

> If the answer above is **no**, this reading is a proxy. A re-survey using the production Pi 5 is
> **mandatory in Phase 3, before the enclosure is sealed.** The Pi's antenna is the one that has to
> work in December, and it differs from a laptop's by 5–10 dB.

    WiFi power save disabled
    (sudo iw dev wlan0 set power_save off):      ____   (allowed: yes | no)

---

## Throughput reference host

    iperf3 server host:                          ____   (hostname or LAN IP)
    Server is WIRED to the router:               ____   (allowed: yes | no)
    If no - fallback method used and
    WAN-variance caveat recorded:                ____

---

## Measurement windows

Three windows, at least 20 minutes each, at different times of day.
**Exactly one of the three must be a weekday-evening window (18:00–22:00, Mon–Fri)** — that is peak
neighbourhood WiFi contention, peak ISP contention, and the actual operating hours of the
installation. One quiet-Sunday-morning reading will pass here and fail in December.

Log a sample every 5 seconds and keep the raw series. Each window produces one
`wifi-samples-<window>-<YYYYMMDD-HHMM>.csv` in this directory.

### Window W1

    Date:                                        ____
    Start time:                                  ____
    End time:                                    ____
    Duration (min, >= 20):                       ____
    Is this the weekday-evening window
    (18:00-22:00, Mon-Fri):                      ____   (allowed: yes | no)
    Weather - temp (F):                          ____
    Precipitation:                               ____
    Wind:                                        ____
    Leaf cover:                                  ____   (allowed: full | partial | bare)
    Raw sample file:                             ____   (wifi-samples-*.csv)

### Window W2

    Date:                                        ____
    Start time:                                  ____
    End time:                                    ____
    Duration (min, >= 20):                       ____
    Is this the weekday-evening window
    (18:00-22:00, Mon-Fri):                      ____   (allowed: yes | no)
    Weather - temp (F):                          ____
    Precipitation:                               ____
    Wind:                                        ____
    Leaf cover:                                  ____   (allowed: full | partial | bare)
    Raw sample file:                             ____   (wifi-samples-*.csv)

### Window W3

    Date:                                        ____
    Start time:                                  ____
    End time:                                    ____
    Duration (min, >= 20):                       ____
    Is this the weekday-evening window
    (18:00-22:00, Mon-Fri):                      ____   (allowed: yes | no)
    Weather - temp (F):                          ____
    Precipitation:                               ____
    Wind:                                        ____
    Leaf cover:                                  ____   (allowed: full | partial | bare)
    Raw sample file:                             ____   (wifi-samples-*.csv)

---

## Outdoor outlet inspection

> **Informational copy** — `ETHERNET-SCOPING.md` (plan 03) is the authoritative record of the outlet
> inspection and is what plan 10 reads. Fill both if you inspect the outlet during the wireless
> survey; if the two disagree, `ETHERNET-SCOPING.md` wins.

    Outlet present at intended power point:      ____   (allowed: yes | no)
    GFCI protection present:                     ____   (allowed: yes | no | unknown)
    In-use (bubble) weatherproof cover present:  ____   (allowed: yes | no)
    Distance from outlet to install spot (ft):   ____

Remediation (adding GFCI or an in-use cover) is an install-phase task. Record the finding here and
move on.

---

## Pass bar — reference only, nothing to fill in

| Metric | Pass |
|--------|------|
| WiFi RSSI | at or above **-67 dBm** |
| WiFi SNR | at or above **25 dB** |
| Packet loss to `api.openai.com` | below **0.5%** |
| Jitter | below **30 ms** |
| RTT to `api.openai.com` | below **100 ms** |
| Sustained throughput | at or above **2 Mbps** in each direction |

**Report min, median and p95 — never the mean.** The p5 RSSI and the p95 jitter are what break
calls; an average hides both.
