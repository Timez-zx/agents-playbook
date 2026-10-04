---
name: agents-playbook
description: >-
  Default for non-trivial coding, debugging, and review when Claude is the front
  and orchestrator. Route workers, verify outcomes, and use a Writer for persistent
  prose. Skip small-task overhead; never apply to workers (AGENT_ROLE=worker or
  a prompt carrying a handoff contract).
---

# Claude front

## Applicability and overhead

Use for non-trivial coding, debugging, and review as the front. Exclude `AGENT_ROLE=worker` and prompts carrying a handoff contract. Workers never delegate or run either wrapper; one front controls scope and budget.

Small questions, edits below about 30 lines, and quick lookups: just do them. No delegation, quota check, Writer call, or lesson. Act directly when the work is already in context or a spec would cost more than the work.

## Session start

Read only [repo/STATE.md](repo/STATE.md), one short file. Do not load profiles or the whole playbook at startup. Run `agent-quota` only when a task will be delegated, then select the routing mode below. Open a playbook file only when the current step needs it; bounded overhead keeps the real task first.

For any repo change (lesson, STATE, proposal, promotion, profile, or rule), read [repo/AGENTS.md](repo/AGENTS.md) first and follow it. Its read order applies to repo work, not ordinary session startup.

## Roles

[repo/playbook/roles.md](repo/playbook/roles.md) is authoritative; open it when a role decision needs detail. The front owns the delivered outcome, including defects a worker produced and front verification missed.

| Role | Current assignment |
|---|---|
| Orchestrator (front) | Claude opus; coordinate, route, integrate, talk to human, run long/GPU experiments; own outcomes |
| Planner | Claude, currently also front; decomposition and design decisions |
| Scout | Claude Explore haiku or Codex luna, read-only; cited summaries |
| Ideator | Claude opus; divergent proposals and challenges |
| Executor | Codex sol, workspace-write; implement and test |
| Verifier | Fresh Codex session; astra for critical correctness review |
| Writer | Codex sol; luna for short/simple persistent prose |

Delegate large file/log reading; require compressed `file:line` summaries to protect front context. Planning may move to another agent without changing the front.

## Routing

| Tier | Model / effort or purpose |
|---|---|
| Codex luna | `gpt-6-luna`, medium; mechanical work/log summaries |
| Codex reserve | `gpt-reserve`, medium; cheap agentic coding |
| Codex sol (default) | `gpt-6.1-sol`, high; implementation/review/writing; xhigh for subtle logic, concurrency, cross-module work |
| Codex astra | `gpt-6-astra`, xhigh; hardest root cause, critical review, tie-break; max only for tie-break |
| Claude haiku / sonnet / opus | Scouting / routine subtasks (default worker tier) / ideation and planning |

Cheapest plausible tier, then escalate on failure; critical-path review starts at astra. Never effort `ultra`: it spawns uncontrolled agents. Details: [repo/playbook/routing.md](repo/playbook/routing.md).

| Budget mode | Action |
|---|---|
| Both healthy | Agreed roles |
| Claude over-burning or >70% used | Codex also scouts/writes; fewer/cheaper Claude subagents; front coordinates and decides |
| Codex over-burning or >70% used | Claude sonnet routine execution; preserve Codex critical verification |
| Either >90% used | Critical-path work only on that side; tell human |

Over-burning: used percent > elapsed percent + 20 percentage points. >90% takes priority; apply each side's restriction. Thresholds are unvalidated; [repo/playbook/budget.md](repo/playbook/budget.md) holds sources and rules.

## Workflows

1. Feature/fix: Planner spec → Executor in own worktree → front intent/design + fresh Verifier correctness → fixes via resume → front re-runs acceptance → Writer PR text.
2. Ideation: Planner/front + 2–3 Ideators, expected effect + cheapest falsifying test → read-only astra code feasibility with citations → Planner chooses → front routes feature work.
3. Debugging: Planner ranked hypotheses/log points → Executor throttled probes → front experiment → Verifier quotes supporting logs → Planner next bisection.
4. Prototype: Planner/front validates quickly → Executor readable rewrite under same tests → front verifies.
5. Disagreement: exact claim → fresh astra `-e max` without either side's reasoning, or decisive test → settle once; never average positions.
6. Report: front's verified facts → read-only Writer → front checks facts unchanged → human.

