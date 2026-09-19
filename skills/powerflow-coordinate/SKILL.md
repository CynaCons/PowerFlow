---
name: powerflow-coordinate
description: Run the coordinator loop over the active PLAN.md iteration with PowerSpawn workers — rehydrate from the plan each cycle, pick ready tasks, dispatch one worker per task with the full contract (goal + gate, pasted context, allowed paths, definition of done, report shape), validate the gate yourself, commit, tick with evidence through powerplan, write memories, and stop cleanly when everything is green or nothing is ready. Use this whenever the user says "coordinate", "spawn workers", "delegate", "run the loop", "keep building until…", "use Codex/Copilot/Grok for this", when an iteration has several independent tasks, or when the coordinator's own context is filling up with file contents that a worker could summarise. Also use its dispatch contract for a single spawn — one worker still needs the whole brief.
---

# powerflow-coordinate — manager of agents, judge of evidence

The coordinator is the session the owner talks to. It owns the documents and
the plan; workers own product code, scoped to a task (METHODOLOGY.md §5). Two
facts shape everything here. Workers are **stateless** — the CLI loads
AGENTS.md and nothing else, so the prompt is the whole brief. And workers are
**unreliable narrators** — PowerSpawn logs every spawn deterministically to
IAC.md precisely because self-reporting fails ~95% of the time; the
coordinator runs the gate itself and never takes the worker's word.

Bundled: `references/dispatch-contract.md` — the prompt shape, provider
choice, batch sizing.

## The cycle

```
rehydrate → pick → dispatch → validate → record → (D12: show the miniplan) → repeat
```

### 1. Rehydrate — every cycle, from durable state

`show_miniplan` and `git log --oneline -20`. Not the conversation: after a
compaction or a long wait_for_agents, the plan and the commits are what is
true. If they disagree with your memory of the session, the plan wins. Read
`docs/agents/context/<slice>.md` (the brief from `powerflow-slice`) and the
memories that match the task's files.

### 2. Pick

Ready = an open task whose prerequisites (earlier tasks it depends on) are
ticked, with a gate you can name. A task without a checkable gate is not
dispatchable — `update_task` it first (add the "done when") or split it.
**Serial by default.** Dispatch two workers at once only when their allowed
paths are provably disjoint; a shared worktree is the cross-contamination
risk, not the token cost. Discovery spikes before dependents.

### 3. Dispatch — the contract, pasted

Build the prompt from `references/dispatch-contract.md`: task text verbatim,
SRS rows pasted, goal + gate (command and literal pass signal), `path:line`
context, allowed paths, the four worker prohibitions (no plan/PRD/SRS edits,
no commits), verify-once instructions, and the exact report shape. Choose a
CLI provider for file changes, an API provider for text-only opinions.
`spawn_* → agent_id`; `wait_for_agents` when you have nothing else to do;
`list` / `result` otherwise. Do useful coordinator work while waiting
(the next brief, a memory, the SRS row a worker will need) — but not
implementation in the same paths.

### 4. Validate — yourself

Read the worker's report, then ignore its conclusion and check:

1. `git status` — only the allowed paths changed; nothing under PLAN/PRD/SRS.
2. Run the gate command; require the literal pass signal; check any expected
   artifact's mtime is after the spawn.
3. Run the project's smoke when the change touches runtime.

Pass → step 5. Fail → re-dispatch **with the failure pasted** (the first
error, the diff of what it changed), same allowed paths, smaller scope if the
first attempt sprawled. Three failed attempts → `defer_task` with the reason
to the backlog, write a memory if the cause is a landmine, move on. Do not
spin.

### 5. Record — commit before tick

Commit the worker's change yourself (`feat(scope): … [worker: <provider>
<agent_id>]`), then `complete_task … agent=<agent_id>` with the gate output
as evidence in your notes. Commit first: if the tick lands and the commit
does not, the plan lies after a crash. IAC.md already holds the prompt and
the raw result; do not duplicate it into the plan.

### 6. Stop conditions

- **All green** — every task in the iteration ticked, the smoke task last;
  `close_iteration`, `check_plan`, commit `plan: close …`. If the final gate
  suite fails while every task is ticked, do not report success: `add_tasks`
  a regression task naming the failing command and keep going.
- **Stalled** — no ready task (all remaining are blocked on the owner or on
  a deferred dependency): report the blocked set with reasons; do not spin.
- **Owner needed** — an owner-report task awaiting its tick, a decision the
  brief did not settle: stop and ask, with the miniplan.

## Between cycles: the console

The owner is often not watching a long loop. Every cycle's report ends with
the miniplan (D12), and the report itself is a table — one row per worker:
task, provider, gate result, commit — not the worker's prose.

```
| # | Task | Worker | Gate | Result |
|---|---|---|---|---|
| 3 | radeau-proto UDP apps | codex #05f1 | cargo test → 41 passed | committed a1b2c3d, ticked |
| 4 | UI Name/Type tables | grok #9c2e | npm test → 1 fail (first: …) | re-dispatched with error |
```

## What not to do

- Do not spawn for a one-file fix you can do in the time it takes to write
  the prompt.
- Do not spawn dependent tasks in parallel.
- Do not let a worker edit PLAN.md, PRD.md or SRS files; if it did, revert
  those hunks before committing.
- Do not tick on the worker's report; tick on your own run of the gate.
- Do not keep a parallel task store (TodoWrite lists, SQL tables) as the
  source of truth — PLAN.md via powerplan is; anything else is scratch and
  must be reconciled to it.
- Do not paste worker transcripts into the report; IAC.md has them.
