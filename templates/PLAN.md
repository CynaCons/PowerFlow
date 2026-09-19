<!-- REFERENCE ONLY. PLAN.md is never copied from a template: powerflow-init
creates it through powerplan (create_plan, append_prose, create_major,
create_iteration, add_tasks, start_iteration) so the single-writer rule holds
from the first byte. This file shows what the result looks like (D2). -->
# {{project}} — Implementation Plan

**Goal:** {{one_liner}} See [PRD.md](PRD.md).

**Philosophy:** PLAN.md first and last. Single writer (powerplan). Evidence or it didn't happen. Plan before code; spec rows before implementation; every iteration ends on a smoke test.

---

## Current Status

The current iteration is the last heading below that is not marked COMPLETE
(`powerplan show_miniplan` / `get_current_iteration`). This header never names
a version, so it cannot go stale. Verify: `{{verify_command}}`. Stack: {{stack}}.

---

## v0.1 — Foundation
> Repo scaffold, documentation backbone, canonical build, CI guards.

### v0.1.0 — Project initiation (current) (ACTIVE)
**Goal:** The methodology backbone is in place before the first feature: PRD, plan, requirement index, decisions, agent briefing, CI guards, and a smoke that proves the scaffold launches.
- [ ] Write PRD.md (problem, users, principles, shape, stack, quality bar, decisions to record)
- [ ] Record the PRD's decisions in docs/decisions/ (one file each, before the affected part is built)
- [ ] Scaffold the application ({{stack}}) with the canonical dev and build commands from AGENTS.md
- [ ] CI: guards job (check-plan, check-req-ids, check-version) + typecheck + unit tests
- [ ] First SRS file for the first feature area, IDs allocated in docs/srs/README.md
- [ ] Smoke test: `{{smoke_command}}` launches with zero console errors; `check_plan` green; guards green

## Backlog
