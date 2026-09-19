# Decision records

Architecture and process decision records for the decisions enumerated in
[PRD.md](../../PRD.md) §9. One file per decision, written before the affected
part is built. Status · Context · Decision · Consequences; the consequences
name the gate that would reopen the decision. IDs are never reused.

- [D1 — Requirement ID scheme](D1-requirement-ids.md) — `SRS-<FEAT>-NNN`, prefixes owned by one file, allocated in the SRS index, CI-checked.
- [D2 — PLAN.md header](D2-plan-header.md) — Goal · Philosophy · Verify · Stack, then a stale-proof Current Status paragraph; no achievement lists.
- [D3 — Coordinator guidance location](D3-coordinator-guidance.md) — lives in `powerflow-coordinate`; CLAUDE.md stays a shim.
- [D4 — powerplan registration](D4-powerplan-registration.md) — `uvx powerplan-mcp` by default; `python -m powerplan` without uv; submodule only when developing powerplan.
- [D5 — Skill naming](D5-skill-naming.md) — `powerflow-*`.
- [D6 — Distribution](D6-distribution.md) — personal plugin for skills; templates copied per project.
- [D7 — Migrated skills](D7-migrated-skills.md) — source repos keep a one-line pointer.
- [D8 — Showcase artifact](D8-showcase-artifact.md) — a PRD quality-bar switch read by `powerflow-verify`.
- [D9 — autosar-101-training](D9-autosar-training.md) — open; repo not located.
- [D10 — PRD cadence](D10-prd-cadence.md) — once per project or on a major redirection.
- [D11 — Session bookends](D11-session-bookends.md) — PLAN.md first (`show_miniplan`) and last (status update).
- [D12 — Turn-end miniplan](D12-turn-end-miniplan.md) — every major turn ends with the miniplan displayed verbatim.
