---
date: 2026-10-04
tags: [budget, tooling]
status: new
agents: ["Codex gpt-6.1-sol Writer"]
---

# Resume short fixes; start large revision rounds fresh

## Context

Two substantial documentation rounds used a fresh Writer thread followed by a large revision on the same thread.

## What happened

The fresh run used 299k input tokens (264k cached) in 12.8 minutes. The next large revision resumed that thread and used 1.33M input tokens (1.23M cached) in 17.4 minutes. Each step re-sent the whole growing thread.

Short resumed follow-ups were cheap, with 90–97% cached input. This round is the first application of the fresh-session approach for a large revision.

## Lesson

Resume short fixes that benefit from retained context. For large revision rounds, start a fresh session with a precise spec. A high cache percentage does not remove the input and time cost of a growing thread.

## Evidence

The orchestrator supplied these run totals and durations for public lesson evidence on 2026-10-04. The comparison is two runs of different scope, not a controlled benchmark or a monetary-cost calculation. Earlier [Codex resume](2026-10-04-resume-cache.md) and [Claude resume](2026-10-04-claude-worker-sandbox.md) observations support short follow-up caching.

## Applies when

Choosing whether to resume a documentation worker for corrections or start a substantial new revision round.
