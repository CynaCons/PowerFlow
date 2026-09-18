# D2 — PLAN.md header

Status: Accepted · 2026-09-18

## Context

Three header styles exist: Goal / Philosophy / Stack (powerplan, RadEAU,
PowerNote); a Quick Summary with Key Metrics and a maintained "Recent
Achievements" list (powertimelines, powerplanner) that reached 110 lines and
drifted; and PowerGit's "Current Status" paragraph, which names no version and
therefore cannot go stale. powerplan resolves the current iteration itself.

## Decision

The PLAN.md header is: title, `**Goal:**`, `**Philosophy:**`, optional
`**Verify:**` (the one-line proof command), optional `**Stack:**`, a rule, then
a `## Current Status` paragraph stating that the current iteration is the last
heading not marked COMPLETE (resolved by `get_current_iteration` /
`show_miniplan`). No version number in the header, no achievement list, no
metrics table. Metrics are computed by `powerflow-status`, never maintained.

## Consequences

- `templates/PLAN.md` and `powerflow-init` produce this header; `create_plan`
  seeds Goal and Philosophy.
- History lives in the closed iterations themselves; release notes are derived
  from them (`powerflow-release`).
- Reopen if a project genuinely needs a maintained dashboard — then it belongs
  in `docs/`, generated, not in the plan header.
