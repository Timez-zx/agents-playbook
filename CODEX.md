# Codex profile

## Strengths

Owner, 2026-10-04: Codex is “more rigorous and detailed”; its “written output is easier for humans to read.” The [readability evidence](lessons/2026-10-04-writer-readability.md) supports Writer, not validation of the full report pass.

A fresh gpt-6-astra review independently found the read-only defect and four other high-severity defects missed by live probes. The [review incident](lessons/2026-10-04-ro-tier-defect.md) supports Verifier; it does not compare astra with sol on the same review. The [owner's sol comparison](lessons/2026-10-04-sol-routing-default.md) supports current routing.

## Weaknesses

None established at the [threshold](AGENTS.md): two independent incidents or an explicit owner statement. Single incidents and operating constraints are not agent weaknesses.

## Roles held now

Executor, Verifier, Writer, and shared Scout (luna); Claude remains front/Planner. See [assignments](playbook/roles.md) and [STATE](STATE.md). A front switch does not exchange roles.

## Candidates

| Held role | Candidate | Deciding evidence |
|---|---|---|
| Scout | Claude Explore haiku | Equally complete cited summaries at lower cost or more headroom |
| Executor | Claude sonnet | Same tests pass with fewer corrections or lower cost |
| Verifier | Claude opus | Concrete defects found against the same criteria |
| Writer | Claude sonnet/opus | Human prefers prose with verified facts unchanged |

Planner/front trials require separate evidence and a [human decision](AGENTS.md); rigor alone does not establish them.

## Mitigations in force

Use short resumed fixes, but fresh sessions for large revision rounds, based on the [thread-growth measurement](lessons/2026-10-04-thread-growth-cost.md). Fresh verification stays independent.

## Operating notes

[Ubuntu sandbox policy](lessons/2026-10-04-ubuntu-sandbox.md), [review argument restrictions](lessons/2026-10-04-review-target-instructions.md), and [user-level skills reaching workers](lessons/2026-10-04-user-skills-reach-workers.md) are observed operating constraints, not weaknesses. The last observation has no assessed code-quality outcome.
