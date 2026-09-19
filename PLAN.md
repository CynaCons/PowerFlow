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

### v0.1.1 — Templates + powerflow-init (2026-09-19) (COMPLETE)
**Goal:** Every project artifact as a template with the D1–D11 decisions baked in, and the skill that stamps them into a new repo.
- [x] templates/PRD.md, PLAN.md (header per D2), AGENTS.md, CLAUDE.md shim, README.md [agent: claude-opus-5]
- [x] templates/docs/srs/README.md (index + prefix allocator, columns per D1) + SRS-template.md [agent: claude-opus-5]
- [x] templates/docs/decisions/README.md + D-template.md [agent: claude-opus-5]
- [x] templates/docs/agents/README.md (memories + context rules) [agent: claude-opus-5]
- [x] templates/.mcp.json (uvx and python -m variants), .claude/settings.local.json, .claude/launch.json [agent: claude-opus-5]
- [x] templates/.github/workflows/ci.yml guards job + scripts/check-req-ids.mjs, check-plan.mjs (lint mirror of check_plan, not PowerGit's one-off normalizer), check-version.mjs (from RadEAU / PowerGit) [agent: claude-opus-5]
- [x] skills/powerflow-init/SKILL.md — interview → stamp → create_plan → v0.1.0 standard tasks → smoke → first commit [agent: claude-opus-5]
- [x] Smoke test: stamp a throwaway repo; its guards run green; check_plan green [agent: claude-opus-5]

### v0.1.2 — Core loop skills (2026-09-19) (COMPLETE)
**Goal:** The skills that run one iteration end to end: plan, slice, srs, verify, status.
- [x] skills/powerflow-plan — iteration lifecycle through powerplan; PLAN first and last (show_miniplan at session start, status update at session end); one active; smoke task last; owner-tick rule [agent: claude-opus-5]
- [x] skills/powerflow-slice — plan-mode brief → SRS rows → PLAN tasks with allowed paths + definition of done, before the first edit [agent: claude-opus-5]
- [x] skills/powerflow-srs — create/extend docs/srs/SRS-<feature>.md, allocate IDs, duplicate check, matching PLAN task [agent: claude-opus-5]
- [x] skills/powerflow-verify — the gate: typecheck + unit, e2e once, smoke launch with console check, evidence lines; screenshot policy; showcase switch (D8) [agent: claude-opus-5]
- [x] skills/powerflow-status — adopt the ASCII gantt + visual board from powerplanner [agent: claude-opus-5]
- [x] Smoke test: open and close this iteration using only these skills [agent: claude-opus-5]

### v0.1.3 — Discipline skills (2026-09-19) (COMPLETE)
**Goal:** bug, decide, memory, release, prd.
- [x] skills/powerflow-bug — symptom-first failing test quoting the owner; task left open as 'fixed <sha>, awaiting owner verification' [agent: claude-opus-5]
- [x] skills/powerflow-decide — ADR file + decisions README + PRD table link [agent: claude-opus-5]
- [x] skills/powerflow-memory — docs/agents memories/context rules (one fact per heading, dated, corrected in place) [agent: claude-opus-5]
- [x] skills/powerflow-release — the ritual; project commands come from AGENTS.md [agent: claude-opus-5]
- [x] skills/powerflow-prd — once per project or on a major redirection (D10); refuses routine edits and points to powerflow-decide / powerflow-srs [agent: claude-opus-5]
- [x] Smoke test: powerflow-release dry run against PowerGit reproduces its release skill's step list [agent: claude-opus-5]
- [x] D12 turn-end miniplan (owner 2026-09-19: 'at the end of each major turn, show me the miniplan'): decision file + PRD table, METHODOLOGY.md section 3, AGENTS.md template + PowerFlow AGENTS.md, powerflow-plan / powerflow-verify report shapes end with the miniplan, one line in the owner's global CLAUDE.md [agent: claude-opus-5]

### v0.1.4 — Orchestration + audit (2026-09-19) (COMPLETE)
**Goal:** coordinate over powerspawn, and audit a repo against the pack.
- [x] skills/powerflow-coordinate — loop over the active iteration via powerspawn; dispatch contract; verify the gate yourself; serial by default, parallel only on disjoint paths [agent: claude-opus-5]
- [x] skills/powerflow-audit — drift report (missing artifacts, header style, SRS scheme, shim, memories, guards, unverified requirements) emitted as PLAN tasks [agent: claude-opus-5]
- [x] Smoke test: audit PowerGit and RadEAU; the drift table from the proposal is reproduced [agent: claude-opus-5]

## v0.2 — Distribution
> Plugin packaging, reference installs, consolidated guards.

### v0.2.0 — Plugin packaging + two reference installs (2026-09-19) (COMPLETE)
**Goal:** One user-level install puts every powerflow-* skill in every session; two real projects run one full iteration through the pack.
- [x] .claude-plugin/plugin.json + marketplace.json; install at user level [agent: claude-opus-5]
- [x] RadEAU audit fix list produced (docs/audits/RadEAU-2026-09-19.md, 10 findings, judgment pass noted); D7 pointers committed in powerplanner (f13df1d); PowerFlow self-stamped (.powerflow/init.json). Stamping a new project and the RadEAU retrofit itself moved to v0.2.2 (owner) [agent: claude-opus-5]
- [x] Smoke test: claude plugin validate green (manifest, marketplace, 13 skills); installed at user scope; details lists 13 skills; throwaway re-stamped with plugin detection (settings.local.json disables the project copy, D14) [agent: claude-opus-5]

### v0.2.1 — Guards package (2026-09-19) (COMPLETE)
**Goal:** check-req-ids, plan-normalize and check-version as one tested script set.
- [x] Guards consolidated: --root on check-req-ids/check-version, 17 node --test cases (npm test), stamp --force protects stateful files; projects vendor them via powerflow-init (npx deferred with the public marketplace, D13) [agent: claude-opus-5]
- [x] Tag v0.2.0 (plugin.json version) on the plan-close commit; CHANGELOG.md 0.2.0 from the closed iterations; PowerFlow CI + version consistency in check.py [agent: claude-opus-5]

### v0.2.2 — Reference installs (owner) (2026-09-19 — published; reference installs deferred to backlog) (COMPLETE)
**Goal:** Two real projects run one full iteration each through the pack with zero hand-edits of PLAN.md - moved from v0.2.0 on 2026-09-19 because both need the owner: a new project to stamp (name it) and RadEAU's retrofit registered in RadEAU's own plan from docs/audits/RadEAU-2026-09-19.md.
- [x] Publish: create github.com/CynaCons/PowerFlow, push main + v0.2.0, set description/homepage/topics, README install via the GitHub URL (owner request 2026-09-19) [agent: claude-opus-5]

## v0.3 — Lean
> Owner 2026-09-19: "way too complicated... too many constraints... strip the fat, keep the essential." One skill describing it all; powerplan and PowerSpawn usage are the parts that matter.

### v0.3.0 — One skill (current) (ACTIVE)
**Goal:** Replace the 13-skill pack with one `powerflow` skill that describes the whole method section by section, with powerplan usage and PowerSpawn usage as the load-bearing sections (PowerSpawn is about to be enhanced a lot); ~1,900 lines to ~500, always-on tokens divided by ten, a new project starts with a handful of files and a plan.
- [ ] D15 Lean pack recorded as a direction change; D1-D15 folded into one DECISIONS.md log; docs/decisions/ removed; PRD trimmed to one page with a revision status line [agent: claude-opus-5]
- [ ] skills/powerflow/SKILL.md: the whole method section by section - start a project, the plan (powerplan tools, bookends, miniplan each turn), requirements, a slice, close the loop, owner reports, workers (PowerSpawn tools, CLI vs API, dispatch contract, validate yourself, what is coming: persistent agents / ask-coordinator / advisor panel), memories + decisions, release, audit [agent: claude-opus-5]
- [ ] skills/powerflow/scripts: stamp.py (7 templates, stateful protection, plugin detection) + audit.py (lean rules); references/workers.md, release.md, smoke.md; the other 12 skill dirs, srs.py and decide.py deleted [agent: claude-opus-5]
- [ ] templates cut to the essential set (PRD, AGENTS ~40 lines, CLAUDE shim, docs/srs/README tag index without allocator, .mcp.json variants, settings variants, .gitignore); guards + CI example + 17 tests moved to extras/guards/ as opt-in; check-req-ids works without an allocator table [agent: claude-opus-5]
- [ ] PowerFlow itself lean: METHODOLOGY.md, docs/srs/, templates/_index.md, mcp-servers.md removed; README carries the ten rules + install; AGENTS.md short; scripts/check.py reduced to check_plan + versions + extras tests; plugin/package/CHANGELOG 0.3.0 [agent: claude-opus-5]
- [ ] Smoke test: claude plugin validate green and details lists exactly 1 skill; stamp a throwaway (handful of files, plan via powerplan); audit.py on PowerFlow reports 0; reinstall the plugin; push + tag v0.3.0 [agent: claude-opus-5]
- [ ] GitHub Pages site for PowerFlow (owner request 2026-09-19): one static page (the loop, the ten rules, install, links to the skill and the repo), deployed by a pages workflow; Pages enabled on the repo; link handed to the owner [agent: claude-opus-5]

## Backlog
- autosar-101-training: fold embedded close-the-loop guidance (SIL, debugger, CAN/XCP, datasheets, SDK references) into powerflow-verify once the repo is located (D9)
- Bidirectional test ↔ requirement map generator for docs/srs/README.md
- powerflow-audit reports the pack version a project was stamped with
- Owner names the new project; powerflow-init stamps it (interview, stamp, plan through powerplan, PRD conversation, first commit) (deferred from v0.2.2: owner-dependent; resumes after the v0.3.0 lean rewrite with the one-skill pack) [agent: claude-opus-5]
- RadEAU retrofit: register docs/audits/RadEAU-2026-09-19.md as a 'PowerFlow retrofit' iteration in RadEAU's PLAN.md via powerplan; decide D<n> there on the XX-NNN ID scheme (keep or migrate) (deferred from v0.2.2: owner-dependent; resumes after the v0.3.0 lean rewrite with the one-skill pack) [agent: claude-opus-5]
- Run one full iteration in each project using only powerflow-* skills; no hand-edit of either PLAN.md (deferred from v0.2.2: owner-dependent; resumes after the v0.3.0 lean rewrite with the one-skill pack) [agent: claude-opus-5]
- Smoke test: powerflow-audit reports 0 findings on both projects; their guards are green in CI (deferred from v0.2.2: owner-dependent; resumes after the v0.3.0 lean rewrite with the one-skill pack) [agent: claude-opus-5]
