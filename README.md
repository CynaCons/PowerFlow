# PowerFlow

**The method, codified once.** PRD → decisions → SRS → PLAN → agents →
verify → release, as a handbook, a template set and a `powerflow-*` skill
plugin for Claude Code — so every project runs the same flow without
re-specifying it.

| | |
|---|---|
| **Handbook** | [METHODOLOGY.md](METHODOLOGY.md) — the canonical text, ~5 pages |
| **Requirements** | [PRD.md](PRD.md) · decisions in [docs/decisions/](docs/decisions/README.md) |
| **Plan** | [PLAN.md](PLAN.md) — operated by [powerplan](https://github.com/CynaCons/powerplan) |
| **Pairs with** | [powerplan](https://github.com/CynaCons/powerplan) (PLAN.md single writer) · [PowerSpawn](https://github.com/CynaCons/PowerSpawn) (workers) |
| **Status** | v0.1.0 — definition (see PLAN.md) |

## What it is

```
METHODOLOGY.md          how work is done here — read once, link forever
templates/              PRD, PLAN header, AGENTS, CLAUDE shim, SRS index + file,
                        decisions, agents README, .mcp.json, CI guards
skills/powerflow-*/     one skill per movement of the loop (13)
.claude-plugin/         install once at user level, use in every project
```

## The loop in one line

Every session: **`show_miniplan` first, plan status update last.** Every
iteration: plan/docs → implement → verify → release, ending on a smoke test.
Every feature: an SRS row before code. Every owner report: a failing test
first, closed by the owner.

## Skills

| Skill | Use it when |
|---|---|
| `powerflow-init` | starting a project |
| `powerflow-prd` | the project starts, or changes direction (never routinely) |
| `powerflow-decide` | a constraint is chosen |
| `powerflow-srs` | a feature is specified |
| `powerflow-slice` | starting the next slice |
| `powerflow-plan` | opening, ticking, closing iterations |
| `powerflow-verify` | before saying "done" |
| `powerflow-bug` | the owner reports a defect |
| `powerflow-release` | shipping |
| `powerflow-memory` | something durable was learned |
| `powerflow-coordinate` | running workers over an iteration |
| `powerflow-status` | "where are we?" |
| `powerflow-audit` | checking a repo against the pack |

## Install

Not yet packaged (v0.2.0). Until then the handbook and templates are usable
by reading; the skills land in v0.1.2–v0.1.4.

## Origin

Distilled 2026-09-18 from eleven repositories by the same author; the
analysis is archived at [docs/proposal-2026-09-18.html](docs/proposal-2026-09-18.html).

## License

MIT.
