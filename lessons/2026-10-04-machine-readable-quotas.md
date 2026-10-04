---
date: 2026-10-04
tags: [budget, routing, tooling]
status: new
agents: ["Claude Code (tier not recorded)", "Codex CLI (tier not recorded)"]
---

# Read both quotas before routing work

## Context

The agents had separate usage budgets. The playbook needed to shift work toward whichever side had headroom.

## What happened

Both quota sources were machine-readable. Codex recorded a `rate_limits` object in session rollout events. Claude Code desktop exposed `get_usage`; Claude's command-line stream emitted `rate_limit_event` with window utilization and reset times.

## Lesson

Use `agent-quota` at session start rather than estimate usage from memory. Read both sides and compare burn rate with elapsed window time. Machine-readable data makes routing advice automatic and repeatable, while raw percent alone can conceal an early fast drain.

## Evidence

The [budget source reference](../playbook/budget.md) names the observed fields: Codex's `primary.used_percent`, `primary.window_minutes`, `primary.resets_at`, `plan_type`, and `credits.balance`; Claude desktop's `percentUsed` / `resetsAt`; and CLI `rate_limit_info.unifiedWindows.<window>.utilization` / `resetsAt`. The first session established that the sources were readable; it did not prove that every later client or account exposes identical data.

## Applies when

Both agents have separate quota windows and their recorded usage sources are available. Routing should follow actual headroom, not an assumed preference for one agent.
