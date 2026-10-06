# Lessons

Lessons record facts and suggested improvements; they do not change behavior. After delivery, capture a general surprise from substantial work: failure, measured routing outcome, tool quirk, or human output preference. Small tasks need no lesson; skip if nothing general was learned.

Use one short background Writer call. Front supplies facts, Writer writes, front checks facts/privacy. Human never waits; upkeep stays in this repo. Retry/drop failures without calling them task failures. One incident has one lesson; relevant profiles cite that record, never rebuttal lessons. Follow [AGENTS.md](../AGENTS.md).

## Template

Use a unique `YYYY-MM-DD-<slug>.md` here:

```markdown
---
date: YYYY-MM-DD
tags: [tooling]
status: new
agents: ["Claude orchestrator, opus", "Codex worker, sol"]
---

# Concrete lesson title

## Context

Relevant task/environment.

## What happened

Observed facts; short sequence.

## Lesson

Suggested improvement and reason; not automatic adoption.

## Evidence

Commands, safe excerpts, measurements, links, verification limits.

## Applies when

Conditions where it helps.
```

Tags: `routing`, `budget`, `tooling`, `pattern`, `writing`, `environment`, `verification`, `role-evidence`. Status: `new`, `promoted`, `retired`. Agents identify models/tiers; exact model reference is [models.md](../playbook/models.md). Record `role-evidence` as concrete comparisons or dated owner statements, not brand rankings.

## Publication and promotion

Facts may go directly to main: pull/rebase → add unique lesson → commit → push. Front publishes after review; workers never commit/push. Resolve/rebase conflicts or defer upkeep. Exact commands and privacy policy: [AGENTS.md](../AGENTS.md).

Two agreeing lessons or one strong lesson justify a short evidence-based proposal after delivery. Human approves → behavior-change PR; unapproved → lesson only. Mark adopted support `promoted` with a rule link after approval; retire obsolete lessons with a reason. Never publish private repo names, home paths, emails, hostnames, credentials, account/session IDs, or unpublished private numbers; use generalized evidence.

## Recorded lessons

- [Ubuntu sandbox startup](2026-10-04-ubuntu-sandbox.md)
- [Review targets and instructions](2026-10-04-review-target-instructions.md)
- [Cached Codex resume](2026-10-04-resume-cache.md)
- [Writer readability](2026-10-04-writer-readability.md)
- [Machine-readable quotas](2026-10-04-machine-readable-quotas.md)
- [User-level skills reach workers](2026-10-04-user-skills-reach-workers.md)
- [Claude worker sandbox/live resume](2026-10-04-claude-worker-sandbox.md)
- [Read-only spec defect and independent review](2026-10-04-ro-tier-defect.md)
- [Research definition changes need a falsifying test first](2026-10-06-definition-change-falsify-first.md)
- [Large-thread growth cost](2026-10-04-thread-growth-cost.md)
- [Owner's sol routing decision](2026-10-04-sol-routing-default.md)
