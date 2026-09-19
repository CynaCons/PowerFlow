# Changelog

Release notes are the closed iterations of [PLAN.md](PLAN.md), one line each.
The version is `.claude-plugin/plugin.json`; `package.json` and this file's top
section must match (`scripts/check.py`).

## 0.2.0 — 2026-09-19

First installable pack: the method as a handbook, templates and thirteen
`powerflow-*` skills, installed at user scope as a Claude Code plugin.

- **v0.1.0 — Project initiation** (2026-09-18): PRD, PLAN.md through powerplan,
  METHODOLOGY.md, decisions D1–D11, AGENTS.md + CLAUDE.md shim, the archived
  proposal, `scripts/check.py`; `show_miniplan` defined and shipped in
  powerplan 0.8.0.
- **v0.1.1 — Templates + powerflow-init** (2026-09-19): 19 templates with
  D1–D11 applied; three Node guards (`check-plan`, `check-req-ids`,
  `check-version`); `powerflow-init` with a deterministic stamp and the exact
  first-iteration powerplan calls.
- **v0.1.2 — Core loop skills** (2026-09-19): `plan`, `slice`, `srs` (with
  `srs.py` new/allocate), `verify` (smoke recipes per platform), `status`
  (the ASCII gantt adopted from powerplanner); PowerFlow's own SRS
  (SRS-SKILL-001..013).
- **v0.1.3 — Discipline skills** (2026-09-19): `bug`, `decide` (with
  `decide.py`), `memory`, `release` (the ritual, incl. check-CI-before-dispatch),
  `prd`; D12 turn-end miniplan; D13 guards in Node.
- **v0.1.4 — Orchestration + audit** (2026-09-19): `coordinate` (dispatch
  contract, commit-before-tick, stop conditions), `audit` (with `audit.py`,
  reproduces the proposal's ten drift points on RadEAU, powertimelines and
  PowerGit).
- **v0.2.0 — Plugin packaging** (2026-09-19): `.claude-plugin/` manifests,
  user-level install (13 skills, ~3.2k tokens always-on); D14 the plugin
  bundles the powerplan registration and the stamp disables the project copy
  locally; D7 pointers in powerplanner; RadEAU audit fix list.
- **v0.2.1 — Guards package** (2026-09-19): `--root` on the guards, 17 guard
  tests (`npm test`), `--force` never overwrites stateful files, PowerFlow CI,
  version consistency in `check.py`.

Owner-dependent: v0.2.2 — two reference projects run one full iteration each
through the pack.
