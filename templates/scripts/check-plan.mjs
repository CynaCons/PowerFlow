#!/usr/bin/env node
// PLAN.md structure guard — the CI mirror of powerplan's `check_plan`
// (PowerFlow D2 / METHODOLOGY.md §2.4). powerplan is the authority and the
// only writer; this script only refuses to merge a plan that drifted.
//   node scripts/check-plan.mjs [PLAN.md]
// Checks: duplicate iteration versions, empty titles, more than one current
// iteration, COMPLETE with open tasks, content after the Backlog, the
// stale-proof "Current Status" header, and checkboxes-only inside iterations.
import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const repo = join(dirname(fileURLToPath(import.meta.url)), "..")
const path = process.argv[2] ?? join(repo, "PLAN.md")
const lines = readFileSync(path, "utf8").split(/\r?\n/)

const MAJOR = /^## (v\d+\.\d+)\s+[—-]\s+(.*)$/
const ITER = /^### (v\d+\.\d+\.\d+)\s+[—-]\s+(.*)$/
const BACKLOG = /^## (Backlog|Future \(Backlog\))\s*$/
const TASK = /^- \[( |x|X)\] (.*)$/
const BULLET = /^(\s*)- (?!\[[ xX]\] )/
const STATUS = /\(([^()]*)\)\s*$/

const failures = []
const fail = (msg) => failures.push(msg)

const iterations = [] // { version, title, status, open, done, line }
let current = null
let inBacklog = false
let sawHeader = false
let afterBacklog = []

for (let i = 0; i < lines.length; i++) {
  const line = lines[i]
  if (/^## Current Status\s*$/.test(line)) sawHeader = true
  if (BACKLOG.test(line)) { inBacklog = true; current = null; continue }
  if (inBacklog) {
    // Sub-headings inside the backlog are backlog content; only a new
    // top-level section after it is a violation.
    if (/^## /.test(line)) afterBacklog.push(`${i + 1}: ${line}`)
    continue
  }
  const im = ITER.exec(line)
  if (im) {
    const rest = im[2]
    const statuses = []
    let title = rest
    let m
    while ((m = STATUS.exec(title))) { statuses.unshift(m[1]); title = title.slice(0, m.index).trimEnd() }
    current = { version: im[1], title, status: statuses.join(" ").toUpperCase(), open: 0, done: 0, line: i + 1 }
    iterations.push(current)
    continue
  }
  if (MAJOR.test(line) || /^## /.test(line)) { current = null; continue }
  if (!current) continue
  const tm = TASK.exec(line)
  if (tm) { if (tm[1] === " ") current.open++; else current.done++; continue }
  if (BULLET.test(line)) fail(`${path}:${i + 1}: non-checkbox bullet inside ${current.version} — iterations hold "- [ ]" tasks only (goal and prose lines are fine)`)
}

if (!sawHeader) fail(`${path}: no "## Current Status" section — the header must say the current iteration is the last heading not marked COMPLETE (D2)`)

const seen = new Map()
for (const it of iterations) {
  const key = it.version.toLowerCase()
  if (seen.has(key)) fail(`${path}:${it.line}: duplicate iteration ${it.version} (first at line ${seen.get(key)})`)
  else seen.set(key, it.line)
  if (!it.title.trim()) fail(`${path}:${it.line}: iteration ${it.version} has an empty title`)
  const complete = /COMPLETE|CLOSED|DONE/.test(it.status)
  if (complete && it.open > 0) fail(`${path}:${it.line}: ${it.version} is marked complete but has ${it.open} open task(s)`)
}
const currents = iterations.filter((it) => /\bCURRENT\b|ACTIVE|IN PROGRESS|WIP/.test(it.status) || /\bcurrent\b/i.test(it.title))
if (currents.length > 1) fail(`more than one current iteration: ${currents.map((c) => c.version).join(", ")}`)
if (afterBacklog.length) fail(`content after the Backlog section (it must be last):\n  ${afterBacklog.join("\n  ")}`)

const openIters = iterations.filter((it) => !/COMPLETE|CLOSED|DONE/.test(it.status) || it.open > 0)
const cur = currents[0] ?? openIters[0] ?? iterations.at(-1)
const done = iterations.reduce((n, it) => n + it.done, 0)
const total = iterations.reduce((n, it) => n + it.open + it.done, 0)
console.log(`plan: ${iterations.length} iteration(s), current ${cur?.version ?? "—"}, tasks ${done}/${total}`)
for (const f of failures) console.error(`FAIL ${f}`)
if (failures.length) process.exit(1)
console.log("plan: OK")
