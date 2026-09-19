# Agent Instructions

Shared briefing for every coding agent on PowerFlow. Codex, Copilot and
Cursor load `AGENTS.md`; Claude loads `CLAUDE.md`, which points here. The
method itself is [METHODOLOGY.md](METHODOLOGY.md) — this file only says how it
applies to this repo.

You are working on **PowerFlow**: the methodology pack — a handbook, a
template set and the `powerflow-*` Claude Code skills. There is no
application to run; the product is Markdown, a plugin manifest and a few
guard scripts. Read [PRD.md](PRD.md) before inventing scope.

## Project shape

```
METHODOLOGY.md        the handbook — canonical prose, every skill cites a section
PRD.md · PLAN.md      product requirements · operational plan (powerplan is the only writer)
docs/decisions/       D1–D11, one ADR per settled convention
docs/agents/          memories and context (living)
docs/proposal-*.html  the archived analysis this repo started from
templates/            files powerflow-init stamps into a project
skills/powerflow-*/   SKILL.md per movement of the loop
scripts/              plan_bootstrap.py (provenance only) · check.py (verify) · check-req-ids.mjs
tests/guards/         node --test cases for the three vendored guards
.claude-plugin/       plugin.json (the version source) + marketplace.json
docs/audits/          audit fix lists for other repos (input to their retrofits)
```

## Commands

```bash
python -m powerplan                 # the MCP server (stdio); registered in .mcp.json (also the plugin's, D14)
python scripts/check.py             # verify: check_plan, decisions, req-ids, skills, versions, guard tests
npm test                            # the 17 guard tests alone (node --test)
node templates/scripts/check-plan.mjs PLAN.md   # the Node mirror against our own plan (D13 gate)
claude plugin validate .            # manifests + skills
```

## How we verify

Proof for this repo is structural: `python scripts/check.py` exits 0, every
decision file is linked from `docs/decisions/README.md`, every skill named in
PRD.md §5 has a directory under `skills/`, and a stamped throwaway repo passes
its own guards (`powerflow-init` smoke). A skill is verified by running it in
a real project and pasting the resulting PLAN.md / SRS diff in the report.

## Bookends

Open every session with `show_miniplan`. Close it with the status update
through powerplan and `check_plan`. End every major turn (files changed, tasks
ticked or added, a gate run, an iteration closed) by showing the miniplan
verbatim in a fenced block (D12). See METHODOLOGY.md §3.

## Who owns which files

| File | Owner |
|---|---|
| `PLAN.md` | Coordinator via powerplan — never hand-edited |
| `PRD.md`, `METHODOLOGY.md`, `docs/decisions/*` | Coordinator, or a task that says so |
| `skills/*`, `templates/*` | Workers, scoped to the task |
| `docs/agents/*` | Anyone; one fact per heading |

Workers must not edit the plan, the PRD, the handbook or decisions unless the
task says so, and never commit or push.

## Engineering rules

- `.mcp.json` at this root is a **plugin surface** (D14): the installed
  `powerflow` plugin serves it as powerplan's registration in every Claude Code
  session on the machine. Change its command only with a decision.

- One canonical text: if a rule is in METHODOLOGY.md, link it — do not
  paraphrase it into a skill or template.
- Skills are procedures: steps, gate, report. Project-specific commands are
  read from the project's AGENTS.md at run time; never hard-code a project.
- Templates carry the decisions (D1–D11) already applied; a placeholder is
  `{{like_this}}` and every placeholder is listed at the top of the file.
- ASCII in PLAN.md task text (powerplan round-trip); Markdown elsewhere.
- Keep diffs small; do not reformat files you are not changing.
- Evidence or it didn't happen: the report shows the command and its output.

## Reporting

What changed (paths), how it was verified (commands, exit codes), what is
still open, which memories were added or corrected.
