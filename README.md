# agents-playbook

A reusable playbook and CLI tools for AI agents collaborating across sessions. Claude Code is today's front; Codex CLI is the main worker. Roles can move independently of the front, and new agents can join through a shared wrapper interface and profile with dated evidence.

The objectives, in order: highest-quality task outcome; highest-quality human explanation (top-down, accurate, concise); fewest tokens only after both. The owner's experience favors Claude for high-level ideas and Codex for rigor and readable prose; [profiles](CLAUDE.md) carry dated agent evidence; [lessons](lessons/README.md) hold general principles, not cases or behavior changes.

## Two-minute quick start

Linux sandbox prerequisites: **bubblewrap and socat**, plus the agents' CLIs. Claude's Bash sandbox needs both; without socat it may silently fail to engage.

```sh
git clone https://github.com/Timez-zx/agents-playbook.git
cd agents-playbook
./install.sh
```

Keep the clone fixed (default `~/agents-playbook`): installed symlinks use updates next session without re-setup. Interface: `install.sh [--with-codex-front] [--uninstall]`. Codex front is experimental and opt-in; installing it does not switch the human's conversation. Backups live outside skill directories in `~/.agent-runs/install-backups/`; never load them.

Ubuntu 24.04 may block Codex sandbox startup through AppArmor. `install.sh` prints the exact human-approval commands when it detects the condition; the fix relaxes system security policy and needs human approval.

When delegating, check both quotas and provide a self-contained handoff:

```sh
agent-quota
codex-task run -n inspect -t luna -s ro -p 'Summarize relevant code; cite file:line.'
```

The [command reference](playbook/handoff.md) documents both wrappers, `codex-task --search`, `agent-quota --json`/`--codex-line`, and `model-review`. Check [STATE.md](STATE.md): Claude rw/resume and corrected ro flags were tested live; final wrapper re-test is pending.

## How a session works

Repo work follows AGENTS → STATE → involved profiles → roles → lessons index → open proposals. Ordinary startup reads only STATE; Claude front also runs `model-review --if-stale 3 --claude-models "<Claude model ids known from system context>"`. Unchanged model lists cost nothing and stay silent. Only changed lists trigger one background Codex sol `--search` research run. Finished results update [model facts](playbook/models.md) directly; the front mentions them briefly. Routing changes still require human approval.

Small questions, edits below about 30 lines, and quick lookups get done directly, without delegation, quota checks, or lessons. Otherwise, front routes a self-contained spec, workers return evidence without delegating, and front verifies, integrates, and owns the outcome.

| Role | Current holder / responsibility |
|---|---|
| Orchestrator (front) | Claude opus; coordinate, decide, integrate, verify delivery, talk to human, run long/GPU experiments |
| Planner | Claude; decomposition/design, independently assignable from front |
| Scout | Claude Explore haiku or Codex luna; cited context summaries |
| Ideator | Claude opus; divergent proposals |
| Executor | Codex sol high; implement/test in writable sandbox |
| Verifier | Fresh Codex sol high; xhigh for critical review; astra only escalation/tie-break |
| Writer | Codex sol high; luna for short/simple prose; front checks facts |

Defaults: **sol high for implementation/writing; sol xhigh for subtle logic and critical review**. Astra is only escalation after sol fails/is uncertain, or a tie-break. Owner, 2026-10-04: sol is close to astra on most tasks at lower cost. [Routing](playbook/routing.md) holds policy; [models](playbook/models.md) holds the catalog.

Claude permissions: `ro` = read-only commands, no tests (Bash sandbox explicitly disabled); `rw` = sandboxed Bash writes inside the working directory, no network; `full` = no restrictions. Codex `ro`/`rw` use read-only/workspace-write sandboxes; network needs per-task `--net`. Critical tooling needs live write probes inside/outside the working directory and independent code review.

Resume short fixes; start fresh sessions with precise specs for large revision rounds. [Context cost](lessons/context-cost.md) explains why cache hits do not eliminate the cost of resending a large thread.

## Budgets

Run `agent-quota` only before delegation. Over-burning means used percent exceeds elapsed-window percent by 20 percentage points. Thresholds remain unvalidated.

| State | Routing change |
|---|---|
| Both healthy | Agreed roles |
| Claude over-burning or >70% used | Codex also scouts/writes; fewer/cheaper Claude subagents; front coordinates/decides |
| Codex over-burning or >70% used | Claude sonnet routine execution; preserve Codex critical verification |
| Either >90% used | Critical work only on that side; tell human |

Above 90% takes priority; apply each side's restriction. [Budget details](playbook/budget.md) describe sources and measurement.

## Evidence and improvements

After delivery, use one short background Writer call only for a general principle that is new or refines an existing lesson; otherwise skip. Judge generality across projects, models, and agents before recording; refine the existing problem lesson or add `lessons/<problem>.md`. Non-general observations never enter lessons. Upkeep stays in this repo, never delays the human, and never turns a maintenance failure into a task failure. If agents discover a better general collaboration method, front proposes it after delivery in one or two lines with evidence. Approved → behavior-change PR; unapproved → lesson only. Facts (lessons, small STATE updates, model catalog) may go directly to main.

One incident, one record: dated agent evidence in its profile, a general principle in a lesson, operational facts where used; no rebuttal records. Weaknesses require two independent incidents or an explicit human statement; single incidents remain dated profile evidence. Profile claims carry dated evidence inline or quote the human. Fold approved general lessons into playbook rules through a PR, then mark `promoted` with rule links.

Front switches and role changes need an evidence-based proposal and human decision; switching fronts does not exchange specialist roles. [AGENTS.md](AGENTS.md) is the operating policy and [CONTRIBUTING.md](CONTRIBUTING.md) points contributors there.

## Repo map

- [STATE](STATE.md), [Claude profile](CLAUDE.md), [Codex profile](CODEX.md): validation and agent evidence.
- [Roles](playbook/roles.md), [routing](playbook/routing.md), [models](playbook/models.md), [patterns](playbook/patterns.md): assignments, defaults, catalog, workflows.
- [Handoff](playbook/handoff.md), [budget](playbook/budget.md), [writing](playbook/writing.md): interfaces, efficiency, explanation style.
- [Lessons](lessons/README.md), [proposals](proposals/README.md): general principles and human decisions.
- [Claude skill](skills/claude/agents-playbook/SKILL.md), [Codex skill](skills/codex/agents-playbook/SKILL.md): compact repo-linked entry points.
- `bin/`: wrappers, quota/model checks; `lib/`: shared support; `install.sh`: installation; `tests/`: fake-CLI fixtures/checks. Tooling revisions are maintained separately from this docs round.

Experimental; tuned on one account (Claude Code Enterprise + Codex Pro). [STATE](STATE.md) separates live evidence from untested modes; preference for the full report pass remains unvalidated.

[MIT](LICENSE). Copyright (c) 2026 Timez-zx.
