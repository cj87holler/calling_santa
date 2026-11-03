#!/usr/bin/env bash
#
# Phase 1 - Procurement, Site Survey & Repo Cleanup
# Verification harness. This script IS the phase gate.
#
# Usage:
#   bash .planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh
#       Default mode. Reports every assertion. PENDING and NOT-YET do not affect
#       the exit code, so the script is useful after every single task commit.
#
#   bash .planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh --gate
#       Gate mode. Every wave has run, so nothing is legitimately outstanding:
#       PENDING and NOT-YET are both upgraded to FAIL.
#
# Result states - three of the four are NOT the same thing:
#   PASS     the assertion is true
#   PENDING  the artefact does not exist yet because the task that produces it
#            has not run
#   NOT-YET  the assertion checks state that a later wave deliberately removes,
#            so it is correctly false right now; the label names the gating plan
#   FAIL     the assertion is false and nothing in the plan explains why
#
# GLOBAL MISSING-FILE RULE: any assertion whose target file does not exist reports
# PENDING and its greps are NOT run. Two reasons this is global rather than local
# to the order group: (a) the README assertion is not NOT-YET gated yet the file
# does not exist until plan 01 task 2, and (b) `! grep -qi camera` inverts a grep
# that exits 2 on a missing file, silently producing a false PASS. Exceptions: the
# WAVE 0 group and the three NOT-YET OPS-01 rows.
#
# DO NOT add `set -e`. Several assertions are expected to be false mid-phase and
# the script must report all of them rather than abort at the first one. Asserted
# absent by the plan's acceptance criteria.
#
# DO NOT relocate this script outside `.planning/`. The OPS-01 stale-reference
# assertion greps the working tree for the literal string 'my-project', which this
# script contains; it is excluded only by the `:!.planning/` pathspec (T-1-06).
#
# Never write a secret value, an API key, or the contents of any .env into this
# script. Existence and shape assertions only (D-24).

set -u

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || exit 2

EV=".planning/phases/01-procurement-site-survey-repo-cleanup/evidence"
SELF=".planning/phases/01-procurement-site-survey-repo-cleanup/verify.sh"

GATE=0
if [ "${1:-}" = "--gate" ]; then
  GATE=1
fi

passed=0
failed=0
pending_n=0
notyet_n=0

pass() {
  passed=$((passed + 1))
  printf 'PASS    %s\n' "$1"
}

fail() {
  failed=$((failed + 1))
  printf 'FAIL    %s\n' "$1"
}

pending() {
  if [ "$GATE" -eq 1 ]; then
    failed=$((failed + 1))
    printf 'FAIL    %s [was PENDING, upgraded by --gate]\n' "$1"
  else
    pending_n=$((pending_n + 1))
    printf 'PENDING %s\n' "$1"
  fi
}

notyet() {
  if [ "$GATE" -eq 1 ]; then
    failed=$((failed + 1))
    printf 'FAIL    %s [was NOT-YET, upgraded by --gate]\n' "$1"
  else
    notyet_n=$((notyet_n + 1))
    printf 'NOT-YET %s\n' "$1"
  fi
}

# ok <exit-status> <label>
ok() {
  if [ "$1" -eq 0 ]; then
    pass "$2"
  else
    fail "$2"
  fi
}

# count_glob <glob...> -> echoes the number of existing regular files
count_glob() {
  local n=0 f
  for f in "$@"; do
    [ -f "$f" ] && n=$((n + 1))
  done
  printf '%s' "$n"
}

echo "== Phase 1 verification =="
if [ "$GATE" -eq 1 ]; then
  echo "   mode: --gate (PENDING and NOT-YET are upgraded to FAIL)"
else
  echo "   mode: default (PENDING and NOT-YET are informational)"
fi
echo

# ---------------------------------------------------------------------------
# WAVE 0 - always evaluated, never PENDING and never NOT-YET
# ---------------------------------------------------------------------------
echo "-- WAVE 0 --"

