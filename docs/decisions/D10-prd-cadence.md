# D10 — PRD cadence

Status: Accepted · 2026-09-18 (owner decision)

## Context

The proposal listed `powerflow-prd` beside the per-iteration skills, which
would invite routine PRD edits. In practice the PRD is written at project
start, iterated with the agent until it can guide the rest, and rewritten only
when the product changes direction (RadEAU's Ethernet-first rework, PowerGit's
"keep C# on Linux"). Routine change belongs in decisions, SRS rows and PLAN
tasks.

## Decision

A PRD is written once per project, or rewritten on a major change of
direction. `powerflow-prd` refuses routine edits and redirects: a constraint →
`powerflow-decide`; a behaviour → `powerflow-srs`; a task → `powerflow-plan`.
A direction change is declared by the owner, recorded as a decision, and only
then triggers a PRD revision with a new status line.

## Consequences

- The PRD stays a stable reference; agents do not churn it.
- `powerflow-init` runs the PRD interview; no other skill opens PRD.md for
  writing.
