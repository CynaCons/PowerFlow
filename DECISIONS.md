# Decisions

Append-only log, one entry per settled choice. A reversed decision gets a new
number that says what it supersedes; numbers are never reused. Each entry ends
with what would reopen it. (Until D15 these were one file each under
`docs/decisions/`; the fold kept the content, dropped the ceremony.)

## D1 — Requirement IDs are `SRS-<FEAT>-NNN` · 2026-09-18
Five schemes were in use across the author's repos. The tag names the feature
area and is owned by one `docs/srs/SRS-<feature>.md`; numbers are never reused
or renumbered — superseded rows are marked, not deleted. The next number is
`max + 1` in that file (D15 dropped the allocator table). Existing repos are
not renumbered; a migration is that repo's own decision. Reopen if a project
routinely needs several tags per file.

## D2 — PLAN.md header is stale-proof · 2026-09-18
Title, Goal, Philosophy, a rule, then `## Current Status`: "the current
iteration is the last heading not marked COMPLETE". No version number, no
maintained achievements list (powertimelines' grew to 110 lines and drifted).
Metrics are computed by tools, never maintained. Reopen if a project needs a
dashboard — then it is generated under `docs/`, not kept in the plan.

## D3 — Coordinator guidance is on demand, CLAUDE.md is a shim · 2026-09-18
powertimelines loaded a 9 KB coordinator manual into every worker turn. The
worker/coordinator procedure lives in the skill (D15: the workers section of
the one skill); CLAUDE.md says "read AGENTS.md"; AGENTS.md carries only what
every agent needs every turn. Reopen if a harness appears that loads neither.

## D4 — powerplan is registered per project, portably · 2026-09-18
`uvx powerplan-mcp` in the template, `python -m powerplan` where uv is absent,
the PowerSpawn submodule path only when developing those tools. Absolute paths
break on every other machine and are an audit finding. Reopen when uv is
standard on the author's machines.

## D5 — Skills are named `powerflow-*` · 2026-09-18 (owner)
Origin visible in any menu; no collision with the `powerplan` server name.
D15 reduced the set to a single skill named `powerflow`.

## D6 — Skills ship as a personal Claude Code plugin · 2026-09-18
One user-level install serves every project; templates are copied into each
project by the stamp because other harnesses and CI must see them. Public
marketplace publication waits for two reference projects.

## D7 — Migrated skills leave a pointer · 2026-09-18
powerplanner's `powerplan` and `visual-plan` skills became pointer files once
the plugin was installed (commit f13df1d there). PowerGit's release skill stays
— it is project-specific; the generic ritual reads it.

## D8 — Showcase artifact is a PRD switch · 2026-09-18
`showcase: required | optional` in the PRD quality bar. When required, an
iteration closes only with screenshots captured from the running app (never
mocked up). PowerNote's rule, made opt-in.

## D9 — autosar-101-training · 2026-09-18 · OPEN
Not on this machine. The embedded close-the-loop profile (SIL, debugger,
CAN/XCP, datasheets, SDKs) stays a note in the smoke recipes until the repo is
located or the owner summarises it.

## D10 — PRD once per project · 2026-09-18 (owner)
Written at start, iterated until it guides the rest, rewritten only on an
owner-declared change of direction — recorded as a decision first. Routine
change goes to decisions, SRS rows, PLAN tasks.

## D11 — Session bookends · 2026-09-18 (owner)
Every session opens with `show_miniplan` and closes with the status update
through powerplan (`check_plan` green). `show_miniplan` was added to powerplan
0.8.0 for this.

## D12 — Every major turn ends with the miniplan · 2026-09-19 (owner)
"I do a lot of context switching — I need to see what's going on quickly when
I come and check the console." A turn that changed files, ticked tasks, ran a
gate or closed an iteration ends with the raw `show_miniplan` block. Also one
line in the owner's global CLAUDE.md. Reopen if it reads as noise.

## D13 — Guards are Node scripts mirroring powerplan · 2026-09-19
`check-plan.mjs` lints what `check_plan` lints (powerplan stays the authority
and only writer); `check-req-ids` and `check-version` need only Node. D15 made
them opt-in under `extras/guards/`. Reopen if the mirror and `check_plan` ever
disagree on a real plan — then the mirror becomes a wrapper around powerplan.

## D14 — The plugin bundles the powerplan MCP registration · 2026-09-19
The plugin loader scans the root `.mcp.json` and there is no manifest opt-out;
kept as a feature: every Claude Code session on the machine has the single
writer and `show_miniplan`. Stamped projects keep their own `.mcp.json` for
clones without the plugin; the stamp writes `settings.local.json` with the
project copy disabled when the plugin is installed, so it is not loaded twice.
Reopen if the loader gains an opt-out or a public release needs `uvx` bundled.

## D15 — Lean pack: one skill, one page, essentials only · 2026-09-19 (owner)
Owner: "way too complicated… too many constraints… strip the fat, keep the
essential." The 0.2.0 pack had turned every observed habit into a mandatory
mechanism: 13 skills (~3.2k tokens always-on in every session), 14 decision
files, a 290-line handbook, 19 templates, 4 scripts, CI guards by default.
The method is the deck's Part F plus D10–D12: PRD once · PLAN.md via powerplan
with the miniplan first, last and per turn · SRS rows before code · close the
loop before "done" · bugs failing-test-first, owner closes · short AGENTS.md +
memories · workers via PowerSpawn · a release checklist.

Decision: **one skill, `powerflow`**, describing the whole method section by
section, with the powerplan and PowerSpawn sections as the load-bearing ones
(PowerSpawn is about to grow — persistent agents, ask-coordinator, advisor
panel). Two scripts (stamp, audit), three short references (workers, release,
smoke). Seven templates. Guards and their tests move to `extras/guards/`,
opt-in. Decisions become this log; SRS keeps the rule and loses the allocator
machinery. PowerFlow's own PRD is trimmed to a page and this is its direction
change (D10). Reopen if the one skill passes ~300 lines — then split by
*procedure* (something with a script), never by rule.
