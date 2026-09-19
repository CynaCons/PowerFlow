# The release ritual — step list

Generic order and refusals (METHODOLOGY.md §8). The project's AGENTS.md (or
its own release notes under `docs/`) supplies the commands, the artifact
names and the storefront facts; this list supplies the sequence and the
gates. Distilled from PowerGit `.claude/skills/release/SKILL.md`, RadEAU PRD
§9.4 and powerplan `docs/RELEASING.md`.

## 0. Preflight — refuse to continue on any miss

- [ ] **The iteration is closed** in PLAN.md through powerplan
      (`close_iteration`; open tasks moved forward, never force-closed).
      PLAN.md is the changelog source; a release from an open iteration has
      no notes and no proof.
- [ ] No owner-report task in the closing iteration without the owner's
      tick ("awaiting owner verification" blocks a release).
- [ ] Gates green: unit/engine tests, e2e once, the visual subset for what
      changed since the last tag (not the whole suite), guards
      (`check-plan`, `check-req-ids`, `check-version`).
- [ ] **Look at it**: start the app (dev or the last packaged build), walk the
      states the project's visual walkthrough lists, one capture per state,
      reviewed. PowerGit v0.13.13 shipped with the selected commit's graph
      node hidden because nobody looked.
- [ ] Working tree clean; everything committed and pushed.

## 1. Version — one source, everything derives

- [ ] Bump the **single version source** named in the PRD (`package.json`,
      `pyproject.toml`, …) — and every file the project's `check-version`
      lists as carrying the version verbatim (powerplan: six files, all
      equal). Nothing else by hand.
- [ ] `node scripts/check-version.mjs --changelog` (or the project's
      equivalent) exits 0: derivation intact, changelog has the section.
- [ ] CHANGELOG entry: the closed iterations since the last tag, one line
      each, owner-readable.
- [ ] Commit `chore: release X.Y.Z` (or `release: vX.Y.Z`).

## 2. Build and smoke the artifact

- [ ] Build with the **canonical command only** (AGENTS.md).
- [ ] Smoke the packaged artifact from a clean directory: extract/install,
      launch, confirm it reports the new version (`/health`, `--version`,
      About), do one real thing. Never publish an artifact nobody launched.
- [ ] `check-version --dist <dir>` (artifact names carry the version) when
      the project has it.

## 3. Tag and publish

- [ ] `git push origin <branch>`; `git tag vX.Y.Z`; `git push origin vX.Y.Z`.
- [ ] Create the GitHub release with notes from the CHANGELOG section (a
      file with only that section — not the whole changelog).
- [ ] **Check whether CI already picked up the tag before dispatching**:
      `gh run list --workflow=<Publish|Release> --limit 2`. A push from the
      owner's credentials starts the workflow; a push with an App token does
      not. If a run for the tag exists, watch it; if not, dispatch
      (`gh workflow run <name> --ref vX.Y.Z`) — and never both: the second
      run reaches the registry/store after the first and fails on
      "duplicate version" (powerplan 0.8.0, 2026-09-19).
- [ ] `gh run watch <id> --exit-status`. Red → fix forward and re-tag
      `vX.Y.Z+1`; never move or reuse a tag that published an artifact.

## 4. Verify the live surfaces

- [ ] Registry / store / PyPI / release assets show `X.Y.Z` (curl the JSON,
      list the assets — a number, not a feeling).
- [ ] For desktop apps with an updater: from an installed previous version,
      "Check for updates" finds `X.Y.Z`; that is the owner's tick for the
      updater.

## 5. Storefront and site

- [ ] Repo description, homepage, topics, issues enabled (`gh repo view
      --json …`; edit only when drifted — settings are not tree content).
- [ ] Showcase/site refresh when install snippets or screens changed
      (screenshots from the running app, never one showing an error state).

## 6. Close out

- [ ] Tick the release task in PLAN.md through powerplan; `check_plan` ok.
- [ ] Record any new failure mode in the project's release notes
      (`docs/RELEASING.md` or AGENTS.md) and as a memory — the next release
      should not rediscover it.
- [ ] Final push. Report: version, tag, artifacts, live-surface checks,
      anything left for the owner.
