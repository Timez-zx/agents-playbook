---
date: 2026-10-04
tags: [tooling]
status: new
agents: ["Claude orchestrator (tier not recorded)", "Codex CLI Verifier (tier not recorded)"]
---

# Put the target into a custom Codex review prompt

## Context

A review needed both a target and custom instructions using `codex exec review`.

## What happened

The command rejected `--uncommitted`, `--base`, or `--commit` combined with instructions:

```text
cannot be used with '[PROMPT]'
```

Describing the target in a custom review prompt succeeded and returned structured JSON findings.

## Lesson

Put the target in the underlying custom prompt when the CLI rejects combined arguments. Shared wrappers still accept target flags plus instructions; see [handoff](../playbook/handoff.md).

## Evidence

The first session recorded rejection and the successful workaround; later CLI versions were not independently checked.

## Applies when

Codex review requires a specific target plus instructions and rejects their argument combination.
