---
date: 2026-10-04
tags: [writing, role-evidence, pattern]
status: new
agents: ["Claude orchestrator (tier not recorded)", "Codex Writer (tier not recorded)"]
---

# Give human-facing reports a separate Writer pass

## Context

The owner read a dense status update from Claude during the first session. The update's meaning was difficult to follow.

## What happened

The human asked, “what does that mean?” The owner reported that Claude's explanations were harder to read and that Codex's reports read more easily. That feedback led to separating machine-facing coordination from human-facing writing.

## Lesson

Have the orchestrator supply facts and the Writer turn them into readable prose. For end-of-task reports longer than about 15 lines, use a report pass and then check that the facts are unchanged. This addresses the observed readability problem without changing who owns the decisions.

Short replies can come directly from the orchestrator using the [writing rules](../playbook/writing.md). Persistent human-facing text gets a Writer pass so a later reader does not need the original conversation.

## Evidence

The evidence is the human's stated preference after the dense update, not an objective comparison of all Claude and Codex output. It informed the [Writer principle](../playbook/roles.md) and [report workflow](../playbook/patterns.md).

## Applies when

The current user finds one agent's writing easier to follow. Record further preferences as `role-evidence`; reassess the Writer assignment if the user's evidence changes.
