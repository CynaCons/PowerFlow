# PowerFlow — The Method

How software is built here, with agents. This is the canonical text: project
files (AGENTS.md, PRD.md) link to it and do not restate it. Each section names
the `powerflow-*` skill that executes it. Decisions behind the conventions are
in [docs/decisions/](docs/decisions/README.md).

---

## 1. The loop

```
PRD.md ──▶ docs/decisions/D-n ──▶ docs/srs/SRS-<feature>.md ──▶ PLAN.md
 (once)      (before building)     (one shall per row, stable IDs)  (iterations)
                                                                        │
              ┌─────────────────────────────────────────────────────────┘
              ▼
   each iteration:  1 plan/docs ─▶ 2 implement ─▶ 3 verify ─▶ 4 release
              ▲                                                    │
              └──── new idea → new task · owner report → failing test first ◀┘

   agents:  coordinator owns the documents, dispatches, verifies
            workers own product code, write memories, report with evidence
   tools:   powerplan (single writer of PLAN.md) · PowerSpawn (workers, IAC.md)
            CI guards (req-IDs, plan structure, version) · e2e on the real binary
```

Everything below is a rule about one arrow of this picture.

## 2. Documents

### 2.1 PRD.md — once per project

The PRD says what the product is, for whom, on what stack, under which
principles and quality bar, and under which methodology constraints. It ends
with a table of decisions to record. It is written when the project starts,
iterated with the agent until it can guide the rest, and rewritten **only on a
major change of direction** declared by the owner. Routine change never
touches it: a constraint becomes a decision, a behaviour becomes an SRS row, a
piece of work becomes a PLAN task. (D10 · `powerflow-init`, `powerflow-prd`)

### 2.2 docs/decisions/ — before the subsystem

One file per decision, `D<n>-slug.md`: Status · Context · Decision ·
Consequences. The consequences name the gate that would reopen it (a CI
threshold, a measured failure). Written **before** the affected part is built;
enumerated in the PRD with a default recommendation. IDs never reused.
(`powerflow-decide`)

### 2.3 docs/srs/ — one file per feature area

`docs/srs/SRS-<feature>.md` opens with a requirements table:

| ID | Requirement | Rationale | Verification | Trace |
|---|---|---|---|---|

- **ID** `SRS-<FEAT>-NNN`, stable forever; the tag is owned by exactly one
  file; `docs/srs/README.md` is the single allocator and CI fails on
  duplicates (D1).
- **Requirement** one testable *shall*; no "fast" or "nice" without a number;
  implementation-neutral unless platform-specific (`[linux]`, `[native]`).
- **Verification** `Test` (preferred), `Analysis`, `Review`, `Demo`.
- **Trace** design §, implementation path, test path — filled as code lands.
  A row with no verification is not done. Status is implied by Trace;
  priority is implied by PLAN.md.

A named feature does not ship without an SRS file. New requirements are
written **before** implementation and land **in the same change** as the code
that satisfies them. The most valuable rows are interaction semantics — which
control wins when states disagree. (`powerflow-srs`)

### 2.4 PLAN.md — the operational backbone

One PLAN.md at the repo root, operated **only** through powerplan (D2, D4).

```
# <Project> — Implementation Plan
**Goal:** …   **Philosophy:** …   **Verify:** <one proof command>   **Stack:** …
---
## Current Status
The current iteration is the last heading below that is not marked COMPLETE.
---
## vX.Y — Major title
> one-line description
### vX.Y.Z — Iteration title
**Goal:** one sentence
- [ ] task … (checkboxes only)
- [ ] Smoke test: <the proof that the iteration works>
## Backlog
- …
```

Rules: checkboxes only — no "files modified", no "impact", no summaries;
exactly one active iteration; append-only (closed iterations are history,
never rewritten; incomplete tasks move forward); Backlog is always the last
section; every iteration ends with a smoke task; the header names no version
so it cannot go stale; never clear the plan — compress if needed, but agents
keep project context from it without reverse-engineering git.
(`powerflow-plan`)

## 3. Sessions: PLAN.md first and last

Every working session has the same two bookends (D11):

1. **First.** `show_miniplan` — the current iteration as raw PLAN.md text with
   its major header and the neighbouring iteration headers. Read it before
   any other file. It answers "what are we doing and where does it sit".
