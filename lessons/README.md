# Lessons

Record general lessons that a later session can use without the original conversation. Each lesson separates the observation from the rule it suggests. Keep evidence public and private-data-free so the repo can safely accumulate experience.

## When and who

After every task, check for something surprising: a failure mode, a routing choice that worked or failed with numbers, a tool quirk, or a human preference about output. Write a lesson when there is new evidence; do not force one from routine work. This keeps the collection useful rather than repetitive.

The orchestrator supplies facts, the Writer writes the prose, and the orchestrator checks the facts. This gives the lesson readable English without changing who is responsible for accuracy.

## Filename and template

Use one new file per lesson: `YYYY-MM-DD-<slug>.md` inside this directory. Make the slug unique and specific, so concurrent sessions do not need to edit the same file.

```markdown
---
date: YYYY-MM-DD
tags: [tooling]
status: new
agents: ["Claude orchestrator, opus", "Codex worker, sol"]
---

# A concrete lesson title

## Context

What task or environment made this relevant?

## What happened

What was observed? Keep the sequence short.

## Lesson

What should a future session do, and why?

## Evidence

Commands, safe excerpts, measurements, or links that support the claim.
State any limits on verification.

## Applies when

Which conditions make this lesson useful?
```

## Front matter

- `date`: the lesson date, so readers can assess its age.
- `tags`: one or more of `routing`, `budget`, `tooling`, `pattern`, `writing`, `environment`, `role-evidence`, so related evidence can be found.
- `status`: `new`, `promoted`, or `retired`, so readers can distinguish an observation from an adopted or obsolete rule.
- `agents`: the models or tiers involved, so an outcome is not attributed to an unspecified agent. Use the full model reference in [routing.md](../playbook/routing.md) when needed; avoid repeating model names throughout lessons.

For `role-evidence`, record a concrete comparison: who found a bug, whose design was simpler, or whose text the human preferred. Evidence tied to a task is more useful than a general claim that one brand is better.

## Publish, promote, and protect privacy

Lessons go straight to main: `git pull --rebase`, commit the new file, and push. Rebase again if concurrent work causes a conflict. Workers do not commit or push; the orchestrator publishes after checking facts. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the exact commands.

When at least two lessons agree, or one has strong evidence, open a pull request to fold the lesson into the playbook. Mark supporting lessons `promoted` and add a link to the rule. Human approval is required because a promoted rule changes behavior for every user. Mark obsolete lessons `retired` with a reason, so the evidence history remains understandable.

Generalize before publishing. Never include private repo names, paths under a user's home, emails, hostnames, credentials, account identifiers, session identifiers, or unpublished numbers from private work. Use placeholders and safe excerpts; a lesson should preserve the cause and result without identifying the original private project.

## Initial lessons

- [Ubuntu 24.04 sandbox startup](2026-10-04-ubuntu-sandbox.md)
- [Review targets and custom instructions](2026-10-04-review-target-instructions.md)
- [Cached input on resumed work](2026-10-04-resume-cache.md)
- [A separate Writer improves readability](2026-10-04-writer-readability.md)
- [Machine-readable quotas enable routing](2026-10-04-machine-readable-quotas.md)
