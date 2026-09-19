---
name: powerflow-release
description: Cut a release the PowerFlow way — refuse to ship from an open iteration, run the preflight gates and look at the app, bump the single version source and check every derived copy, build with the canonical command, smoke the packaged artifact, tag, confirm CI picked up the tag before dispatching it (never both), write release notes from the closed iterations, verify the live surfaces (registry, store, PyPI, release assets, updater), check the storefront, and tick the release in PLAN.md. Use this whenever the user says "release", "ship", "publish", "cut vX.Y.Z", "tag it", "push to PyPI / the registry / the store", or asks whether something is ready to release. Use it even for "just bump the version" — the bump is step 1 of the ritual, not a standalone edit.
---

# powerflow-release — the ritual, not a push

A release is the fourth movement of an iteration (METHODOLOGY.md §4.4, §8).
It is a ritual because every step in it exists for a shipped mistake: the
iteration left open (no notes, no proof), the version bumped in five files
and forgotten in the sixth, the artifact nobody launched, the tag pushed
twice into the registry, the release that shipped with the selected commit
invisible because nobody looked. The ritual's order is fixed; the commands,
artifact names and storefront facts are the project's — read them from its
AGENTS.md and its `docs/RELEASING.md` if it has one.

Bundled: `references/ritual.md` — the step list with its refusals. Walk it
top to bottom; do not reorder.

## 0. Read the project's release facts

`show_miniplan` — is the iteration closed? Then AGENTS.md → "Commands",
"Packaging & release", the version source (PRD §5), the CI workflow names
(`.github/workflows/`), and any project release guide. If the project keeps
its own release skill or guide (PowerGit, powerplan), that file is the
authority for *facts*; this skill is the authority for *order and refusals*.
Do not invent a package name, a registry namespace or a publish channel — if
the project has not written them down, stop and ask.

## 1. Walk `references/ritual.md`

Six stages: preflight → version → build and smoke the artifact → tag and
publish → verify the live surfaces → storefront and close-out. Each checkbox
is a gate; a red gate ends the release attempt with a report of what is
missing — it does not get skipped "this once". The three refusals that matter
most:

1. **Open iteration** → close it through powerplan first (open tasks move
   forward; never `force`). The release notes are the closed iterations.
2. **Owner-report task awaiting the owner's tick** → not releasable until the
   owner confirms (`powerflow-bug`).
3. **CI already running for the tag** → watch it; do not dispatch a second
   run. If nothing picked up the tag, dispatch once.

## 2. Evidence, not narrative

Every stage produces a line the owner can check: the `check-version` output,
the artifact smoke ("extracted to a clean dir, `/health` reports 0.8.0"), the
run id and its conclusion, the live JSON (`info.version = 0.8.0`), the
registry listing with its status. Curl the surfaces; do not assume a green
workflow means the store updated.

## 3. Learn

A release that hit a new failure mode records it twice: in the project's
release guide (its "failures we have already hit" table) and as a memory
(`powerflow-memory`). Then update the project's release skill/guide if the
order itself needs a step — as powerplan's did after the duplicate dispatch.

## Report

```
Release vX.Y.Z — <project>
  preflight  iteration vX.Y.Z closed <date> · gates green · looked at <n> states
  version    <source> X.Y.Z · check-version OK (<k> derived files)
  artifact   <name> smoked: <what was confirmed>
  tag        vX.Y.Z pushed · release <url>
  ci         run <id> (<push|dispatch>) → success
  live       <PyPI|registry|store|assets>: X.Y.Z <status>
  storefront <ok | edited: …>
  plan       release task ticked · check_plan ok
  learned    <memory / guide row | nothing new>
```

Then the miniplan (D12).

## What not to do

- Do not release from an open iteration or force-close one to release.
- Do not bump a version by hand in a derived file — fix the derivation.
- Do not publish an artifact you did not launch.
- Do not dispatch a workflow without checking whether the tag push already
  started it.
- Do not move or reuse a tag that published anything; ship `+1`.
- Do not edit repo settings "to record them" — check them, edit only drift.