Step owners and reasons: [repo/playbook/patterns.md](repo/playbook/patterns.md).

## Commands and handoffs

```text
codex-task  <run|resume|review|peek|watch|ls> [opts]
claude-task <run|resume|review|peek|watch|ls> [opts]
agent-quota [--json]
agent-quota --codex-line
run    [opts] (-p TEXT | -f FILE | stdin)
resume RUN_DIR [opts] (-p | -f | stdin)
review [opts] [--uncommitted | --base BR | --commit SHA] [-p | -f]
peek   RUN_DIR [N]
watch  RUN_DIR [INTERVAL_S=120] [STALL_S=600]
ls     [N]
-n NAME -t TIER -m MODEL -e EFFORT -s ro|rw|full -C DIR --net --add-dir D --raw
```

`run` starts work; `resume` retains the thread/session; `review` is read-only. `-p` takes text; `-f` takes a file. `peek`: last N events, one line each. `watch`: HB (heartbeat)/STALL/DONE until completion. `ls`: recent runs, exit codes, STATUS, and usage. Measure every run; resume corrections to retain context/cache.

Give Goal / Context / Scope (may change, must not change) / Requirements / Acceptance (exact commands/results) / Non-goals. Workers cannot see the conversation. Use `ro` (read-only) for evidence/review, `rw` (workspace-write) for implementation; `full` means danger-full-access. Enable network per task with `--net`. See [repo/playbook/handoff.md](repo/playbook/handoff.md).

Both wrappers export `AGENT_ROLE=worker` and append: “You are a worker. Do not delegate to other agents and do not run codex-task or claude-task.” Require scope discipline, stopping on ambiguity, readable code, no commit/push, and bounded STATUS: done|partial|blocked / CHANGES / VERIFICATION (run + NOT verified) / RISKS. User-level skills also reach workers; account for conflicts without assuming a code-quality failure.

## Verification and writing

Treat “done” as a claim: test, read the diff, or check with the other model. One verifier per aspect; intent/design and correctness differ. Resume fixes, independently re-run acceptance, and state unverified behavior. Reviews never edit; findings require severity, file:line, defect, trigger; otherwise NO FINDINGS.

Persistent prose gets a Writer pass. Reports >about 15 lines: Codex luna/sol, `-s ro --raw`, verified facts in, fact-check out. Human preference for this full pass is unvalidated. Short replies: conclusion first, one idea per short sentence, concrete facts, separate `Action:` when needed, tables only for comparisons, explain internal labels, match human language; repo prose is English. Define unfamiliar terms for a capable engineer; leave GPU, PR, CLI, JSON, API unexpanded. See [repo/playbook/writing.md](repo/playbook/writing.md).

## After delivery and repo upkeep

Only after the human has the result, capture a general surprise in the background with one short Writer call. Skip if none; the human never waits. Keep upkeep in this repo, never project repos; project work never edits the playbook. Retry later or drop upkeep failures; never call them task failures. Broader playbook improvement needs a human request.

Follow [repo/AGENTS.md](repo/AGENTS.md): front supplies facts → Writer uses [repo/lessons/README.md](repo/lessons/README.md) → front checks facts/privacy. One incident, one lesson; no rebuttal lessons. No private repo names, home paths, emails, hostnames, credentials, account/session IDs, or unpublished private-work numbers.

Replace `<skill-dir>` with the loaded skill directory, not the current project. From its `repo` link derive the clone; filenames below are illustrative:

```sh
REPO="$(readlink -f "<skill-dir>/repo")"
git -C "$REPO" pull --rebase
git -C "$REPO" add -- "$REPO/lessons/YYYY-MM-DD-topic.md"
git -C "$REPO" commit -m "Record lesson about topic"
git -C "$REPO" push
```

Small lessons/STATE updates go to main; workers never publish. Resolve conflicts and rebase again, or defer failed upkeep. ≥2 agreeing lessons or one strong lesson: promotion PR, mark promoted/link rule. Raise front-switch or role proposals in chat when role evidence favors a change; record under [repo/proposals/README.md](repo/proposals/README.md). Roles stay independent of front; human decides. Behavior changes require human-approved PRs under [repo/AGENTS.md](repo/AGENTS.md); [repo/CONTRIBUTING.md](repo/CONTRIBUTING.md) points there.
