---
name: powerflow-slice
description: Start the next slice of work the PowerFlow way — explore the repo and the plan, ask the owner what cannot be inferred, write a brief (context with file:line citations, outcome, SRS rows, tasks with allowed paths and definition of done), get it approved, then turn it into SRS rows and PLAN tasks before the first edit. Use this whenever the user says "let's start the next slice / iteration", "let's do v0.x.y", "plan this feature", "how should we build X", opens a piece of work bigger than a one-file fix, or describes a feature request or owner feedback that has no tasks yet. Use it even if the user says "just implement it" when the work touches more than a couple of files — the brief is what makes the implementation short.
---

# powerflow-slice — plan mode, then rows and tasks, then code

An iteration walks four movements; this skill is the first one (METHODOLOGY.md
§4.1). It exists because work that starts from a vague sentence gets
re-investigated every time the context resets, while work that starts from a
brief with citations and a definition of done can be handed to any worker and
resumed by any session. Plan mode is the harness's way of forcing the explore
→ ask → write → approve order; use it when the harness offers it, and follow
the same order by hand when it does not.

Bundled: `references/brief-template.md` — the brief's shape.

## 1. Where does this sit? (`powerflow-plan` opener)

`show_miniplan` first. Then decide:

- The work fits the **current** iteration → it becomes tasks there.
- It is a coherent new outcome → it becomes the **next** iteration
  (`create_iteration` under the right major), started only after the current
  one closes.
- It is an owner report of a defect → `powerflow-bug`, not this skill.
- The PRD contradicts it → that is a direction change: stop and say so
  (D10); a slice does not quietly rewrite product intent.

## 2. Explore before asking

Read what the slice touches — the SRS files for the area, the code paths, the
tests, the memories in `docs/agents/`. The goal of exploring is to be able to
write "X already exists at `path:line` and does Y; the gap is Z". Most
questions answer themselves here, and the ones that survive are the ones
worth the owner's time.

Note what you find as you go; those `path:line` facts are the brief's
Context section and the worker's starting point.

## 3. Ask — one round

Ask only what the repo cannot tell you: which of two behaviours the owner
wants when they conflict, the number behind a "fast", whether a platform is
in scope, what "done" looks like to them. Batch the questions into one
message. Offer a default for each so a "yes" is a complete answer.

## 4. Write the brief

Use `references/brief-template.md`. The parts that matter most:

- **Context** quotes the owner and cites existing machinery, so nobody
  re-derives it after a compaction.
- **Requirements** lists the SRS rows by ID — allocate them now with
  `powerflow-srs` if the behaviour is new. Behaviour without a row is not
  ready to build.
- **Work** is one block per task, each with *allowed paths* and *done when*
  (a command and its literal pass signal, or the owner-visible state). Those
  two fields are what make a task dispatchable to a worker and gateable by
  the coordinator.
- **Out of scope** names what was considered and dropped, and sends the good
  ideas to `add_to_backlog` so they stop haunting the slice.

Keep it under two screens. A brief that needs scrolling is two slices.

## 5. Approval, then registration — before any edit

Present the brief; the owner approves, amends or redirects. Then, in this
order:

1. `powerflow-srs`: the rows land in `docs/srs/`, allocator bumped,
   `check-req-ids` OK.
2. `powerflow-plan`: `create_iteration` (if new) with the Outcome as the
   Goal; `add_tasks` — one per Work block, in order, IDs cited in the text;
   the last task is the smoke test; `start_iteration` when the previous one
   is closed.
3. Save the brief where the next agent finds it: `docs/agents/context/<slice>.md`
   (delete it when the slice closes and the SRS + code carry everything).

Only now does implementation begin. If you catch yourself editing product
code before the tasks exist, stop and register them — that is the whole rule.

## 6. Hand-off

If workers will implement (`powerflow-coordinate`), each Work block is one
dispatch: its Files are the allowed paths, its Done-when is the gate. If you
implement yourself, work the tasks in order and tick each with evidence
(`powerflow-plan`), then close the loop with `powerflow-verify`.

## Report (after registration)

```
Slice vX.Y.Z — <title>
  brief: docs/agents/context/<slice>.md (approved <date>)
  SRS: <k> rows — SRS-X-004..006 (tag X extended) · check-req-ids OK
  PLAN: <n> tasks added; smoke task: "<text>"; iteration <started | queued behind vX.Y.Z-1>
  first task: <text> — files <paths>, done when <gate>
```

## What not to do

- Do not start with code and write the brief afterwards "to document it".
- Do not put implementation detail in PLAN tasks — the brief carries it; the
  task names the deliverable and the gate.
- Do not ask questions the SRS or the memories already answer.
- Do not let the brief grow a design document; if design is needed, it is
  `docs/decisions/` (a decision) or the SRS Notes section (design context).
