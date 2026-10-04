---
date: 2026-10-04
tags: [tooling]
status: new
agents: ["Codex sol"]
---

# User-level skills also reach delegated workers

## Context

A delegated Codex worker was executing a task on a machine with user-level Codex skills. Its handoff contract specified the task's scope and working rules.

## What happened

The worker announced that it was applying a user-level skill that pushes minimal implementations. Delegation had not isolated the worker from the machine's user-level skills or instruction files.

## Lesson

Account for user-level skills and instruction files when delegating. They apply to workers too and can reinforce or conflict with the handoff contract. A clear worker contract remains necessary, but it is not the only instruction source the worker receives.

Do not treat the announcement alone as a code-quality failure or an agent weakness. Its outcome on code quality has not yet been assessed. Both profiles cite this one lesson so the observation does not become competing accounts of the same incident.

## Evidence

The evidence is the delegated Codex sol worker's announcement that it was applying a skill favoring minimal implementations. The supplied observation establishes instruction reach; no code-quality outcome was supplied or independently assessed.

## Applies when

Delegating to any agent on a machine with user-level skills or instruction files.
