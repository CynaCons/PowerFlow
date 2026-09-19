# D14 — The plugin bundles the powerplan MCP registration

Status: Accepted · 2026-09-19

## Context

Installing PowerFlow as a Claude Code plugin (D6) revealed that the plugin
loader treats the repository's root `.mcp.json` as a plugin component:
`claude plugin details powerflow@powerflow` lists `MCP servers (1) powerplan`,
and `plugin.json` offers no opt-out (`"mcpServers": {}` has no effect). D4
says each project registers powerplan in its own `.mcp.json`; with the plugin
installed, a stamped project on the author's machine would load powerplan
twice (project copy + plugin copy) — two stdio processes, two tool namespaces,
~24 duplicated schemas per session. The alternative — removing PowerFlow's
own `.mcp.json` — would break PowerFlow's own sessions and give up a real
gain: every session on the machine, in any repo, gets `show_miniplan`
(powertimelines has no powerplan registration at all today).

## Decision

The plugin **bundles** the powerplan registration on purpose: PowerFlow's root
`.mcp.json` (`python -m powerplan`, the author's editable install) is the
plugin's MCP server, so Claude Code has the single writer in every session.
Stamped projects **keep** their own `.mcp.json` (D4) so clones without the
plugin — and other harnesses — still register it. To avoid the duplicate,
`powerflow-init`'s stamp detects an installed `powerflow` plugin and writes
`.claude/settings.local.json` with `"disabledMcpjsonServers": ["powerplan"]`
instead of enabling it; that file is git-ignored, so the choice is per clone
and never reaches a machine without the plugin. The bundled command stays
`python -m powerplan` (requires `pip install powerplan-mcp`) until uv is
standard on the author's machines (D4 gate).

## Consequences

- `templates/.claude/settings.local.plugin.json` exists beside the enabling
  variant; `stamp.py` picks by `claude plugin list` / `installed_plugins.json`.
- PowerFlow's `.mcp.json` is now a public surface of the plugin: changing its
  command changes every session's powerplan; note it in `AGENTS.md`.
- Reopen if Claude Code gains a manifest-level opt-out for root `.mcp.json`,
  or if a public marketplace release (D6) needs `uvx powerplan-mcp` as the
  bundled command — then PowerFlow's own dev registration moves to user scope.
