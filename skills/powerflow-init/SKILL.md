---
name: powerflow-init
description: Bootstrap a project with the PowerFlow methodology — PRD, PLAN.md through powerplan, requirement index, decision records, agent briefing (AGENTS.md + CLAUDE.md shim), MCP registration and CI guards, stamped from templates with the conventions already decided. Use this whenever the user starts a new project or repository, says "new project", "init", "bootstrap", "scaffold", "set up the methodology / PowerFlow here", or points at an empty or young directory and asks how to begin — even when they do not name PowerFlow. Also use it to retrofit the backbone onto a repo that has code but no PRD/PLAN/SRS.
---

# powerflow-init — start a project the PowerFlow way

You are setting up the backbone a project runs on for its whole life: the
documents, the plan, the guards. Everything that can be copied is copied by a
script; your job is the interview, the plan, the PRD conversation and the
proof. The method is `METHODOLOGY.md` in the PowerFlow repo; this skill
executes its §2 (documents) and §3 (session bookends) for a fresh repo.

Layout of this skill: `scripts/stamp.py` (deterministic copy + placeholder
fill), `references/first-iteration.md` (the exact powerplan calls for the
first plan). Templates live at `../../templates/` relative to this file.

## 0. Look before asking

Read the target directory first. Most answers are already there:

| Signal | Infer |
|---|---|
| `package.json` scripts | `dev_command`, `test_command`, `typecheck_command` (`tsc -b`), `version_source = package.json`, dev port from vite config |
| `src-tauri/` | `platform = desktop`, `smoke_command = npm run tauri dev` |
| `pyproject.toml` / `Cargo.toml` / `*.csproj` | version source and test runner |
| `.mcp.json` already present | keep it; only add the powerplan entry |
| `PLAN.md` already present | stop — this is a retrofit: run `powerflow-audit` instead of overwriting anything |

Propose the inferred values in one message; ask only for what is missing.

## 1. Interview (one round)

Collect these; write them as JSON (the stamp script reads it):

| Key | Ask as | Notes |
|---|---|---|
| `project` | "Name?" | as written in headings |
| `one_liner` | "In one sentence, what is it and for whom?" | becomes the PRD one-liner and the plan goal |
| `stack` | "Stack, one line" | e.g. `Tauri 2 (Rust core) + React + TypeScript + Vite` |
| `platform` | web · desktop · cli · library · mcp · embedded | embedded → D9 note: verify guidance is partial |
| `dev_command`, `smoke_command`, `test_command`, `typecheck_command`, `e2e_command` | the canonical commands | if one does not exist yet, use an honest `echo "no e2e yet"` — never invent a script name |
| `verify_command` | the one-line proof | usually `typecheck && unit && node scripts/check-plan.mjs` |
| `version_source` | the single file that carries the version | `package.json`, `pyproject.toml`, `Cargo.toml` |
| `showcase` | "Visual product? Should every iteration publish a screenshot artifact?" | `required` \| `optional` (D8) |
| `github`, `license`, `author`, `dev_port` | optional | `dev_port` enables `.claude/launch.json` |

Save to `<target>/.powerflow/init.json` (the stamp rewrites it with
provenance: pack version, date, files written — `powerflow-audit` reads it).

## 2. Stamp

```bash
python <this skill>/scripts/stamp.py --target <repo> --answers <repo>/.powerflow/init.json
```

It copies PRD, AGENTS, CLAUDE shim, README, .gitignore, the SRS/decisions/agents
READMEs, `.claude/settings.local.json` (+ `launch.json` when a port was
given), the CI workflow and the three guard scripts, fills every placeholder,
and picks `.mcp.json` for `uvx powerplan-mcp` or `python -m powerplan`
depending on what resolves (D4). When the `powerflow` plugin is installed on
this machine it writes `settings.local.json` with the project's powerplan
**disabled** — the plugin already provides it, and two copies would load
(D14); `--plugin yes|no` overrides the detection. It keeps existing files
(`--force` to overwrite) and never writes PLAN.md. If it exits non-zero, read the message:
it names the missing answer or the leftover placeholder.

## 3. Register the MCP, then make sure it is live

`.mcp.json` and `.claude/settings.local.json` are in place after the stamp,
but MCP servers load at session start. If `powerplan` tools are not in this
session, tell the owner to restart the session before step 4 — or, when the
`powerplan` Python package is importable, drive the same functions through
`python -c "from powerplan import mutations as m; ..."`. Do not hand-write
PLAN.md to save a restart; the single-writer rule starts at byte one.

## 4. Create the plan through powerplan

Follow `references/first-iteration.md` call by call: `create_plan` (no seed
major), `append_prose` with the stale-proof header, `create_major v0.1`,
`create_iteration v0.1.0`, `add_tasks` with the six standard tasks,
`start_iteration`, then `check_plan` → `ok: true`. The wording is fixed so
every project's first iteration reads the same and `powerflow-verify` can
recognise the smoke task.

## 5. The PRD conversation — the one time it is written

The stamped `PRD.md` is a skeleton with HTML comments where the content goes.
Walk it with the owner now, section by section, one question round: problem,
users, principles, product shape (in / out of v1), stack table, quality bar,
non-goals, decisions to record, success criteria. Write what they say; do not
pad. This is the only skill that writes PRD.md routinely (D10) — later change
goes to decisions, SRS rows and PLAN tasks. When the PRD names decisions, tick
the first PLAN task and record each decision as `docs/decisions/D<n>-slug.md`
from `templates/docs/decisions/D-template.md` (or hand off to
`powerflow-decide`).

## 6. Prove it

Run, and paste the output in the report:

```bash
node scripts/check-plan.mjs && node scripts/check-req-ids.mjs && node scripts/check-version.mjs
```

`check-version` fails until `version_source` exists with an `X.Y.Z` — fine on
an empty directory; say so rather than faking a package file. Then `check_plan`
through powerplan. If the application already exists, run `smoke_command` and
confirm it launches with no console error; if not, the smoke task stays open
for the scaffold step.

## 7. First commit, and the bookend

`git init` if needed; commit `chore: PowerFlow scaffold` with everything
stamped plus PLAN.md and PRD.md. Ask before pushing anywhere. Then the closing
bookend (D11): tick what has evidence (`complete_task` with your agent id),
leave the rest open, `check_plan`, and report.

## Report

```
Stamped <n> files into <repo> (mcp: uvx|python) — list
PLAN.md created through powerplan: v0.1.0 active, <k>/6 tasks ticked
PRD.md: sections filled / still skeleton
Guards: check-plan OK · check-req-ids OK · check-version <OK|pending version source>
Smoke: <command> → <result | pending scaffold>
Next: <the first open task>, or "restart the session so powerplan tools load"
```

Then the miniplan of the new plan, verbatim (D12).

## What not to do

- Do not copy `templates/PLAN.md` — it is a rendering of what powerplan
  produces, kept for reading, not stamping.
- Do not register powerplan by absolute path; do not add PowerSpawn unless the
  project will use workers (`templates/mcp-servers.md` has the block).
- Do not fill PRD sections the owner did not answer; a skeleton with comments
  is more honest than invented users.
- Do not run the guards through a pipe when reporting exit codes.
