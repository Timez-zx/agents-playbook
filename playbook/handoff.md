# Handoffs and command reference

A worker cannot see the conversation, so every handoff must carry the goal, scope, and acceptance criteria. Both wrappers share the interface and contracts below, allowing either agent to be the worker. Workers return bounded evidence; the orchestrator owns integration and verification.

## Spec template

Copy this structure and replace each placeholder. Keep the spec terse but self-contained so the worker does not have to infer missing requirements.

```text
Goal
  The result to achieve.
Context
  Relevant facts, files, and constraints; the worker cannot see the conversation.
Scope
  May change: ...
  Must not change: ...
Requirements
  Required behavior and style.
Acceptance
  Exact commands and expected results.
Non-goals
  Work deliberately excluded.
```

The goal identifies success. Context supplies the facts the conversation would otherwise hide. Scope protects unrelated work. Requirements define the behavior. Acceptance makes “done” testable. Non-goals prevent plausible but unwanted expansion.

## Shared work contract

Both wrappers append the same work contract. Both also export `AGENT_ROLE=worker` to the worker process. Orchestrator skills do not apply when that variable is set or a prompt carries a handoff contract; this prevents recursive delegation.

```text
You are a worker. Do not delegate to other agents and do not run codex-task or claude-task.
Stay inside the specified scope. Stop if the task is ambiguous or blocked; report it rather than guessing.
Write readable code: clear names, small functions, match the surrounding style,
and add comments only for non-obvious intent.
Do not commit or push.
End the final message with these sections:
STATUS: done|partial|blocked
CHANGES: each changed file and its purpose
VERIFICATION: what ran, its results, and what was NOT verified
RISKS: assumptions, uncertainties, and follow-ups
```

No delegation keeps routing and budget under one coordinator. Scope and ambiguity rules prevent guesses from becoming unintended changes. Readable code makes review cheaper. Keeping commits and pushes with the orchestrator preserves integration control. The final sections cap the response to information the orchestrator needs, including limits on what “done” means.

## Shared review contract

```text
Never modify files.
Report only defects tied to a concrete failure.
For each finding, give severity, file:line, defect, and trigger.
If there are no findings, return NO FINDINGS.
```

Read-only review preserves the evidence being assessed. A concrete failure and trigger separate defects from preferences. Severity supports prioritization, and `file:line` lets the orchestrator check the claim. “NO FINDINGS” is an explicit result, not proof that every behavior was tested.

## Exact command interface

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

-n NAME   -t TIER   -m MODEL   -e EFFORT   -s ro|rw|full   -C DIR
--net   --add-dir D   --raw
```

`codex-task` runs Codex CLI as the worker. `claude-task` runs Claude Code CLI through `claude -p`. `agent-quota` reports both quotas, burn-rate status, and routing advice; `--json` requests machine-readable output. All model and tier mappings are in [routing.md](routing.md).

- `run` starts a new task. Supply prompt text with `-p TEXT`, a file with `-f FILE`, or standard input, so the handoff is explicit.
- `resume RUN_DIR` sends a follow-up in the same worker thread or session. Its `-p` and `-f` take text and a file respectively; retained context makes fixes cheaper.
- `review` runs a read-only review. Choose the uncommitted diff, a base branch (`BR`), or a commit identifier (`SHA`), and optionally supply instructions with `-p` or `-f`. A named target makes the review's scope checkable.
- `peek RUN_DIR [N]` shows the last N events, one line each. It gives a small view without flooding orchestrator context.
- `watch RUN_DIR [INTERVAL_S=120] [STALL_S=600]` prints `HB` (heartbeat), `STALL`, or `DONE` lines until the run ends. The interval is in seconds; a heartbeat tracks progress, while a stall is a signal to investigate.
- `ls [N]` shows recent runs of that agent, including exit code and the worker's `STATUS` line. Run records also support token measurement, so compare usage rather than guess.

The common options select name (`-n`), tier (`-t`), model (`-m`), effort (`-e`), sandbox (`-s`), and working directory (`-C`). `--net` enables network access for the task; `--add-dir D` adds a directory. The report workflow uses `--raw`. Explicit options make the environment part of the handoff.

Sandbox shorthands are `ro` for read-only, `rw` for workspace-write, and `full` for danger-full-access. Use read-only for evidence gathering and reviews, and workspace-write for implementation, so access matches the work. The Ubuntu [sandbox lesson](../lessons/2026-10-04-ubuntu-sandbox.md) explains a startup failure and its approved fix; full access is not a substitute for fixing that policy issue.

```sh
codex-task run -n implement -t sol -s rw -C WORKTREE -f spec.md
codex-task resume RUN_DIR -f fixes.md
codex-task review -t astra -s ro --base main -f review.md
codex-task peek RUN_DIR 10
codex-task watch RUN_DIR 120 600
codex-task ls 5
claude-task run -n proposals -t opus -s ro -f ideas.md
agent-quota --json
```

The same subcommands and options apply to `claude-task`. `WORKTREE` and `RUN_DIR` are placeholders, not new flags. The examples use the spec's working directory and the run directory returned by the tool.

Codex's underlying review command rejects a target flag combined with custom instructions. The workaround describes the target in the prompt and runs a custom review, which returns structured JSON (JavaScript Object Notation) findings. See the [review lesson](../lessons/2026-10-04-review-target-instructions.md); the shared wrapper interface still accepts the target and instruction options above.

## Run records

Both wrappers use this directory layout:

```text
${AGENT_RUNS_ROOT:-$HOME/.agent-runs}/<YYYYmmdd-HHMMSS>-<codex|claude>-<name>/
  prompt.md
  events.jsonl
  stderr.log
  last.md
  meta.env
  pid
  exit_code
```

The path is a configurable template. `prompt.md` holds the handoff, `events.jsonl` holds newline-delimited JSON events, `stderr.log` holds diagnostics, and `last.md` holds the last worker message. The process identifier (`pid`), exit code, and metadata make the run inspectable without rereading everything.

Both agents' `meta.env` keys are:

```text
NAME KIND AGENT MODEL EFFORT SANDBOX SANDBOX_SHORT NET CWD PARENT START
END EXIT THREAD TOKENS_IN TOKENS_CACHED TOKENS_OUT TOKENS_REASONING
```

Claude adds `COST_USD` and `CLAUDE_UTIL_<WINDOW>` / `CLAUDE_RESETS_<WINDOW>` from `rate_limit_event`. These record cost in US dollars and utilization/reset data for each quota window. Keep raw run records local: prompts, paths, and identifiers may be private. Publish only generalized lesson evidence.
