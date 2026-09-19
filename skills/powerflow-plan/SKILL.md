---
name: powerflow-plan
description: Operate PLAN.md through powerplan — open the session on the current iteration (show_miniplan), register new work as tasks or iterations the moment it appears, tick tasks only with evidence, close iterations when every task has proof, and end the session with the status update and check_plan. Use this at the start and end of every working session, whenever the user says "add this to the plan", "open the next iteration", "what's the current iteration", "close v0.x.y", "put it in the backlog", "update the plan", or whenever you are about to mark anything done. Also use it the moment you discover work that is not yet a task — before doing that work.
---

# powerflow-plan — the plan is the session's memory

PLAN.md is the operational backbone (METHODOLOGY.md §2.4, §3). It is written
by **powerplan only** — never by hand — because every project where agents
edited the plan freeform ended with stale headers, "COMPLETE" stamped without
proof, and work nobody could see. This skill is the discipline around the
tools: what to call, when, and what counts as evidence.

## The two bookends (D11)

**First thing in a session:** `show_miniplan`. It returns the current
iteration verbatim with its major header and the neighbouring iteration
headers — enough to know what we are doing and where it sits. Read it before
any other file. Do not `Read PLAN.md` whole; if you need another iteration,
`show_miniplan version=vX.Y.Z` or `get_iteration`.

**Last thing in a session:** the status update — tasks ticked with evidence,
discovered work registered, the iteration closed if every task has proof,
`check_plan` green — then the report to the owner. A session that ends without
this did not happen: the next session resumes from the plan, not from the
conversation.

## Registering work — before doing it

Whenever new work appears (owner feedback, a bug, a discovery while exploring,
a follow-up you would otherwise "just do"), register it first:

| Situation | Call |
|---|---|
| Belongs to the current iteration | `add_tasks version=<current> tasks=[…]` |
| A coherent new slice | `create_iteration` (see below), then `add_tasks` |
| Good idea, not now | `add_to_backlog texts=[…]` |
| Task in the current iteration should not be done here | `defer_task` (moves it to the backlog with a reason) |

This is what keeps the plan the source of truth for "what is open" — and what
lets a compacted or restarted session pick up where this one stopped.

## Iterations

Format (`## vX.Y — Major` / `### vX.Y.Z — Iteration` / `**Goal:**` /
checkboxes / `## Backlog` last) is produced by the tools; you supply the
content:

- **Goal** — one sentence, the outcome, not the activity. Include the date and
  the owner's words when the iteration exists because they asked
  ("Requested 2026-08-30 after 'EtherType 0x86DD' showed up undecoded").
- **Tasks** — checkboxes only; one deliverable each; the definition of done
  in the text when it is not obvious ("… (pytest green)", "… E2E asserts the
  stopped-state stillness"). No sub-bullets, no "files modified", no impact
  prose — git has those.
- **Last task is always the smoke test** — `Smoke test: <command> launches with
  zero console errors; …`. `powerflow-verify` looks for it when closing.
- Exactly **one active** iteration: `start_iteration` marks it and clears the
  previous marker. Do not open the next one until the current is closed.
- Versions are monotonic. A new major (`create_major`) groups a theme; new
  iterations attach with `major=vX.Y`.

Owner-report tasks quote the owner verbatim and are **never ticked by an
agent** (`powerflow-bug`): when fixed, `update_task` the text to
`… — fixed <sha>, awaiting owner verification` and leave the box open. The
iteration stays open until the owner ticks.

## Ticking — evidence or it didn't happen

`complete_task` when, and only when, you can name the proof: a test that
passed (command + count), a commit hash, an artifact path, a `check_plan`
result, a captured state the owner can look at. Put that proof in the report,
not in the task text. Pass `agent=<your id>` so the line carries who did it.
Build passing is not evidence that a feature works; "I implemented it" is not
evidence of anything.

If a task turns out wrong, `update_task` it (the tool preserves the done
state); if it splits, `add_tasks` the parts and `remove_task` the original
only when nothing has referenced it yet.

## Closing

`close_iteration version=vX.Y.Z stamp=<YYYY-MM-DD>` refuses while tasks are
open — that refusal is the point. Never pass `force=true` to make a status
look good; move the unfinished tasks forward (`defer_task`, or `add_tasks` on
the next iteration and `remove_task` here) and say so in the goal of the next
one. After closing, `start_iteration` the next, then `check_plan` → `ok: true`,
and commit the plan separately: `plan: close vX.Y.Z, open vX.Y.Z+1 (title)`.

## When powerplan is not loaded

The MCP server registers from `.mcp.json` at session start. If the
`powerplan` tools are missing: tell the owner a restart loads them; if the
Python package is importable, drive the same functions
(`from powerplan import mutations as m; m.mutate_and_save(path, fn)`). Do not
hand-edit PLAN.md as a shortcut; a bootstrap without powerplan is the one
exception and it is a `powerflow-init` job.

## Report shape (end of session)

```
Iteration vX.Y.Z — <n>/<m> tasks
  ticked: <index> <task> — <evidence>
  added:  <task> (why it appeared)
  open:   <task> — <what is missing>
check_plan: ok · commit <sha>
Next: <the first open task, or the next iteration>
```
