---
name: powerflow-memory
description: Write, correct or retire the durable agent memories of a project — docs/agents/memories/<topic>.md with one dated fact per heading (landmines, mappings, measurements, decisions easy to violate) and docs/agents/context/<feature>.md briefings that are deleted once absorbed — so the next agent does not rediscover what this one just learned. Use this whenever you hit something non-obvious that cost time (a platform-only API, an encoding quirk, a build trap, a tool's surprising behaviour, a measurement that must match), whenever the user says "remember this", "note that", "that's a landmine", "write that down", or when you find an existing memory that is wrong. Also use it at the end of a slice to decide what to keep and what to delete.
---

# powerflow-memory — agents get smarter by writing markdown

Agents improve across sessions by writing files, not by hoping the context
window remembers (PowerGit `docs/agents/README.md`, 55 memories and
counting). A memory is a fact the next agent would otherwise have to
rediscover: the `net10.0-windows` trap, where a reference implementation
hides a behaviour, a Linux font quirk, the pixel height that must match.
METHODOLOGY.md §5.2 fixes the two kinds and the rules; this skill is the
judgment about what is worth writing and how to keep it true.

## 1. Memory or context — or neither

| It is… | Write to | Lifetime |
|---|---|---|
| A durable fact about the code, platform, tools or a decision easy to violate | `docs/agents/memories/<topic>.md` | until proven wrong — then corrected in place |
| A briefing for a worker about to touch one feature (files, model, findings so far) | `docs/agents/context/<feature>.md` | until the slice closes and the SRS + code carry it — then deleted |
| Task status, progress, "what's next" | PLAN.md via `powerflow-plan` | — |
| A behaviour the product must have | SRS row via `powerflow-srs` | — |
| A choice between alternatives | `powerflow-decide` | — |
| A secret, a token, a path to a credential | nowhere | — |

The test: *would a fresh agent with the SRS, the plan and the code still
have to find this out the hard way?* If yes, memory. If the SRS or a code
comment should carry it instead, put it there and skip the memory.

## 2. Writing one

`docs/agents/memories/<topic>.md`, topic = the thing (`engine-token.md`,
`webkitgtk-css.md`, `line-endings-drift.md`), not the date or the session.

```md
# <Topic>

## <one fact, as a heading that reads like a claim>
Short paragraph or bullets. Path references as `path/file.ext:line`.
Date the first write when the fact might rot (`2026-09-19`).
```

One heading per fact — a file grows by headings, not by essays. Say what
was observed and what to do about it; skip the narrative of how you found it
unless the search itself is the landmine. Correct a wrong fact **in place**;
a stale memory is worse than none because it is trusted.

## 3. Reading them

Before a task, read `docs/agents/README.md` and any memory whose topic
matches the files you are about to touch. The AGENTS.md of a stamped project
says so; this skill is where the habit is enforced. Finding an answer in a
memory that you would otherwise have rediscovered is the whole return on the
practice.

## 4. Retiring

When a slice closes: delete its `context/<feature>.md` if the SRS and code now
carry everything, or trim it to what still is not written anywhere. When a
memory's fact is now enforced by a guard or a test, note that in the memory
(`enforced by scripts/check-version.mjs since v0.13.5`) — it may still save
someone from arguing with the guard.

## Report

```
memories: <added|corrected> docs/agents/memories/<topic>.md — "<heading>"
context:  <created|deleted> docs/agents/context/<feature>.md
```

## What not to do

- Do not write task status, PLAN excerpts or SRS copies as memories.
- Do not write secrets, tokens or credential paths.
- Do not leave a memory you know is wrong "for history" — correct it or
  delete it; git has the history.
- Do not write one file per session or per bug; write per topic and add
  headings.
