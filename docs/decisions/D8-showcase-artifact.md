# D8 — Showcase artifact

Status: Accepted · 2026-09-18

## Context

PowerNote requires a published artifact with real, Playwright-captured
screenshots for every iteration ("a written summary alone is not delivery");
no other repo does. It is a strong closure proof for visual products and pure
overhead for a CLI or an MCP server.

## Decision

The PRD template's quality-bar section carries a switch
`showcase: required | optional` (default `optional`). `powerflow-verify`
reads it: when `required`, the iteration's smoke task is not ticked until the
artifact is published from the running app, never mocked up.

## Consequences

- Visual products opt in at PRD time; the rule is then enforced by the skill,
  not remembered.
- Capture scripts follow PowerNote's gotchas: script inside the repo,
  element-clipped shots, deleted after use.
