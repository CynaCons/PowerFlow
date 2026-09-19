---
name: powerflow-status
description: Show where the project stands as an ASCII gantt of the current milestone's iterations — done, active, next, later, unowned — with a "now" line, cross-checked against git so the chart never claims more than the commits do, followed by a short detail per remaining iteration and the top risks. Use this when the user asks "where are we", "what's next", "status", "show me the plan", "powerplan", "gantt", "roadmap", after closing an iteration, or at the start of a session when the owner wants the big picture rather than the current iteration alone (that one is show_miniplan). Offer the interactive board variant when they say "visual", "board" or "roadmap page".
---

# powerflow-status — the plan as one picture

Adopted from the powerplanner `powerplan` skill (D7): one terminal-friendly
picture of the current milestone, a "now" line marking exactly where work
stands, then a few sentences per remaining iteration. The chart is
**ordinal, not calendar** — horizontal position means sequence, bar width
roughly means size — unless the plan actually carries dates. The plan file is
the source of truth; the chart is a view of it.

## Steps

1. **Read through powerplan, not the file.** `show_plan` for the index and
   progress, `list_iterations filter=open` for what remains, `get_iteration`
   for any you need to describe. `show_miniplan` if the current one matters
   in detail. Do not `Read PLAN.md` whole — it is the largest file in most of
   these repos.
2. **Cross-check against reality.** `git log --oneline -30`. A commit that
   names a task or iteration still open in the plan means the plan is stale:
   tick it through `complete_task` (never a hand edit — `powerflow-plan`) and
   lead the response with the correction. Never draw a bar as done that the
   commits do not support.
3. **Scope the chart** to the current major and its remaining iterations.
   Collapse fully completed earlier majors into one line each (or omit). List
   post-milestone work as a one-line "After:" footer.
4. **Render** in a fenced block, under ~100 columns so it never wraps.
5. **Details below the chart** — for each remaining iteration, 1–4 sentences:
   what it is, its gate (the smoke task), dependencies, anything absorbed
   into it (a defect fix scheduled inside a later slice).
6. **Flag the top 1–3 risks or decisions** — unowned items, gates awaiting the
   owner (an owner-report task awaiting its tick, a pending visual review),
   known issues no iteration owns. End with the single concrete next action.

## Chart format

```
<Major code + title>                             now
                                                  │
v0.1.0  Project initiation          ████████████──┤  done, <one-line note>
v0.1.1  Templates + init                ██████████┤  done (<evidence>)
v0.1.2  Core loop skills                          ├▓▓▓▓▓▓  ◀ NEXT: <what & why>
v0.1.3  Discipline skills                         │      ░░░░░░
v0.1.4  Orchestration + audit                     │        ░░░  <hook>
──────────────────────────────────────────────────┼──────────────────────────
Parallel / unscheduled                            │
      <owner-report task awaiting tick>           ├─?─?─?  <needs the owner>
      <recurring gate, e.g. visual review>        ●      ●      ●
──────────────────────────────────────────────────┴──────────────────────────
After v0.1:  v0.2 Distribution — plugin, reference installs, guards package
```

Legend (include it under the chart when symbols beyond █/░ are used):
`████` done · `▓▓▓▓` active/next · `░░░░` planned · `─?─` unscheduled/unowned ·
`●` gate or review point · `│` the now line · `◀ NEXT` the single next unit.

Rules:
- Exactly one `◀ NEXT`. Done bars end at (touch) the now line; the next unit
  starts just right of it; later work steps progressively rightward.
- One row per iteration; indent sub-units two spaces under their row only
  when the plan has them.
- Right-of-bar annotations are ≤ ~40 chars — details belong in the section
  below, not in the chart.
- The `Parallel / unscheduled` band is only for real cross-cutting items
  (owner-report tasks awaiting a tick, recurring review gates); omit it when
  empty.

## The board variant (on request)

When the owner wants something to click — "visual", "board", "roadmap page"
— publish an Artifact page: status-coloured iteration nodes grouped by major
(lanes), click-to-inspect goal + tasks, a one-line legend (`done` = success
tint, `active` = accent, `next` = warning, `later` = muted). Derive every
node from the same powerplan reads as the chart. The board is a view: after
the owner reprioritises on it, update the plan through powerplan first, then
regenerate. Sentence case, no emoji, CSS variables for colour so it survives
dark mode.

## Notes

- Lead with any status correction from step 2 ("v0.1.2's srs task is
  committed but was unticked — ticked"), then the chart, then details, then
  flags.
- After the owner reprioritises in conversation, update the plan
  (`powerflow-plan`), then re-render; never re-render a picture the plan does
  not yet say.
