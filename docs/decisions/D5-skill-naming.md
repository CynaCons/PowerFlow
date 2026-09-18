# D5 — Skill naming

Status: Accepted · 2026-09-18 (owner decision)

## Context

The proposal suggested `flow-*` for brevity in the slash menu. The tool family
is `powerplan`, `powerspawn`, `powerflow`; a skill named `flow-verify` does
not say where it came from once it sits in a project's menu next to
project-local skills.

## Decision

Skills are named `powerflow-<movement>`: `powerflow-init`, `powerflow-prd`,
`powerflow-decide`, `powerflow-srs`, `powerflow-plan`, `powerflow-slice`,
`powerflow-verify`, `powerflow-bug`, `powerflow-release`, `powerflow-memory`,
`powerflow-coordinate`, `powerflow-status`, `powerflow-audit`. The plugin is
named `powerflow`.

## Consequences

- Origin is obvious in any menu; no collision with the `powerplan` MCP server
  name or with project skills.
- Skill directories, PLAN tasks and the PRD skill table use the full name.
- Reopen never; renaming skills breaks muscle memory.
