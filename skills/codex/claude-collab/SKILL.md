---
name: claude-collab
description: >-
  Use only when the user asks Codex to orchestrate and delegate to Claude.
  Coordinate Claude workers for non-trivial coding, debugging, and review work;
  verify results and route human-facing prose through the Writer. Never apply
  to a worker (AGENT_ROLE=worker or a prompt carrying a handoff contract).
---

# Codex orchestrates; Claude works

## Applicability

Inactive until the user asks Codex to orchestrate and delegate to Claude. Then use for non-trivial coding, debugging, and review work. Do not use for workers: `AGENT_ROLE=worker` or a prompt carrying a handoff contract excludes this skill. Workers never delegate or run either task wrapper; one coordinator keeps scope and budget controlled.

Act directly for a change below about 30 lines already in context, or when a spec costs more than the work. Persistent human-facing text still gets a Writer pass. See [roles and principles](playbook/roles.md).

## Session start

1. Run `agent-quota` (or `agent-quota --json`) to read both quotas and burn-rate advice.
2. Pick the routing mode below; compare usage with elapsed window time, not raw usage alone.
3. Confirm the user-selected swap. [playbook/roles.md](playbook/roles.md) is authoritative; the table here is the prepared alternative and must be aligned in the swap PR.

| Role | Assignment after user-requested swap |
|---|---|
| Orchestrator | Codex main session, own effort tiers: frame, ideate, route, decide, integrate, talk to user; run long/GPU experiments |
| Scout | Codex luna or Claude haiku via claude-task, read-only; return cited summaries |
| Ideator | Claude opus via claude-task; divergent proposals and challenges |
| Executor | Claude sonnet via claude-task, workspace-write; implement and test |
| Verifier | Fresh Codex session; astra for critical correctness review |
| Writer | Claude via claude-task, sonnet for routine prose; all persistent human-facing text |

GPU means graphics processing unit. The owner's evidence favors Claude for ideas and Codex for rigor/readability; this alternative Writer assignment needs reassessment after a swap. Delegate large file/log reading and require compressed `file:line` summaries; protect orchestrator context.

## Routing

| Own Codex tier | Model / effort or purpose |
|---|---|
| luna | `gpt-6-luna`, medium; mechanical work and log summaries |
| reserve | `gpt-reserve`, medium; cheap agentic coding |
| sol (default) | `gpt-6.1-sol`, high; implementation/review/writing; xhigh for subtle logic, concurrency, cross-module work |
| astra | `gpt-6-astra`, xhigh; hardest root cause, critical review, tie-break; max only for tie-break |
| Claude haiku / sonnet / opus | Scouting / routine subtasks (default worker tier) / ideation and orchestration |

Use the cheapest plausible tier for yourself and workers; escalate on failure. Critical-path review goes straight to astra. Never use effort `ultra`: it spawns uncontrolled agents. Full tables: [routing.md](playbook/routing.md).

| Budget mode | Action |
|---|---|
| Both healthy | User-selected roles above |
| Claude over-burning or >70% used | Codex takes Scout/Writer work too; fewer/cheaper Claude tasks; reserve orchestration for decisions |
| Codex over-burning or >70% used | Claude sonnet handles routine execution; save Codex for critical verification |
| Either >90% used | Only critical-path work on that side; tell user |

Over-burning means used percent > elapsed percent + 20 percentage points. The >90% rule takes priority; apply each side's restriction if both are constrained. See [budget.md](playbook/budget.md).

## Workflow

1. Feature/fix: spec → Claude Executor in own worktree → Codex intent/design review + fresh Verifier correctness review → Executor fixes via resume → Codex re-runs acceptance → Writer writes PR text.
2. Ideation: Codex + 2–3 Claude Ideators propose expected effect and cheapest falsifying test → read-only astra checks code feasibility with citations → choose → feature workflow.
3. Debugging: ranked hypotheses and discriminating log points → Claude Executor adds throttled probes → Codex runs experiment → Verifier quotes supporting logs → next bisection.
4. Prototype: Codex validates quickly → Claude Executor rewrites readable code under the same tests → verify.
5. Disagreement: exact disputed claim → fresh astra `-e max` without either side's reasoning, or decisive test → decide; never average positions.
6. Report: verified terse facts → read-only Claude Writer → Codex checks facts unchanged → user.

