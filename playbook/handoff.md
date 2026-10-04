# Handoffs and command reference

Workers cannot see the conversation. Supply goal, scope, and acceptance; front owns integration and verification. Both wrappers share this interface and contracts. Tooling is implemented separately; check [STATE](../STATE.md) for validation.

## Spec template

```text
Goal: result to achieve
Context: relevant facts, files, constraints
Scope: may change / must not change
Requirements: behavior and style
Acceptance: exact commands + expected results
Non-goals: excluded work
```

## Shared work contract

Both wrappers export `AGENT_ROLE=worker` and append:

```text
You are a worker. Do not delegate to other agents and do not run codex-task or claude-task.
Stay inside the specified scope. Stop if ambiguous or blocked; report rather than guess.
Write readable code: clear names, small functions, match style; comments only for non-obvious intent.
Do not commit or push.
End the final message with these sections:
STATUS: done|partial|blocked
CHANGES: each changed file and its purpose
VERIFICATION: what ran, results, and what was NOT verified
RISKS: assumptions, uncertainties, follow-ups
```

Orchestrator skills exclude `AGENT_ROLE=worker` or prompts carrying a handoff contract. User-level skills/instructions still reach workers; the [observed announcement](../lessons/2026-10-04-user-skills-reach-workers.md) does not establish a code-quality failure.

## Shared review contract

```text
Never modify files.
Report only defects tied to a concrete failure.
For each finding: severity, file:line, defect, trigger.
If none: NO FINDINGS.
```

One verifier per aspect. Intent/design and correctness differ; critical tooling also needs live inside/outside write probes. “NO FINDINGS” does not prove every behavior was tested.

## Exact command interface

```text
codex-task  <run|resume|review|peek|watch|ls> [opts]   # Codex CLI worker
claude-task <run|resume|review|peek|watch|ls> [opts]   # Claude Code (`claude -p`) worker
agent-quota [--json]                                # both quotas, burn-rate status, routing advice
agent-quota --codex-line

run    [opts] (-p TEXT | -f FILE | stdin)            # new task
resume RUN_DIR [opts] (-p | -f | stdin)             # same worker thread/session
review [opts] [--uncommitted | --base BR | --commit SHA] [-p | -f]
peek   RUN_DIR [N]                                 # last N events, one line each
watch  RUN_DIR [INTERVAL_S=120] [STALL_S=600]         # HB / STALL / DONE until run ends
ls     [N]                                        # recent agent runs, exit code, STATUS

-n NAME   -t TIER   -m MODEL   -e EFFORT   -s ro|rw|full   -C DIR
--net   --add-dir D   --raw
codex-task only: --search
model-review --if-stale [DAYS] [--claude-models ids] [--force] [--dry-run]
install.sh [--with-codex-front] [--uninstall]
```

`-p` takes text; `-f` a file, including on resume/review. `review` is read-only; targets are uncommitted changes, base branch (`BR`), or commit (`SHA`). `watch` intervals are seconds; `HB` means heartbeat and `STALL` signals investigation. `ls` and metadata support usage measurement.

Options select name, tier, model, effort, sandbox, working directory, network, extra directory, and raw output. `--search` enables Codex search for research. [Model catalog](models.md) holds exact tier mappings: Codex luna (`gpt-6-luna`, medium), reserve (`gpt-reserve`, medium), sol (`gpt-6.1-sol`, high; default), astra (`gpt-6-astra`, xhigh); Claude haiku, sonnet (default), opus. [Routing](routing.md) governs selection.

| Agent / tier | Permission boundary |
|---|---|
| Codex `ro` | Read-only sandbox for evidence/review |
| Codex `rw` | Workspace-write sandbox for implementation; network disabled unless `--net` |
| Claude `ro` | Read-only commands only; no tests. Explicitly disables Bash sandbox, which would allow working-directory writes |
| Claude `rw` | Sandboxed Bash can write inside working directory; outside writes fail; no network |
| Either `full` | No restrictions (Codex danger-full-access) |

Claude `ro` auto-allows commands such as `git diff`, `git log`, and `grep`; write commands are blocked. Non-interactive `claude -p` cannot answer approvals. Do not enable its Bash sandbox for read-only workers. See the [live sandbox evidence](../lessons/2026-10-04-claude-worker-sandbox.md).

```sh
codex-task run -n implement -t sol -s rw -C WORKTREE -f spec.md
codex-task resume RUN_DIR -f fixes.md
codex-task review -t sol -e xhigh -s ro --base main -f review.md
codex-task peek RUN_DIR 10
codex-task watch RUN_DIR 120 600
codex-task ls 5
claude-task run -n proposals -t opus -s ro -f ideas.md
agent-quota --json
```

`WORKTREE`/`RUN_DIR` are placeholders. Both wrappers accept the shared subcommands/options. Underlying Codex review rejects target flags plus custom instructions; wrapper custom review describes the target in the prompt and returns structured JSON findings. See the [observed restriction](../lessons/2026-10-04-review-target-instructions.md).

## Installation and model checks

Linux sandbox prerequisites: **bubblewrap and socat**. Claude's Bash sandbox needs both; missing socat silently prevented engagement in live tests, blocking non-read-only commands and tests. Ubuntu AppArmor may also block Codex namespaces; the [policy fix](../lessons/2026-10-04-ubuntu-sandbox.md) requires human approval.

Default install supplies Claude-front skill; `--with-codex-front` adds the opt-in, unvalidated Codex-front skill. Human decides front separately. `--uninstall` removes installation; backups live outside skill directories in `~/.agent-runs/install-backups/` and must never be loaded.

`model-review --if-stale 3 --claude-models "<Claude model ids known from system context>"` is the Claude-startup check. It is free/silent when lists are unchanged; only changed lists start one background Codex sol `--search` research run. Read completed results, update [catalog facts](models.md) directly, mention briefly, and propose routing changes under [AGENTS.md](../AGENTS.md). This is event-driven research, not a schedule.

## Run records

```text
${AGENT_RUNS_ROOT:-$HOME/.agent-runs}/<YYYYmmdd-HHMMSS>-<codex|claude>-<name>/
  prompt.md events.jsonl stderr.log last.md meta.env pid exit_code
```

The prompt, newline-delimited events, diagnostics, final message, metadata, process ID, and exit code allow bounded inspection. Both agents' `meta.env` keys:

```text
NAME KIND AGENT MODEL EFFORT SANDBOX SANDBOX_SHORT NET CWD PARENT START
END EXIT THREAD TOKENS_IN TOKENS_CACHED TOKENS_OUT TOKENS_REASONING
```

Claude adds `COST_USD` and `CLAUDE_UTIL_<WINDOW>` / `CLAUDE_RESETS_<WINDOW>` from `rate_limit_event`. Keep raw records local: prompts, paths, IDs, and account data may be private. Publish only generalized evidence.
