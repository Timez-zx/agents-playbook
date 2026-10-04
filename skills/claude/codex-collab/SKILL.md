---
name: codex-collab
description: >-
  Default for non-trivial coding, debugging, and review work when Claude is the
  orchestrator. Coordinate Codex workers, verify results, and route human-facing
  prose through the Writer. Never apply to a worker (AGENT_ROLE=worker or a
  prompt carrying a handoff contract).
---

# Claude orchestrates; Codex works

## Applicability

Use for non-trivial coding, debugging, and review work in an orchestrator session. Do not use for workers: `AGENT_ROLE=worker` or a prompt carrying a handoff contract excludes this skill. Workers never delegate or run either task wrapper; one coordinator keeps scope and budget controlled.

Act directly for a change below about 30 lines already in context, or when a spec costs more than the work. Persistent human-facing text still gets a Writer pass. See [roles and principles](playbook/roles.md).

## Session start

1. Run `agent-quota` (or `agent-quota --json`) to read both quotas and burn-rate advice.
2. Pick the routing mode below; compare usage with elapsed window time, not raw usage alone.
3. Confirm the user-selected role assignment. [playbook/roles.md](playbook/roles.md) is authoritative; the table here is compact.

| Role | Assignment |
|---|---|
| Orchestrator | Claude main session, opus: frame, ideate, route, decide, integrate, talk to user; run long/GPU experiments |
| Scout | Claude Explore haiku or Codex luna, read-only; return cited summaries |
| Ideator | Claude opus subagents; divergent proposals and challenges |
| Executor | Codex sol, workspace-write; implement and test |
| Verifier | Fresh Codex session; astra for critical correctness review |
| Writer | Codex sol; luna for short/simple text; all persistent human-facing prose |

GPU means graphics processing unit. Delegate large file/log reading and require compressed `file:line` summaries; protect orchestrator context.

## Routing

| Worker tier | Model / effort or purpose |
|---|---|
| Codex luna | `gpt-6-luna`, medium; mechanical work and log summaries |
| Codex reserve | `gpt-reserve`, medium; cheap agentic coding |
| Codex sol (default) | `gpt-6.1-sol`, high; implementation/review/writing; xhigh for subtle logic, concurrency, cross-module work |
| Codex astra | `gpt-6-astra`, xhigh; hardest root cause, critical review, tie-break; max only for tie-break |
| Claude haiku / sonnet / opus | Scouting / routine subtasks (default worker tier) / ideation and orchestration |

Use the cheapest plausible tier; escalate on failure. Critical-path review goes straight to astra. Never use effort `ultra`: it spawns uncontrolled agents. Full tables: [routing.md](playbook/routing.md).

| Budget mode | Action |
|---|---|
| Both healthy | Default roles |
| Claude over-burning or >70% used | Codex also scouts/writes; fewer/cheaper Claude subagents; orchestrator only decides |
| Codex over-burning or >70% used | Claude sonnet handles routine execution; save Codex for critical verification |
| Either >90% used | Only critical-path work on that side; tell user |

Over-burning means used percent > elapsed percent + 20 percentage points. The >90% rule takes priority; apply each side's restriction if both are constrained. See [budget.md](playbook/budget.md).

## Workflow

1. Feature/fix: spec → Executor in own worktree → orchestrator intent/design review + fresh Verifier correctness review → Executor fixes via resume → orchestrator re-runs acceptance → Writer writes PR text.
2. Ideation: orchestrator + 2–3 Ideators propose expected effect and cheapest falsifying test → read-only astra checks code feasibility with citations → choose → feature workflow.
3. Debugging: ranked hypotheses and discriminating log points → Executor adds throttled probes → orchestrator runs experiment → Verifier quotes supporting logs → next bisection.
4. Prototype: orchestrator validates quickly → Executor rewrites readable code under the same tests → verify.
5. Disagreement: exact disputed claim → fresh astra `-e max` without either side's reasoning, or decisive test → decide; never average positions.
6. Report: verified terse facts → read-only Writer → orchestrator checks facts unchanged → user.

