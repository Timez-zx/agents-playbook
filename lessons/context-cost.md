---
status: promoted
updated: 2026-10-06
---

# Reuse sessions only while their context stays small and relevant

## Principle

Carried context is resent on every call, so its cost grows with the conversation even when cached. Reuse a session only while its context is small and relevant.

## Why it happens

Each call carries earlier context alongside the current request. Cache hits can reduce cost but do not eliminate the input and time cost of resending a growing conversation. Irrelevant history spends context without helping the current decision.

## How to apply

- Resume for short fixes to the same work.
- Start a fresh session with a precise spec for large revision rounds.
- Delegate raw large files/logs and ask for compressed `file:line` summaries.
- Never preload the whole playbook; read the startup state and open other documents as needed.

## Applies when

Choosing whether to resume a worker, handing off large revisions, reading large files/logs, or loading collaboration instructions.

## Rules

- Session reuse: [Claude skill](../skills/claude/agents-playbook/SKILL.md#workflows-and-verification), [Codex skill](../skills/codex/agents-playbook/SKILL.md#workflows-and-verification), [W1](../playbook/patterns.md#w1-spec--build--two-sided-review).
- Compressed summaries: [Claude skill routing](../skills/claude/agents-playbook/SKILL.md#roles-and-routing), [Codex skill routing](../skills/codex/agents-playbook/SKILL.md#roles-and-routing), [budget efficiency](../playbook/budget.md#spend-less-without-losing-quality).
- Reading overhead: [AGENTS reading rules](../AGENTS.md#reading-and-task-overhead).
