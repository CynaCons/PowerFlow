---
name: powerflow-decide
description: Record an architecture or process decision as a numbered decision record (docs/decisions/D<n>-slug.md) with Status, Context, Decision and Consequences that name the gate which would reopen it — linked from the decisions README and the PRD's decisions table — before the affected part is built. Use this whenever a choice between alternatives is being made or has just been made (a library, a transport, a memory strategy, a convention, a "we will not do X"), whenever the user says "let's go with", "decision", "ADR", "record that", "we decided", or when a PRD lists a decision to record that has no file yet. Also use it when an owner amends the method — an accepted amendment is a decision.
---

# powerflow-decide — write it down before it is built

Decisions that live only in a chat or a commit message get re-litigated by
the next agent, or silently reversed by a "simplification". A decision record
is short, has a number that never changes, and — the part that matters most —
says what would reopen it: a CI threshold, a measured slope, an owner report,
a date (METHODOLOGY.md §2.2). RadEAU's D1–D9 were written before the
subsystems existed and each names its gate; PowerFlow's own D1–D12 follow the
same shape.

Bundled: `scripts/decide.py` — next number, file from the template, README
line, PRD table row. The prose is yours.

## 1. Is it a decision?

Yes when alternatives existed and one was chosen with consequences that
constrain later work. No when it is a task (PLAN), a behaviour (SRS row), or
a fact discovered (memory). An owner's amendment to the method ("PRD once per
project") is a decision. A direction change for the product is a decision
*first*, and only then a PRD revision (D10).

## 2. Create the file

```bash
python <skill>/scripts/decide.py --title "Renderer memory strategy" --summary "workers + shared buffers; revisit if the overnight slope gate fails"
```

It picks the next `D<n>` (numbers are never reused, even for reversed
decisions), writes `docs/decisions/D<n>-<slug>.md` from the template with
today's date, appends the README line and — when the PRD has a "Decisions to
record" table — its row. Then write the three sections:

- **Context** — the forces: what is being built, the alternatives considered,
  what was measured or observed. Cite PRD/SRS sections and prior-art failures
  by path. This is where the *why* lives; keep it factual.
- **Decision** — one paragraph, active voice: what is adopted, what is
  explicitly not. Include the default when the decision is provisional
  ("adopted provisionally; must be confirmed before the first consumer").
- **Consequences** — what becomes mandatory, what becomes forbidden, and
  **"Reopen if …"** with a concrete gate. A decision without a reopening gate
  is an opinion.

## 3. Reversing or superseding

Never edit a decision into its opposite. Write a new `D<m>` whose Decision
says "supersedes D<n>", and change D<n>'s status line to
`Status: Superseded by D<m> · <date>`. History stays readable.

## 4. Prove and register

`python scripts/check.py`-style guards in stamped projects check that every
`D*.md` is linked from the README and has the four sections; run whatever the
project's verify command is. If the decision came out of a slice, cite it in
the iteration's Goal or in the relevant task text (`powerflow-plan`), so the
plan says why the work took that shape.

## Report

```
D<n> — <title> (Accepted <date>)
  file:    docs/decisions/D<n>-<slug>.md · README linked · PRD row <added|absent>
  gate:    reopen if <…>
  affects: <SRS rows / PLAN tasks that now depend on it>
```

Then the miniplan (D12) when the turn changed the plan.

## What not to do

- Do not record a decision after the code shipped "for completeness" — if
  it is already built, the record is still worth writing, but say so in
  Context and date it honestly.
- Do not renumber or delete decision files.
- Do not write Consequences without a reopening gate.
- Do not put the alternatives' full analysis in the file; two lines per
  alternative, cite the analysis if it exists elsewhere.
