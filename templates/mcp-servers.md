# MCP servers a stamped project registers

`.mcp.json` carries **powerplan** (PowerFlow D4): `uvx powerplan-mcp` by
default, `python -m powerplan` (`.mcp.python.json`) where uv is absent.
`powerflow-init` picks whichever resolves on the machine. `.claude/settings.local.json`
enables it; it is git-ignored, so each clone opts in once.

## PowerSpawn (add when the project uses workers)

Add the block to `mcpServers` and `"powerspawn"` to `enabledMcpjsonServers`.
Requires a PowerSpawn checkout importable as `powerspawn` (submodule or
`PYTHONPATH`):

```json
"powerspawn": {
  "command": "python",
  "args": ["-m", "powerspawn.mcp_server"],
  "env": { "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1" }
}
```

Never register a server by absolute path (`C:/dev/...`): it breaks on every
other machine and is a `powerflow-audit` finding.
