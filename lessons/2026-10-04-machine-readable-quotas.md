---
date: 2026-10-04
tags: [budget, routing, tooling]
status: new
agents: ["Claude Code (tier not recorded)", "Codex CLI (tier not recorded)"]
---

# Read both quotas before routing work

## Context

Agents had separate usage budgets; routing needed to follow available headroom.

## What happened

Both quota sources were machine-readable. Codex recorded `rate_limits` in session events. Claude desktop exposed `get_usage`; its CLI emitted `rate_limit_event` with window utilization/reset times.

## Lesson

Before delegation, use `agent-quota` rather than memory. Compare both sides' burn rates with elapsed window time; raw usage can hide fast spending. Small tasks skip the check.

## Evidence

[Budget sources](../playbook/budget.md): Codex `primary.used_percent`, `primary.window_minutes`, `primary.resets_at`, `plan_type`, `credits.balance`; Claude desktop `percentUsed`/`resetsAt`; CLI `rate_limit_info.unifiedWindows.<window>.utilization`/`resetsAt`. These sources were readable in the first session; later clients/accounts may differ.

## Applies when

Both agents have separate quota windows and recorded usage sources are available.
