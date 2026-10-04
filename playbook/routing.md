# Routing models and effort

Choose the cheapest tier likely to succeed, then escalate after failure. Critical-path review starts at the top tier because correctness matters more than the initial saving. This file is the full model reference; only the skills repeat compact tables so names can be updated in a small, known set of places.

## Codex worker tiers

Use `codex-task -t TIER`. An explicit `-m MODEL` or `-e EFFORT` selects the model or effort for the task.

| Tier or override | Model | Effort | Use and why |
|---|---|---|---|
| `luna` | `gpt-6-luna` | `medium` | Mechanical work and log summaries; cheap context collection protects the orchestrator |
| `reserve` | `gpt-reserve` | `medium` | Cheap agentic coding; try it when the spec is routine enough to succeed |
| `sol` (default) | `gpt-6.1-sol` | `high` | Implementation, review, and writing; the usual balance of rigor and cost |
| `sol -e xhigh` | `gpt-6.1-sol` | `xhigh` | Subtle logic, concurrency, and cross-module changes; spend more reasoning on interacting behavior |
| `astra` | `gpt-6-astra` | `xhigh` | Hardest root causes, critical review, and tie-breaks; use the strongest tier where mistakes are costly |
| `astra -e max` | `gpt-6-astra` | `max` | Tie-breaks only; reserve the extra effort for an exact disputed claim |

Never use effort `ultra`. It spawns its own agents, making delegation and spending uncontrollable under this playbook.

## Claude worker tiers

Use `claude-task -t TIER`. The wrapper uses Claude Code's `claude -p` interface.

| Tier | Use and why |
|---|---|
| `haiku` | Scouting; gather bounded context cheaply |
| `sonnet` (default) | Routine subtasks; Executor fallback when Codex budget is low, to preserve critical verification capacity |
| `opus` | Ideation and orchestration; the owner's observations favor Claude for flexible high-level thinking |

## Apply routing to the task

1. Run `agent-quota` only when a task will be delegated, then choose the mode in [budget.md](budget.md). Both quotas matter for routing; small tasks skip the check because they need no delegation.
2. Choose the role from [roles.md](roles.md), then its cheapest plausible tier. A small mechanical edit and a disputed concurrency claim require different reasoning.
3. Escalate after failure with the concrete failure and acceptance criteria. Reusing the same vague prompt at a higher tier does not explain what must improve.
4. Send critical-path reviews directly to astra at `xhigh`. Use `max` only for a tie-break, so expensive effort has a defined purpose.
5. Resume an Executor thread for fixes. Retained context and cached input reduce the cost of explaining the same work again.

When Codex is the front, it uses these Codex effort tiers for itself and routes Claude worker tasks with the Claude table. Specialist roles remain as agreed unless reassigned; the human must make Codex the front and ask it to orchestrate. The opt-in skill does not activate itself, and this mode remains [unvalidated](../STATE.md).

To add another agent, supply a `<agent>-task` wrapper matching [handoff.md](handoff.md), a top-level `<AGENT>.md` evidence-linked profile, and routing rows here. Keep the shared interface so a new agent can participate without changing every handoff.