test -d "$EV/orders" -a -d "$EV/site-survey" -a -d "$EV/spend-controls"
ok $? "WAVE0 evidence tree exists (orders, site-survey, spend-controls)"

test -x "$SELF"
ok $? "WAVE0 verify.sh is executable"

# ---------------------------------------------------------------------------
# HW-01 - order records. Value-shaped, never label-shaped.
#
# Every order file is created by its owning plan as an empty field form BEFORE
# the human buys anything, so the label `Order #:` is on disk with no purchase
# made. A label match greens the HW-01 gate over unspent money (T-1-40). Test
# the value.
# ---------------------------------------------------------------------------
echo
echo "-- HW-01 order records --"

# check_order <file> <label> <order-regex> <eta-regex> <price-regex>
check_order() {
  local f="$1" label="$2" p_order="$3" p_eta="$4" p_price="$5"
  if [ ! -f "$f" ]; then
    pending "HW-01 $label exists"
    pending "HW-01 $label has a filled Order # value"
    pending "HW-01 $label has a filled Delivery ETA value"
    pending "HW-01 $label has a filled Actual price paid (USD) value"
    return
  fi
  pass "HW-01 $label exists"
  grep -qE "$p_order" "$f"
  ok $? "HW-01 $label has a filled Order # value"
  grep -qE "$p_eta" "$f"
  ok $? "HW-01 $label has a filled Delivery ETA value"
  grep -qE "$p_price" "$f"
  ok $? "HW-01 $label has a filled Actual price paid (USD) value"
}

check_order "$EV/orders/enclosure-order.md" "enclosure-order.md" \
  'Order #: *[A-Za-z0-9-]{4,}' \
  'Delivery ETA: *[0-9A-Za-z]' \
  'Actual price paid \(USD\): *\$?[0-9]'

check_order "$EV/orders/phone-order.md" "phone-order.md" \
  'Order #: *[A-Za-z0-9-]{4,}' \
  'Delivery ETA: *[0-9A-Za-z]' \
  'Actual price paid \(USD\): *\$?[0-9]'

check_order "$EV/orders/site-hardware-order.md" "site-hardware-order.md" \
  'Order #: *[A-Za-z0-9-]{4,}' \
  'Delivery ETA: *[0-9A-Za-z]' \
  'Actual price paid \(USD\): *\$?[0-9]'

check_order "$EV/orders/pi-and-electronics-order.md" "pi-and-electronics-order.md" \
  'Order #: *[A-Za-z0-9-]{4,}' \
  'Delivery ETA: *[0-9A-Za-z]' \
  'Actual price paid \(USD\): *\$?[0-9]'

check_order "$EV/orders/connectivity-order.md" "connectivity-order.md" \
  'Order #: *[A-Za-z0-9-]{4,}' \
  'Delivery ETA: *[0-9A-Za-z]' \
  'Actual price paid \(USD\): *\$?[0-9]'

# ---------------------------------------------------------------------------
# HW-01 - budget reconciliation
# ---------------------------------------------------------------------------
echo
echo "-- HW-01 budget --"

BUDGET="$EV/orders/budget-actual.md"
if [ ! -f "$BUDGET" ]; then
  pending "HW-01 budget-actual.md exists"
  pending "HW-01 budget-actual.md carries no camera line item"
  pending "HW-01 budget-actual.md carries a machine-readable BUDGET STATUS line"
else
  pass "HW-01 budget-actual.md exists"
  if grep -qi camera "$BUDGET"; then
    fail "HW-01 budget-actual.md carries no camera line item"
  else
    pass "HW-01 budget-actual.md carries no camera line item"
  fi
  grep -qE '^BUDGET STATUS: (WITHIN CEILING|OVERRUN \$[0-9])' "$BUDGET"
  ok $? "HW-01 budget-actual.md carries a machine-readable BUDGET STATUS line"
fi

# ---------------------------------------------------------------------------
# HW-06 - branch-aware. The assertion set is selected by reading
# evidence/site-survey/CONNECTIVITY-BRANCH (D-06 through D-09).
# ---------------------------------------------------------------------------
echo
echo "-- HW-06 connectivity --"

