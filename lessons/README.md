# General lessons

Lessons hold general principles, not cases or behavior changes. Before recording anything, judge whether the observation would recur across projects, models, and agents. If it is not general, record no lesson and do not merge it into a class. Operational facts belong where used (install, handoff, budget, or routing notes); agent-specific evidence belongs in that agent's profile with its date.

For a general observation, identify the fundamental problem. Refine the wording or “How to apply” items of the lesson already covering it; otherwise add one lesson named by that problem, `<problem>.md`. State the principle only; never narrate cases.

After delivery, use one short background Writer call only for a new general principle or a refinement. Front supplies facts and checks prose/privacy. Human never waits; upkeep stays in this repo. Retry/drop failures without making them task failures. One incident, one record; no rebuttal records. Follow [AGENTS.md](../AGENTS.md).

## Template

```markdown
---
status: new|promoted
updated: YYYY-MM-DD
---

# <principle as a title>

## Principle

The general principle.

## Why it happens

The underlying mechanism.

## How to apply

Concrete checks or actions; distinguish suggestions awaiting approval from rules.

## Applies when

Conditions where the principle helps.

## Rules

Links to promoted rules, or “none yet”.
```

## Publication, promotion, and retirement

General lesson additions/refinements, small STATE updates, and model-catalog facts may go directly to main after front fact/privacy review: pull/rebase → add `lessons/<problem>.md` → commit → push. Workers never commit/push. Resolve/rebase conflicts or defer upkeep; exact commands are in [AGENTS.md](../AGENTS.md#facts-small-direct-commits-to-main).

Propose a general lesson for promotion with evidence after delivery. Owner approval authorizes folding it into a playbook rule through a PR; mark it `promoted` and link the rules. Unapproved suggestions remain lessons. Retire obsolete lessons with a reason in the change; preserve history. Keep the set small: when lessons with `status: new` exceed about eight, the next repo-maintenance session merges, promotes, or retires before adding.

Never publish private repo names, home paths, emails, hostnames, credentials, account/session IDs, or unpublished private numbers. Generalize observations; follow [writing.md](../playbook/writing.md) and [privacy policy](../AGENTS.md#privacy-and-review).

Case records written before this restructuring are in git history before this change.

## Index

- [Independent validation](independent-validation.md) — `new`: Validate important outputs against their real target with a check independent of the author; existing applications are rules, while the research-definition check awaits approval.
- [Context cost](context-cost.md) — `promoted`: Reuse a session only while its carried context is small and relevant, because it is resent on every call even when cached.
