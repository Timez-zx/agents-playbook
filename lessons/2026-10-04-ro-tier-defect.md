---
date: 2026-10-04
tags: [verification, tooling, role-evidence]
status: new
agents: ["Claude Opus front/Planner", "Codex gpt-6.1-sol Executor", "Codex gpt-6-astra Verifier"]
---

# A faithful implementation can preserve a permission error in the spec

## Context

The front specified permission tiers for `claude-task`; Executor implemented them and a fresh Verifier reviewed critical tooling.

## What happened

The front's spec required Claude Code's Bash sandbox for the read-only tier. Executor followed that spec faithfully; offline tests using fake CLI binaries passed. A live write probe by the front then showed the “read-only” worker could create files inside its working directory: the sandbox permits those writes.

An independent astra code review, without seeing the live result, reported the same defect and four more high-severity defects that live probes did not cover:

- Resume could widen permissions through a newline injected into a run name.
- Signals left workers running without an exit record.
- Installer could replace symlinks it did not own.
- Sandbox could fail open.

Root cause class: **spec/handoff**, owned and self-reported by the front. Executor's faithful implementation does not transfer ownership; front also owns verification.

## Lesson

Probe every permission tier live inside and outside the working directory. Critical tooling gets independent code review plus live probes because they catch different defects. Fix the spec and verification process; one self-reported incident is below the agent-weakness threshold.

## Evidence

The orchestrator supplied the spec, offline-pass result, live probe, and independent review findings on 2026-10-04. This records reported findings, not independent confirmation that every fix is complete. The review is astra Verifier evidence; no same-review comparison with sol was supplied. [Sandbox tests](2026-10-04-claude-worker-sandbox.md) record runtime prerequisites and corrected flags.

## Applies when

Specifying or reviewing worker permissions, resume handling, process cleanup, installation ownership, or sandbox enforcement.
