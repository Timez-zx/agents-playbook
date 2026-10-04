# Collaboration patterns

Pick the workflow that answers the task's main uncertainty. Planner owns design and decomposition; the front owns routing, integration, verification, and delivery even when another agent plans. Small tasks bypass these workflows because their coordination cost exceeds the benefit.

## W1: Spec → build → two-sided review

Use this as the default for features and fixes. Separate review of intent from review of correctness, so each aspect has one owner.

1. **Planner:** Design and decompose the change; **Orchestrator:** turn it into a handoff using [handoff.md](handoff.md). Exact scope and acceptance commands let a worker succeed without seeing the conversation.
2. **Executor:** Implement in its own worktree and run the specified tests. Isolation prevents concurrent edits from mixing.
3. **Orchestrator:** Review intent and design fit. The coordinator knows the user goal and integration constraints.
4. **Fresh Verifier:** Review correctness in a new session. Fresh context reduces reliance on the Executor's assumptions; do not duplicate the intent review.
5. **Executor:** Fix findings through `resume` of the same thread. This retains context and benefits from cached input.
6. **Orchestrator:** Re-run acceptance. A worker's successful report still needs independent confirmation.
7. **Writer:** Write the pull request text; **Orchestrator:** check its facts. Reviewers need readable prose that preserves the verified result.

## W2: Diverge → filter → converge

Use this when the plan itself is uncertain. Generate alternatives before committing implementation budget.

1. **Planner/front and two or three Ideators:** Propose candidates from different angles. Each proposal includes its expected effect and cheapest falsifying test, so ideas can be rejected cheaply.
2. **Verifier:** Use read-only astra to check feasibility against real code, citing `file:line`. Code evidence filters attractive proposals that cannot work.
3. **Planner:** Pick a candidate; **Orchestrator:** route the spec/build workflow above. One explicit design decision avoids implementing incompatible plans while keeping delivery with the front.

## W3: Hypothesis → evidence

Use this for debugging. Make the next experiment distinguish explanations rather than merely collect more logs.

1. **Planner:** Rank hypotheses and identify discriminating log points. A ranked list gives the experiment a clear question.
2. **Executor:** Add throttled probes. Bounded logging keeps the experiment readable and avoids overwhelming it.
3. **Orchestrator:** Run the experiment, including long or GPU experiments. The coordinator controls the conditions being compared.
4. **Verifier:** Read the logs, quote supporting lines, and state which hypothesis the evidence supports. Delegated reading protects orchestrator context while keeping the conclusion checkable.
5. **Planner:** Pick the next bisection step; **Orchestrator:** coordinate it. Each experiment should narrow the remaining uncertainty.

## W4: Prototype → rewrite

Use this when a fast experiment can validate an idea before polishing it. Keep the same tests so the rewrite preserves the demonstrated behavior.

1. **Planner/front:** Prototype quickly to validate the idea. Early evidence can prevent an expensive implementation of the wrong approach.
2. **Executor:** Rewrite into the final readable form under the same tests. Clear names, small functions, and matching style make the result maintainable.
3. **Orchestrator:** Check the diff and test results. Passing prototype tests is still a claim until checked.

## W5: Resolve a disagreement

Use this when agents disagree on a concrete claim. Do not average their positions; correctness is not a compromise.

1. **Orchestrator:** State the exact disputed claim. Narrowing the question makes a decisive answer possible.
2. **Fresh Verifier:** Use astra with `-e max`, without either side's reasoning; alternatively, **Orchestrator:** run a decisive test. Unprimed judgment or direct evidence breaks the tie without inheriting the argument.
3. **Orchestrator:** Decide from the result and record any reusable lesson. The evidence should explain the decision to future sessions.

## W6: Report pass

Use this for human-facing end-of-task reports longer than about 15 lines. The owner's experience favored Codex's readable writing, so prose gets its own pass.

1. **Orchestrator:** Supply verified facts as terse bullets. Keep writing work separate from responsibility for evidence.
2. **Writer:** Rewrite them using luna or sol with `-s ro --raw`. Read-only access suits a report pass that only needs to return text.
3. **Orchestrator:** Check that the facts are unchanged, then send the report to the user. Clear prose must not introduce new claims.

Writer assignment is independent of the front. Codex remains the assigned Writer if the front changes, unless an accepted reassignment or budget shift routes prose to Claude through `claude-task`. Choose tiers from [routing.md](routing.md); preserve `-s ro --raw` for the report pass. Human preference for the full pass is still [unvalidated](../STATE.md).

For short replies and small tasks, the front writes directly using [writing.md](writing.md), because a handoff would cost more than the text. After delivery, general lesson capture uses one short Writer call in the background and never delays the human; follow [AGENTS.md](../AGENTS.md).
