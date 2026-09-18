# D1 — Requirement ID scheme

Status: Accepted · 2026-09-18

## Context

Five schemes are in use across the author's repos: `SRS-NAV-001` (PowerGit,
powerplanner), two-letter prefixes with a registry (`VU-001`, RadEAU),
`CC-REQ-ZOOM-001` (powertimelines), `REQ-TEXT-001` (PowerNote) and
per-document `R1…R21` (A2L-Forge). Two-letter prefixes need a registry lookup
to be readable; per-document numbering cannot be cited across files; long
prefixes cost table width. The two most recent repos converged on
`SRS-<FEAT>-NNN`.

## Decision

Requirement IDs are `SRS-<FEAT>-NNN`: `FEAT` is a short uppercase feature tag
owned by exactly one `docs/srs/SRS-<feature>.md`, `NNN` a zero-padded sequence
that is never reused or renumbered. `docs/srs/README.md` is the single
allocator (tag → file → next free number). Superseded requirements are marked,
not deleted. CI fails on a duplicate definition (`check-req-ids`).

## Consequences

- Every SRS file opens with a table whose first column is the ID; the tag is
  readable without the registry, and the registry still prevents collisions.
- Existing repos are not renumbered; `powerflow-audit` reports the scheme in
  use, and a migration is a project decision, not a pack requirement.
- Reopen if a project routinely needs several feature tags per file (RadEAU's
  `SRS_graphing.md` owns six) — the allocator already allows it, so that is a
  documentation question, not a scheme change.
