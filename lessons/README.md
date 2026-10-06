# General lessons

Lessons hold general principles, not cases or behavior changes. Roles (front, Writer, workers), STATE, and workflows W1–W6 are defined in [AGENTS.md](../AGENTS.md) and [patterns.md](../playbook/patterns.md).

Before recording anything, ask: would this observation change how an agent works on a different project, with a different model or tool? If yes, it is general. If it concerns one tool, environment, person, or project, it is not general: record no lesson. Put such an operational fact where it is used (install, handoff, budget, or routing notes), an owner preference in the rule document it affects (for example writing.md or routing.md), and agent-specific evidence, dated, in that agent's profile.

For a general observation, identify the fundamental problem behind it. If a lesson already states that problem, change it only when the observation adds a new kind of work where the principle applies (a new “How to apply” item) or corrects its wording; otherwise change nothing. If no lesson states that problem, add a new lesson file named after the problem, for example `independent-validation.md`. State the principle only; never narrate cases.

- After delivery, make at most one short background Writer call, and only for a new principle or a refinement.
- The front supplies facts and checks prose and privacy.
- Upkeep stays in this repo and never makes the human wait; retry or drop failed upkeep without reporting it as a task failure.
- One incident, one record: a lesson refinement, a dated profile entry, or a fact in the document that uses it; no rebuttal records.

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

- [Validate important outputs independently against their real target](independent-validation.md) — `new`: a check that uses the author's own spec or understanding cannot find errors in it; existing applications are rules, while the research-definition check awaits approval.
- [Reuse sessions only while their context stays small and relevant](context-cost.md) — `promoted`: carried context is resent on every call, even when cached.
