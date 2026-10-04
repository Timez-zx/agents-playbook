# Collaboration patterns

Choose the workflow for the task's uncertainty. Planner owns design; front owns routing, integration, verification, and delivery. Small tasks bypass coordination overhead. Apply [routing defaults](routing.md): sol high for implementation/writing, sol xhigh for subtle logic/critical review, astra only escalation after sol failure/uncertainty or tie-breaks.

## W1: Spec → build → two-sided review

Default for features/fixes; intent/design and correctness each have one reviewer.

1. Planner designs; front creates a self-contained [handoff](handoff.md) with scope and acceptance commands.
2. Executor (sol high, xhigh for subtle logic) implements in its own worktree and runs tests.
3. Front reviews intent and design fit.
4. Fresh Verifier reviews correctness: sol high normally, sol xhigh for critical review; astra only after sol fails/is uncertain. Critical tooling also gets live permission probes inside/outside the working directory; code review and probes catch different defects.
5. Executor resumes short fixes in the same thread; large revision rounds get a fresh session and precise spec.
6. Front re-runs acceptance rather than rely on the worker's claim.
7. Writer (sol high) writes PR text; front checks facts.

## W2: Diverge → filter → converge

Use when the plan is uncertain; reject weak ideas before implementation.

1. Planner/front and two or three Ideators propose different candidates, each with expected effect and cheapest falsifying test.
2. Read-only sol xhigh Verifier checks feasibility against code with `file:line` citations; escalate to astra only after sol fails/is uncertain.
3. Planner picks; front routes the spec/build workflow.

## W3: Hypothesis → evidence

Use debugging experiments that distinguish explanations.

1. Planner ranks hypotheses and discriminating log points.
2. Executor adds throttled probes to keep logs bounded.
3. Front runs the experiment, including long/GPU work.
4. Verifier reads logs, quotes evidence, and states the supported hypothesis.
5. Planner picks the next bisection; front coordinates it.

## W4: Prototype → rewrite

Validate an idea before polishing it.

1. Planner/front prototypes quickly.
2. Executor rewrites into readable final form under the same tests.
3. Front checks diff and results.

## W5: Resolve a disagreement

Settle a concrete claim once; never average positions.

1. Front states the exact disputed claim.
2. Run a decisive test or use fresh astra `-e max` without either side's reasoning. Tie-breaks are an explicit exception to the sol-first rule.
3. Front decides from evidence; capture reusable lessons after delivery. Reopen only with new evidence.

## W6: Report pass

For human-facing end-of-task reports longer than about 15 lines:

1. Front supplies verified facts as terse bullets.
2. Writer uses sol high (luna for short/simple text), `-s ro --raw`, and [writing rules](writing.md).
3. Front checks facts unchanged and delivers the report.

Writer assignment is independent of front. Codex remains Writer unless accepted reassignment or budget shift routes prose to Claude; keep `-s ro --raw`. Human preference for the full pass remains [unvalidated](../STATE.md).

Short replies come directly from front using the same writing rules. After delivery, one short background Writer call may capture a general surprise; evidence-based improvement proposals never block the task. Follow [AGENTS.md](../AGENTS.md).
