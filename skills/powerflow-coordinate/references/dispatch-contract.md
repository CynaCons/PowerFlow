# Dispatch contract — what every worker prompt contains

Workers are stateless. The CLI auto-loads the project's AGENTS.md (Codex,
Copilot, Cursor) or CLAUDE.md → AGENTS.md (Claude); everything else must be
**pasted, not referenced**. A prompt missing any block below produces either
a worker that re-explores for twenty minutes or one that "finishes" without
proof.

```markdown
## Task: <one line — the deliverable, not the activity>

PLAN.md task: vX.Y.Z / <index> — "<task text verbatim>"
SRS rows: <SRS-X-004..006 — pasted, one line each>

### Goal and gate
<The outcome in two sentences.> Done when `<gate command>` prints
`<literal pass signal>` (and `<artifact path>` exists with a fresh mtime,
when one is expected).

### Context
- <path:line — what it does today, in one line each; the findings already
  recorded in docs/agents/context/<slice>.md and the memories that apply>
- <the data model / the contract the change must respect>

### Constraints
- Change only: <allowed paths>. Do not touch: <paths>.
- Do not edit PLAN.md, PRD.md, docs/srs/*, docs/decisions/* — the coordinator owns them.
- Do not commit, push or rewrite history.
- Keep the diff small; do not reformat files you are not changing.
- <project-specific rules pasted from AGENTS.md that matter here — build
  flags, forbidden dependencies, theme tokens>

### Verify before you report
Run `<typecheck>`, `<unit>`, and `<gate command>` once each. If red, read the
first error, fix, run once. Do not loop.

### Report back (exact shape)
- Changed: <paths>
- Gate: `<command>` → <exit code, the pass signal or the first error>
- Open: <what you could not do and why>
- Memories: <docs/agents/memories/*.md you added or corrected, or "none">
- Unknowns: <anything the coordinator must decide>
```

## Choosing the provider

| Need | Spawn | Why |
|---|---|---|
| Files changed, commands run | `spawn_claude` / `spawn_codex` / `spawn_copilot` / `spawn_grok force=true` | CLI agents edit and execute; they auto-load AGENTS.md |
| A second opinion, a review, a draft | `spawn_gemini` / `spawn_mistral` / `spawn_grok_api` | API agents return text only; the coordinator applies it |
| Claude rate-limited | Codex / Copilot / Grok | separate quotas — the load-distribution value of PowerSpawn |

`timeout`: default 600 s; long builds 900 s; a worker that times out is
recorded in IAC.md as failed — re-dispatch with the failure context and a
smaller scope, not the same prompt.

## Batch sizing (audits and sweeps)

Read-only rounds first (findings, no edits), then edit rounds grouped by
type. 4–5 files per worker, 3–4 workers in parallel, each worker verifies
its own batch, coordinator commits after each round.