DECISION="$EV/site-survey/CONNECTIVITY-DECISION.md"
SCOPING="$EV/site-survey/ETHERNET-SCOPING.md"
BRANCH_FILE="$EV/site-survey/CONNECTIVITY-BRANCH"

hw06_transport_evidence() {
  local tag="$1"
  local mtr_n ip_n
  mtr_n="$(count_glob "$EV"/site-survey/mtr-*.json)"
  ip_n="$(count_glob "$EV"/site-survey/iperf3-*.txt)"
  if [ "$mtr_n" -ge 1 ] && [ "$ip_n" -ge 1 ]; then
    pass "HW-06 $tag at least one mtr-*.json and one iperf3-*.txt present"
  else
    pending "HW-06 $tag at least one mtr-*.json and one iperf3-*.txt present"
  fi
}

hw06_undetermined() {
  local tag="(branch undetermined)"
  pending "HW-06 $tag CONNECTIVITY-BRANCH exists and reads exactly ethernet or wireless"
  pending "HW-06 $tag (wireless) at least 3 wifi-samples-*.csv files present"
  pending "HW-06 $tag (wireless) every wifi-samples-*.csv has at least 200 rows"
  pending "HW-06 $tag (ethernet) ETHERNET-SCOPING.md exists"
  pending "HW-06 $tag (ethernet) ETHERNET-SCOPING.md records a line-anchored VERDICT: FEASIBLE"
  pending "HW-06 $tag (ethernet) ETHERNET-SCOPING.md records Measured cable run length (ft) as a number"
  pending "HW-06 $tag (ethernet) ETHERNET-SCOPING.md records a line-anchored Spot marker placed: yes"
  pending "HW-06 $tag at least one mtr-*.json and one iperf3-*.txt present"
  pending "HW-06 $tag CONNECTIVITY-DECISION.md exists"
  pending "HW-06 $tag (wireless) CONNECTIVITY-DECISION.md names WiFi or LTE"
  pending "HW-06 $tag (wireless) CONNECTIVITY-DECISION.md cites a dBm figure"
  pending "HW-06 $tag (ethernet) CONNECTIVITY-DECISION.md names Ethernet"
  pending "HW-06 $tag (ethernet) CONNECTIVITY-DECISION.md cites an Mbps figure"
}

hw06_wireless() {
  local tag="(wireless)"
  local csv_n short any f lines

  csv_n="$(count_glob "$EV"/site-survey/wifi-samples-*.csv)"
  if [ "$csv_n" -ge 3 ]; then
    pass "HW-06 $tag at least 3 wifi-samples-*.csv files present"
  elif [ "$csv_n" -eq 0 ]; then
    pending "HW-06 $tag at least 3 wifi-samples-*.csv files present"
  else
    fail "HW-06 $tag at least 3 wifi-samples-*.csv files present (found $csv_n)"
  fi

  short=0
  any=0
  for f in "$EV"/site-survey/wifi-samples-*.csv; do
    [ -f "$f" ] || continue
    any=1
    lines="$(wc -l < "$f")"
    [ "$lines" -ge 200 ] || short=$((short + 1))
  done
  if [ "$any" -eq 0 ]; then
    pending "HW-06 $tag every wifi-samples-*.csv has at least 200 rows"
  else
    [ "$short" -eq 0 ]
    ok $? "HW-06 $tag every wifi-samples-*.csv has at least 200 rows"
  fi

  hw06_transport_evidence "$tag"

  if [ ! -f "$DECISION" ]; then
    pending "HW-06 $tag CONNECTIVITY-DECISION.md exists"
    pending "HW-06 $tag CONNECTIVITY-DECISION.md names WiFi or LTE"
    pending "HW-06 $tag CONNECTIVITY-DECISION.md cites a dBm figure"
  else
    pass "HW-06 $tag CONNECTIVITY-DECISION.md exists"
    grep -qE 'WiFi|LTE' "$DECISION"
    ok $? "HW-06 $tag CONNECTIVITY-DECISION.md names WiFi or LTE"
    grep -q 'dBm' "$DECISION"
    ok $? "HW-06 $tag CONNECTIVITY-DECISION.md cites a dBm figure"
  fi
}

