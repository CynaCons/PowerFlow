# Agent Instructions — PowerFlow

This repo *is* the method: one skill (`skills/powerflow/SKILL.md`), the
templates it stamps, opt-in guards. Codex/Copilot/Cursor load this file; Claude
loads `CLAUDE.md`, which points here. Read `PRD.md` before inventing scope.

## Commands

```bash
python -m powerplan                             # the MCP server; .mcp.json here is also the plugin's (D14)
python scripts/check.py                         # verify: check_plan · versions agree · guard tests
npm test                                        # the 18 guard tests alone
node extras/guards/check-plan.mjs PLAN.md       # the Node mirror on our own plan (D13 gate)
claude plugin validate .                        # manifests + the one skill
claude plugin marketplace update powerflow && claude plugin uninstall powerflow@powerflow && claude plugin install powerflow@powerflow   # refresh the installed copy after skill edits
```

## The plan

`PLAN.md` is written only through powerplan. `show_miniplan` first; register
work before doing it; tick with evidence; show the miniplan at the end of every
major turn; `check_plan` before reporting.

## Rules for this repo

- One canonical text: the method lives in `skills/powerflow/SKILL.md`. Do not
  paraphrase it into README, templates or PRD — link it. Keep it under ~300
  lines; if it grows, split by procedure (something with a script), not by rule.
- The PowerSpawn section of the skill is updated in the same change as a
  PowerSpawn release.
- Templates carry the decisions already; a placeholder is `{{like_this}}` and
  is listed at the top of the file. `stamp.py` refuses to leave one behind.
- Versions: `.claude-plugin/plugin.json` is the source; `package.json` and the
  CHANGELOG top section match.
- Decisions go to `DECISIONS.md` (append; never renumber). Memories to
  `docs/agents/memories/`.
- Bash heredocs here mangle backslashes and backticks — write files with the
  editor tools, commit messages with `-F`.

## Reporting

What changed · how verified (command → result) · what is open · memories. Then
the miniplan.
