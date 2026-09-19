<!-- placeholders: project, one_liner, github, date, stack, platform, showcase, version_source -->
# {{project}} — Product Requirements

**One-liner:** {{one_liner}}

**Home:** {{github}}

Status: PRD {{date}} — written once at project start (PowerFlow D10); rewritten
only on a major change of direction, declared by the owner and recorded as a
decision. Build plan: [PLAN.md](PLAN.md). Requirements: [docs/srs/](docs/srs/README.md).
Method: [PowerFlow METHODOLOGY.md](https://github.com/CynaCons/PowerFlow/blob/main/METHODOLOGY.md).

---

## 1. Problem

<!-- What hurts today, for whom, and why existing tools do not fix it. Two or
three paragraphs. Name the measured failure modes if there are any. -->

## 2. Users

- **Primary user:** who they are, what job they come to do.
- **The owner:** reads PLAN.md, arbitrates scope, closes owner reports.
- **Coordinator and worker agents:** operate PLAN.md through powerplan; keep
  memories in `docs/agents/`.

## 3. Product principles

<!-- Numbered. Each one a rule that settles arguments later. Keep the ones that
are specific to this product; the method's own rules live in METHODOLOGY.md. -->

1.
2.
3.

## 4. Product shape

<!-- The architecture in one diagram or one paragraph, then scope. -->

### In scope (v1)

1.

### Explicitly out of v1

-

## 5. Stack

| Layer | Choice |
|---|---|
| | {{stack}} |
| Platform | {{platform}} |
| Version source | `{{version_source}}` — the only file that carries the version; everything else derives from it |
| Agent methodology | PowerFlow: powerplan (PLAN.md single writer), PowerSpawn (workers), `docs/srs/`, `docs/decisions/`, `docs/agents/` |

## 6. Quality bar

- Smoke: the app launches without a crash or console error on the current
  platform before an iteration is called complete.
- Every named feature has an SRS file before it ships; every requirement row
  gains a test path before it is called verified.
- `showcase: {{showcase}}` — when `required`, an iteration closes only with a
  published artifact captured from the running app (PowerFlow D8).
<!-- Add the product-specific bars: performance numbers, platforms, a11y. -->

## 7. Methodology constraints specific to this project

<!-- Only what differs from or sharpens METHODOLOGY.md: e.g. "tests drive the
built binary over CDP", "one spectrum module serves both views", "raw sleeps
banned". Delete the section if nothing is specific. -->

## 8. Non-goals

-

## 9. Decisions to record (docs/decisions/)

Each requires one written decision before the affected part is built.

| # | Decision | Default recommendation |
|---|---|---|
| D1 | | |

## 10. Success criteria

-
