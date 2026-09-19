# Slice brief — template

The brief is what plan mode produces and the owner approves. It is written
for two readers: the owner (who decides) and the next agent (who must be able
to execute from it alone after a context reset). Keep it under two screens;
cite files with `path:line`; quote the owner verbatim.

```markdown
# vX.Y.Z — <title, the outcome in a few words>

## Context

<The owner's request, quoted verbatim, dated.>

<What already exists that this touches — name the machinery by file and
line, and say what it does today. State what is *not* the problem, so the
next reader does not re-investigate it. If a prior attempt exists, say why
it fell short.>

## Outcome

<One paragraph: what the owner will see when this is done. This becomes the
iteration's **Goal:** line.>

## Requirements

<The SRS rows this slice adds or changes — IDs from the allocator, one line
each. New tag? say so. Behaviour with no row yet is not ready to build.>

- SRS-<FEAT>-<NNN> — <shall …>

## Work

<One block per task; each becomes a PLAN checkbox. Order = execution order.>

### <task title>
- Files: <paths this task may change — the worker's allowed paths>
- Done when: <the command and the literal pass signal, or the owner-visible state>
- Notes: <the two or three facts the implementer needs and would otherwise dig for>

## Verification

<What `powerflow-verify` will run for this slice: the unit/e2e commands,
the smoke, which states to look at. Name the test files that will exist.>

## Out of scope

<What was considered and deliberately left out, so it does not creep back in
during implementation. Backlog candidates go to `add_to_backlog`.>
```
