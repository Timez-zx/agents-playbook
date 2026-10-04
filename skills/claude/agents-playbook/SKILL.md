---
name: agents-playbook
description: >-
  Default for non-trivial coding, debugging, and review when Claude is front; coordinate workers, verify outcomes, use Writer for persistent prose.
  Never apply to workers (AGENT_ROLE=worker or a handoff contract).
---

# Objectives

1. Highest-quality task outcome.
2. Highest-quality human explanation: top-down (conclusion, supporting points, detail), accurate, concise.
3. Fewest tokens only after both; never trade quality for tokens. Every other rule serves these objectives, in this strict priority order.

## Applicability and startup

Use as Claude front for non-trivial coding/debugging/review. Exclude `AGENT_ROLE=worker` and prompts carrying a handoff contract. Workers never delegate or run either wrapper.

Small questions, edits below about 30 lines, quick lookups: just do them; no delegation, quota check, Writer call, or lesson. Work directly if already in context or a spec costs more than the work.

Read only [repo/STATE.md](repo/STATE.md) at startup; open other docs on demand. Run `agent-quota` only before delegation. For repo changes, read [repo/AGENTS.md](repo/AGENTS.md) first and follow its repo read order.

Run `model-review --if-stale 3 --claude-models "<the Claude model ids you know from your system context>"`. Free/silent when model lists are unchanged; only changed lists start one background Codex sol `--search` research run. Read its completed result, update [repo/playbook/models.md](repo/playbook/models.md) directly with facts/evidence/dates, mention in one line at a natural point, and propose any routing change after delivery under AGENTS (human approval required). Research is event-driven, not scheduled.

## Roles and routing

[repo/playbook/roles.md](repo/playbook/roles.md) is authoritative. Front owns delivered outcomes, including worker defects and front verification misses. Planner may move without changing front; specialist assignments survive front switches. Delegate raw large files/logs; request compressed `file:line` summaries.

| Role | Assignment |
|---|---|
| Orchestrator | Claude opus; coordinate, route, integrate, verify, talk to human, run long/GPU experiments |
| Planner | Claude, also front; decomposition/design |
| Scout | Claude Explore haiku or Codex luna, read-only; cited summaries |
| Ideator | Claude opus; divergent proposals |
| Executor | Codex sol high, rw; Claude sonnet on budget shift/accepted reassignment |
| Verifier | Fresh Codex sol high; xhigh for critical review; astra only escalation/tie-break |
| Writer | Codex sol high; luna short/simple; Claude on budget shift/accepted reassignment |

| Tier | Default effort / use |
|---|---|
| Codex luna / reserve | medium; mechanical summaries / bounded routine coding |
| Codex sol (default) | high implementation/writing/review; xhigh subtle logic, concurrency, cross-module, critical review |
| Codex astra | xhigh only after sol fails/is uncertain, or tie-break; max only tie-break |
| Claude haiku / sonnet (default) / opus | Scout / routine subtasks and budget execution fallback / ideation and planning |

Quality before cost; use cheapest plausible tier without lowering quality. Never `ultra` (uncontrolled agents). Policy: [repo/playbook/routing.md](repo/playbook/routing.md); IDs/efforts/evidence: [repo/playbook/models.md](repo/playbook/models.md).

| Budget mode | Action |
|---|---|
| Both healthy | Agreed roles |
| Claude over-burning or >70% | Codex also scouts/writes; fewer/cheaper Claude subagents; front coordinates/decides |
| Codex over-burning or >70% | Claude sonnet routine execution; preserve Codex critical verification |
| Either >90% | Critical work only on that side; tell human |

Over-burning = used percent > elapsed percent +20 points. >90% takes priority; apply each side's restriction. Thresholds unvalidated; sources: [repo/playbook/budget.md](repo/playbook/budget.md).

## Workflows and verification

