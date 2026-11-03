---
phase: 01-procurement-site-survey-repo-cleanup
plan: 06
status: complete
completed: 2026-11-02
requirements: [OPS-03]
deviations: [D-29]
---

# 01-06 Summary — Spend controls

Owner configured the OpenAI dashboard on 2026-11-02. Full record in
`evidence/spend-controls/SPEND-CEILING.md`.

- `call-santa-prod` project exists; Standard service tier; no key-governance restrictions set.
- Project hard limit **$200**, org hard limit **$120** (usage-tier maximum, and therefore the binding
  cap), enforcement ON at both scopes. Alerts $60 / $90 / $110. Auto-recharge OFF. Credit balance $5.
- **Deviations (D-29):** owner attestation in place of screenshots; the single existing key was kept
  and moved into `call-santa-prod` instead of being revoked, after a re-scan found it in zero commits
  and no built bundle on disk.
- `verify.sh` amended to accept `OWNER ATTESTATION:` and `KEY RETAINED:`; OPS-03 now 7/7 PASS
  (overall `passed=11 failed=0 pending=36 not-yet=3`).
- Plan 09 gate amended: `rm -rf voice/` now requires `KEY BACKED UP: yes on <date>` — the
  `voice/my-project/.env` file may be the only on-disk copy of the live key.

## Open for the owner
- ~~Save the key outside `voice/`~~ — done 2026-11-02 (owner confirmed, password manager).
- Add season credit early in November so the usage tier rises before go-live; until then $120/month
  (≈8 calls/day full model, ≈25/day mini) is the ceiling.
