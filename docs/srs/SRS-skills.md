# SRS — Skills

Feature tag: `SKILL`. Traces up to [PRD.md](../../PRD.md) §5.
Rows are allocated in [README.md](README.md); IDs are never reused.

The pack's features are its skills: each row is one `powerflow-*` procedure,
what it shall do, and how that is verified. Verification is structural where
a script can check it (`scripts/check.py`: frontmatter, size, presence) and
`Demo` where only running the skill in a real project proves it — the Trace
column then names the run that did.

## 0. Requirements

| ID | Requirement | Rationale | Verification | Trace |
|---|---|---|---|---|
| SRS-SKILL-001 | `powerflow-init` shall stamp the PowerFlow templates into a target repo with every placeholder filled, register powerplan, and create PLAN.md only through powerplan calls, never by copying a file. | Single-writer rule from byte one (D2, D4); a leftover placeholder is a silent defect. | Test | `skills/powerflow-init/`; `scripts/check.py`; stamped throwaway 2026-09-19 (15 files, guards green, plan via MCP) |
| SRS-SKILL-002 | `powerflow-prd` shall write PRD.md only at project start or on an owner-declared change of direction, and shall redirect routine change to decisions, SRS rows or PLAN tasks. | PRD cadence (D10). | Demo | `skills/powerflow-prd/` (v0.1.3) |
| SRS-SKILL-003 | `powerflow-decide` shall create `docs/decisions/D<n>-slug.md` with Status, Context, Decision and Consequences naming the reopening gate, and link it from the decisions README and the PRD table. | Decisions before the subsystem (§2.2). | Test | `skills/powerflow-decide/` (v0.1.3); `scripts/check.py` decisions check |
| SRS-SKILL-004 | `powerflow-srs` shall allocate IDs only from the project's allocator table, register a tag to exactly one file, bump the allocator, and run the ID guard before reporting. | D1; the guard must never see an ID the table did not hand out. | Test | `skills/powerflow-srs/scripts/srs.py`; `scripts/check-req-ids.mjs`; this file |
| SRS-SKILL-005 | `powerflow-plan` shall open a session with `show_miniplan`, register new work before it is done, tick tasks only with named evidence, refuse to force-close, and end with `check_plan` green. | Session bookends (D11); evidence or it didn't happen. | Demo | `skills/powerflow-plan/`; this iteration's closure |
| SRS-SKILL-006 | `powerflow-slice` shall produce an approved brief (owner words verbatim, `path:line` context, SRS rows, tasks with allowed paths and definition of done) and register SRS rows and PLAN tasks before the first product edit. | Movement 1 of every iteration (§4.1). | Demo | `skills/powerflow-slice/`; `docs/agents/context/v0.1.3-discipline-skills.md` |
| SRS-SKILL-007 | `powerflow-verify` shall run the gate ladder in order (typecheck + unit, e2e once, smoke with clean console, look at changed UI, guards), emit one evidence line per rung, fill SRS Trace for rows a test verifies, and tick only tasks whose evidence line exists. | Closing the loop (§6); token budget (verify once, screenshots opt-in). | Demo | `skills/powerflow-verify/`; this iteration's verify report |
| SRS-SKILL-008 | `powerflow-bug` shall register an owner report quoting the owner verbatim, write a failing test reproducing the symptom on the reported platform before any fix, and leave the task open as "fixed <sha>, awaiting owner verification". | Owner reports are symptom-first and owner-closed (§7). | Demo | `skills/powerflow-bug/` (v0.1.3) |
| SRS-SKILL-009 | `powerflow-release` shall refuse to ship from an open iteration, bump the single version source and check derivation, build with the canonical command, smoke the packaged artifact, tag, confirm CI is running before dispatching it, and derive release notes from closed iterations. | Release ritual (§8); the duplicate-dispatch lesson of powerplan 0.8.0. | Demo | `skills/powerflow-release/` (v0.1.3) |
| SRS-SKILL-010 | `powerflow-memory` shall write `docs/agents/memories/<topic>.md` with one fact per heading, dated when it may rot, and shall refuse task status, secrets and SRS copies. | Recursive improvement (§5.2). | Demo | `skills/powerflow-memory/` (v0.1.3) |
| SRS-SKILL-011 | `powerflow-coordinate` shall rehydrate from PLAN.md each cycle, dispatch workers with the full contract (goal + gate, context, allowed paths, definition of done, report format), validate the gate itself, and stop cleanly on stall instead of spinning. | Coordinator/worker split (§5); PLAN.md as the only durable state (D3). | Demo | `skills/powerflow-coordinate/` (v0.1.4) |
| SRS-SKILL-012 | `powerflow-status` shall render the current major as an ordinal ASCII gantt read through powerplan tools, cross-checked against `git log`, with exactly one `◀ NEXT`, and shall correct stale ticks through powerplan before drawing. | Adopted from powerplanner (D7); never draw done what the commits do not support. | Demo | `skills/powerflow-status/`; this iteration's status render |
| SRS-SKILL-013 | `powerflow-audit` shall report a repo's drift from the pack (missing artifacts, header style, SRS scheme, shim, memories, guards, unverified rows, absolute MCP paths) as PLAN tasks, reading `.powerflow/init.json` when present. | Success criterion PRD §10; the ten drift points of the proposal. | Demo | `skills/powerflow-audit/` (v0.1.4) |

## 1. Pack-wide

| ID | Requirement | Rationale | Verification | Trace |
|---|---|---|---|---|

<!-- Cross-cutting rows (frontmatter contract, size limit, script console
safety) are allocated when the plugin packaging lands in v0.2.0. -->

## Notes

`scripts/check.py` enforces the structural contract for every skill named in
PRD §5: a `SKILL.md` exists or an open PLAN task names it; the frontmatter
`name` equals the directory; the description is long enough to trigger on;
the body stays under 500 lines. Behavioural rows (`Demo`) are verified by
running the skill in a real project and citing the run in Trace.
