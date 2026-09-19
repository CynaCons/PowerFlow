// Tests for the three opt-in guards (D13, D15). Each case builds a minimal repo
// in a temp dir and runs the script from extras/guards against it.
//   node --test "extras/guards/tests/**/*.test.mjs"
import { test } from "node:test"
import assert from "node:assert/strict"
import { spawnSync } from "node:child_process"
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from "node:fs"
import { tmpdir } from "node:os"
import { join, dirname } from "node:path"
import { fileURLToPath } from "node:url"

const scripts = join(dirname(fileURLToPath(import.meta.url)), "..")

function repo(files) {
  const dir = mkdtempSync(join(tmpdir(), "pf-guard-"))
  for (const [rel, content] of Object.entries(files)) {
    mkdirSync(join(dir, dirname(rel)), { recursive: true })
    writeFileSync(join(dir, rel), content)
  }
  return dir
}
function run(script, args) {
  const r = spawnSync(process.execPath, [join(scripts, script), ...args], { encoding: "utf8" })
  return { code: r.status, out: r.stdout + r.stderr }
}

// --- check-plan ---------------------------------------------------------------

const GOOD_PLAN = `# Demo — Implementation Plan

**Goal:** demo

---

## Current Status

The current iteration is the last heading below that is not marked COMPLETE.

---

## v0.1 — Foundation
> first

### v0.1.0 — Init (2026-09-19) (COMPLETE)
**Goal:** start
- [x] scaffold
- [x] Smoke test: launches

### v0.1.1 — Next (current) (ACTIVE)
**Goal:** go on
- [ ] a thing
- [ ] Smoke test: still launches

## Backlog
- later idea
### From an older list
- older idea
`

test("check-plan: canonical plan passes; sub-heading inside the backlog is fine", () => {
  const d = repo({ "PLAN.md": GOOD_PLAN })
  const r = run("check-plan.mjs", [join(d, "PLAN.md")])
  assert.equal(r.code, 0, r.out)
  assert.match(r.out, /current v0\.1\.1, tasks 2\/4/)
  rmSync(d, { recursive: true, force: true })
})

for (const [name, mutate, expect] of [
  ["missing Current Status header", (p) => p.replace("## Current Status", "## Status"), /no "## Current Status"/],
  ["non-checkbox bullet inside an iteration", (p) => p.replace("- [ ] a thing", "- [ ] a thing\n- a prose bullet"), /non-checkbox bullet inside v0\.1\.1/],
  ["duplicate iteration version", (p) => p.replace("### v0.1.1 — Next", "### v0.1.0 — Next"), /duplicate iteration v0\.1\.0/],
  ["COMPLETE with an open task", (p) => p.replace("- [x] Smoke test: launches", "- [ ] Smoke test: launches"), /marked complete but has 1 open/],
  ["two current iterations", (p) => p.replace("### v0.1.0 — Init (2026-09-19) (COMPLETE)", "### v0.1.0 — Init (ACTIVE)"), /more than one current/],
  ["top-level section after the backlog", (p) => p + "\n## v0.2 — Late\n", /content after the Backlog/],
]) {
  test(`check-plan: ${name} fails`, () => {
    const d = repo({ "PLAN.md": mutate(GOOD_PLAN) })
    const r = run("check-plan.mjs", [join(d, "PLAN.md")])
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, expect)
    rmSync(d, { recursive: true, force: true })
  })
}

// --- check-req-ids ---------------------------------------------------------------

const README = (rows) => `# SRS\n\n| Tag | File | Feature | Allocated | Next free |\n|---|---|---|---|---|\n${rows}\n`
const SRS = (tag, nums) => `# SRS\n\n| ID | Requirement | Rationale | Verification | Trace |\n|---|---|---|---|---|\n` +
  nums.map((n) => `| SRS-${tag}-${String(n).padStart(3, "0")} | shall | | Test | |`).join("\n") + "\n"

