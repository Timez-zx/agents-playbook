# Codex profile

## Strengths

Owner, 2026-10-04: Codex is “more rigorous and detailed”; its “written output is easier for humans to read.” This owner feedback supports Writer.

One owner-approved report on 2026-10-04 supports sol high for prose and fresh luna medium for cold reading: the reader recovered the full structure and caught real issues, with some over-flagging.

2026-10-04: a fresh gpt-6-astra review independently found the read-only defect and four other high-severity defects missed by live probes. This supports Verifier; it does not compare astra with sol on the same review. Owner, 2026-10-04: sol is close to astra on most tasks at lower cost; this supports current routing.

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

Use short resumed fixes, but fresh sessions for large revision rounds, under the [context-cost principle](lessons/context-cost.md). Fresh verification stays independent.

## Operating notes

Ubuntu AppArmor may block sandbox startup; Codex review rejects target flags plus custom instructions; user-level skills reach workers. These are operating constraints, not weaknesses; the skill observation has no assessed code-quality outcome. See [handoff notes](playbook/handoff.md) for the facts and usable workarounds.
