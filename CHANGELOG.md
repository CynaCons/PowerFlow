# Changelog

Release notes are the closed iterations of [PLAN.md](PLAN.md). The version is
`.claude-plugin/plugin.json`; `package.json` and this file's top section match.

## 0.3.0 — 2026-09-19

**Lean** (D15). Owner: "way too complicated… strip the fat, keep the
essential." One skill, `powerflow`, describing the whole method section by
section, with the powerplan and PowerSpawn sections as the load-bearing ones.

- 13 skills → 1 (`skills/powerflow/SKILL.md`, ~250 lines); always-on cost
  ~3.2k → ~300 tokens per session.
- 14 decision files + README + PRD table → one `DECISIONS.md` log (D1–D15).
- 290-line METHODOLOGY.md removed; the skill is the canonical text.
- 19 templates → 9 files (PRD, AGENTS ~40 lines, CLAUDE shim, SRS index as a
  tag table without allocator, `.mcp.json` ± python variant, settings ± plugin
  variant, `.gitignore`). `srs.py` and `decide.py` removed.
- Guards, CI example and 18 tests moved to `extras/guards/` (opt-in);
  `check-req-ids` accepts the lean tag table.
- `stamp.py`: 7 required answers, `--force` never overwrites stateful files.
- PowerFlow itself: PRD to one page, `check.py` to four checks, PowerFlow's own
  SRS removed; a GitHub Pages site.

## 0.2.0 — 2026-09-19

First installable pack: handbook, templates and thirteen `powerflow-*` skills
installed at user scope as a Claude Code plugin (v0.1.0–v0.2.1 iterations).
powerplan 0.8.0 shipped `show_miniplan` for it.
