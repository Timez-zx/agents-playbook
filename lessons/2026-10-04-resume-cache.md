---
date: 2026-10-04
tags: [tooling, budget]
status: new
agents: ["Claude orchestrator (tier not recorded)", "Codex Executor (tier not recorded)"]
---

# Resume short follow-ups to reuse context and cached input

## Context

An Executor needed a follow-up in an existing Codex thread.

## What happened

`codex exec resume <thread> -` retained context. The measured first follow-up had about 53k of 58k input tokens cached (~90%).

## Lesson

Use `codex-task resume RUN_DIR` for short fixes to the same work. Retained context avoids restating the task; cached input can reduce cost. For large revisions, follow the later [thread-growth evidence](2026-10-04-thread-growth-cost.md).

## Evidence

The initial session supplied the 53k/58k measurement and successful context reuse. It establishes neither a guaranteed cache rate nor fixed monetary savings.

## Applies when

The same Executor is fixing or briefly continuing work. Independent verification uses a fresh session.
