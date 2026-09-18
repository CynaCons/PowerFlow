# D11 — Session bookends

Status: Accepted · 2026-09-18 (owner decision)

## Context

Every repo already says "update PLAN.md" somewhere, phrased differently
(realtime, before and after, when instructed). What is missing is a fixed
shape for a working session: where it starts and where it ends. powerplan's
JSON and ASCII views are tool-shaped; the owner wants the plan's own Markdown
as the view, scoped to the ongoing work.

## Decision

Every working session begins with PLAN.md and ends with PLAN.md:

1. **First** — `show_miniplan`: the current iteration as raw PLAN.md text
   with its major header and the neighbouring iteration headers for context.
   The coordinator reads it before any other file.
2. **Last** — status update through powerplan: tasks ticked with evidence,
   discovered work added as tasks, the iteration closed when every task has
   proof, `check_plan` green. Then the report to the owner.

`show_miniplan` is added to powerplan (v0.8.0) because the pack depends on it.

## Consequences

- `powerflow-plan`, `powerflow-slice`, `powerflow-verify` and
  `powerflow-coordinate` all open with the miniplan and close with the status
  update; the handbook states it once.
- Until powerplan 0.8.0 is released, `get_current_iteration` stands in for
  the opening call.
