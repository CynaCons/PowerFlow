# D4 — powerplan registration

Status: Accepted · 2026-09-18

## Context

Four registrations exist for the same server: `uvx powerplan-mcp` (published
path), `python -m powerplan` (pip-installed, RadEAU), the PowerSpawn
submodule path `powerspawn/powerplan/powerplan_server.py` (PowerGit,
powerplanner) and an absolute `C:/dev/...` path (ARXMLExplorer). The absolute
path breaks on any other machine; the submodule path couples every project to
a PowerSpawn checkout; uv is not installed on the author's Windows box today.

## Decision

`templates/.mcp.json` carries the `uvx powerplan-mcp` entry as the default
and a `python -m powerplan` variant for machines without uv. `powerflow-init`
picks the one that resolves on the machine it runs on. The submodule path is
used only in repos that develop powerplan or PowerSpawn themselves. Absolute
paths are a finding in `powerflow-audit`.

## Consequences

- A stamped project runs on any machine with uv or a pip install; no path
  edits on clone.
- PowerFlow itself uses `python -m powerplan` (no uv on this machine); the
  template still leads with uvx.
- Reopen when uv becomes standard on the author's machines — then drop the
  variant.
