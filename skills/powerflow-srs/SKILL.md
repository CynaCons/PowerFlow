---
name: powerflow-srs
description: Write or extend a feature's requirements as an ASPICE-style SRS table in docs/srs/SRS-<feature>.md — stable SRS-<FEAT>-NNN IDs allocated from the project's index, one testable "shall" per row with rationale, verification method and trace, the allocator bumped, the CI ID guard run, and the matching PLAN task registered. Use this whenever a feature is being specified, when the user says "spec this", "add requirements for", "write the SRS", "what should it do exactly", when a slice introduces new behaviour that no SRS row covers, when a test lands that verifies an existing row (fill its Trace), or when an owner report reveals a behaviour that was never written down. Requirements come before code, never after.
---

# powerflow-srs — the *what*, as rows

A named feature does not ship without an SRS file, and a requirement is
written **before** the code that satisfies it, landing in the same change
(METHODOLOGY.md §2.3). The rows are the contract that tests, reviews and owner
reports refer to by ID for the life of the project — which is why IDs are
never reused and the allocator in `docs/srs/README.md` is the only place
numbers come from (D1).

Bundled: `scripts/srs.py` (`new` registers a tag and creates the file from the
template; `allocate` hands out the next IDs and bumps the allocator). Use it
rather than editing the table by hand — the CI guard `check-req-ids.mjs` fails
on any ID the table did not hand out.

## 1. Find the home

`show_miniplan` first (the slice this belongs to). Then read
`docs/srs/README.md`'s allocator table:

- The feature area already has a tag → extend that file.
- New area → pick a short uppercase tag that reads in a sentence
  ("`SRS-NAV-004`") and register it:
  `python <skill>/scripts/srs.py new --tag NAV --feature "Navrail" --prd-section 5.5`
  (creates `docs/srs/SRS-navrail.md` from the template, registers `NAV → SRS-navrail.md`).
- A file that would need two tags is usually two files. RadEAU's graphing SRS
  owns six tags because they are one subsystem with six sub-areas; that is the
  exception, not the pattern.

## 2. Allocate, then write

`python <skill>/scripts/srs.py allocate --tag NAV --count 3` prints
`SRS-NAV-004 … 006` and bumps the table. Now write the rows:

| ID | Requirement | Rationale | Verification | Trace |
|---|---|---|---|---|

- **Requirement**: one behaviour, one *shall*, testable as written. "The rail
  shall highlight the active repo" — yes. "The rail shall be intuitive" — no.
  Numbers replace adjectives: not "fast", but "≤ 200 ms p95 input-to-paint".
  Implementation-neutral unless the feature is platform-specific; then tag
  it `[linux]` / `[native]` / `[web]`.
- **Rationale**: why it exists — the intent, a prior-art failure, the owner's
  words. Never a restatement of the requirement.
- **Verification**: `Test` (preferred), `Analysis`, `Review`, `Demo`. Choose
  what will actually be done; `Test` with no test path in Trace later is a
  lie the guard cannot catch, only the owner.
- **Trace**: design §, implementation path, test path. Leave the test path
  empty until the test exists; fill it in the same change as the test.

The most valuable rows are **interaction semantics**: which control wins when
states disagree, what happens on the boundary, the priority order. Those are
the rows that settle arguments a year later. Write them even when they feel
obvious.

## 3. Superseding, never deleting

A requirement that changes gets a **new row** with a new ID; the old row's
Requirement cell gains `(superseded by SRS-NAV-009)`. A requirement that is
dropped is marked `(withdrawn <date>: reason)`. Numbers are never reused, so
a gap in the sequence is normal.

## 4. Prove and register

```bash
node scripts/check-req-ids.mjs
```

must print `OK` (unique IDs, one tag per file, allocator honest). Then the
plan: `add_tasks` on the current iteration with the IDs in the text
("Implement SRS-NAV-004..006: …"), or `update_task` an existing task to cite
them. A PLAN task that implements behaviour without an ID is the smell this
skill exists to remove.

## 5. When a test lands

`powerflow-verify` fills Trace: the test path goes in the row's last column,
in the same change as the test. A row with a test path is *verified*; the SRS
index has no Status column because Trace is the status.

## Report

```
docs/srs/SRS-<feature>.md — <k> rows (<SRS-X-001..003>), tag <X> registered|extended
allocator: next free <NNN> · check-req-ids: OK
PLAN: <task text> added to vX.Y.Z
```

## What not to do

- Do not write requirements in prose, PLAN tasks, or `docs/*.md` notes and
  call them the spec — if it is a shall, it is a row.
- Do not renumber, reorder or delete rows to "clean up".
- Do not mark Verification `Test` for behaviour that will only be demoed.
- Do not put priority or status columns in the table: priority is PLAN.md,
  status is Trace.
