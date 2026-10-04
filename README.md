# claude-codex-playbook

A reusable playbook and command-line tools for one AI agent orchestrating another. Today, Claude Code plans and coordinates work, while Codex CLI implements, verifies, and writes. Install once; new sessions reuse the same skills, and lessons from later sessions improve the playbook. The tools share an interface so the agents can swap roles when the evidence warrants it.

## Why this exists

In the owner's experience, Claude has been stronger at high-level ideas: smarter, more flexible, and more creative. Its explanations have sometimes been hard to follow because they were dense, used jargon or unexplained abbreviations, and skipped steps. Codex has been more rigorous and detailed, and its writing has been easier for the owner to read. These are observations from one user's experience, not universal claims about either agent.

The aim is to spend each token where it helps most. Roles follow measured strengths, and routing follows the available budgets. Different users and accounts will need different assignments. See the [roles and principles](playbook/roles.md).

## Two-minute quick start

```sh
git clone https://github.com/Timez-zx/claude-codex-playbook.git
cd claude-codex-playbook
./install.sh
```

Keep this clone in a fixed location. Installation uses symlinks, so later edits are live in new sessions without another setup step. The default local clone location is a directory named `claude-codex-playbook` in your home directory. The active skill is for Claude orchestration; the Codex entry is for a user-requested role swap.

On Ubuntu 24.04, AppArmor can prevent the Codex sandbox from starting. Read the [sandbox lesson](lessons/2026-10-04-ubuntu-sandbox.md) before changing system policy. The recorded fix needs human approval because it relaxes a security policy.

Try the shared tools:

```sh
agent-quota
codex-task run -n inspect -t luna -s ro -p 'Summarize the relevant code; cite file:line.'
claude-task run -n alternatives -t opus -s ro -p 'Propose alternatives and a cheap test for each.'
```

The [command reference and contracts](playbook/handoff.md) explain the complete interface.

## What happens in a session

The orchestrator checks both quotas, frames the task, and routes work. Workers receive a self-contained contract. They cannot delegate further. The orchestrator verifies the result and checks the Writer's facts before sending a long report to the user.

```text
                         Orchestrator
                              |
          +---------+---------+---------+---------+
          |         |         |         |         |
        Scout    Ideator   Executor  Verifier   Writer
```

For the final report, the Writer returns prose to the orchestrator, who checks the facts and sends it to the user. The [six workflows](playbook/patterns.md) cover implementation, ideation, debugging, prototypes, disagreements, and reports.

| Role | Responsibility | Current holder |
|---|---|---|
| Orchestrator | Frame, ideate, decompose, route, decide, integrate, talk to the user, run long or graphics processing unit (GPU) experiments | Claude main session, opus |
| Scout | Gather context cheaply; return a cited summary | Claude Explore, haiku; or Codex luna, read-only |
| Ideator | Offer divergent proposals; challenge the plan | Claude subagents, opus |
| Executor | Implement a spec and run tests | Codex sol, writable sandbox |
| Verifier | Review diffs; check hypotheses against code and logs | Fresh Codex session; astra for critical work |
| Writer | Write all persistent human-facing text | Codex sol; luna for short, simple work |

The [authoritative role table](playbook/roles.md) can change with evidence. The orchestrator may act directly for a change below about 30 lines that is already in context, or when writing the spec would cost more than doing the work.

## Repo map

- [Roles](playbook/roles.md): assignments, principles, and the swap procedure.
- [Routing](playbook/routing.md): model and effort tables.
- [Patterns](playbook/patterns.md): who does each step of a workflow.
- [Handoff](playbook/handoff.md): specs, worker contracts, commands, and run records.
- [Budget](playbook/budget.md): quota sources, burn rate, and load shifts.
- [Writing](playbook/writing.md): rules for readable English and direct replies.
- [Lessons](lessons/README.md): reusable findings and their evidence.
- [Claude skill](skills/claude/codex-collab/SKILL.md) and [Codex skill](skills/codex/claude-collab/SKILL.md): session instructions that share the playbook.
- `bin/`: `codex-task`, `claude-task`, and `agent-quota`.
- `lib/`: shared tooling support; `install.sh`: installation.
- `tests/`: fixtures and a test script using fake `codex` and `claude` binaries.

## Budgets

Run `agent-quota` at session start. It reports both quotas, burn-rate status, and routing advice. Burn rate compares usage with the fraction of the window already elapsed; raw usage alone can hide a fast drain.

| State | Routing change |
|---|---|
| Both healthy | Use default roles |
| Claude over-burning or above 70% used | Codex also scouts and writes; use fewer or cheaper Claude subagents; Claude decides |
| Codex over-burning or above 70% used | Claude sonnet handles routine execution; preserve Codex for critical verification |
| Either above 90% used | Use that side only for critical-path work; tell the user |

Choose the cheapest tier likely to succeed, then escalate after failure. Critical-path review starts at the top tier because a missed defect can outweigh the savings. See [budget rules](playbook/budget.md) and [routing tiers](playbook/routing.md).

## Swapping roles

Record comparisons as lessons tagged `role-evidence`: who found the bug, whose design was simpler, or whose text the human preferred. When those lessons consistently favor the other agent for orchestration, prompt the user to decide. One pull request updates the table in `playbook/roles.md` and both skills' role tables. Shared commands and contracts make the swap possible without redesigning the handoff.

## Status

Experimental; tuned so far on one account: Claude Code Enterprise + Codex Pro. The assignments and thresholds are starting points to test against your own evidence.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). General, private-data-free lessons go to main; behavior changes need a pull request and human approval because they affect every user.

## License

[MIT](LICENSE). Copyright (c) 2026 Timez-zx.
