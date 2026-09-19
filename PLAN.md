# PowerFlow — Implementation Plan

**Goal:** Codify the PRD → decisions → SRS → PLAN → agents → verify → release methodology once — as a handbook (METHODOLOGY.md), a template set and a `powerflow-*` skill plugin — so every project runs the same flow without re-specifying it. See [PRD.md](PRD.md).

**Philosophy:** PLAN.md first and last. Single writer (powerplan). Evidence or it didn't happen. Deterministic where a program can do it. Dogfood: PowerFlow follows PowerFlow from the first commit.

---

## Current Status

The current iteration is the last heading below that is not marked COMPLETE
(`powerplan get_current_iteration` / `show_miniplan`). This header never names
a version, so it cannot go stale. Verify: `python scripts/check.py` (plan lint
+ index consistency); skills are verified by a dry run in a stamped throwaway repo.

---

## v0.1 — Definition
> Handbook, decisions, templates and the core skills.

### v0.1.0 — Project initiation (2026-09-18) (COMPLETE)
**Goal:** Repo scaffold, PRD, this plan under powerplan, decisions D1–D11 recorded, handbook first draft, the 2026-09-18 proposal archived, show_miniplan defined in powerplan.
- [x] Write PRD.md (problem, users, principles, contents, skill surface, distribution, non-goals, success criteria, decisions to record) [agent: claude-opus-5]
- [x] Create PLAN.md through powerplan (this file); register powerplan in .mcp.json + .claude/settings.local.json [agent: claude-opus-5]
- [x] Record decisions D1–D11 in docs/decisions/ with a README index [agent: claude-opus-5]
- [x] Write METHODOLOGY.md — the handbook (the loop, documents, PLAN first and last, four movements, agents, close the loop, owner reports, release, determinism, conventions) [agent: claude-opus-5]
- [x] AGENTS.md + CLAUDE.md shim + README.md for PowerFlow itself [agent: claude-opus-5]
- [x] Archive the 2026-09-18 proposal page under docs/ [agent: claude-opus-5]
- [x] Define show_miniplan in powerplan: PRD §5 row + v0.8.0 iteration in powerplan/PLAN.md (implementation tracked there) [agent: claude-opus-5]
- [x] git init, .gitignore, first commit [agent: claude-opus-5]
- [x] Smoke test: powerplan check_plan green; every decision file linked from docs/decisions/README.md; every skill named in PRD.md has a catalog row [agent: claude-opus-5]

### v0.1.1 — Templates + powerflow-init (current) (ACTIVE)
**Goal:** Every project artifact as a template with the D1–D11 decisions baked in, and the skill that stamps them into a new repo.
- [x] templates/PRD.md, PLAN.md (header per D2), AGENTS.md, CLAUDE.md shim, README.md [agent: claude-opus-5]
- [x] templates/docs/srs/README.md (index + prefix allocator, columns per D1) + SRS-template.md [agent: claude-opus-5]
- [x] templates/docs/decisions/README.md + D-template.md [agent: claude-opus-5]
- [x] templates/docs/agents/README.md (memories + context rules) [agent: claude-opus-5]
- [x] templates/.mcp.json (uvx and python -m variants), .claude/settings.local.json, .claude/launch.json [agent: claude-opus-5]
- [x] templates/.github/workflows/ci.yml guards job + scripts/check-req-ids.mjs, check-plan.mjs (lint mirror of check_plan, not PowerGit's one-off normalizer), check-version.mjs (from RadEAU / PowerGit) [agent: claude-opus-5]
- [x] skills/powerflow-init/SKILL.md — interview → stamp → create_plan → v0.1.0 standard tasks → smoke → first commit [agent: claude-opus-5]
- [x] Smoke test: stamp a throwaway repo; its guards run green; check_plan green [agent: claude-opus-5]

### v0.1.2 — Core loop skills
**Goal:** The skills that run one iteration end to end: plan, slice, srs, verify, status.
- [ ] skills/powerflow-plan — iteration lifecycle through powerplan; PLAN first and last (show_miniplan at session start, status update at session end); one active; smoke task last; owner-tick rule
- [ ] skills/powerflow-slice — plan-mode brief → SRS rows → PLAN tasks with allowed paths + definition of done, before the first edit
- [ ] skills/powerflow-srs — create/extend docs/srs/SRS-<feature>.md, allocate IDs, duplicate check, matching PLAN task
- [ ] skills/powerflow-verify — the gate: typecheck + unit, e2e once, smoke launch with console check, evidence lines; screenshot policy; showcase switch (D8)
- [ ] skills/powerflow-status — adopt the ASCII gantt + visual board from powerplanner
- [ ] Smoke test: open and close this iteration using only these skills

### v0.1.3 — Discipline skills
**Goal:** bug, decide, memory, release, prd.
- [ ] skills/powerflow-bug — symptom-first failing test quoting the owner; task left open as 'fixed <sha>, awaiting owner verification'
- [ ] skills/powerflow-decide — ADR file + decisions README + PRD table link
- [ ] skills/powerflow-memory — docs/agents memories/context rules (one fact per heading, dated, corrected in place)
- [ ] skills/powerflow-release — the ritual; project commands come from AGENTS.md
- [ ] skills/powerflow-prd — once per project or on a major redirection (D10); refuses routine edits and points to powerflow-decide / powerflow-srs
- [ ] Smoke test: powerflow-release dry run against PowerGit reproduces its release skill's step list

### v0.1.4 — Orchestration + audit
**Goal:** coordinate over powerspawn, and audit a repo against the pack.
- [ ] skills/powerflow-coordinate — loop over the active iteration via powerspawn; dispatch contract; verify the gate yourself; serial by default, parallel only on disjoint paths
- [ ] skills/powerflow-audit — drift report (missing artifacts, header style, SRS scheme, shim, memories, guards, unverified requirements) emitted as PLAN tasks
- [ ] Smoke test: audit PowerGit and RadEAU; the drift table from the proposal is reproduced

## v0.2 — Distribution
> Plugin packaging, reference installs, consolidated guards.

### v0.2.0 — Plugin packaging + two reference installs
**Goal:** One user-level install puts every powerflow-* skill in every session; two real projects run one full iteration through the pack.
- [ ] .claude-plugin/plugin.json + marketplace.json; install at user level
- [ ] Stamp one new project with powerflow-init; retrofit RadEAU with powerflow-audit's fix list
- [ ] Smoke test: one full iteration in each project with zero hand-edits of PLAN.md

### v0.2.1 — Guards package
**Goal:** check-req-ids, plan-normalize and check-version as one tested script set.
- [ ] Consolidate the three guard scripts with tests; projects vendor or npx them
- [ ] Tag v0.2; release notes from the closed iterations

## Backlog
- autosar-101-training: fold embedded close-the-loop guidance (SIL, debugger, CAN/XCP, datasheets, SDK references) into powerflow-verify once the repo is located (D9)
- Bidirectional test ↔ requirement map generator for docs/srs/README.md
- powerflow-audit reports the pack version a project was stamped with
