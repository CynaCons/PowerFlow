# PowerFlow — Product Requirements

**One-liner:** The way I build software with agents — PRD once, PLAN.md through
powerplan, SRS rows before code, close the loop before "done", workers through
PowerSpawn — as **one skill** that describes it all, so no project re-specifies it.

**Home:** [github.com/CynaCons/PowerFlow](https://github.com/CynaCons/PowerFlow) ·
**Status:** PRD revision 2026-09-19 — D15 *Lean pack* (direction change: 13
skills → 1; see [DECISIONS.md](DECISIONS.md)). Plan: [PLAN.md](PLAN.md).
Origin: [docs/proposal-2026-09-18.html](docs/proposal-2026-09-18.html).

## 1. Problem
Eleven repos by one author run the same loop and each re-decided how to encode
it (five ID schemes, three plan headers, four powerplan registrations). The
first attempt to fix that (0.2.0) over-corrected: every observed habit became a
mandatory mechanism — 13 skills, 14 decision files, a 290-line handbook, CI
guards by default, ~3.2k tokens of skill descriptions in every session.

## 2. Users
The owner, who starts projects, steers slices, closes owner reports and ships;
the coordinator session that operates the plan and the workers; the workers
(Claude, Codex, Copilot, Grok, …) that receive a brief and return evidence.

## 3. Principles
1. **One skill, one page.** The method is `skills/powerflow/SKILL.md`; project
   files link to it. If it passes ~300 lines, split by *procedure*, never by rule.
2. **powerplan and PowerSpawn are the load-bearing parts.** Everything else is
   rules around them; the PowerSpawn section evolves with the tool.
3. **PLAN.md first and last, miniplan every major turn** (D11, D12).
4. **PRD once** (D10). Routine change is a decision, an SRS row or a task.
5. **Evidence or it didn't happen.** Ticks carry proof; owner reports are closed
   by the owner.
6. **Lean by default, rigor on demand.** Guards, CI, per-file decisions and
   showcase artifacts are opt-in; a side project starts with five files.

## 4. Shape
```
skills/powerflow/   SKILL.md (the method) · scripts/stamp.py · scripts/audit.py · references/{workers,release,smoke}.md
templates/          PRD · AGENTS · CLAUDE shim · docs/srs/README · .mcp.json (+python variant) · .claude/settings (+plugin variant) · .gitignore
extras/guards/      check-plan · check-req-ids · check-version · ci.yml · 18 tests   (opt-in)
.claude-plugin/     plugin.json (version source) · marketplace.json   — the repo is its own marketplace
```
**In scope:** start a project, operate the plan, requirements, slices, verify,
owner reports, workers, memories/decisions, release, audit — as sections of the
one skill. **Out:** a web UI; enforcement beyond opt-in guards; per-harness
forks of the method; a training deck (that is `training-ai-software-engineering-101`).

## 5. Stack
Markdown + Python 3.10 (two scripts) + Node 22 (opt-in guards and their tests).
Version source `.claude-plugin/plugin.json`; `package.json` and the CHANGELOG top
section must match (`scripts/check.py`). Depends on powerplan ≥ 0.8.0
(`show_miniplan`) and PowerSpawn ≥ 1.8.

## 6. Quality bar
`claude plugin validate .` green; `claude plugin details` lists exactly one
skill; `scripts/check.py` green (plan, versions, guard tests); `audit.py` on
PowerFlow reports nothing above low; a stamped throwaway has a plan created through powerplan
and no leftover placeholder. `showcase: optional`.

## 7. Non-goals
Public marketplace listing before two reference projects; an npm package for
the guards; a second implementation of powerplan's plan model.

## 8. Decisions
[DECISIONS.md](DECISIONS.md), D1–D15. Open: D9 (autosar-101-training).

## 9. Success criteria
Two real projects run one full iteration each through the pack with zero
hand-edits of PLAN.md; a new session reaches "what to do now" from
`show_miniplan` alone; the owner never re-explains the procedure in chat.
