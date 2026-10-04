---
date: 2026-10-04
tags: [writing, role-evidence, pattern]
status: new
agents: ["Claude orchestrator (tier not recorded)", "Codex Writer (tier not recorded)"]
---

# Give human-facing reports a separate Writer pass

## Context

The owner found a dense Claude status update hard to follow.

## What happened

The human asked, “what does that mean?” The owner said Claude explanations were harder to read and Codex reports read more easily. This informed separation of coordination from human-facing writing.

## Lesson

Front supplies facts; Writer turns them into readable prose; front checks facts unchanged. Persistent text gets a Writer pass; reports over about 15 lines use the [report workflow](../playbook/patterns.md). Short replies use the [writing rules](../playbook/writing.md) directly. Front keeps decision and evidence ownership.

## Evidence

This is the human's preference, not an objective comparison of all output. It informed the [Writer principle](../playbook/roles.md); preference for the full report workflow remains [unvalidated](../STATE.md).

## Applies when

A user prefers one agent's prose. Record further preferences as role evidence and reconsider Writer assignment if evidence changes.
