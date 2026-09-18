# D9 — autosar-101-training

Status: Open · 2026-09-18

## Context

The owner named `autosar-101-training` as part of the corpus. It is not on
this machine (`C:\dev\LIDAR\Config\AUTOSAR` is the only AUTOSAR path). The
training deck's Part F5 describes embedded close-the-loop practice (SIL,
debugger interfaces, CAN/XCP read–write, datasheets, MCU description files,
vendor SDKs, the Linux kernel as C reference) that `powerflow-verify` should
carry for embedded targets.

## Decision

Deferred. `powerflow-verify` ships with the web/desktop gate first. The
embedded profile is a backlog item until the repo is located or the owner
summarises its methodology angle.

## Consequences

- A `platform: embedded` answer in `powerflow-init`'s interview is accepted
  and recorded, but the verify skill only prints the deck's F5 checklist for
  it until this decision closes.
