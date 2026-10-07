---
status: new
updated: 2026-10-07
---

# Validate important outputs independently against their real target

## Principle

Checks that use the producer's own spec or understanding as the standard cannot find errors in that spec or understanding. Validate each important output against its real target with a check independent of its author.

## Why it happens

Tests and code review compare code with its spec; agreement does not establish that the spec satisfies the real claim. An author reads their own text with their own context, which can hide what a reader cannot understand. Independent validation tests the missing assumption and avoids spending worker tokens on a wrong idea.

## How to apply

- **Permissions and sandboxes (rule):** Run live write probes inside and outside the working directory to check the actual permission boundary.
- **Workers' “done” (rule):** Use a test, diff read, or other-model check before accepting completion.
- **Human-facing documents (promoted rule):** Use an independent cold read with only the finished text to check what a reader understands.
- **Measuring code and emulations (lesson, not a rule):** Validate measuring code and emulations independently before launching the runs that depend on them; run each validation outside the process and state of the thing being validated.
- **Research definitions (suggestion awaiting owner approval):** When changing what a metric, baseline, estimator, or threshold means, or which samples it uses, run the cheapest falsifying test on the data that defines the claim the definition must satisfy, before writing a spec. Route such changes through W2, not W1. This suggestion is not yet a rule.

## Applies when

An important output depends on a spec, interpretation, or assumed target that its author could have misunderstood.

## Rules

- Permissions: [AGENTS privacy and review](../AGENTS.md#privacy-and-review), [handoff permission notes](../playbook/handoff.md#exact-command-interface).
- Worker completion: [Claude skill verification](../skills/claude/agents-playbook/SKILL.md#workflows-and-verification), [Codex skill verification](../skills/codex/agents-playbook/SKILL.md#workflows-and-verification), [W1 acceptance](../playbook/patterns.md#w1-spec--build--two-sided-review).
- Documents: [W6](../playbook/patterns.md#w6-structure--prose--cold-read--checked-fixes), [writing process](../playbook/writing.md#process-structure--prose--cold-read--checked-fixes).
- Research definitions: none yet; [W2](../playbook/patterns.md#w2-diverge--filter--converge) is the suggested route, pending owner approval.
