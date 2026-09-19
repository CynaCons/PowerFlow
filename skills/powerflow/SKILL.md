---
name: powerflow
description: The PowerFlow way of building software with agents — start a project (PRD once, PLAN.md through powerplan, a short AGENTS.md), run every session and turn on the plan (show_miniplan first, status update last, miniplan at the end of each major turn), write SRS rows before code, close the loop before saying "done", handle owner-reported bugs failing-test-first, spawn and supervise PowerSpawn workers with a full brief, keep memories, cut releases, and audit a repo for drift. Use this whenever the user starts a new project, says "powerflow", "start a slice", "what's next", "verify", "bug:", "release", "spawn workers / use Codex / Copilot / Grok for this", "how do we work here", or opens a repo that has a PLAN.md — the plan is the session's memory and this skill is how it is operated.
---

# PowerFlow

One method, ten rules, two tools. **powerplan** writes PLAN.md — nobody else
does. **PowerSpawn** spawns workers and logs them — the coordinator verifies.
Everything else here is how to use those two well. Scripts: `scripts/stamp.py`
(start a project), `scripts/audit.py` (measure drift). References, read when
the section says so: `references/workers.md`, `references/release.md`,
`references/smoke.md`.

## 1. Start a project

Look before asking: `package.json` scripts, `src-tauri/`, `pyproject.toml`
tell you the stack, the commands and the version source. Then one round of
questions for what is left — name, one-liner, platform, the canonical
`dev / smoke / test / typecheck / e2e` commands (an honest `echo "no e2e yet"`
beats an invented script), `showcase: required|optional`. Save the answers to
`.powerflow/init.json` and stamp:

```bash
python <skill>/scripts/stamp.py --target <repo> --answers <repo>/.powerflow/init.json
```

That writes PRD skeleton, AGENTS.md, CLAUDE.md shim, `docs/srs/README.md`,
`.mcp.json` (powerplan; `uvx` or `python -m`), `.claude/settings.local.json`
(project powerplan disabled when the plugin already provides it), `.gitignore`,
`docs/agents/memories/`. It never writes PLAN.md and never overwrites a file
that carries project state. A repo that already has a PLAN.md is a retrofit:
§10, not a stamp.

Then create the plan **through powerplan** (§2): `create_plan` (no seed
major), `append_prose` with the Current Status header, `create_major v0.1`,
`create_iteration v0.1.0`, `add_tasks` (PRD · decisions · scaffold · first SRS
· `Smoke test: <smoke_command> launches with zero console errors`),
`start_iteration`, `check_plan`. Then the **PRD conversation** — the one time
PRD.md is written (D10): problem, users, principles, shape (in / out of v1),
stack, quality bar, non-goals, decisions to record, success criteria; the
owner's words, no padding. Commit `chore: PowerFlow scaffold`. Ask before
pushing.

## 2. The plan — powerplan

PLAN.md is the operational backbone and the session's memory. It is written
**only through powerplan tools**; a hand edit is a process violation because
every project where agents edited the plan freeform ended with stale headers
and "COMPLETE" stamped without proof. Format, produced by the tools:
`## vX.Y — Major` · `### vX.Y.Z — Iteration` · `**Goal:**` one sentence ·
`- [ ]` checkboxes only · last task `Smoke test: …` · `## Backlog` last ·
header `## Current Status` = "the last heading not marked COMPLETE" (never a
version number).

| Need | Tool |
|---|---|
| What are we doing, where does it sit | `show_miniplan` (raw plan text: current iteration + neighbouring headers; `version`, `before`, `after`) |
| The same as JSON / one iteration / all open | `get_current_iteration` · `get_iteration version` · `list_iterations filter=open` |
| Find a task / read the backlog / skim everything | `find_task text` · `get_backlog` · `show_plan` |
| New work | `create_major` · `create_iteration version title major goal` · `add_tasks version tasks[]` · `add_to_backlog texts[]` |
| Change work | `update_task` (text, keeps done state) · `remove_task` · `defer_task` (to backlog, with reason) |
| Progress | `complete_task version indexes[] agent` · `reopen_task` · `start_iteration` · `close_iteration version stamp` |
| Health | `check_plan` (duplicates, two currents, complete-with-open, backlog last) · `create_plan` when none exists |

The rules around the tools:

- **Bookends (D11).** First thing in a session: `show_miniplan`. Last thing:
  ticks with evidence, discovered work registered, `check_plan` green, then
  the report. The conversation is not state; after a compaction the plan is
  where work resumes.
- **Miniplan at the end of every major turn (D12).** A turn that changed
  files, ticked or added tasks, ran a gate or closed an iteration ends with
  the raw `show_miniplan` block, after the report, before any question. The
  owner switches contexts and reads the console cold.