2. **Last.** Update the plan through powerplan: tick tasks **with evidence**
   (test output, commit, artifact path), add discovered work as tasks or
   backlog items, close the iteration only when every task has proof and
   owner-report tasks carry the owner's tick, run `check_plan`. Then report.

The conversation is not state. If the context compacts, the plan is where
work resumes. A session that ends without the status update did not happen.

## 4. Iterations: the four movements

Each `vX.Y.Z` walks the same four movements, in order (RadEAU PRD §9.1):

1. **Plan / docs.** Start the slice in plan mode: explore, ask the owner what
   the template cannot answer, write the brief. On approval, turn the brief
   into SRS rows and PLAN tasks — each task with its allowed paths and its
   definition of done — **before the first edit**. (`powerflow-slice`)
2. **Implement.** Scoped diffs; pure modules for every non-obvious algorithm;
   `data-testid` on every interactive element; spec and plan updated in the
   same change.
3. **Verify — close the loop.** §6. (`powerflow-verify`)
4. **Release** when the iteration is a shippable unit. §8. (`powerflow-release`)

Baby steps in the right direction: each iteration should work correctly and
look right on its own. New ideas become new tasks or iterations, never
untracked work.

## 5. Agents

### 5.1 Roles and ownership

| Owns | Coordinator | Worker |
|---|---|---|
| PLAN.md (via powerplan), PRD.md, docs/srs, docs/decisions, AGENTS.md | yes | never, unless the task says so |
| Product code | may | yes, scoped to the task |
| docs/agents/memories, context | yes | yes |
| git commit / push / history | yes | never |
| Verifying a worker's claim | yes — runs the gate itself | reports evidence |

The coordinator is the session the owner talks to. Workers are spawned
through PowerSpawn (Claude, Codex, Copilot, Grok) and start with zero context;
CLIs auto-load AGENTS.md / CLAUDE.md, everything else is in the prompt.
(D3 · `powerflow-coordinate`)

### 5.2 Briefing files

- **AGENTS.md** — the one shared briefing, loaded every turn: project shape,
  commands, how we verify, who owns which files, engineering rules, report
  format, pointers. Short and project-specific; links here for the method.
- **CLAUDE.md** — a shim: "read AGENTS.md". Nothing else.
- **docs/agents/memories/<topic>.md** — durable facts: landmines, mappings,
  measurements, decisions easy to violate. One heading per fact, dated when it
  may rot, corrected in place. Never task status, secrets or SRS copies.
- **docs/agents/context/<feature>.md** — a worker briefing for one feature;
  deleted once absorbed into code comments and SRS. (`powerflow-memory`)

### 5.3 Dispatch contract

Every worker prompt contains, pasted not referenced: the **goal** and its gate
(command + literal pass signal), the **context** (files, model, findings
already recorded), the **constraints** (allowed paths, what not to touch),
the **definition of done**, and the **report format** (what changed, how it
was verified, what is open, which memories were written). Serial dispatch by
default; parallel only when allowed paths are provably disjoint. The
coordinator validates against the gate itself — never on the worker's word.

## 6. Closing the loop

The agent must be able to see its own work; observability is an architecture
requirement, not a nicety. For web and desktop products:

- Tests drive the **real built binary** (CDP / remote-debugging port), never a
  mocked backend. Selection only on stable `data-testid`; semantic waits; raw
  sleeps banned. Test hooks behind a diagnostics flag are a public API.
- Numbered E2E files `NN-topic.spec.ts`, numbers allocated from the SRS index;
  each names the requirement IDs it covers.
- **Run e2e once.** If red: read the first error, fix, run once. No rerun
  loops "to be sure". `retries: 0`, first failure stops.
- **Screenshots are opt-in.** DevTools captures re-enter the context and have
  dominated whole sessions; pixel-diff suites and headed demos run only when
  the owner asks. Where layers compose and the DOM cannot see the result,
  sample composited pixels in a test.