Owners and reasons: [patterns.md](playbook/patterns.md). PR means pull request.

## Commands and handoffs

Give every worker Goal / Context / Scope (may change, must not change) / Requirements / Acceptance (exact commands and expected results) / Non-goals. Workers cannot see the conversation. Contracts and run records: [handoff.md](playbook/handoff.md).

```text
codex-task  <run|resume|review|peek|watch|ls> [opts]
claude-task <run|resume|review|peek|watch|ls> [opts]
agent-quota [--json]
run    [opts] (-p TEXT | -f FILE | stdin)
resume RUN_DIR [opts] (-p | -f | stdin)
review [opts] [--uncommitted | --base BR | --commit SHA] [-p | -f]
peek   RUN_DIR [N]
watch  RUN_DIR [INTERVAL_S=120] [STALL_S=600]
ls     [N]
-n NAME -t TIER -m MODEL -e EFFORT -s ro|rw|full -C DIR --net --add-dir D --raw
```

`run` starts work; `resume` follows up in the same thread/session; `review` is read-only. `-p` takes text; `-f` takes a file. `peek` returns one line per event; `watch` prints HB (heartbeat)/STALL/DONE until completion; `ls` shows recent runs, exit codes, STATUS, and usage. Resume fixes to retain context/cache; measure every run.

Use `ro` (read-only) for scouting/review, `rw` (workspace-write) for implementation, and `full` (danger-full-access) only when required. Network is enabled per task with `--net`. Both wrappers export `AGENT_ROLE=worker` and append: “You are a worker. Do not delegate to other agents and do not run codex-task or claude-task.”

Require readable code, scope discipline, stopping on ambiguity, no commit/push, and bounded final sections: STATUS: done|partial|blocked / CHANGES / VERIFICATION (run and NOT verified) / RISKS. Reviews never edit files; findings require severity, file:line, defect, trigger; otherwise NO FINDINGS.

## Verification

- Treat “done” as a claim; verify by test, diff read, or the other model.
- Assign one verifier per aspect; intent/design and correctness are separate aspects.
- Resume Executor fixes, then independently re-run acceptance; report anything not verified.
- Use fresh context for independent correctness review and unprimed tie-breaks.

## Human-facing writing

Send reports longer than about 15 lines through Codex Writer, luna/sol, `-s ro --raw`; supply facts, then check they are unchanged. Writer writes or rewrites all persistent human-facing text, including docs, PR descriptions, lessons, and review write-ups.

For short direct replies: conclusion first; one idea per short sentence; define or avoid abbreviations; use concrete facts; put required action on a separate `Action:` line; tables only for comparisons; explain internal labels; match the user's language. Repo text is English. See [writing.md](playbook/writing.md).

## End of task

1. Check for a general lesson after every task; write one for surprises, failures, measured routing outcomes, tool quirks, or human preferences.
2. Supply facts to Writer; use [lesson template](../../../lessons/README.md), unique `lessons/YYYY-MM-DD-<slug>.md`; check facts and privacy before publication.
3. Never publish private repo names, home paths, emails, hostnames, credentials, account/session identifiers, or unpublished private-work numbers; generalize evidence.
4. On main, publish only the lesson: `git pull --rebase` → `git add lessons/YYYY-MM-DD-<slug>.md` → `git commit -m "Record lesson about <topic>"` → `git push`; resolve conflicts and rebase again if needed. Workers never publish.
5. If ≥2 lessons agree or one has strong evidence, propose promotion by PR; mark supporting lessons promoted and link the rule. Skills/scripts/rules/role changes need a branch and human-approved PR under [CONTRIBUTING.md](../../../CONTRIBUTING.md).
6. Tag concrete comparisons `role-evidence`; prompt the user when evidence consistently favors another orchestrator. A swap updates roles.md and both skills' tables in one PR.
