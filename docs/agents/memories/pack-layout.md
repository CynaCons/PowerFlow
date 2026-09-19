# Pack layout

## Since 0.3.0 (D15) there is one skill: skills/powerflow/
`SKILL.md` is the canonical method; `scripts/stamp.py`, `scripts/audit.py`,
`references/{workers,release,smoke}.md`. `PACK_ROOT = parents[3]` from the
scripts still resolves to the repo root. Guards live in `extras/guards/` (opt-in)
with their tests; `npm test` runs them. 2026-09-19.

## Skills find templates through the pack root, not a copy
`skills/<name>/scripts/*.py` resolve `PACK_ROOT = Path(__file__).resolve().parents[3]`
and read `PACK_ROOT/templates/`. This works in the repo and in an installed
plugin only because the plugin root *is* the repo root (`.claude-plugin/` at
the top). Do not move `skills/` or `templates/` deeper without updating
`parents[n]` in every script. 2026-09-19.

## PLAN.md preamble: create_plan already ends with a rule
`create_plan` writes Goal, Philosophy and `---`. Anything appended before the
first major must start at `## Current Status`; putting Verify/Stack lines
before it produces a double rule. Verify and Stack live inside the Current
Status paragraph (see `skills/powerflow-init/references/first-iteration.md`).

## Placeholders may contain digits
`{{e2e_command}}` — the placeholder regex is `[a-z0-9_]+`; a `[a-z_]+`
version silently left it in AGENTS.md and the leftover check (same regex)
could not see it. Keep the two using one compiled pattern.

## The plugin bundles root .mcp.json; the stamp protects stateful files
`claude plugin details` lists `MCP servers (1) powerplan` because the loader
scans the plugin root's `.mcp.json`; `"mcpServers": {}` in plugin.json does not
opt out (tested 2026-09-19). Decision D14 keeps it. `stamp.py --force` keeps
PRD/AGENTS/README and the SRS/decisions indexes (`STATEFUL`) — a re-stamp once
wiped a live allocator table; `--force-all` is the explicit override.

## Guards take --root; PowerFlow's own CI runs the Node mirror on its plan
`check-req-ids.mjs --root <dir>` / `check-version.mjs --root <dir>` (2026-09-19)
let `tests/guards/guards.test.mjs` drive them against temp fixtures. CI runs
`node templates/scripts/check-plan.mjs PLAN.md` beside `check.py` so a
disagreement between the mirror and powerplan's `check_plan` shows up here first
(D13 reopen gate).

## subprocess on POSIX: a list with shell=True runs only the first element
`subprocess.run(["npm", "test"], shell=True)` ran a bare `npm` on ubuntu-latest
(CI red on the first push, 2026-09-19) while Windows joined the list. Call the
binary directly without a shell (`["node", "--test", "<glob>"]`); node expands
its own test globs on both platforms.
