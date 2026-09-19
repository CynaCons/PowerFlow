# Smoke recipes by platform

"Smoke" means: the real thing starts, stays up, and its own console is clean.
The commands come from the project's AGENTS.md (`smoke_command`,
`dev_command`); these recipes say how to *observe* the result without
screenshots. Run in the background, poll, then stop the process.

## Web (Vite / any dev server)

```bash
<dev_command> > .smoke.log 2>&1 &          # background
# poll up to ~30 s for the port from .claude/launch.json or the Vite banner
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/     # expect 200
grep -iE "error|exception|failed" .smoke.log | head                  # expect nothing
```

Console errors in the *browser* are not in the server log. If the
chrome-devtools MCP is loaded: one `navigate_page` + one
`list_console_messages` (filter errors) — text, not a screenshot. If it is
not, the project's e2e smoke spec (`tests/**/01-*.spec.ts`) is the console
check: Playwright's `page.on("console")` asserting zero errors.

## Desktop (Tauri)

```bash
<smoke_command> > .smoke.log 2>&1 &         # e.g. npm run tauri dev
# the process must still be alive after ~20 s (a crash exits)
grep -iE "panicked|error\[|thread .* panicked|uncaught" .smoke.log   # expect nothing
```

The Rust side prints to the log; the WebView console does not. Projects that
follow RadEAU/PowerGit expose a hidden-window CDP port for e2e — the e2e
smoke phase (launch → shell visible → one navigation) is the WebView console
check. Never smoke by killing the developer's running instance: test binaries
run under a staged executable name.

## CLI / Python tool / MCP server

```bash
<smoke_command>                             # e.g. python -m tool --version, or tools/list over stdio
echo "exit=$?"                              # expect 0
```

For an MCP server: start it over stdio with the SDK client, `initialize`,
`list_tools`, call one read-only tool. That is the smoke — not "it imports".

## Library

No process to launch: smoke = the public API round-trips on a fixture
(`python -c "import lib; lib.parse(fixture)"`) plus the packaging test.

## Embedded (D9 — partial until the reference repo is located)

The loop closes by design or not at all. In order of preference: SIL or an
emulator that runs the firmware and exposes state; a debugger interface the
agent can drive (registers, memory dump, reflash); bus read/write the agent
can observe (CAN, XCP); instruments plugged in and queryable. Reference
material to feed the agent: datasheets, MCU description files (registers,
addresses), vendor SDK/HAL example projects, the Linux kernel as a C
reference. Until the project names its observation path in AGENTS.md, this
skill can only run the unit and typecheck gates and must say so.

## Looking at it (UI work only)

One capture per changed state, via the project's capture script
(`scripts/capture-window.ps1` in PowerGit; a Playwright element-clipped shot
elsewhere), written to disk and reviewed — not pasted into the chat. DevTools
screenshots re-enter the context as images and have dominated whole sessions;
they are opt-in, on the owner's request.
