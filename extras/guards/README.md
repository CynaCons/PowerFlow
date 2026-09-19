# Guards — opt-in CI checks

Three Node scripts that fail CI on the drift the method cares about. They are
**optional** (D15): a side project does not need a CI job on day one; RadEAU
and PowerGit want them. Copy what you use into your repo's `scripts/` and add
the job from `ci.yml`.

| Script | Fails on |
|---|---|
| `check-plan.mjs [PLAN.md]` | duplicate iteration versions, two current iterations, COMPLETE with open tasks, a section after the Backlog, no `## Current Status` header, non-checkbox bullets inside iterations — the lint mirror of powerplan's `check_plan` (powerplan stays the authority and the only writer) |
| `check-req-ids.mjs [--root .]` | an `SRS-<FEAT>-NNN` defined twice, a tag defined in two files, a tag missing from `docs/srs/README.md`'s tag table (or past its "Next free" when that column exists), duplicate `NN-` e2e numbers |
| `check-version.mjs [--tag vX.Y.Z] [--changelog] [--root .]` | a derived version copy that drifted from the single source; fill `SOURCE` and `DERIVED` at the top |

Tests: `node --test "extras/guards/tests/**/*.test.mjs"` (18 cases, temp-dir
fixtures). If `check-plan.mjs` and powerplan's `check_plan` ever disagree on a
real plan, that is a bug here — powerplan wins (D13).
