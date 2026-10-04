# Codex profile

## Strengths

Owner statements, 2026-10-04: Codex is "more rigorous and detailed" and its "written output is easier for humans to read." These support the current Executor, Verifier, and Writer assignments for this owner's work. The [readability lesson](lessons/2026-10-04-writer-readability.md) records the writing preference; it does not validate the full report-pass workflow.

## Weaknesses

No agent weakness has been established by the supplied evidence at the threshold in [AGENTS.md](AGENTS.md): at least two independent incidents or an explicit human statement. Single incidents belong in lessons. The tooling and environment observations below are not agent weaknesses.

## Roles held now

Codex holds Executor, Verifier, and Writer, and shares Scout through luna. Claude remains the front and Planner. See the [assignment table](playbook/roles.md) and [current state](STATE.md); a future front switch does not automatically reassign these roles.

## Candidates

These are possible comparisons to run, not established advantages.

| Held role | Candidate | Evidence that would decide |
|---|---|---|
| Scout | Claude Explore haiku | Equally complete, cited summaries with lower measured cost or more budget headroom |
| Executor | Claude sonnet | Independent tasks pass the same tests with fewer corrections or lower measured cost |
| Verifier | Claude opus | Concrete defects found against the same acceptance criteria, without duplicating a review aspect |
| Writer | Claude sonnet or opus | The human prefers its text while verified facts remain unchanged |

Codex as Planner or front is also a possible trial, not a validated capability claim. Follow the [proposal process](AGENTS.md) and record comparisons rather than infer them from rigor alone.

## Mitigations in force

- Use the [worker contracts](playbook/handoff.md) and independent verification: the front owns the delivered outcome under [AGENTS.md](AGENTS.md), whichever worker produced it.
- Resume corrections in the same Executor thread when appropriate, based on the [cache measurement](lessons/2026-10-04-resume-cache.md). Fresh verification remains separate, so cached context does not replace independence.
- Keep tooling and environment incidents in their existing lessons, and use those notes when constructing a handoff. [One incident, one lesson](AGENTS.md) prevents competing blame narratives.

## Operating notes

- On the recorded Ubuntu 24.04 setup, AppArmor blocked the bubblewrap sandbox. The [sandbox lesson](lessons/2026-10-04-ubuntu-sandbox.md) documents the human-approved policy fix and remaining access limits. This is an environment restriction.
- The underlying Codex review command rejected target flags combined with custom instructions. The [review lesson](lessons/2026-10-04-review-target-instructions.md) records the custom-prompt workaround. This is a tooling restriction.
- User-level skills and instruction files also reach delegated workers. The [worker-skills lesson](lessons/2026-10-04-user-skills-reach-workers.md) records one worker announcement; its code-quality effect has not been assessed.
- [Quota sources](lessons/2026-10-04-machine-readable-quotas.md) and [resume caching](lessons/2026-10-04-resume-cache.md) are operating evidence, not guarantees about every future client or run.

## Evidence links

The owner statements above were supplied for 2026-10-04. These are the same incident records cited by the Claude profile:

- [Human preference about readability](lessons/2026-10-04-writer-readability.md)
- [User-level skills reach workers](lessons/2026-10-04-user-skills-reach-workers.md)
- [Ubuntu sandbox policy](lessons/2026-10-04-ubuntu-sandbox.md)
- [Review target/instruction restriction](lessons/2026-10-04-review-target-instructions.md)
- [Resume cache measurement](lessons/2026-10-04-resume-cache.md)
- [Machine-readable quotas](lessons/2026-10-04-machine-readable-quotas.md)