Owners and reasons: [patterns.md](playbook/patterns.md). PR means pull request.

## Commands and handoffs

Give every worker Goal / Context / Scope (may change, must not change) / Requirements / Acceptance (exact commands and expected results) / Non-goals. Workers cannot see the conversation. Contracts and run records: [handoff.md](playbook/handoff.md).

```text
claude-task <run|resume|review|peek|watch|ls> [opts]
codex-task  <run|resume|review|peek|watch|ls> [opts]
agent-quota [--json]
run    [opts] (-p TEXT | -f FILE | stdin)
resume RUN_DIR [opts] (-p | -f | stdin)
review [opts] [--uncommitted | --base BR | --commit SHA] [-p | -f]
peek   RUN_DIR [N]
watch  RUN_DIR [INTERVAL_S=120] [STALL_S=600]
ls     [N]
-n NAME -t TIER -m MODEL -e EFFORT -s ro|rw|full -C DIR --net --add-dir D --raw
```

`run` starts work; `resume` follows up in the same thread/session; `review` is read-only. `-p` takes text; `-f` takes a file. `peek` returns one line per event; `watch` prints HB (heartbeat)/STALL/DONE until completion; `ls` shows recent runs, exit codes, STATUS, and usage. Resume fixes to retain context; measure every run.

Use `ro` (read-only) for scouting/review, `rw` (workspace-write) for implementation, and `full` (danger-full-access) only when required. Network is enabled per task with `--net`. Both wrappers export `AGENT_ROLE=worker` and append: “You are a worker. Do not delegate to other agents and do not run codex-task or claude-task.”

Require readable code, scope discipline, stopping on ambiguity, no commit/push, and bounded final sections: STATUS: done|partial|blocked / CHANGES / VERIFICATION (run and NOT verified) / RISKS. Reviews never edit files; findings require severity, file:line, defect, trigger; otherwise NO FINDINGS.

## Verification

- Treat “done” as a claim; verify by test, diff read, or the other model.
- Assign one verifier per aspect; intent/design and correctness are separate aspects.
- Resume Executor fixes, then independently re-run acceptance; report anything not verified.
- Use fresh context for independent correctness review and unprimed tie-breaks.

## Human-facing writing

Send reports longer than about 15 lines through Claude Writer with `-s ro --raw`; choose its tier from routing.md, supply facts, then check they are unchanged. Writer writes or rewrites all persistent human-facing text, including docs, PR descriptions, lessons, and review write-ups.

For short direct replies: conclusion first; one idea per short sentence; define or avoid abbreviations; use concrete facts; put required action on a separate `Action:` line; tables only for comparisons; explain internal labels; match the user's language. Repo text is English. See [writing.md](playbook/writing.md).

## End of task

1. Check for a general lesson after every task; write one for surprises, failures, measured routing outcomes, tool quirks, or human preferences.
2. Supply facts to Writer; use [lesson template](../../../lessons/README.md), unique `lessons/YYYY-MM-DD-<slug>.md`; check facts and privacy before publication.
3. Never publish private repo names, home paths, emails, hostnames, credentials, account/session identifiers, or unpublished private-work numbers; generalize evidence.
4. On main, publish only the lesson: `git pull --rebase` → `git add lessons/YYYY-MM-DD-<slug>.md` → `git commit -m "Record lesson about <topic>"` → `git push`; resolve conflicts and rebase again if needed. Workers never publish.
5. If ≥2 lessons agree or one has strong evidence, propose promotion by PR; mark supporting lessons promoted and link the rule. Skills/scripts/rules/role changes need a branch and human-approved PR under [CONTRIBUTING.md](../../../CONTRIBUTING.md).
6. Tag concrete comparisons `role-evidence`; prompt the user when evidence consistently favors another orchestrator. A swap updates roles.md and both skills' tables in one PR.
