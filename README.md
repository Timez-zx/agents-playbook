# agents-playbook

A reusable playbook and command-line tools for AI agents working together. The design is agent-agnostic because more agents will appear; today's main pair is Claude Code + Codex CLI because the owner currently considers them the strongest. Claude is the current front, while specialist roles can go to either agent. Install once, reuse the skills across sessions, and improve the library through evidence from real tasks. Adding an agent means adding a `<agent>-task` wrapper with the shared interface, an `<AGENT>.md` profile, and rows in `playbook/routing.md`.

## Why this exists

In the owner's experience, Claude has been stronger at high-level ideas: smarter, more flexible, and more creative. Its explanations have sometimes been hard to follow because they were dense, used jargon or unexplained abbreviations, and skipped steps. Codex has been more rigorous and detailed, and its writing has been easier for the owner to read. These are observations from one user's experience, not universal claims. The [Claude](CLAUDE.md) and [Codex](CODEX.md) profiles keep the evidence and possible alternatives.

The aim is to spend each token where it helps most. Roles follow measured strengths; routing follows available budgets. The playbook serves the session's real task: small questions, edits below about 30 lines, and quick lookups get done without delegation, quota checks, or lessons. Learning happens after delivery, so the human never waits for upkeep.

## Two-minute quick start

```sh
git clone https://github.com/Timez-zx/agents-playbook.git
cd agents-playbook
./install.sh
```

Keep the clone in a fixed location; the default is `~/agents-playbook`. Installation uses symlinks, so the next session uses updates without re-setup. Claude is the default front. The experimental Codex-front skill is installed only with `./install.sh --with-codex-front`; installing it does not itself switch the conversation.

The installer interface is `install.sh [--with-codex-front] [--uninstall]`. Install backups move outside skill directories into `~/.agent-runs/install-backups/`, so an obsolete backed-up skill is never loaded.

On Ubuntu 24.04, AppArmor can prevent the Codex sandbox from starting. Read the [sandbox lesson](lessons/2026-10-04-ubuntu-sandbox.md) before changing system policy. The recorded fix needs human approval because it relaxes a security policy.

When a task needs delegation, check quotas and use a self-contained handoff:

```sh
agent-quota
codex-task run -n inspect -t luna -s ro -p 'Summarize the relevant code; cite file:line.'
```

The [command reference](playbook/handoff.md) covers both wrappers, `agent-quota --json`, and `agent-quota --codex-line`. See [STATE.md](STATE.md) before relying on a mode; `claude-task` still needs a live test.

## What happens in a session

At startup, the installed skill reads only the short STATE file. The front checks both quotas only when it will delegate, then routes work. Workers receive a self-contained contract and cannot delegate further. The front verifies results, integrates them, and owns everything delivered to the human.

```text
                           Front / Orchestrator
                                    |
          +---------+---------+-----+----+---------+---------+
          |         |         |          |         |         |
        Planner   Scout    Ideator    Executor  Verifier   Writer
```

Planner makes decomposition and design decisions; the front coordinates even if another agent plans. The Writer returns prose for the front to fact-check before delivery. The [six workflows](playbook/patterns.md) cover implementation, ideation, debugging, prototypes, disagreements, and reports.

| Role | Responsibility | Current holder |
|---|---|---|
| Orchestrator (front) | Frame goals, route, decide, integrate, verify delivery, talk to the human, run long/GPU experiments; own outcomes | Claude main session, opus |
| Planner | Decompose tasks and make design decisions | Claude, currently also the front |
| Scout | Gather context cheaply; return a cited summary | Claude Explore, haiku; or Codex luna, read-only |
| Ideator | Offer divergent proposals; challenge the plan | Claude subagents, opus |
| Executor | Implement a spec and run tests | Codex sol, writable sandbox |
| Verifier | Review diffs; check hypotheses against code and logs | Fresh Codex session; astra for critical work |
| Writer | Write persistent human-facing text | Codex sol; luna for short, simple work |

The [authoritative role table](playbook/roles.md) changes through evidence and human-approved PRs. Do the work directly when a small change is already in context or a spec would cost more than the work; small tasks do not need orchestration overhead.

## Repo map

- [AGENTS.md](AGENTS.md): operating, update, iteration, git, PR, and privacy rules; the single source of truth.
- [STATE.md](STATE.md): front, validation status, and open proposals.
- [CLAUDE.md](CLAUDE.md) and [CODEX.md](CODEX.md): evidence-linked agent profiles.
- [Roles](playbook/roles.md), [routing](playbook/routing.md), and [patterns](playbook/patterns.md): assignments, tiers, and workflows.
- [Handoff](playbook/handoff.md), [budget](playbook/budget.md), and [writing](playbook/writing.md): contracts, efficiency, and readable reports.
- [Lessons](lessons/README.md): reusable findings; [proposals](proposals/README.md): role/front decisions and trials.
- [Claude skill](skills/claude/agents-playbook/SKILL.md) and [Codex skill](skills/codex/agents-playbook/SKILL.md): compact instructions linked to the repo.
- `bin/`: `codex-task`, `claude-task`, and `agent-quota`; `lib/`: shared support; `install.sh`: installation.
- `tests/`: fixtures and a test script using fake `codex` and `claude` binaries.

## Budgets

Before delegating, run `agent-quota`. It reports both quotas, burn-rate status, and routing advice. Burn rate compares usage with the fraction of the window already elapsed; raw usage alone can hide a fast drain. These thresholds remain unvalidated.

| State | Routing change |
|---|---|
| Both healthy | Use agreed roles |
| Claude over-burning or above 70% used | Codex also scouts and writes; use fewer or cheaper Claude subagents; front only coordinates and decides |
| Codex over-burning or above 70% used | Claude sonnet handles routine execution; preserve Codex for critical verification |
| Either above 90% used | Use that side only for critical-path work; tell the human |

Choose the cheapest tier likely to succeed, then escalate after failure. Critical-path review starts at the top tier because a missed defect can outweigh the saving. See [budget rules](playbook/budget.md) and [routing tiers](playbook/routing.md).

## Switching fronts or reassigning roles

The front is the agent the human talks to; roles can be held by any agent regardless of the front. Record concrete comparisons as `role-evidence` lessons, then raise a proposal in chat when evidence favors a change. The human decides. An accepted front switch updates the assignments and profiles, installs the opt-in skill, and updates STATE; the human then starts talking to the new front. A role reassignment is a separate PR. See [AGENTS.md](AGENTS.md) for the full process.

## Status

Experimental; tuned so far on one account: Claude Code Enterprise + Codex Pro. [STATE.md](STATE.md) distinguishes live validation from offline tests and untested modes. The owner's writing preference is evidence; human preference for the full report pass still needs validation.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), which points to the operating rules. Lessons and small status updates go to main; behavior changes need a PR and human approval because they affect every user.

## License

[MIT](LICENSE). Copyright (c) 2026 Timez-zx.
