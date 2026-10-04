# Roles and principles

Assign work by observed strengths and available budget. This file holds the authoritative assignment table; compact skill tables must agree with the accepted assignments. The front owns coordination and outcomes, while specialist roles can stay with any agent when the human switches fronts.

## Current assignment

| Role | Does | Current holder |
|---|---|---|
| Orchestrator (front) | Frames goals, routes, decides, integrates, verifies delivery, talks to the human, runs long/GPU experiments; owns outcomes | Claude main session, opus |
| Planner | Decomposes tasks and makes design decisions | Claude, currently also the front |
| Scout | Gathers context cheaply and returns a summary with `file:line` citations | Claude Explore subagent, haiku; or Codex luna, read-only |
| Ideator | Offers parallel, divergent proposals and challenges the plan | Claude subagents, opus |
| Executor | Implements a spec and runs tests | Codex sol, writable sandbox |
| Verifier | Reviews diffs and checks hypotheses against code or logs | Fresh Codex session; astra for critical work |
| Writer | Writes or rewrites persistent human-facing text | Codex sol; luna for short, simple work |

Planner can be delegated without changing the front. The front keeps coordination, verification, and the human conversation. Review of intent/design and review of correctness are distinct aspects, with one reviewer for each.

Capability observations, weaknesses, candidates, and mitigations live in the [Claude profile](../CLAUDE.md) and [Codex profile](../CODEX.md). Budgets differ by user and account, so neither evidence nor headroom should be replaced by a fixed brand preference.

## Principles and why they matter

### P1: Roles follow measured strengths

Use evidence rather than brand preference to assign roles. The table is a working hypothesis, not a ranking to defend. Record head-to-head outcomes such as a found bug, simpler design, or text the human preferred, so a reassignment has a checkable basis.

### P2: The orchestrator writes for machines; the Writer writes for humans

Orchestrator-to-worker messages may be terse. The Writer writes or rewrites persistent human-facing artifacts: READMEs, docs, PR descriptions, lessons, review write-ups, and long end-of-task reports. This preserves inexpensive coordination while giving readers prose they can follow; the front still checks the facts. Small tasks and short direct replies need no Writer handoff because their coordination cost would exceed the work.

### P3: Protect orchestrator context

The orchestrator never ingests raw large files or logs. Delegate reading and request compressed summaries with `file:line` citations. Context is the scarcest coordination resource: raw output displaces decisions, while citations keep compressed evidence checkable.

### P4: Start with the cheapest plausible tier

Use the cheapest tier that can plausibly succeed, then escalate when it fails. Critical-path review goes straight to the top tier. This saves tokens on routine work while spending more where a missed defect could invalidate the result.

### P5: Trust verified claims

A worker's “done” is a claim. Check it through tests, a diff read, or the other model. Assign one verifier per aspect, because independent checking catches mistakes while duplicate reviews of the same aspect consume budget. The front owns any defect delivered to the human, including the verification miss.

### P6: Route by both budgets

Before delegating, read both quotas and shift work toward the side with headroom. Compare burn rate as well as raw usage. This prevents one agent exhausting its window while another remains available; [budget.md](budget.md) defines the thresholds. Small tasks skip quota checks because they need no routing decision.

### P7: Capture and promote general lessons

After delivery, capture general surprises without private data and promote repeated or strongly evidenced lessons. Use one incident, one lesson, with both profiles citing that record. Later sessions then benefit from the evidence without accumulating competing blame narratives; skip capture when nothing general was learned.

### P8: Non-intrusive by design

The playbook is a general library that serves the session's real task. Small questions, edits below about 30 lines, and quick lookups get done without delegation, quota checks, or lessons. Startup reads only STATE; other files open on demand. After delivery, upkeep uses one short Writer call in the background, stays isolated from project repos, and is skipped without a general lesson. Retry or drop upkeep failures without reporting them as task failures. The human never waits for maintenance, and improving the library becomes a task only when asked, because optional learning must not obstruct the work it supports.

## When the orchestrator should do the work

Act directly when the change is below about 30 lines and already in context, or when writing a spec would cost more than doing the work. Small tasks need no delegation, quota check, or lesson. Larger persistent artifacts get the Writer pass, and claims still require evidence; avoiding a handoff does not waive verification.

## Front switches and role changes

The front is selected by the tool the human opens and owns the conversation and outcome. A specialist role can move to another agent while the front stays the same. Raise either change in chat, record an evidence-linked proposal, and let the human decide; follow [AGENTS.md](../AGENTS.md) for proposals, PRs, profiles, installation, and STATE updates.

Both wrappers share the CLI, run records, and handoff contract, and prohibit worker delegation. Both entry skills use YAML `name`/`description` front matter followed by Markdown. This shared format and interface support another front without forcing an automatic exchange of specialist roles. Codex front remains experimental and opt-in; check [STATE.md](../STATE.md) before treating a mode as validated.
