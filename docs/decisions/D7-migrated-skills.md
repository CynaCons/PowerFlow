# D7 — Migrated skills

Status: Accepted · 2026-09-18

## Context

powerplanner's `.claude/skills/powerplan` (ASCII gantt) and `visual-plan`
were written as portable; PowerGit's `release` skill and RadEAU's
`check-req-ids.mjs` are the sources of `powerflow-release` and the guards
template. Leaving copies behind means two diverging versions.

## Decision

Once a skill ships in PowerFlow, its source repo keeps a one-line pointer
file at the old path (name, "moved to PowerFlow", the new skill name) and the
body is removed. Project-specific parts (PowerGit's release commands) stay in
that project's AGENTS.md, which `powerflow-release` reads.

## Consequences

- No divergent copies; repos stay self-describing.
- Applied in PowerFlow v0.2.0 when the plugin is installed on this machine,
  not before — the pointer must not precede the replacement.
