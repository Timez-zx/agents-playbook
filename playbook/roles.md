# Roles and principles

Assign work by observed strengths and available budget. This file holds the authoritative role table; the compact tables in the skills must agree with the user-selected orchestration direction. Evidence can change the assignments without changing what each role does.

## Current assignment

| Role | Does | Current holder |
|---|---|---|
| Orchestrator | Frames, ideates, decomposes, routes, decides, integrates, talks to the user, runs long or graphics processing unit (GPU) experiments | Claude main session, opus |
| Scout | Gathers context cheaply and returns a summary with `file:line` citations | Claude Explore subagent, haiku; or Codex luna, read-only |
| Ideator | Offers parallel, divergent proposals and challenges the plan | Claude subagents, opus |
| Executor | Implements a spec and runs tests | Codex sol, writable sandbox |
| Verifier | Reviews diffs and checks hypotheses against code or logs | Fresh Codex session; astra for critical work |
| Writer | Writes or rewrites all persistent human-facing text | Codex sol; luna for short, simple work |

The roles separate different kinds of judgment. In particular, the orchestrator checks intent and integration, while the Verifier checks correctness. These are distinct aspects, not duplicate reviews.

## Capability observations

The owner has found Claude smarter, more flexible, and more creative at high-level ideas. Claude's written feedback has also been harder for the owner to read: dense prose, jargon, unexplained abbreviations, and skipped steps. The owner has found Codex more rigorous and detailed, with writing that is easier to follow. These are observations from one user's experience, not universal truths.

Budgets differ by user and account. The goal is to spend each token where it helps most, rather than preserve an assignment when evidence or headroom changes.

## Principles and why they matter

### Roles follow measured strengths

Use evidence rather than brand preference to assign roles. The table is a working hypothesis, not a ranking that must be defended. Record head-to-head observations so future changes reflect actual outcomes: a found bug, a simpler design, or text the human could understand.

### The orchestrator writes for machines; the Writer writes for humans

Orchestrator-to-worker messages may be terse. The Writer writes or rewrites every persistent human-facing artifact: READMEs, docs, pull request descriptions, lessons, review write-ups, and long end-of-task reports. This preserves inexpensive coordination while giving readers explanations they can follow; the orchestrator still checks that the facts did not change.

### Protect orchestrator context

The orchestrator never ingests raw large files or logs. Delegate reading and request compressed summaries with `file:line` citations. Context is the scarcest orchestration resource: filling it with raw output leaves less room for decisions, and citations make the compressed evidence checkable.

### Start with the cheapest plausible tier

Use the cheapest tier that can plausibly succeed, then escalate when it fails. Critical-path review goes straight to the top tier. This saves tokens on routine work while spending more where a missed defect could invalidate the result.

### Trust verified claims

A worker's “done” is a claim. Check it through tests, a diff read, or the other model. Assign one verifier per aspect, because independent verification catches mistakes but repeated reviews of the same aspect waste budget without a clear purpose.

### Route by both budgets

Read both quotas and shift load toward the side with headroom. Use burn rate as well as raw usage. This keeps one agent from exhausting its window while the other remains available; [budget.md](budget.md) defines the thresholds.

### Capture and promote general lessons

After every task, check for a general lesson and record surprising evidence without private data. Promote repeated or strongly evidenced lessons into the playbook. This makes later sessions benefit from earlier work rather than rediscover the same failure modes.

## When the orchestrator should do the work

Act directly when the change is below about 30 lines and already in context, or when writing a spec would cost more than doing the work. Handoffs have a cost; avoid them when they add no useful separation. Persistent human-facing text still gets a Writer pass, and all claims still need verification.

## Swapping the agents

Both worker tools use the same command interface, run directory layout, and handoff contract. `codex-task` runs Codex CLI; `claude-task` runs Claude Code through `claude -p`. Both export `AGENT_ROLE=worker`, and both prohibit worker delegation, so switching tools does not create recursive orchestration.

The two entry skills use YAML front matter with `name` and `description`, followed by Markdown. Claude Code and Codex share this skill format. The Claude entry is active today. The Codex entry applies only when the user asks Codex to orchestrate and delegate to Claude.

1. Record comparisons in lessons tagged `role-evidence`. Use concrete outcomes so the user can judge the evidence.
2. If lessons consistently favor the other agent for orchestration work, prompt the user to decide. A role change needs the user's judgment, not an automatic ranking.
3. After the user chooses a swap, update this table and both skills' role tables in one pull request. Keep the alternative entry aligned with the new direction so sessions do not receive inconsistent instructions.
4. Have the human approve the merge under [CONTRIBUTING.md](../CONTRIBUTING.md). A role change affects every user who loads the skills.

For Codex orchestration, Codex coordinates and uses its own effort tiers from [routing.md](routing.md). Claude via `claude-task` supplies Ideator, Executor, and Writer work, with tiers chosen from the same routing guide. This is the prepared alternative, not evidence that Claude has become the stronger Writer; reassess assignments from the user's observations after a swap.
