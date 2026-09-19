# D12 — Turn-end miniplan

Status: Accepted · 2026-09-19 (owner decision)

## Context

Owner: *"at the end of each major turn, I want the agent to show me the
miniplan. This is because I do a lot of context switching — I need to be able
to see what's going on quickly when I come and check the console."* D11 fixed
the session's bookends (plan first, status update last) but said nothing
about what the owner sees between them. A long turn's report is prose; the
owner returning to the console needs state, not narrative. `show_miniplan`
already produces that state in the plan's own format.

## Decision

Every **major turn** — one that changed files, ticked or added tasks, ran a
gate, or closed an iteration — ends with the current miniplan displayed
verbatim in a fenced block, after the report and before any question to the
owner. A quick answer that changed nothing does not need it. The block is the
raw `show_miniplan` output (current iteration, neighbouring headers); no
paraphrase, no trimming of tasks.

## Consequences

- `powerflow-plan` and `powerflow-verify` report shapes end with the miniplan
  block; skills that close through them inherit it.
- Stamped `AGENTS.md` carries the rule under its bookends section so every
  harness sees it, and the owner's global `CLAUDE.md` carries one line so it
  holds in repos not yet stamped.
- The miniplan is displayed even when the plan did not change in the turn —
  the point is the glance, not the diff.
- Reopen if the owner reports the block as noise; the fallback is showing it
  only when the plan changed.
