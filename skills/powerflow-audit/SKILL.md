---
name: powerflow-audit
description: Measure how far a repository has drifted from the PowerFlow pack — missing PRD/PLAN/AGENTS, CLAUDE.md not a shim, plan header without the stale-proof Current Status, achievements lists, prose bullets inside iterations, SRS location and ID scheme and table columns off canon, no allocator, decisions or memories missing, powerplan unregistered or registered by absolute path, guards absent from CI, unnumbered spec files — and turn the findings into PLAN tasks the project can work through. Use this when the user says "audit", "does this repo follow the method", "retrofit PowerFlow onto X", "what's drifted", when powerflow-init meets a repo that already has a PLAN.md, or before claiming a project "runs on the pack". Also use it on PowerFlow itself after changing a template or a decision.
---

# powerflow-audit — drift, measured

The pack exists because eleven repos by one author re-decided the same
conventions (PRD §1). An audit is how a repo learns which of its choices are
now decisions it can adopt, and how the pack learns whether a decision is
being followed. The script does the measuring; you do two judgments: which
findings are worth a task in *this* repo, and whether a finding is really a
pack bug.

Bundled: `scripts/audit.py` — read-only; findings grouped by area with the
canonical fix; `--tasks` emits PLAN task lines; `--json` for tooling.

## 1. Run it

```bash
python <skill>/scripts/audit.py --root <repo>
```

Read every finding with its fix. Severities: **high** = a rule the method
cannot work without (no plan, no powerplan, duplicate iterations); **medium**
= a decision D1–D13 not applied; **low** = hygiene the guards would catch
once installed. `pack:` at the top says whether and when `powerflow-init`
stamped the repo (`.powerflow/init.json`).

## 2. Judge, per finding

- **Adopt** — most medium/low items: the fix is a stamp, a header line, a
  README, an alias in CI. These become tasks.
- **Decide instead** — a scheme change with history (RadEAU's `VU-001` IDs,
  powertimelines' `CC-REQ-*`): renumbering a live SRS corpus is a project
  decision, not a lint fix. The task is "record D<n>: keep `XX-NNN` / migrate
  to `SRS-<FEAT>-NNN`", and the audit finding is closed by the decision either
  way (D1 allows it).
- **Pack bug** — the repo does the right thing under another name and the
  script did not recognise it (a guard alias, a legitimate layout). Fix the
  script in PowerFlow, add a memory, re-run; do not create a task in the
  repo for the pack's blind spot.

## 3. Register the fix list

In the audited repo, through powerplan (`powerflow-plan`): a new iteration
`vX.Y.Z — PowerFlow retrofit` with the Goal naming the audit date and count,
tasks from `audit.py --tasks` after your judgment pass, the last task
`Smoke test: audit.py reports 0 findings; guards green`. For a repo without
powerplan registered, that registration is the first task and is done by
hand exactly once (the bootstrap exception).

Order the tasks so the guards land early: once `check-plan`, `check-req-ids`
and `check-version` run in CI, the rest of the retrofit cannot regress.

## 4. Re-audit to close

The retrofit iteration closes when `audit.py` prints `findings: 0` and the
guards are green in CI. Record any scheme the repo kept by decision in its
AGENTS.md so future audits read it as intended, not as drift.

## Report

```
audit <repo> — <n> findings (high h, medium m, low l) · stamped: <version|no>
  adopt:   <k> → tasks in vX.Y.Z
  decide:  <list — the decisions the repo must record>
  pack:    <false positives fixed in audit.py, or none>
next: <first task>
```

Then the miniplan of the audited repo (D12) when its plan changed.

## What not to do

- Do not "fix" a live SRS numbering scheme as a lint item — that is a
  decision with a migration cost.
- Do not hand-edit the audited repo's PLAN.md to add the tasks.
- Do not treat every finding as equal; a repo with a working plan and a
  missing README index is not in the same state as one with two active
  iterations.
- Do not run the audit and stop — a finding list without registered tasks
  is a report nobody works through.
