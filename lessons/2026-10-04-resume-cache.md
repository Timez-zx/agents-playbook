---
date: 2026-10-04
tags: [tooling, budget]
status: new
agents: ["Claude orchestrator (tier not recorded)", "Codex Executor (tier not recorded)"]
---

# Resume follow-ups to reuse context and cached input

## Context

An Executor needed a follow-up in an existing Codex thread. Restarting would have required supplying the same task context again.

## What happened

`codex exec resume <thread> -` retained the context. In the measured first follow-up turn of the same thread, about 53k of 58k input tokens were cache hits: approximately 90%.

## Lesson

Use `codex-task resume RUN_DIR` for fixes and follow-ups to the same work. Retained context avoids restating the task, and cached input can make the turn cheaper. Treat the measured cache rate as evidence from one follow-up, not a guarantee for every resumed task.

## Evidence

The initial session supplied the 53k cached / 58k total input-token measurement. The underlying resume command and the retained context support the reuse rule. No claim is made about a fixed monetary saving.

## Applies when

The same Executor is addressing findings or continuing a task. Use a fresh session for an independent Verifier when fresh context is part of the review design.