- **Register before doing.** Owner feedback, a bug, a discovery, a follow-up
  you would "just do" — it becomes a task (`add_tasks`), an iteration, or a
  backlog item first. This is what keeps "what is open" true.
- **Tick with evidence.** `complete_task` only when you can name the proof: a
  test count, a commit, an artifact path, a `check_plan` result. Pass
  `agent=<your id>`. "I implemented it" is not evidence; build passing is not
  a feature working.
- **One active iteration**, versions monotonic, iterations append-only.
  `close_iteration` refuses while tasks are open — that refusal is the point.
  Never `force`; move tasks forward (`defer_task`, or `add_tasks` on the next)
  and say so. Commit plan closures separately: `plan: close vX.Y.Z, open …`.
- **Owner-report tasks are ticked by the owner** (§6).
- **Task text is ASCII-safe** where the MCP round-trips it; iteration goals
  quote the owner and carry the date when the iteration exists because they
  asked.
- If the `powerplan` tools are missing, a restart loads them (`.mcp.json`);
  do not hand-write the plan to save one.

## 3. Requirements — SRS rows before code

`docs/srs/SRS-<feature>.md`, one per feature area, opens with:

| ID | Requirement | Rationale | Verification | Trace |
|---|---|---|---|---|

`SRS-<FEAT>-NNN` (D1): the tag is owned by one file (`docs/srs/README.md`
lists tag → file), the next number is `max + 1` in that file, numbers are
never reused — a changed requirement is a new row and the old one is marked
`(superseded by …)`. One testable *shall* per row, a number instead of "fast",
`Test | Analysis | Review | Demo`, the test path in Trace once it exists (a
`Test` row with no path is not verified). A named feature does not ship
without its file; rows land in the same change as the code. The rows worth
most are interaction semantics — which control wins when states disagree.

## 4. A slice

Explore first (the SRS, the code, `docs/agents/`), until you can write "X
exists at `path:line` and does Y; the gap is Z". Ask the owner one round of
what the repo cannot tell you, with defaults. Write a brief — owner's words
verbatim, `path:line` context, outcome, SRS rows, one block per task with
**files it may touch** and **done when** (command + literal pass signal) —
save it as `docs/agents/context/<slice>.md`. On approval: SRS rows (§3), then
PLAN tasks (§2), then the first edit. Never the other order. Delete the brief
when the slice closes and the SRS + code carry it.

## 5. Close the loop — before "done"

In order, one evidence line each, stop at the first red and fix it:

1. typecheck + unit (counts);
2. **e2e once** on the real binary / dev server — red → read the *first*
   error, fix, run once; no rerun loops, no retries "to be sure";
3. **smoke**: the app launches and its console is clean
   (`references/smoke.md` per platform) — your global rule, no exceptions;
4. **look at it** for UI work: one capture per changed state via the
   project's capture script, reviewed — DevTools screenshots into the chat are
   opt-in only (they have dominated whole sessions);
5. guards, if the project has them (`extras/guards`).

Where layers compose and the DOM cannot see the result, assert composited
pixels; "feels laggy" is measured in-page. `showcase: required` (D8) means the
iteration closes only with screenshots from the running app. Then fill SRS
Trace for rows a test now verifies, tick with the evidence lines, close the
iteration if everything has proof, and end with the miniplan.

## 6. Owner reports

The owner's sentence is the requirement. Register it verbatim
(`Owner report <date>: "…" [platform]`). First commit: a **failing test that
reproduces the symptom on the reported platform**, asserting what the owner
sees — not your diagnosis of it (PowerGit tested "author-highlight class
absent" for three iterations while the selected commit stayed hidden; nobody
looked at the window). Fix, run once. Then `update_task` to
`… — fixed <sha>, awaiting owner verification` and **leave the box open**; the
owner ticks it, and the iteration waits.

## 7. Workers — PowerSpawn

PowerSpawn spawns real CLI agents (Claude, Codex, Copilot, Grok, Cursor,
Gemini) and API agents (Grok, Gemini, Mistral), logs every spawn and result
to `IAC.md` deterministically, and lets the coordinator distribute work across
subscriptions. It exists because agents self-report unreliably — the log is
the record, and the coordinator runs the gate. This section will grow with
PowerSpawn; keep it the most current one in the file.

| Tool | Use |
|---|---|
| `spawn_claude prompt model? timeout?` · `spawn_codex prompt model?` · `spawn_copilot prompt model?` · `spawn_grok prompt model? force? timeout?` · `spawn_cursor` · `spawn_gemini_cli` | **CLI agents** — edit files, run commands; auto-load AGENTS.md (Claude also CLAUDE.md). `force=true` on Grok to apply edits |
| `spawn_grok_api` · `spawn_gemini` · `spawn_mistral` | **API agents** — text back only; the coordinator applies it. Second opinions, reviews, drafts, research |
| `list` · `result agent_id` · `wait_for_agents timeout?` | Watch, collect, join. Results and cost are also in `IAC.md` |

