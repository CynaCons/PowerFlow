---
name: powerflow-prd
description: Write a project's PRD.md once, at the start, or rewrite it on an owner-declared change of direction — and refuse routine PRD edits by redirecting them to a decision record, an SRS row or a PLAN task. Use this when the user says "write the PRD", "product requirements", "let's define the product", when a fresh project has a skeleton PRD to fill, or when the user says the product is changing direction ("we're pivoting", "the target is now X", "forget the old scope"). Also use it — to redirect — whenever someone reaches for PRD.md to record a constraint, a behaviour, a task or a status: those do not belong there.
---

# powerflow-prd — once, then leave it alone

The PRD is the stable reference for what the product is, for whom, on what
stack, under which principles and quality bar. It is written when a project
starts, iterated with the owner until it can guide the rest, and rewritten
only on a major change of direction that the owner declares (METHODOLOGY.md
§2.1, D10). Everything else that looks like a PRD edit is one of three other
things, and this skill's first job is to say which.

## 0. Which of the four cases is this?

| The owner wants to… | Do |
|---|---|
| Start a project (PRD is a stamped skeleton) | **Write it** — §1 below, once, in one conversation |
| Change the product's direction (new target user, new core, a principle reversed) | **Redirect the product** — §2: a decision first, then a PRD revision with a new status line |
| Record a constraint, a chosen alternative, a "we will not" | `powerflow-decide` — decisions live in `docs/decisions/`; the PRD only lists them |
| Specify a behaviour, a threshold, an interaction rule | `powerflow-srs` — rows, with IDs |
| Add work, note progress, mark something done | `powerflow-plan` — the PRD never carries status |

Say which case it is in one sentence and proceed. Refusing a routine edit is
not obstruction: it keeps the PRD trustworthy, which is why agents can read
it before inventing product behaviour.

## 1. Writing it — the one time

The stamped `PRD.md` (`templates/PRD.md`) has the sections with HTML-comment
prompts. Walk them with the owner in **one question round**, offering a
default for each so a "yes" is a complete answer:

1. **Problem** — what hurts, for whom, why existing tools do not fix it;
   measured failure modes if any.
2. **Users** — the primary user's job; the owner; the agents (they are users
   of the methodology parts).
3. **Principles** — numbered rules that will settle arguments later. Keep the
   product-specific ones; the method's own live in METHODOLOGY.md.
4. **Product shape** — architecture in one picture or paragraph; in scope
   for v1 (named by the owner), explicitly out.
5. **Stack** — the table, including the single version source and the
   agent-methodology row.
6. **Quality bar** — smoke rule, SRS coverage rule, `showcase: required|optional`
   (D8), the product's numbers (performance, platforms, a11y).
7. **Methodology constraints specific to this project** — only what
   sharpens the method for this product (real binary over CDP, raw sleeps
   banned, one theme token source…). Delete the section if nothing is.
8. **Non-goals**, 9. **Decisions to record** (the table `powerflow-decide`
   fills), 10. **Success criteria** — measurable.

Write what the owner says; do not pad. A section the owner did not answer
keeps its comment — a skeleton is more honest than invented users. Iterate
in the same conversation until the owner says it can guide the rest, then
tick the PLAN task ("Write PRD.md") with the commit as evidence and record
the listed decisions (`powerflow-decide`).

## 2. Redirecting the product

A direction change is declared by the owner, in their words. Then, in order:

1. `powerflow-decide`: `D<n> — <the redirection>` with Context (what changes
   and why), Decision (the new direction, what is dropped), Consequences
   (which SRS rows are withdrawn, which iterations are superseded, the gate).
2. Revise the PRD: new **Status** line (`PRD revision <date> — <reason>, see
   D<n>`), rewrite the affected sections, keep the rest. Do not rewrite
   history in the sections that did not change.
3. `powerflow-plan`: close or supersede the iterations the decision names;
   open the first iteration of the new direction; backlog what is parked.
4. `powerflow-srs`: withdraw rows (`(withdrawn <date>: D<n>)`), never delete.

RadEAU's "Ethernet-first rework" and PowerGit's "keep C# on Linux" are the
shape of it: one decision, one PRD revision, the plan re-pointed.

## Report

```
PRD.md — <written | revised (D<n>) | not touched: redirected to powerflow-<decide|srs|plan>>
  sections filled: <list> · still skeleton: <list>
  decisions listed: D1..D<k> (<m> recorded)
  PLAN: "Write PRD.md" ticked (<sha>) | iterations re-pointed: <…>
```

Then the miniplan (D12) when the plan changed.

## What not to do

- Do not touch PRD.md for a constraint, a behaviour or a task.
- Do not revise the PRD without a decision naming the redirection.
- Do not fill sections the owner did not answer.
- Do not keep a "Recent changes" or status section in the PRD — status is
  the plan's.
