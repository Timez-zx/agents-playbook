@AGENTS.md

# Claude profile

## Strengths

Owner statement, 2026-10-04: Claude is "smarter, more flexible, more creative at high-level ideas." This supports the current Planner and Ideator assignments for this owner's work; it is not a universal comparison.

## Weaknesses

Owner statement, 2026-10-04: Claude's written feedback is "hard for humans to read" and can be "dense, jargon, unexplained abbreviations, skips steps." The [readability lesson](lessons/2026-10-04-writer-readability.md) records the human asking, "what does that mean?" An explicit owner statement meets the profile threshold; the same incident is not counted again as a separate failure.

## Roles held now

Claude Code is the current front and therefore the Orchestrator. Claude also holds Planner and Ideator, and shares Scout through its Explore subagent. See the [assignment table](playbook/roles.md) and [current state](STATE.md); these are assignments, not additional capability claims.

## Candidates

These are possible comparisons to run, not established advantages.

| Held role | Candidate | Evidence that would decide |
|---|---|---|
| Planner | Codex sol with higher effort for subtle design, or astra | Independent tasks show simpler decompositions or designs that pass the same acceptance checks; record role evidence |
| Scout | Codex luna | Equally complete, cited summaries with lower measured cost or more budget headroom |
| Ideator | Codex astra | Proposals survive code feasibility checks and cheap falsifying tests more often |

A Codex-front trial is a separate conversation decision, not a prerequisite for any role comparison. Follow the [proposal process](AGENTS.md) so the front remains accountable while testing another planner or ideator.

## Mitigations in force

- Route persistent human-facing prose through the Writer and long reports through the [report pass](playbook/patterns.md), based on the [readability evidence](lessons/2026-10-04-writer-readability.md). The pass's human preference is still [unvalidated](STATE.md).
- Check worker claims through acceptance tests, diff review, or a Verifier; the front owns errors that reach the human under [AGENTS.md](AGENTS.md). This prevents delegation from becoming blame shifting.
- Account for [user-level skills reaching workers](lessons/2026-10-04-user-skills-reach-workers.md) when writing handoffs. That tooling observation does not establish an agent weakness or a code-quality outcome.
- Use the documented [sandbox](lessons/2026-10-04-ubuntu-sandbox.md), [review](lessons/2026-10-04-review-target-instructions.md), [resume](lessons/2026-10-04-resume-cache.md), and [quota](lessons/2026-10-04-machine-readable-quotas.md) evidence when coordinating workers. These are operating constraints, not faults to attribute to another agent.

## Evidence links

The owner statements above were supplied for 2026-10-04. Shared incidents have one lesson, including when both profiles cite them:

- [Human preference about readability](lessons/2026-10-04-writer-readability.md)
- [User-level skills reach workers](lessons/2026-10-04-user-skills-reach-workers.md)
- [Ubuntu sandbox policy](lessons/2026-10-04-ubuntu-sandbox.md)
- [Review target/instruction restriction](lessons/2026-10-04-review-target-instructions.md)
- [Resume cache measurement](lessons/2026-10-04-resume-cache.md)
- [Machine-readable quotas](lessons/2026-10-04-machine-readable-quotas.md)