test("check-req-ids: unique IDs, registered tags, honest allocator, unique e2e numbers pass", () => {
  const d = repo({
    "docs/srs/README.md": README("| NAV | SRS-navrail.md | Navrail | 001–002 | 003 |\n| SET | SRS-settings.md | Settings | 001 | 002 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1, 2]),
    "docs/srs/SRS-settings.md": SRS("SET", [1]),
    "tests/e2e/01-shell.spec.ts": "", "tests/e2e/02-navrail.spec.ts": "",
  })
  const r = run("check-req-ids.mjs", ["--root", d])
  assert.equal(r.code, 0, r.out)
  assert.match(r.out, /3 defined across 2 SRS file\(s\), 2 tag\(s\); e2e numbers: 2/)
  rmSync(d, { recursive: true, force: true })
})

test("check-req-ids: the lean tag table (no Next free column) passes on unique IDs", () => {
  const d = repo({
    "docs/srs/README.md": "# SRS\n\n| Tag | File | Feature |\n|---|---|---|\n| NAV | SRS-navrail.md | Navrail |\n",
    "docs/srs/SRS-navrail.md": SRS("NAV", [1, 2, 7]),
  })
  const r = run("check-req-ids.mjs", ["--root", d])
  assert.equal(r.code, 0, r.out)
  rmSync(d, { recursive: true, force: true })
})

for (const [name, files, expect] of [
  ["duplicate ID across files", {
    "docs/srs/README.md": README("| NAV | SRS-navrail.md | Navrail | 001 | 002 |\n| SET | SRS-settings.md | Settings | 001 | 002 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1]), "docs/srs/SRS-settings.md": SRS("NAV", [1]),
  }, /SRS-NAV-001 defined in both/],
  ["tag defined in two files", {
    "docs/srs/README.md": README("| NAV | SRS-navrail.md | Navrail | 001–002 | 003 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1]), "docs/srs/SRS-other.md": SRS("NAV", [2]),
  }, /tag NAV is defined in .* a tag is owned by exactly one file/],
  ["tag missing from the tag table", {
    "docs/srs/README.md": README("| NAV | SRS-navrail.md | Navrail | 001 | 002 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1]), "docs/srs/SRS-settings.md": SRS("SET", [1]),
  }, /tag SET .* is not listed/],
  ["allocator not bumped", {
    "docs/srs/README.md": README("| NAV | SRS-navrail.md | Navrail | 001 | 002 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1, 2]),
  }, /SRS-NAV-002 is defined but README says next free is 002/],
  ["registered to another file", {
    "docs/srs/README.md": README("| NAV | SRS-nav.md | Navrail | 001 | 002 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1]),
  }, /listed for SRS-nav.md but defined in SRS-navrail.md/],
  ["duplicate e2e number", {
    "docs/srs/README.md": README("| NAV | SRS-navrail.md | Navrail | 001 | 002 |"),
    "docs/srs/SRS-navrail.md": SRS("NAV", [1]),
    "tests/a/07-x.spec.ts": "", "tests/b/07-y.spec.ts": "",
  }, /e2e number 07 used by both/],
]) {
  test(`check-req-ids: ${name} fails`, () => {
    const d = repo(files)
    const r = run("check-req-ids.mjs", ["--root", d])
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, expect)
    rmSync(d, { recursive: true, force: true })
  })
}

// --- check-version -----------------------------------------------------------------

function versionScript(dir, source, derived = "") {
  // render the template with the given SOURCE, plus a DERIVED entry when asked
  let s = readFileSync(join(scripts, "check-version.mjs"), "utf8").replace(/const SOURCE = "[^"]+"/, `const SOURCE = "${source}"`)
  if (derived) s = s.replace("const DERIVED = [", `const DERIVED = [\n  ${derived},`)
  mkdirSync(join(dir, "scripts"), { recursive: true })
  writeFileSync(join(dir, "scripts", "check-version.mjs"), s)
  return join(dir, "scripts", "check-version.mjs")
}
function runVersion(dir, args) {
  const r = spawnSync(process.execPath, [join(dir, "scripts", "check-version.mjs"), ...args], { encoding: "utf8" })
  return { code: r.status, out: r.stdout + r.stderr }
}

test("check-version: package.json source, matching tag and changelog pass", () => {
  const d = repo({ "package.json": JSON.stringify({ name: "x", version: "1.2.3" }), "CHANGELOG.md": "# Changelog\n\n## 1.2.3 — 2026-09-19\n\n- x\n" })
  versionScript(d, "package.json")
  const r = runVersion(d, ["--tag", "v1.2.3", "--changelog"])
  assert.equal(r.code, 0, r.out)
  rmSync(d, { recursive: true, force: true })
})

test("check-version: pyproject source with a matching derived file passes; a drifted one fails", () => {
  const d = repo({ "pyproject.toml": '[project]\nname = "x"\nversion = "0.8.0"\n', "server.json": '{ "version": "0.8.0" }' })
  versionScript(d, "pyproject.toml", '["server.json", /"version":\\s*"([^"]+)"/]')
  assert.equal(runVersion(d, []).code, 0)
  writeFileSync(join(d, "server.json"), '{ "version": "0.7.0" }')
  const r = runVersion(d, [])
  assert.equal(r.code, 1, r.out)
  assert.match(r.out, /server\.json carries "0\.7\.0", pyproject\.toml says 0\.8\.0/)
  rmSync(d, { recursive: true, force: true })
})

test("check-version: tag mismatch and missing changelog section fail", () => {
  const d = repo({ "package.json": JSON.stringify({ version: "1.2.3" }), "CHANGELOG.md": "# Changelog\n\n## 1.2.2\n" })
  versionScript(d, "package.json")
  const r = runVersion(d, ["--tag", "v1.2.4", "--changelog"])
  assert.equal(r.code, 1, r.out)
  assert.match(r.out, /tag v1\.2\.4 does not match v1\.2\.3/)
  assert.match(r.out, /CHANGELOG\.md has no "## 1\.2\.3" section/)
  rmSync(d, { recursive: true, force: true })
})
