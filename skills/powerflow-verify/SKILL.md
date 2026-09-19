---
name: powerflow-verify
description: Close the loop before anything is called done — run the project's gate ladder (typecheck + unit, e2e once on the real binary, smoke launch with a clean console, a look at changed UI states), collect the evidence lines, fill SRS Trace for rows a test now verifies, tick PLAN tasks through powerplan with that evidence, and close the iteration when every task has proof. Use this whenever you are about to say "done", "implemented", "fixed", "ready", or "works"; when the user asks "are we done?", "verify", "run the tests", "does it work?", "close the loop", or "ship it"; and before every report that claims progress. Build passing is not verification; this skill is.
---

# powerflow-verify — evidence or it didn't happen

The third movement of every iteration (METHODOLOGY.md §4.3, §6). Its job is
to turn "I think it works" into lines the owner can check: a command, its
exit code, a number, a path. It is also where the token budget is protected:
the rules about running e2e once and keeping screenshots opt-in come from
sessions that burned their context re-running suites and pasting images.

Bundled: `references/smoke-recipes.md` — how to observe a launch per platform
without screenshots.

## 0. What is being verified

`show_miniplan` — the current iteration, its tasks, and its smoke task (the
last one, `Smoke test: …`). Read AGENTS.md "Commands" and "How we verify":
the project's commands and any project-specific gates (pixel subsets, harness
scenarios, capture scripts) come from there, never from memory. Read the
PRD's quality bar for the `showcase:` switch (D8).

## 1. The ladder

Run in this order; stop at the first red and fix it, then resume from that
rung. Each rung produces one evidence line.

1. **Typecheck + unit** — `<typecheck_command>`, `<test_command>`. Record the
   counts ("118 passed").
2. **E2E, once** — `<e2e_command>` against the real built binary or the
   real dev server, never a mocked backend. If red: read the *first* error,
   fix, run once more. Do not run the suite again "to be sure" and do not
   turn on retries, traces or video to be thorough — seven tests failing on
   one missing element is one crash, not seven investigations.
3. **Smoke** — the app launches and its console is clean
   (`references/smoke-recipes.md` for the platform). This is the rung your
   global rule names: no completion claim without it.
4. **Look at it** (UI work only) — one capture per changed state via the
   project's capture script, reviewed against the project's visual
   walkthrough or the SRS rows. Not DevTools screenshots into the chat.
5. **Guards** — `node scripts/check-plan.mjs && node scripts/check-req-ids.mjs && node scripts/check-version.mjs`.

Where layers compose and the DOM cannot see the result (a canvas under rows,
a dialog over a grid), a class or computed-style assertion is not proof —
the test samples composited pixels. Where the owner said "feels laggy", the
test measures in-page timing. Assert what the owner sees.

## 2. Showcase (when the PRD says `showcase: required`)

Visual products opt in at PRD time. Then the iteration closes only with a
published artifact whose screenshots come **from the running app**: a
Playwright script *inside the repo* (Node resolves `@playwright/test` from
the script's location), `deviceScaleFactor: 2`, `locator.screenshot()`
element-clipped, then the script is deleted. A recreation of the UI in HTML
is not evidence and must not be presented as one.

## 3. Trace, then tick

- Every SRS row that a test now verifies gets the test path in its Trace
  column, in this same change (`powerflow-srs` §5). A row with `Test` and no
  path is still unverified.
- `complete_task` (via `powerflow-plan`) for each task whose evidence line
  exists, `agent=<your id>`. Owner-report tasks are **not** ticked:
  `update_task` to `… — fixed <sha>, awaiting owner verification`.
- All tasks proven → `close_iteration` with today's date; `check_plan` →
  `ok`. Any task without proof stays open and the iteration stays open; say
  which and why.

## 4. Commit

Spec, plan and code land together (`feat(scope): …`, `fix: …`), the plan
closure separately (`plan: close vX.Y.Z`). Do not push unless the project's
AGENTS.md or the owner says the coordinator pushes.

## Report — evidence lines

```
vX.Y.Z — verify
  typecheck   <cmd> → exit 0
  unit        <cmd> → 118 passed
  e2e         <cmd> → 12 passed (1 run)
  smoke       <cmd> → up in 6 s, console clean
  look        <n> states captured → <path>, reviewed against <walkthrough|SRS-X-00n>
  guards      check-plan OK · check-req-ids OK · check-version OK
  trace       SRS-X-004 ← tests/e2e/14-navrail.spec.ts
  showcase    <artifact url | not required>
ticked: <indexes> · open: <index> — <missing proof>
close_iteration vX.Y.Z: <done | blocked by …> · check_plan ok
```

Followed by the miniplan in its own fenced block (D12) — the owner returning to
the console sees the state, then the evidence.

## What not to do

- Do not report "tests pass" without the command and the count.
- Do not re-run a suite that already passed; do not re-run a failed suite
  before reading its first error.
- Do not screenshot a blank page — read the console or the Vite log first
  (`ReferenceError` after HMR means restart the dev server).
- Do not tick a task because the code is written; tick it because the
  evidence line exists.
- Do not force-close an iteration to make a release look ready.
