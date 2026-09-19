# Templates

Files `powerflow-init` stamps into a new project. Every decision in
[docs/decisions/](../docs/decisions/README.md) is already applied; a project
never re-decides them. Placeholders are `{{name}}`; the stamping script
(`skills/powerflow-init/scripts/stamp.py`) fills them from the interview
answers and refuses to leave any behind.

| Template | Lands at | Placeholders |
|---|---|---|
| `PRD.md` | `PRD.md` | project, one_liner, github, date, stack, platform, showcase, version_source |
| `PLAN.md` | *(reference only — the plan is created through powerplan, never copied)* | — |
| `AGENTS.md` | `AGENTS.md` | project, one_liner, stack, dev_command, smoke_command, test_command, typecheck_command, e2e_command, verify_command |
| `CLAUDE.md` | `CLAUDE.md` | project |
| `README.md` | `README.md` | project, one_liner, dev_command, test_command, license |
| `.gitignore` | `.gitignore` | — |
| `docs/srs/README.md` | same | project |
| `docs/srs/SRS-template.md` | *(copied by `powerflow-srs` per feature, not at init)* | feature, FEAT, prd_section |
| `docs/decisions/README.md` | same | project |
| `docs/decisions/D-template.md` | *(copied by `powerflow-decide` per decision)* | n, slug, title, date |
| `docs/agents/README.md` | same | project |
| `.mcp.json` | `.mcp.json` when `uvx` resolves | — |
| `.mcp.python.json` | `.mcp.json` when it does not | — |
| `.claude/settings.local.json` | same (git-ignored) | — |
| `.claude/launch.json` | same | dev_command_exe, dev_command_args, dev_port |
| `.github/workflows/ci.yml` | same | typecheck_command, test_command, stack |
| `scripts/check-req-ids.mjs` | same | — |
| `scripts/check-plan.mjs` | same | — |
| `scripts/check-version.mjs` | same | version_source |

Placeholder values come from `skills/powerflow-init/SKILL.md` § Interview. A
template that gains a placeholder must add it to this table and to the
interview.
