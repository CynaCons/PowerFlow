# D6 — Distribution

Status: Accepted · 2026-09-18

## Context

Skills can be copied into each project's `.claude/skills/` (powerplanner and
PowerGit do this), placed at user level, or packaged as a Claude Code plugin.
The author already runs six plugins from `~/.claude/settings.json`. Templates
and guards must live inside each project for Codex, Copilot and CI to see
them; skills are Claude-specific.

## Decision

Skills ship as a personal Claude Code plugin (`.claude-plugin/plugin.json` +
`marketplace.json`) installed once at user level. Templates and guard scripts
are copied into each project by `powerflow-init`. The handbook is linked, not
copied. Public marketplace publication waits for two reference projects.

## Consequences

- One install, every project; a skill fix reaches all sessions on the next
  plugin update.
- `powerflow-audit` can later report which pack version a project was stamped
  with (backlog).
- Reopen if a team member without Claude Code needs the procedures — then the
  skills' procedure sections are mirrored into a handbook appendix.
