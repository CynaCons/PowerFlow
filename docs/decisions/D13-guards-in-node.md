# D13 — Guards are Node scripts mirroring powerplan

Status: Accepted · 2026-09-19

## Context

Stamped projects need CI guards for the plan structure (D2), requirement IDs
(D1) and the single version source (METHODOLOGY.md §8). powerplan already
implements the plan lint (`check_plan`) in Python, and RadEAU/PowerGit ship
their guards as `.mjs` files (`check-req-ids.mjs`, `check-version.mjs`,
`plan-normalize.mjs --dry`). Alternatives: (a) run powerplan in CI
(`pip install powerplan-mcp` + a Python entry — pulls the MCP SDK into every
CI job, and PowerFlow's own projects are mostly Node); (b) Node scripts that
re-implement the invariants — a second implementation of the plan rules, but
zero dependencies on every runner the projects already use; (c) a published
npm package — one more release channel before the pack has proven itself.

## Decision

The three guards are **vendored Node scripts** (`templates/scripts/*.mjs`,
copied by `powerflow-init`), needing only Node 22. `check-plan.mjs` is a
**lint mirror** of powerplan's `check_plan` plus PowerFlow's format rules
(checkboxes-only, stale-proof header); powerplan remains the authority and
the only writer. PowerGit's `plan-normalize.mjs` is not carried forward — it
was a one-off restructure, and a CI guard lints, it does not rewrite. An npm
package is deferred until two reference projects run on the pack (D6).

## Consequences

- Every stamped CI runs the guards in a job with no toolchain beyond Node;
  PowerFlow's own `scripts/check.py` calls the same `check-req-ids.mjs`.
- Any new invariant lands in **both** `powerplan check_plan` and
  `check-plan.mjs` in the same change; `v0.2.1` adds tests for the scripts
  so the mirror is checked against fixtures, not assumed.
- Reopen if the two implementations disagree on a real plan (a guard red
  where `check_plan` is green, or the reverse) — then the mirror becomes a
  thin wrapper that runs powerplan, and CI installs it.
