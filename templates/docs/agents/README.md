<!-- placeholders: project -->
# Agent memories and context

Agents on {{project}} improve across sessions by writing Markdown here.
`AGENTS.md` is the standing briefing; this folder is the durable scratchpad.

```
docs/agents/
  README.md        this file
  memories/        durable facts: landmines, mappings, measurements, decisions easy to violate
  context/         per-feature working context for a worker; deleted once absorbed
```

## When to write a memory

Write or update `memories/<topic>.md` when you discover something the next
agent would otherwise have to rediscover: a platform-only API in a file we
thought was portable, where a reference implementation hides a behaviour, an
encoding or credential quirk, a measurement that must match, a decision in
PRD/SRS that is easy to violate in code.

Do **not** write: task status (that is PLAN.md), secrets, or a copy of the SRS.

## Format

```md
# Topic

## <one fact>
Short paragraph or bullets. Path references as `path/file.ext`.
Date the first write if the fact might rot (`2026-01-31`).
```

One heading per fact. Correct wrong facts in place — a stale memory is worse
than none.

## When to write context

`context/<feature>.md` is a briefing for a worker about to touch that feature.
Keep it current; delete it when it is fully absorbed into code comments and
the SRS.

## Coordinator vs worker

Workers may create and edit files here. They still must not edit PLAN.md,
PRD.md or SRS files unless the task says so.