Registration: `.mcp.json` → `"powerspawn": {"command": "python", "args": ["-m", "powerspawn.mcp_server"]}`
with a PowerSpawn checkout importable (submodule or `PYTHONPATH`); enable it in
`.claude/settings.local.json`.

**When to spawn.** Independent multi-file work; anything you would otherwise
read in full and could receive as a summary (keeps the coordinator's context
lean); parallel independent tasks; a second model's opinion; Claude
rate-limited → Codex / Copilot / Grok. Not for a one-file fix that takes less
time than writing the brief, and never for dependent tasks in parallel.

**The brief is the whole context.** Workers are stateless; paste, do not
reference (`references/workers.md` has the template): the PLAN task verbatim
and its SRS rows; goal and **gate** (command + literal pass signal, expected
artifact); `path:line` context and the memories that apply; **allowed paths**
and the four prohibitions (no PLAN/PRD/SRS edits, no commits, no history
rewrites, no reformatting); verify-once instructions; the exact report shape
(changed / gate output / open / memories / unknowns). A prompt missing a block
buys twenty minutes of re-exploration or a false "done". `timeout` 600 s
default, 900 s for builds; a timed-out worker is re-dispatched with the failure
pasted and a smaller scope, not the same prompt.

**The loop.** `show_miniplan` + `git log` → pick a ready task with a nameable
gate → dispatch (serial by default; parallel only on provably disjoint paths)
→ do coordinator work while waiting, never implementation in the same paths →
**validate yourself**: `git status` shows only allowed paths changed, run the
gate, require the pass signal, run the smoke if runtime changed → **commit
before tick** (`feat(scope): … [worker: <provider> <id>]`, then
`complete_task … agent=<id>`) → memory if a landmine surfaced → miniplan.
Three failed attempts → `defer_task` with the reason; move on. Stop cleanly
when all tasks are proven (close the iteration) or nothing is ready (report the
blocked set) — never spin. Report as a table: task · worker · gate · result.

**Coming in PowerSpawn** (design docs in its repo — `DESIGN-fleet-agents.md`,
`docs/advisor-panel-spec.md`): *persistent role agents* re-invoked by name on
their own CLI session (`create_persistent_agent`, `ask_persistent_agent`), the
*ask-coordinator* channel where a running worker blocks on a question
(`list_pending_questions`, `answer_agent`), and the *advisor panel* (criteria →
converge → independent answers → merge across models). When they land: a
persistent expert replaces re-briefing for repeated work in one area; a worker
question is answered from the plan and the SRS, not from memory; a panel
informs a decision (§8), it never ticks a task. Update this section in the
same change as the PowerSpawn release.

## 8. Memories and decisions

`docs/agents/memories/<topic>.md` — one dated fact per heading, corrected in
place — when you hit something the next agent would rediscover: a platform
trap, a build quirk, a measurement that must match. Never task status,
secrets, or SRS copies. `docs/agents/context/<slice>.md` is the slice brief,
deleted when absorbed. Decisions — a choice between alternatives with lasting
consequences — go to `DECISIONS.md` (or `docs/decisions/D<n>.md` in projects
that prefer files): context, decision, and what would reopen it. A direction
change for the product is a decision first, then a PRD revision (D10).

## 9. Release

`references/release.md` is the checklist; the project's AGENTS.md and release
notes supply the commands. The refusals: never from an open iteration (close
it — the notes are the closed iterations); never with an owner report awaiting
its tick; one version source, every derived copy checked; the packaged
artifact launched before it is published; **check `gh run list` before
dispatching a workflow** — a tag pushed from the owner's credentials already
started it, and a second run fails at the registry (powerplan 0.8.0). Never
move a tag that published; ship `+1`. Record a new failure mode in the
project's release notes and as a memory.

## 10. Audit — retrofit an existing repo

```bash
python <skill>/scripts/audit.py --root <repo> [--tasks]
```

Read-only. Findings by area with the canonical fix: missing PRD/PLAN/AGENTS,
CLAUDE.md not a shim, no stale-proof header, achievements lists, prose bullets
in iterations, SRS location/scheme/columns, no memories, powerplan missing or
registered by absolute path, unnumbered specs. Judge each: **adopt** (a stamp,
a header line), **decide** (a live ID scheme is that repo's decision, not a
lint fix), or **pack bug** (fix `audit.py`). Register the adopt list as a
"PowerFlow retrofit" iteration in that repo through powerplan; the retrofit
closes when the audit prints `findings: 0`.

## Reports

Evidence lines, not narrative: command → exit code / count / path. Workers as
a table. Then the miniplan.