hw06_ethernet() {
  local tag="(ethernet)"

  # The two numeric assertions exist because D-09 says a decision without a cited
  # number does not satisfy HW-06. Without them the cheapest way to pass this
  # branch is to hand-write VERDICT: FEASIBLE and never go outside.
  #
  # Both string assertions are LINE-ANCHORED on purpose. The phase-wide template
  # convention prints allowed values inline, so plan 03's blank form contains the
  # literal lines `VERDICT: FEASIBLE | NOT FEASIBLE` and `Spot marker placed: yes | no`.
  # An unanchored match would green against the blank template from indoors -
  # the same label-versus-value defect the order assertions were strengthened to close.
  if [ ! -f "$SCOPING" ]; then
    pending "HW-06 $tag ETHERNET-SCOPING.md exists"
    pending "HW-06 $tag ETHERNET-SCOPING.md records a line-anchored VERDICT: FEASIBLE"
    pending "HW-06 $tag ETHERNET-SCOPING.md records Measured cable run length (ft) as a number"
    pending "HW-06 $tag ETHERNET-SCOPING.md records a line-anchored Spot marker placed: yes"
  else
    pass "HW-06 $tag ETHERNET-SCOPING.md exists"
    grep -qE '^VERDICT: FEASIBLE *$' "$SCOPING"
    ok $? "HW-06 $tag ETHERNET-SCOPING.md records a line-anchored VERDICT: FEASIBLE"
    grep -qE 'Measured cable run length \(ft\): *[0-9]+' "$SCOPING"
    ok $? "HW-06 $tag ETHERNET-SCOPING.md records Measured cable run length (ft) as a number"
    grep -qE '^Spot marker placed: *yes *$' "$SCOPING"
    ok $? "HW-06 $tag ETHERNET-SCOPING.md records a line-anchored Spot marker placed: yes"
  fi

  hw06_transport_evidence "$tag"

  if [ ! -f "$DECISION" ]; then
    pending "HW-06 $tag CONNECTIVITY-DECISION.md exists"
    pending "HW-06 $tag CONNECTIVITY-DECISION.md names Ethernet"
    pending "HW-06 $tag CONNECTIVITY-DECISION.md cites an Mbps figure"
  else
    pass "HW-06 $tag CONNECTIVITY-DECISION.md exists"
    grep -q 'Ethernet' "$DECISION"
    ok $? "HW-06 $tag CONNECTIVITY-DECISION.md names Ethernet"
    grep -qE 'Mbps' "$DECISION"
    ok $? "HW-06 $tag CONNECTIVITY-DECISION.md cites an Mbps figure"
  fi
}

if [ ! -f "$BRANCH_FILE" ]; then
  hw06_undetermined
else
  BRANCH="$(cat "$BRANCH_FILE")"
  BRANCH="${BRANCH//[[:space:]]/}"
  case "$BRANCH" in
    wireless)
      pass "HW-06 CONNECTIVITY-BRANCH exists and reads exactly ethernet or wireless (wireless)"
      hw06_wireless
      ;;
    ethernet)
      pass "HW-06 CONNECTIVITY-BRANCH exists and reads exactly ethernet or wireless (ethernet)"
      hw06_ethernet
      ;;
    *)
      fail "HW-06 CONNECTIVITY-BRANCH must contain exactly ethernet or wireless"
      ;;
  esac
fi

# ---------------------------------------------------------------------------
# OPS-01 - exactly one authoritative implementation path
#
# Three of these four assertions are deliberately false until plan 09 runs in
# wave 4. They report NOT-YET with the gating plan named, so a red line always
# means a real defect rather than a wave that has not happened yet (T-1-41).
# The README assertion is NOT gated - plan 01 task 2 satisfies it in wave 1.
# ---------------------------------------------------------------------------
echo
echo "-- OPS-01 single implementation path --"

