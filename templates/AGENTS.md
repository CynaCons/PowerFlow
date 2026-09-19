<!-- placeholders: project, one_liner, stack, dev_command, smoke_command, test_command, typecheck_command, e2e_command -->
# Agent Instructions — {{project}}

{{one_liner}} Stack: {{stack}}.

Shared briefing for every coding agent (Codex, Copilot and Cursor load this
file; Claude loads `CLAUDE.md`, which points here). The method is PowerFlow:
[skills/powerflow/SKILL.md](https://github.com/CynaCons/PowerFlow/blob/main/skills/powerflow/SKILL.md).
Read [PRD.md](PRD.md) before inventing product behaviour.

## Commands

```bash
{{dev_command}}          # dev
{{typecheck_command}}    # typecheck
{{test_command}}         # unit tests
{{e2e_command}}          # e2e — run once, read the first error, fix, run once
{{smoke_command}}        # smoke: launches with zero console errors — before any "done"
```

## The plan

`PLAN.md` is written only through the **powerplan** tools. Open every session
with `show_miniplan`; register new work before doing it; tick only with
evidence; end every major turn by showing the miniplan. Requirements are rows
in `docs/srs/SRS-<feature>.md` (`SRS-<FEAT>-NNN`, never reused), written before
the code that satisfies them.

## Who owns what

Coordinator: `PLAN.md` (via powerplan), `PRD.md`, `docs/srs/`, this file,
commits. Workers: product code within the task's allowed paths, and memories
in `docs/agents/memories/`. Workers never edit the plan, PRD or SRS, and never
commit or push.

## Rules

- Owner reports are symptom-first: a failing test quoting the owner, on the
  reported platform, before the fix; the owner ticks the task.
- Keep diffs small; do not reformat what you are not changing.
- Write a memory (`docs/agents/memories/<topic>.md`, one dated fact per
  heading) when you hit something the next agent would rediscover.
<!-- project-specific rules go here: layering, forbidden deps, theme tokens, licence -->

## Reporting

What changed (paths) · how it was verified (commands, exit codes, counts) ·
what is open · memories written. Then the miniplan.
