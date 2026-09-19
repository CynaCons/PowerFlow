#!/usr/bin/env node
// Requirement-ID guard (PowerFlow D1). A requirement ID `SRS-<FEAT>-<NNN>` is
// DEFINED where it appears as the first cell of a table row in docs/srs/*.md;
// references elsewhere are fine. Rules enforced:
//   1. an ID is defined exactly once across docs/srs/
//   2. a tag (FEAT) is defined in exactly one file
//   3. every defined tag is registered in docs/srs/README.md's allocator
//      table, against the same file, and every defined number is below the
//      table's "Next free" for that tag
//   4. E2E test numbers `NN-topic.spec.*` under tests/ are unique
//   node scripts/check-req-ids.mjs
import { readdirSync, readFileSync, statSync } from "node:fs"
import { dirname, join, relative } from "node:path"
import { fileURLToPath } from "node:url"

const repo = join(dirname(fileURLToPath(import.meta.url)), "..")
const srsDir = join(repo, "docs", "srs")
const ROW = /^\|\s*SRS-([A-Z][A-Z0-9]*)-(\d{3,})\s*\|/
const failures = []
const fail = (msg) => failures.push(msg)

// --- definitions -----------------------------------------------------------
const defined = new Map() // id -> file
const tagFiles = new Map() // tag -> Set(file)
const tagMax = new Map() // tag -> max NNN
let files = []
try { files = readdirSync(srsDir).filter((n) => /^SRS-.*\.md$/.test(n) && n !== "SRS-template.md") } catch { files = [] }
for (const name of files) {
  const text = readFileSync(join(srsDir, name), "utf8").split(/\r?\n/)
  text.forEach((line, i) => {
    const m = ROW.exec(line)
    if (!m) return
    const [, tag, num] = m
    const id = `SRS-${tag}-${num}`
    if (defined.has(id)) fail(`${id} defined in both ${defined.get(id)} and ${name}:${i + 1}`)
    else defined.set(id, name)
    if (!tagFiles.has(tag)) tagFiles.set(tag, new Set())
    tagFiles.get(tag).add(name)
    tagMax.set(tag, Math.max(tagMax.get(tag) ?? 0, Number(num)))
  })
}
for (const [tag, set] of tagFiles) {
  if (set.size > 1) fail(`tag ${tag} is defined in ${[...set].join(", ")} — a tag is owned by exactly one file`)
}

// --- allocator table in README.md -------------------------------------------
let registry = new Map() // tag -> { file, nextFree }
try {
  const readme = readFileSync(join(srsDir, "README.md"), "utf8").split(/\r?\n/)
  for (const line of readme) {
    // | Tag | File | Feature | Allocated | Next free |
    const m = /^\|\s*([A-Z][A-Z0-9]*)\s*\|\s*\[?([^\]|]*?)\]?(?:\([^)]*\))?\s*\|[^|]*\|[^|]*\|\s*(\d{3,})\s*\|/.exec(line)
    if (m) registry.set(m[1], { file: m[2].trim().replace(/^`|`$/g, ""), nextFree: Number(m[3]) })
  }
} catch {
  fail("docs/srs/README.md is missing — it is the ID allocator")
}
for (const [tag, set] of tagFiles) {
  const file = [...set][0]
  const reg = registry.get(tag)
  if (!reg) { fail(`tag ${tag} (in ${file}) is not registered in docs/srs/README.md's allocator table`); continue }
  if (reg.file && reg.file !== file) fail(`tag ${tag} is registered to ${reg.file} but defined in ${file}`)
  const max = tagMax.get(tag)
  if (max >= reg.nextFree) fail(`tag ${tag}: SRS-${tag}-${String(max).padStart(3, "0")} is defined but README says next free is ${String(reg.nextFree).padStart(3, "0")} — bump the allocator`)
}

// --- e2e numbering ------------------------------------------------------------
const testNums = new Map() // NN -> file
const walk = (dir) => {
  let entries = []
  try { entries = readdirSync(dir) } catch { return }
  for (const e of entries) {
    if (e === "node_modules" || e.startsWith(".")) continue
    const p = join(dir, e)
    if (statSync(p).isDirectory()) walk(p)
    else {
      const m = /^(\d{2,3})-[^/\\]*\.(spec|test)\.[cm]?[jt]sx?$/.exec(e)
      if (!m) continue
      const rel = relative(repo, p)
      if (testNums.has(m[1])) fail(`e2e number ${m[1]} used by both ${testNums.get(m[1])} and ${rel}`)
      else testNums.set(m[1], rel)
    }
  }
}
walk(join(repo, "tests"))

console.log(`requirement IDs: ${defined.size} defined across ${files.length} SRS file(s), ${tagFiles.size} tag(s); e2e numbers: ${testNums.size}`)
for (const f of failures) console.error(`FAIL ${f}`)
if (failures.length) process.exit(1)
console.log("requirement IDs: OK")
