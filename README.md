# PowerFlow

**One skill for the way I build software with agents.** PRD once · PLAN.md
through [powerplan](https://github.com/CynaCons/powerplan) · SRS rows before
code · close the loop before "done" · bugs failing-test-first · workers through
[PowerSpawn](https://github.com/CynaCons/PowerSpawn).

Site: **https://cynacons.github.io/PowerFlow/** · The method:
[skills/powerflow/SKILL.md](skills/powerflow/SKILL.md) · Decisions:
[DECISIONS.md](DECISIONS.md) · Plan: [PLAN.md](PLAN.md)

## The ten rules

1. **PRD once.** Iterate it with the agent at the start; rewrite only on a
   declared change of direction.
2. **PLAN.md is the backbone**, written only by powerplan: iterations,
   checkboxes, smoke task last, a header that cannot go stale.
3. **Miniplan first, last, and at the end of every major turn** — the console
   shows the state when you come back.
4. **Register work before doing it**; tick only with evidence.
5. **SRS rows before code**: `SRS-<FEAT>-NNN`, one shall per row, never reused.
6. **Close the loop before "done"**: tests once, the app launches clean, look
   at the UI you changed.
7. **Owner reports**: quote the owner, failing test first, the owner ticks.
8. **Short AGENTS.md, CLAUDE.md a shim, memories** when you hit a landmine.
9. **Workers get the whole brief** (goal + gate, context, allowed paths, done
   when, report shape); the coordinator verifies, commits, then ticks.
10. **Release is a checklist**, never from an open iteration; check CI before
    dispatching it.

## Install

```bash
claude plugin marketplace add CynaCons/PowerFlow
claude plugin install powerflow@powerflow      # user scope: every project, every session
pip install powerplan-mcp                      # the plugin registers powerplan as `python -m powerplan`
```

Restart Claude Code. In a new directory: *"start a new project"*. In an
existing repo: *"audit this repo against PowerFlow"*. Any time: *"where are
we"*, *"start the next slice"*, *"verify"*, *"bug: …"*, *"spawn workers for
this"*, *"release"*.

## What's in the repo

```
skills/powerflow/    SKILL.md · scripts/stamp.py · scripts/audit.py · references/{workers,release,smoke}.md
templates/           PRD · AGENTS · CLAUDE shim · docs/srs/README · .mcp.json · .claude/settings · .gitignore
extras/guards/       opt-in CI guards (plan, requirement IDs, version) + tests
DECISIONS.md         D1–D15, why things are the way they are
```

## License

MIT.