- **Smoke before reporting.** The app launches with no console errors
  (`npm run dev` / `npm run tauri dev` / the project's canonical command).
  Build passing ≠ feature working.
- **Look at it** before closing UI work: one capture per state, checked
  against the project's visual walkthrough.
- Owner-facing evidence goes in the report as lines (command, exit code,
  numbers), and when the PRD says `showcase: required`, as a published
  artifact captured from the running app (D8).

Embedded targets: SIL or emulation, debugger interfaces, bus read/write
(CAN, XCP), instruments the agent can query, datasheets and MCU description
files as reference — the loop closes by design or it does not close (D9,
pending).

## 7. Owner reports

An owner report is closed by the owner. When the owner reports a defect:

1. Register the task quoting the owner's sentence verbatim.
2. The first commit is a **failing test that reproduces the symptom** on the
   platform it was reported from, asserting what the owner sees — pixels where
   layers compose, in-page timing for "feels laggy". Do not rewrite the report
   into a diagnosis and test the diagnosis.
3. Fix. Then update the task text to `fixed <sha>, awaiting owner verification`
   and **leave the box open**. The iteration stays open until the owner ticks.

(`powerflow-bug`)

## 8. Release ritual

1. Close the iteration in PLAN.md first — the plan is the changelog source.
2. Preflight: gates green, visual subset for what changed, look at it, working
   tree clean, no open owner-report task without an owner tick.
3. Bump the **single version source**; everything else derives; a check script
   fails on drift.
4. Build with the canonical command only.
5. Smoke the packaged artifact from a clean directory.
6. Tag → CI builds and attaches artifacts (dispatch the workflow explicitly if
   an agent's push does not trigger it).
7. Release notes from the iterations closed since the last tag.
8. Storefront check (description, homepage, topics); showcase refresh if the
   project has one.
9. Tick the release task in PLAN.md through powerplan.

Conventional commits: `feat(scope)`, `fix`, `perf`, `docs(spec)`,
`plan: close vX.Y.Z`, `release: vX.Y.Z`. (`powerflow-release`)

## 9. Determinism

Everything that can be done by a program is done by a program (PowerSpawn
DESIGN §2.1). Agents reason; they do not bookkeep.

| Done by a program | Done by an agent |
|---|---|
| PLAN.md writes (powerplan) | deciding what the next task is |
| IAC.md logging of spawns (PowerSpawn) | writing the prompt |
| Duplicate-ID, plan-structure, version-derivation guards (CI) | writing the requirement |
| Test runs, smoke launches, artifact checks | reading the first error |

The MCP cannot block a raw edit; enforcement is the single-writer rule in
AGENTS.md, the CI guards, and the owner's judgment of evidence.

## 10. Conventions

| Thing | Convention |
|---|---|
| Requirement ID | `SRS-<FEAT>-NNN` (D1) |
| SRS file | `docs/srs/SRS-<feature>.md`; index `docs/srs/README.md` |
| Decision | `docs/decisions/D<n>-slug.md` |
| Memory | `docs/agents/memories/<topic>.md`; context `docs/agents/context/<feature>.md` |
| Plan sections | `## vX.Y — Title` · `### vX.Y.Z — Title` · `**Goal:**` · `- [ ]` · `## Backlog` |
| Iteration closure | last task is `Smoke test: …`; `(COMPLETE)` stamped by `close_iteration` |
| Task attribution | optional `[agent: <id>]` tag, written by powerplan |
| E2E file | `NN-topic.spec.ts` |
| Commit | conventional prefix; version in scope for release-bound work |
| MCP servers | `.mcp.json` at root: `powerplan` (+ `powerspawn` when workers are used); enabled in `.claude/settings.local.json` |
| Skills | `powerflow-<movement>` from the `powerflow` plugin; project skills live in `.claude/skills/` |

## 11. Quick reference

```
start a project      powerflow-init      →  PRD interview, templates, create_plan, v0.1.0, smoke, commit
record a decision    powerflow-decide    →  docs/decisions/D<n>, README, PRD table
spec a feature       powerflow-srs       →  SRS rows + IDs + PLAN task, duplicate check
start a slice        powerflow-slice     →  plan-mode brief → SRS rows + tasks before code
operate the plan     powerflow-plan      →  open / tick with evidence / close / check_plan
close the loop       powerflow-verify    →  typecheck+unit, e2e once, smoke, evidence lines
owner reported a bug powerflow-bug       →  failing test quoting the owner → fix → awaiting tick
ship                 powerflow-release   →  the ritual above
learned something    powerflow-memory    →  one fact per heading
run workers          powerflow-coordinate→  miniplan → dispatch contract → verify → tick
where are we         powerflow-status    →  ASCII gantt vs git
does this repo drift powerflow-audit     →  findings as PLAN tasks
```

Every session: **miniplan first, status update last.**
