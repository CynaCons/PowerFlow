# D3 — Coordinator guidance location

Status: Accepted · 2026-09-18

## Context

powertimelines keeps a 9 KB coordinator manual (delegation patterns, spawn
prompt shape, verification, audit rounds) in CLAUDE.md, which the harness
loads into every turn — including worker turns that must ignore it. PowerGit,
powerplanner, ARXMLExplorer and the training repo reduced CLAUDE.md to a shim
pointing at AGENTS.md. Skills load on demand.

## Decision

Coordinator procedure lives in the `powerflow-coordinate` skill (and the
handbook's agents section). CLAUDE.md is a shim that points at AGENTS.md.
AGENTS.md carries only what every agent needs every turn: project shape,
commands, how we verify, who owns which files, engineering rules, reporting
format.

## Consequences

- Worker turns stop paying for orchestration text they must not follow.
- The dispatch contract, ownership table and verification loop are written
  once in the skill and reused by every project.
- Reopen if a harness appears that cannot load skills and has no AGENTS.md
  equivalent — then the shim grows a minimal pointer to the handbook section.
