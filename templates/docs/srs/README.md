<!-- placeholders: project -->
# Software Requirements Specification (SRS)

Requirements for {{project}}, ASPICE-style. Each `SRS-<feature>.md` states
what the product **shall** do for one feature area, as uniquely identified,
verifiable, traceable shall-statements. This layer is **what**; design notes
and code are **how**. Product intent: [PRD.md](../../PRD.md). Priority is
implied by [PLAN.md](../../PLAN.md), not a column here.

## Requirement ID scheme (PowerFlow D1)

`SRS-<FEAT>-<NNN>` — `FEAT` is the feature tag, owned by exactly one file in
this directory; `NNN` a zero-padded sequence that is **never reused or
renumbered**. Superseded requirements are marked `(superseded by …)` in the
Requirement cell, not deleted. `scripts/check-req-ids.mjs` fails CI on a
duplicate definition or a tag defined in two files.

## Allocator — the single source of tags and numbers

| Tag | File | Feature | Allocated | Next free |
|---|---|---|---|---|
| | | | — | 001 |

E2E test numbers (`tests/**/NN-topic.spec.ts`) are allocated here too:
allocated none · next free `01`.

## Table format

Every SRS file opens with this table:

| Column | Meaning |
|---|---|
| **ID** | `SRS-<FEAT>-<NNN>`, stable forever |
| **Requirement** | One testable "shall" |
| **Rationale** | Why it exists — intent, not restatement |
| **Verification** | `Test`, `Analysis`, `Review`, `Demo` |
| **Trace** | Design §, implementation path, test path — filled as code lands |

Rules: one shall per row; no "fast" or "nice" without a number;
implementation-neutral unless the feature is platform-specific (`[linux]`,
`[windows]`, `[macos]`, `[web]`, `[native]`). A row with no test path in
Trace is not verified. The most valuable rows are interaction semantics —
which control wins when states disagree — with an explicit priority order.

## Verification methods

- **Test** — automated. Prefer this; cite the test file.
- **Analysis** — argued from the algorithm or spec when a test is impractical.
- **Review** — inspection against a reference behaviour or this SRS.
- **Demo** — shown in the running app; record what was demonstrated.

## Coverage rule

A named product feature does not ship without an SRS file. New features get a
new file (or new rows) **before** implementation, and the rows land in the
same change as the code that satisfies them.
