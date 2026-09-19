---
name: powerflow-bug
description: Handle an owner-reported defect the PowerFlow way — register the report quoting the owner verbatim, write a failing test that reproduces the symptom on the platform it was reported from before touching the fix, fix until that test passes, then mark the task "fixed <sha>, awaiting owner verification" and leave it open for the owner to tick. Use this whenever the user reports something broken, wrong, missing, slow or ugly in their own words ("commits disappear when selected", "feels laggy", "the button does nothing", "still not fixed"), pastes an error they hit, or says "bug", "regression", "it broke". Use it even when the cause looks obvious — the test is the point, not the diagnosis.
---

# powerflow-bug — the symptom is the spec

An owner report is the most valuable requirement a project gets: a real
person saw a real failure. The failure mode this skill exists to prevent is
concrete — in PowerGit, "commits disappear when selected" was rewritten by
the agent into "author-highlight class absent" and *that* diagnosis was tested
for three iterations (v0.12.1 → v0.13.13) while the selected commit's graph
node stayed hidden under the row background. Nobody looked at the window. The
test asserted the agent's theory, not the owner's sentence.

So: the owner's sentence is the requirement, the failing test is its
verification, and only the owner closes it (METHODOLOGY.md §7).

## 1. Register — before investigating

`show_miniplan`, then `add_tasks` on the current iteration (or a new
`vX.Y.Z — Owner feedback <date>` iteration when several arrive together):

```
Owner report <date>: "<the sentence, verbatim>" [<platform> — <version/build>]
```

Verbatim means verbatim: their typo, their vagueness. Do not translate
"feels laggy" into "render latency > 100 ms" in the task text — that
translation is your hypothesis and belongs in the test's name, not in the
requirement.

If the behaviour the owner expected is not an SRS row yet, it becomes one now
(`powerflow-srs`): the report revealed a requirement that was never written
down.

## 2. Reproduce with a failing test — first commit

Write the test that fails today and would have caught this, on the platform
the owner was on (Linux AppImage reports get a Linux test; the Windows dev
box passing proves nothing). Assert **what the owner sees**:

- Where layers compose and the DOM cannot see the result (a canvas under
  rows, a dialog over a grid, zoomed content), sample composited pixels —
  screenshot a clip, decode it in the test, count colours. A class or
  computed-style assertion on such a surface is not proof.
- "Feels laggy" → measure in-page timing (`performance.now()` around the
  interaction) and assert a number; put the number in the SRS row.
- "Does nothing" → assert the state after the action, not that a handler
  was called.

Quote the owner's sentence in the test's description so the mapping is
permanent. Commit: `test: reproduce "<owner sentence>" (<platform>)`. Red is
the expected result of this commit.

## 3. Fix until green — once

Fix, run that test once, run the project's suite once (`powerflow-verify`
rules: read the first error, no rerun loops). Keep the diff small; a bug fix
that reformats the file hides the fix. If the fix changes behaviour an SRS
row describes, update the row in the same change.

## 4. Hand it back — do not tick

```
update_task version=<v> task="Owner report …" text="<same text> — fixed <sha>, awaiting owner verification"
```

The box stays open. The iteration stays open. When the owner confirms — in
their words, ideally on their platform — *they* tick it (or tell you to,
which you record in the task text: "owner confirmed <date>"). Ticking it
yourself because the test is green is exactly the failure mode from the
opening paragraph.

Write a memory (`powerflow-memory`) if the cause was a landmine the next
agent could step on again.

## Report

```
Owner report: "<verbatim>" [<platform>]
  test:   <path>::<name> — red on <sha_before>, green on <sha_fix>
  fix:    <sha_fix> — <one line: what changed>
  SRS:    <row added/updated | none needed>
  status: awaiting owner verification (task left open)
```

Then the miniplan (D12).

## What not to do

- Do not diagnose first and test the diagnosis.
- Do not fix without a failing test "because it's a one-liner" — the
  one-liner regresses next month.
- Do not test on a platform other than the reported one and call it
  reproduced.
- Do not tick the task. Do not close the iteration around it.
- Do not rewrite the owner's words in the task or the test.
