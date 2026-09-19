#!/usr/bin/env node
// placeholders: version_source
// Single-version-source guard (PowerFlow METHODOLOGY.md §8). Exactly one file
// carries the version; everything else derives from it or is checked here to
// match. Exit 1 on any drift.
//   node scripts/check-version.mjs [--tag vX.Y.Z] [--changelog] [--root <repo>]
// Fill DERIVED with every other place the version appears verbatim (manifest
// copies, server.json, a packaging test). A file that derives at build time
// (tauri.conf.json pointing at ../package.json, a build.rs export) belongs in
// DERIVED with a regex that matches the *reference*, not a copy.
import { existsSync, readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const rootArg = process.argv.indexOf("--root")
const repo = rootArg >= 0 ? process.argv[rootArg + 1] : join(dirname(fileURLToPath(import.meta.url)), "..")

// The only file that carries the version.
const SOURCE = "{{version_source}}"

// [relative path, regex whose first capture group must equal the version]
const DERIVED = [
  // ["src-tauri/tauri.conf.json", /"version":\s*"([^"]+)"/],
  // ["server.json", /"version":\s*"([^"]+)"/],
  // ["tests/test_packaging.py", /__version__ == "([^"]+)"/],
]

const args = process.argv.slice(2)
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined }
const failures = []
const ok = (what) => console.log(`ok   ${what}`)
const fail = (what) => { failures.push(what); console.log(`FAIL ${what}`) }

function readVersion(path) {
  const text = readFileSync(join(repo, path), "utf8")
  if (path.endsWith(".json")) return JSON.parse(text).version
  if (/pyproject\.toml$/.test(path)) return /^\[project\][\s\S]*?^version\s*=\s*"([^"]+)"/m.exec(text)?.[1]
  if (/Cargo\.toml$/.test(path)) return /^\[package\][\s\S]*?^version\s*=\s*"([^"]+)"/m.exec(text)?.[1]
  if (/\.csproj$/.test(path)) return /<Version>([^<]+)<\/Version>/.exec(text)?.[1]
  return /version\s*[:=]\s*["']?(\d+\.\d+\.\d+[^"'\s]*)/i.exec(text)?.[1]
}

if (!existsSync(join(repo, SOURCE))) {
  fail(`version source ${SOURCE} does not exist`)
} else {
  const version = readVersion(SOURCE)
  if (!version || !/^\d+\.\d+\.\d+/.test(version)) fail(`${SOURCE} has no X.Y.Z version (got "${version}")`)
  else {
    ok(`${SOURCE} version ${version} (source of truth)`)
    for (const [path, re] of DERIVED) {
      if (!existsSync(join(repo, path))) { fail(`${path} missing`); continue }
      const found = re.exec(readFileSync(join(repo, path), "utf8"))?.[1]
      if (found === version) ok(`${path} carries ${version}`)
      else fail(`${path} carries "${found}", ${SOURCE} says ${version}`)
    }
    const tag = opt("--tag")
    if (tag) {
      if (tag === `v${version}`) ok(`tag ${tag} matches`)
      else fail(`tag ${tag} does not match v${version}`)
    }
    if (args.includes("--changelog")) {
      const cl = join(repo, "CHANGELOG.md")
      if (!existsSync(cl)) fail("CHANGELOG.md missing")
      else if (new RegExp(`^## \\[?${version.replace(/\./g, "\\.")}\\b`, "m").test(readFileSync(cl, "utf8"))) ok(`CHANGELOG.md has a ${version} section`)
      else fail(`CHANGELOG.md has no "## ${version}" section`)
    }
  }
}

if (failures.length) { console.error(`${failures.length} version drift(s)`); process.exit(1) }
console.log("version: OK")
