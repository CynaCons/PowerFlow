# The first iteration, verbatim

`powerflow-init` creates PLAN.md through powerplan with exactly these calls so
every project starts from the same shape (D2). Substitute the answers; keep
the wording — the smoke task in particular is what `powerflow-verify` looks
for when it closes an iteration.

## 1. `create_plan`

```
title:      "<project> — Implementation Plan"
goal:       "<one_liner> See [PRD.md](PRD.md)."
philosophy: "PLAN.md first and last. Single writer (powerplan). Evidence or it didn't happen. Plan before code; spec rows before implementation; every iteration ends on a smoke test."
seed_major: false
```

## 2. `append_prose` — the stale-proof header

`create_plan` has already written Goal, Philosophy and a rule; append only:

```
## Current Status

The current iteration is the last heading below that is not marked COMPLETE
(`powerplan show_miniplan` / `get_current_iteration`). This header never names
a version, so it cannot go stale. Verify: `<verify_command>`. Stack: <stack>.

---
```

## 3. `create_major`

```
version: "v0.1"   title: "Foundation"
description: "Repo scaffold, documentation backbone, canonical build, CI guards."
```

## 4. `create_iteration`

```
version: "v0.1.0"   title: "Project initiation"   major: "v0.1"
goal: "The methodology backbone is in place before the first feature: PRD, plan, requirement index, decisions, agent briefing, CI guards, and a smoke that proves the scaffold launches."
```

## 5. `add_tasks` on v0.1.0

```
Write PRD.md (problem, users, principles, shape, stack, quality bar, decisions to record)
Record the PRD's decisions in docs/decisions/ (one file each, before the affected part is built)
Scaffold the application (<stack>) with the canonical dev and build commands from AGENTS.md
CI: guards job (check-plan, check-req-ids, check-version) + typecheck + unit tests
First SRS file for the first feature area, IDs allocated in docs/srs/README.md
Smoke test: `<smoke_command>` launches with zero console errors; check_plan green; guards green
```

## 6. `start_iteration("v0.1.0")`

Then `check_plan` must report `ok: true`, `current: v0.1.0`.

## Ticking as you go

The stamp itself completes nothing in this list — PRD.md exists but is a
skeleton until the interview fills it; decisions are recorded when the PRD
names them. Tick a task only when its evidence exists (`complete_task` with
the `agent` you are running as).
