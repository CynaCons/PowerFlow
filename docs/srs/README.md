# Requirements — PowerFlow

One `SRS-<feature>.md` per feature area. Each opens with a table:

| ID | Requirement | Rationale | Verification | Trace |
|---|---|---|---|---|

- **ID** `SRS-<FEAT>-NNN`. The tag is owned by exactly one file (below); the
  next number is the highest in that file + 1; numbers are never reused — a
  changed requirement is a new row, the old one marked `(superseded by …)`.
- **Requirement** one testable *shall*; a number instead of "fast".
- **Verification** `Test` (preferred) · `Analysis` · `Review` · `Demo`.
- **Trace** the test path once it exists. A `Test` row with no path is not
  verified. Priority is the plan's, not a column here.

Rows are written before the code that satisfies them and land in the same
change. A named feature does not ship without its file.

PowerFlow's behaviour is the skill text (`skills/powerflow/SKILL.md`); an SRS
file appears here when a script grows a contract worth rows (the `stamp.py`
answers schema is the first candidate).

## Tags

| Tag | File | Feature |
|---|---|---|
| | | |
