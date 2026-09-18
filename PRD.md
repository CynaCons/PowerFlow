# PowerFlow — Product Requirements

**One-liner:** The PRD → decisions → SRS → PLAN → agents → verify → release
methodology, codified once — a handbook, a template set and a `powerflow-*`
skill plugin — so every project runs the same flow without re-specifying it.

**Home:** `C:\dev\public-repo\PowerFlow` (GitHub: CynaCons/PowerFlow, to be
published). Sibling of [powerplan](https://github.com/CynaCons/powerplan)
(single writer of PLAN.md) and
[PowerSpawn](https://github.com/CynaCons/PowerSpawn) (cross-model workers).

Status: PRD 2026-09-18 — see [PLAN.md](PLAN.md) for the build plan and
[METHODOLOGY.md](METHODOLOGY.md) for the method itself. The analysis this PRD
rests on is archived at [docs/proposal-2026-09-18.html](docs/proposal-2026-09-18.html).

---

## 1. Problem

Eleven repositories (PowerGit, RadEAU, powerplanner, powertimelines,
powerplan, powerspawn, ARXMLExplorer, OpenT A2L-Forge, PowerNote, powerforge,
training-ai-software-engineering-101) run the same development loop, and each
one re-decided how to encode it. Observed drift, all from the same author:

- Five requirement-ID schemes (`SRS-NAV-001`, `VU-001` + registry,
  `CC-REQ-ZOOM-001`, `REQ-TEXT-001`, `R1…R21`), three SRS locations, four
  table-column sets.
- Three PLAN.md header styles — one of which (a maintained "Recent
  Achievements" list) grew to 110 lines and went stale.
- CLAUDE.md as a shim in four repos, a full duplicate in one, a 9 KB
  coordinator manual loaded into every worker turn in another.
- Four ways to register the same powerplan MCP server.
- Memories, decision records and CI guards present in the newest repo only.

The method is stable; the encoding is not. Every new project pays the
re-specification cost, and every agent session pays it again in context.

## 2. Users

- **The owner** (Constantin): starts projects, steers iterations, closes owner
  reports, cuts releases. Wants to say "start the next slice" and have the
  procedure be the same in every repo.
- **The coordinator agent:** the Claude Code session the owner talks to. Owns
  PRD, PLAN, SRS, AGENTS; dispatches workers; verifies; never trusts a
  worker's word.
- **Worker agents** (Claude, Codex, Copilot, Grok via PowerSpawn): receive a
  scoped task, change product code, write memories, report with evidence.
- **A future collaborator or reader:** opens `METHODOLOGY.md` and understands
  how work is done here in one sitting.

## 3. Product principles

1. **One canonical text.** The method is written once in `METHODOLOGY.md`.
   Project files link to it; they do not restate it. AGENTS.md stays short and
   project-specific.
2. **Decisions baked into templates.** Every drift point in §1 is settled by a
   recorded decision (`docs/decisions/`) and pre-filled in `templates/`.
   Stamping a project is a copy, not a design session.
3. **Skills execute movements, not opinions.** Each `powerflow-*` skill covers
   one movement of the loop with a definite procedure, its inputs, its gate and
   its report. Project-specific commands come from the project's AGENTS.md;
   the ritual comes from the skill.
4. **PLAN.md first and last.** Every working session opens on the current
   iteration (`show_miniplan`) and closes by updating its status through
   powerplan. The plan is the durable session state; the conversation is not.
5. **PRD once.** A PRD is written when a project starts and rewritten only on a
   major change of direction. Routine change goes to decisions, SRS and PLAN.
6. **Evidence or it didn't happen.** Inherited from powerplan: a task is ticked
   with proof, owner reports are closed by the owner, a red CI is the gate.
7. **Deterministic where possible.** What a script can check (duplicate IDs,
   plan structure, version derivation) is checked by a script in CI, not by an
   instruction an agent may forget.
8. **Harness-agnostic core.** The handbook, templates and guards work for
   Codex, Copilot and Cursor. Skills are the Claude Code delivery of the same
   procedures.

## 4. What PowerFlow contains

| Part | Path | Role |
|---|---|---|
| Handbook | `METHODOLOGY.md` | The method as prose: loop, documents, sessions, movements, agents, verification, owner reports, release, determinism, conventions |
| Decisions | `docs/decisions/D1…` | One ADR per settled drift point (§9) |
| Templates | `templates/` | PRD, PLAN header, AGENTS, CLAUDE shim, README, SRS index + file, decisions index + file, agents README, `.mcp.json`, `.claude/*.json`, CI guards workflow, guard scripts |
| Skills | `skills/powerflow-*/SKILL.md` | Thirteen procedures, one per movement (§5) |
| Plugin | `.claude-plugin/` | `plugin.json` + `marketplace.json` so one user-level install serves every project |
| Guards | `templates/scripts/` | `check-req-ids`, `plan-normalize`, `check-version` — vendored into projects or run via npx |
| Dogfood | `PRD.md`, `PLAN.md`, `AGENTS.md`, `docs/agents/` | PowerFlow is operated with PowerFlow |

## 5. Skill surface

| Skill | Movement | Procedure in one line |
|---|---|---|
| `powerflow-init` | start a project | Interview → stamp templates → `create_plan` → v0.1.0 standard tasks → smoke → first commit |
| `powerflow-prd` | once per project / major redirection | Draft or rewrite PRD.md against the template sections, one question round at a time; refuses routine edits |
| `powerflow-decide` | record a decision | `docs/decisions/D<n>-slug.md` (Status · Context · Decision · Consequences with the reopening gate), linked from README and PRD |
| `powerflow-srs` | specify a feature | Create/extend `docs/srs/SRS-<feature>.md`, allocate IDs from the index, one shall per row, duplicate check, matching PLAN task |
| `powerflow-plan` | operate the plan | Iteration lifecycle through powerplan; PLAN first and last; one active; smoke task last; owner-tick rule; `check_plan` before reporting |
| `powerflow-slice` | start a slice | Plan-mode brief → approved → SRS rows + PLAN tasks with allowed paths and definition of done, before the first edit |
| `powerflow-verify` | close the loop | Typecheck + unit, e2e once on the real binary, smoke launch, evidence lines; no rerun loops; screenshots opt-in; showcase per D8 |
| `powerflow-bug` | owner report | Failing test quoting the owner's sentence on the reported platform → fix → task text "fixed <sha>, awaiting owner verification", box left open |
| `powerflow-release` | ship | Preflight (iteration closed, gates green, look at it) → single version source bump → derivation check → canonical build → smoke the artifact → tag → CI → notes from PLAN → storefront → tick |
| `powerflow-memory` | learn | `docs/agents/memories/<topic>.md` one fact per heading, dated, corrected in place; `context/<feature>.md` deleted once absorbed |
| `powerflow-coordinate` | orchestrate | Loop over the active iteration via PowerSpawn: rehydrate from PLAN.md, dispatch with the full contract, verify the gate yourself, tick with evidence, stop cleanly on stall |
| `powerflow-status` | review | ASCII gantt cross-checked against git; optional visual board (adopted from powerplanner) |
| `powerflow-audit` | conform | Drift report against this pack, emitted as PLAN tasks |

## 6. powerplan additions this product depends on

- **`show_miniplan(version?, before?, after?, plan_path?)`** — returns the
  current (or named) iteration as **raw PLAN.md text**: its major header, the
  neighbouring iterations collapsed to their header lines, the iteration
  itself byte-for-byte. The plan's own format is the agent view — no JSON, no
  ASCII rendering — so the coordinator can start and end every session on the
  plan without reading the whole file. Specified and tracked in
  `powerplan/PLAN.md` v0.8.0.

## 7. Distribution

- **Skills:** a personal Claude Code plugin (`powerflow`) installed once at user
  level. Skills are namespaced `powerflow-*` so their origin is visible in any
  project's slash menu.
- **Templates and guards:** copied into each project by `powerflow-init`
  (they must live in the repo for Codex, Copilot and CI to see them).
- **Handbook:** linked from every stamped AGENTS.md; also readable on GitHub.
- Publishing to a public marketplace is out of scope until two reference
  projects have run on the pack.

## 8. Non-goals (v0.x)

- Not a task tracker, not a replacement for powerplan or PowerSpawn — PowerFlow
  orchestrates them.
- No web UI; Markdown and skills only.
- No enforcement beyond CI guards and process rules; the MCP cannot block a
  raw edit (powerplan PRD §7).
- No per-harness forks of the handbook; one text.
- Not a training deck; the deck (`training-ai-software-engineering-101`)
  teaches the method, PowerFlow executes it.

## 9. Decisions to record (docs/decisions/)

| # | Decision | Resolution |
|---|---|---|
| D1 | Requirement ID scheme | `SRS-<FEAT>-NNN`; prefixes owned by one file each, allocated in `docs/srs/README.md`, CI-checked |
| D2 | PLAN.md header | Goal · Philosophy · (Verify) · Stack, then the stale-proof "Current Status" paragraph; no achievement lists |
| D3 | Coordinator guidance location | In `powerflow-coordinate`, loaded on demand; CLAUDE.md stays a shim |
| D4 | powerplan registration | `uvx powerplan-mcp` in the template; `python -m powerplan` where uv is absent; submodule only when developing powerplan |
| D5 | Skill naming | `powerflow-*` |
| D6 | Distribution | Personal plugin for skills; templates copied per project |
| D7 | Migrated skills | Replaced in their source repos by one-line pointer files |
| D8 | Showcase artifact | PRD quality-bar switch `showcase: required \| optional`, read by `powerflow-verify` |
| D9 | autosar-101-training | Open — repo not on this machine |
| D10 | PRD cadence | Once per project, or on a major change of direction; never for routine change |
| D11 | Session bookends | PLAN.md first (`show_miniplan`) and last (status update via powerplan) in every working session |

## 10. Success criteria

- Two real projects (one new via `powerflow-init`, one retrofitted via
  `powerflow-audit`) run one full iteration each through the pack with zero
  hand-edits of PLAN.md and zero re-explanation of procedure in chat.
- `powerflow-audit` reproduces the drift table from the 2026-09-18 proposal on
  the current repos, then reports zero drift on the two reference projects.
- A new agent session in a stamped project reaches "what to do now" from
  `show_miniplan` alone.
- The handbook is under five pages and every skill cites the section it
  executes.
