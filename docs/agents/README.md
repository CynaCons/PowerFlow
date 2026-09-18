# Agent memories and context

Agents on PowerFlow improve across sessions by writing Markdown here.
`AGENTS.md` is the standing briefing; this folder is the durable scratchpad.
The rules are METHODOLOGY.md §5.2; this file is the local copy of the layout.

```
docs/agents/
  README.md        this file
  memories/        durable facts: landmines, mappings, measurements, decisions easy to violate
  context/         per-feature working context for a worker; deleted once absorbed
```

Write `memories/<topic>.md` when the next agent would otherwise rediscover
something: a powerplan round-trip quirk, a plugin manifest field that the
harness ignores, a template placeholder that collides with a project's own
syntax. One heading per fact, dated when it might rot, corrected in place.

Do **not** write task status (PLAN.md), secrets, or copies of the handbook.
