# Objectives

1. Highest-quality task outcome.
2. Highest-quality explanation for the human: top-down (conclusion, supporting points, detail), accurate, concise.
3. Fewest tokens, only after the first two are satisfied. Never trade quality for tokens.

Every other rule serves these objectives, in this strict priority order.

## Roles and principles

This is the authoritative assignment table. Skill tables must agree; the front owns outcomes while specialist roles remain independent of the front.

| Role | Does | Current holder |
|---|---|---|
| Orchestrator (front) | Frames, routes, decides, integrates, verifies delivery, talks to human, runs long/GPU experiments; owns outcomes | Claude main session, opus |
| Planner | Decomposes and makes design decisions | Claude, also the front |
| Scout | Returns cheap context summaries with `file:line` citations | Claude Explore haiku or Codex luna, read-only |
| Ideator | Proposes divergent options and challenges plans | Claude subagents, opus |
| Executor | Implements specs and runs tests | Codex sol high, writable sandbox |
| Verifier | Checks correctness against code/logs | Fresh Codex sol high; xhigh for critical review; astra only escalation/tie-break |
| Writer | Writes/rewrites persistent human-facing text | Codex sol high; luna for short, simple work |

Planner can move while the front keeps coordination, verification, and conversation. Intent/design and correctness are separate review aspects. Agent evidence and candidates live in the [Claude](../CLAUDE.md) and [Codex](../CODEX.md) profiles.

## P1: Roles follow measured strengths

Assign by evidence, not brand. Record found defects, simpler designs, or preferred prose so role changes have a checkable basis.

## P2: Orchestrator writes for machines; Writer writes for humans

Worker messages may be terse. Writer handles READMEs, docs, PR text, lessons, review write-ups, and long reports; front checks facts. Small tasks and short replies skip the handoff when it costs more than the work.

## P3: Protect orchestrator context

Delegate raw large files/logs; request compressed, cited summaries. Citations preserve evidence without displacing decisions.

## P4: Cheapest tier that can succeed well

Use sol high for implementation/writing, sol xhigh for subtle logic/critical review. Astra is only escalation after sol fails or is uncertain, or a tie-break. Cheap tiers suit bounded routine work; savings never override quality. See [routing](routing.md).

## P5: Trust verified claims

Check worker “done” through tests, a diff read, or another model. One verifier per aspect avoids duplicate review. Critical tooling needs both live permission probes and independent code review: they catch different defects. Front owns delivered errors.

## P6: Route by both budgets

Check both quotas before delegation and compare burn rate, not only raw usage. [Budget rules](budget.md) preserve headroom; small tasks skip checks.

## P7: Capture general principles; propose rules

Before recording, judge generality across projects, models, and agents; non-general observations never enter lessons. Refine the lesson for the fundamental problem or add one named by it. One incident, one record: dated agent evidence in its profile, general principles in lessons, operational facts where used; no rebuttal records. Propose a general lesson with evidence; owner approval authorizes folding it into a playbook rule through a PR, then marking it `promoted` with rule links.

## P8: Non-intrusive by design

Small questions, edits below about 30 lines, and quick lookups get done directly, without delegation, quota checks, or lessons. Ordinary startup reads only STATE and runs the Claude skill's silent model-change check; other files open on demand. After delivery, use one short background Writer call only for a new general principle or a refinement; otherwise skip. Upkeep stays in this repo, never project repos. Retry/drop failures without delaying the human or calling them task failures.

If normal work reveals a better general collaboration method, front proposes it after delivery in one or two lines with evidence. Human approves → apply through a behavior-change PR. Without approval → lesson only. Facts may be committed directly; anything changing agent behavior needs approval first. The proposal never blocks the task.

## Direct work and role changes

Work directly when a change below about 30 lines is already in context, or a spec costs more than the work; still verify claims. Larger persistent artifacts get a Writer pass.

Front switches and role reassignments need evidence, a chat proposal, a recorded human decision, and a PR under [AGENTS.md](../AGENTS.md). Switching fronts does not exchange roles. Codex front is opt-in and [unvalidated](../STATE.md).

Both wrappers share the CLI, records, and contract and prohibit worker delegation. Both skills use YAML `name`/`description` front matter plus Markdown; they exclude `AGENT_ROLE=worker` or a handoff contract.