1. Feature/fix: Planner spec → Executor worktree → front intent/design + fresh sol correctness (xhigh critical) → short fixes via resume → front acceptance → Writer PR text.
2. Ideation: Planner/front + 2–3 Ideators, effect + cheapest falsifying test → ro sol xhigh code feasibility/citations → Planner picks → feature workflow. Astra only after sol fails/is uncertain.
3. Debug: Planner ranked hypotheses/log points → Executor throttled probes → front experiment → Verifier cited logs → Planner bisection.
4. Prototype: Planner/front validates → Executor readable rewrite under same tests → front verifies.
5. Disagreement: exact claim → decisive test or fresh astra max without either side's reasoning → settle once; never average. Reopen only with new evidence.
6. Reports >about 15 lines, PR descriptions, README-level docs: front skeleton → fresh Writer sol high → fresh cold reader luna medium → front triages, Writer resumes fixes, front checks facts. Both workers use `-s ro --raw`; templates and rules: [W6](repo/playbook/patterns.md#w6-structure--prose--cold-read--checked-fixes).

Treat “done” as a claim: test, diff read, or other-model check; one verifier per aspect. Critical tooling gets independent code review plus live write probes inside/outside working directory. Resume short fixes; fresh precise specs for large revisions. Details: [repo/playbook/patterns.md](repo/playbook/patterns.md).

## Commands and handoffs

```text
codex-task  <run|resume|review|peek|watch|ls> [opts]
claude-task <run|resume|review|peek|watch|ls> [opts]
agent-quota [--json]
agent-quota --codex-line
run [opts] (-p TEXT | -f FILE | stdin)
resume RUN_DIR [opts] (-p | -f | stdin)
review [opts] [--uncommitted | --base BR | --commit SHA] [-p | -f]
peek RUN_DIR [N]
watch RUN_DIR [INTERVAL_S=120] [STALL_S=600]
ls [N]
-n NAME -t TIER -m MODEL -e EFFORT -s ro|rw|full -C DIR --net --add-dir D --raw
codex-task only: --search
model-review --if-stale [DAYS] [--claude-models ids] [--force] [--dry-run]
install.sh [--with-codex-front] [--uninstall]
```

`run` new; `resume` same session; `review` read-only; `-p` text/`-f` file. `peek` last N events, one line each; `watch` HB/STALL/DONE until end; `ls` recent agent runs, exit code, STATUS, usage. Both wrappers record tokens.

Give Goal / Context / Scope (may/must not change) / Requirements / Acceptance (exact commands/results) / Non-goals. Workers cannot see conversation. Codex ro/rw = read-only/workspace-write; network per task via `--net`. Claude ro = read-only commands, no tests, Bash sandbox explicitly disabled; rw = sandboxed Bash writes inside working directory, no network. Full = no restrictions. Linux requires bubblewrap + socat. [repo/playbook/handoff.md](repo/playbook/handoff.md) holds exact records/interface.

Both wrappers export `AGENT_ROLE=worker` and append: “You are a worker. Do not delegate to other agents and do not run codex-task or claude-task.” Require scope, stop on ambiguity, readable code, no commit/push, bounded STATUS/CHANGES/VERIFICATION (run + NOT verified)/RISKS. User-level skills also reach workers; account for conflicts without assuming code-quality failure. Reviews never edit; report severity, file:line, defect, trigger or NO FINDINGS.

Persistent prose gets Writer pass; front supplies structure and evidence, then checks facts. Short replies follow [repo/playbook/writing.md](repo/playbook/writing.md) directly: standalone claims, same-kind points, comfortable paragraphs, plain description before technical terms. Keep prose top-down, accurate, concise; use concrete facts, tables for comparisons, and a separate `Action:` if needed. Match human language; repo English.

## After delivery and upkeep

After result, one short background Writer call may record a general surprise; skip if none. Human never waits. Upkeep stays in this repo, never project repos; project work does not edit playbook. Retry/drop failures without calling them task failures.

When normal work reveals a better general collaboration method, front proposes it after delivery in one or two lines with evidence. Human approves → behavior-change PR; unapproved → lesson only. Front supplies facts → Writer uses [repo/lessons/README.md](repo/lessons/README.md) → front checks facts/privacy. One incident/lesson; no rebuttals. No private repo names, home paths, emails, hostnames, credentials, account/session IDs, unpublished private numbers.

Derive clone from loaded skill's `repo` link, not project/install directory; replace illustrative placeholders:

```sh
REPO="$(readlink -f "<skill-dir>/repo")"
git -C "$REPO" pull --rebase
git -C "$REPO" add -- "$REPO/lessons/YYYY-MM-DD-topic.md"
git -C "$REPO" commit -m "Record lesson about topic"
git -C "$REPO" push
```

Small lessons/STATE/model-fact updates go to main; workers never publish. Resolve/rebase conflicts or defer upkeep. ≥2 agreeing lessons or one strong lesson justify promotion proposal; approval first, then PR and promoted/link rule. Role/front proposals: chat then [repo/proposals/README.md](repo/proposals/README.md); human decides. Behavior changes need approval and PR/merge review under AGENTS; [repo/CONTRIBUTING.md](repo/CONTRIBUTING.md) points there.