GATE_NOTE="(gated on plan 09 deletion, wave 4)"

if [ -z "$(git ls-files voice)" ]; then
  pass "OPS-01 no tracked files remain under voice/"
elif [ -d voice ]; then
  notyet "OPS-01 no tracked files remain under voice/ $GATE_NOTE"
else
  fail "OPS-01 no tracked files remain under voice/"
fi

if ! git grep -q -i 'my-project' -- . ':!.planning/'; then
  pass "OPS-01 no stale my-project references outside .planning/"
elif [ -d voice ]; then
  notyet "OPS-01 no stale my-project references outside .planning/ $GATE_NOTE"
else
  fail "OPS-01 no stale my-project references outside .planning/"
fi

if [ ! -f README.md ]; then
  pending "OPS-01 README.md exists at the repo root"
  pending "OPS-01 README.md names poc/ as the authoritative implementation path"
else
  pass "OPS-01 README.md exists at the repo root"
  grep -q 'poc/' README.md
  ok $? "OPS-01 README.md names poc/ as the authoritative implementation path"
fi

if [ ! -d voice ]; then
  pass "OPS-01 voice/ is gone from disk"
else
  notyet "OPS-01 voice/ is gone from disk $GATE_NOTE"
fi

# ---------------------------------------------------------------------------
# OPS-03 - spend controls
#
# The KEY REVOKED assertion is structured on purpose. Plan 06 writes the heading
# `## Key rotation record` unconditionally, so the older `grep -qi 'revok\|rotat'`
# matched with no revocation performed - and plan 09 gates an irreversible
# `rm -rf voice/` on it (T-1-02). Per D-24 the token carries the key NAME and
# LAST FOUR characters only; a key value must never appear.
# ---------------------------------------------------------------------------
echo
echo "-- OPS-03 spend controls --"

CEILING="$EV/spend-controls/SPEND-CEILING.md"

# D-29: the owner may attest to the dashboard configuration in SPEND-CEILING.md
# instead of capturing the four screenshots. The attestation line satisfies all four.
ATTESTED=1
[ -f "$CEILING" ] && grep -qE '^OWNER ATTESTATION: .+ on 20[0-9]{2}-[0-9]{2}-[0-9]{2}$' "$CEILING" && ATTESTED=0
for png in org-hard-limit.png project-hard-limit.png spend-alerts.png auto-recharge-off.png; do
  if [ -f "$EV/spend-controls/$png" ]; then
    pass "OPS-03 $png captured"
  elif [ "$ATTESTED" -eq 0 ]; then
    pass "OPS-03 $png covered by OWNER ATTESTATION (D-29)"
  else
    pending "OPS-03 $png captured"
  fi
done
if [ ! -f "$CEILING" ]; then
  pending "OPS-03 SPEND-CEILING.md exists"
  pending "OPS-03 SPEND-CEILING.md records a dollar figure"
  pending "OPS-03 SPEND-CEILING.md carries a KEY REVOKED or KEY RETAINED record"
else
  pass "OPS-03 SPEND-CEILING.md exists"
  grep -qE '\$[0-9]' "$CEILING"
  ok $? "OPS-03 SPEND-CEILING.md records a dollar figure"
  # D-29: either a structured revocation, or an owner-accepted retention line.
  grep -qE '^KEY REVOKED: .+ last-four [0-9A-Za-z]{4} on 20[0-9]{2}-|^KEY RETAINED: .+ on 20[0-9]{2}-[0-9]{2}-[0-9]{2}$' "$CEILING"
  ok $? "OPS-03 SPEND-CEILING.md carries a KEY REVOKED or KEY RETAINED record"
fi

# ---------------------------------------------------------------------------
echo
printf 'passed=%s failed=%s pending=%s not-yet=%s\n' \
  "$passed" "$failed" "$pending_n" "$notyet_n"

if [ "$failed" -gt 0 ]; then
  exit 1
fi
exit 0
