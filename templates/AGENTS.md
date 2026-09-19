<!-- placeholders: project, one_liner, stack, dev_command, smoke_command, test_command, typecheck_command, e2e_command, verify_command -->
# Agent Instructions

Shared briefing for every coding agent on **{{project}}**. Codex, Copilot and
Cursor load `AGENTS.md`; Claude loads `CLAUDE.md`, which points here. The
method is [PowerFlow METHODOLOGY.md](https://github.com/CynaCons/PowerFlow/blob/main/METHODOLOGY.md);
this file says only how it applies to this repo. Read [PRD.md](PRD.md) before
inventing product behaviour.

{{one_liner}}

## Project shape

```
PRD.md · PLAN.md        product requirements · operational plan (powerplan is the only writer)
docs/srs/               requirements, one SRS-<feature>.md per feature area; README.md allocates IDs
docs/decisions/         D<n> decision records
docs/agents/            memories and context (living)
scripts/                check-plan · check-req-ids · check-version (CI guards)
<!-- add the source tree: one line per top-level directory, what lives there -->
```

## Commands

```bash
{{dev_command}}          # dev
{{typecheck_command}}    # typecheck
{{test_command}}         # unit tests
{{e2e_command}}          # e2e (real binary; run once, fix, run once)
{{smoke_command}}        # smoke: launches with zero console errors
node scripts/check-plan.mjs && node scripts/check-req-ids.mjs && node scripts/check-version.mjs   # guards
```

## How we verify

Proof is what the owner would see, asserted by a test, with the command and
its output in the report. Verify command: `{{verify_command}}`.

- Run the e2e suite **once**. If it is red, read the first error, fix, run once.
- Screenshots are opt-in: no DevTools captures for routine debugging (they
  re-enter the context and dominate the token budget); pixel diffs only when
  the owner asks.
- Smoke before reporting: `{{smoke_command}}` launches without a crash or
  console error. Build passing ≠ feature working.
- Selection only on stable `data-testid`; semantic waits; no raw sleeps.

## Session bookends

Open with `powerplan show_miniplan`. Close with the status update through
powerplan (tasks ticked with evidence, discovered work added, `check_plan`
green). The conversation is not state; the plan is.

## Who owns which files

| File | Owner |
|---|---|
| `PLAN.md` | Coordinator via powerplan — never hand-edited |
| `PRD.md`, `docs/srs/*`, `docs/decisions/*` | Coordinator, or a task that says so |
| `AGENTS.md`, `CLAUDE.md` | Coordinator; workers may append a memory under `docs/agents/` |
| Product code | Workers, scoped to the task |

Workers must not edit the plan, PRD or SRS unless the task says so, and never
commit, push or rewrite history.

## Engineering rules

- Spec and plan land in the same change as the code. A named feature does
  not ship without an SRS file; a requirement row is not verified without a
  test path.
- Owner reports are symptom-first: the first commit is a failing test quoting
  the owner's sentence on the reported platform. Owner-report tasks are ticked
  by the owner, not by an agent (`fixed <sha>, awaiting owner verification`).
- Pure modules for every non-obvious algorithm, unit-tested without launching
  the app.
- Keep diffs small; do not reformat files you are not changing.
<!-- add the product-specific rules: layering, forbidden dependencies, theme tokens, licences -->

## Memories

Read `docs/agents/README.md` and any memory that matches the task before
starting. Write one when you learn something durable (one fact per heading,
dated if it may rot); correct wrong ones in place.

## Reporting

What changed (paths), how it was verified (commands, exit codes, numbers),
what is still open, which memories were added or corrected.
