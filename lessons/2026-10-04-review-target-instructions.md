---
date: 2026-10-04
tags: [tooling]
status: new
agents: ["Claude orchestrator (tier not recorded)", "Codex CLI Verifier (tier not recorded)"]
---

# Put the target into a custom Codex review prompt

## Context

The session needed a Codex review with both a specific target and custom instructions. The underlying command was `codex exec review`.

## What happened

The command rejected a target flag (`--uncommitted`, `--base`, or `--commit`) combined with custom instructions. Its error included:

```text
cannot be used with '[PROMPT]'
```

Describing the target in the prompt and running a custom review avoided the incompatible argument combination. The custom review returned structured JSON (JavaScript Object Notation) findings.

## Lesson

When using the underlying Codex command with custom instructions, put the intended target in the prompt rather than combine it with a target flag. This preserves the review scope while avoiding the command's argument restriction. The shared wrappers' public interface still accepts target flags and instructions; see [handoff.md](../playbook/handoff.md).

## Evidence

The first session recorded the rejection and the successful custom-review workaround. This lesson describes the observed command behavior; it does not independently verify later CLI versions.

## Applies when

A Codex review needs both a target and custom instructions, and the underlying CLI rejects that combination.
