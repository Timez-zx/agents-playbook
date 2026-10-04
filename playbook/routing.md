# Routing rules

Quality comes before cost. The [owner's 2026-10-04 experience](../lessons/2026-10-04-sol-routing-default.md) favors sol as close to astra on most tasks at lower cost; this is owner evidence, not a universal benchmark. Model IDs, tier mappings, supported effort, capability evidence, and check dates live in [models.md](models.md).

| Work | Default | Escalation |
|---|---|---|
| Implementation and writing | Codex sol, high | Astra xhigh after sol fails or is uncertain |
| Routine correctness review | Fresh Codex sol, high | Sol xhigh for deeper logic; astra after failure/uncertainty |
| Subtle logic, concurrency, cross-module work, critical review | Codex sol, xhigh | Astra xhigh after failure/uncertainty |
| Exact disputed claim | Decisive test or fresh astra, max | Tie-break only; omit both sides' reasoning |
| Mechanical work/log summaries | Codex luna, medium | Sol high if the task exceeds the tier |
| Bounded routine agentic coding | Codex reserve, medium | Sol high if it fails or is uncertain |
| Scouting / routine Claude subtasks / ideation and planning | Claude haiku / sonnet / opus | Follow evidence and budget |

`codex-task -t sol` and `claude-task -t sonnet` are wrapper defaults; explicit `-m`/`-e` override model/effort. Astra is permitted only after sol fails/is uncertain or for tie-breaks. Never use `ultra`: it spawns agents outside this playbook's delegation control.

1. Run `agent-quota` only before delegation; apply [budget modes](budget.md).
2. Select the [role](roles.md) and cheapest tier likely to satisfy the quality objectives. Critical review starts at sol xhigh.
3. Escalate with the concrete failure/uncertainty and acceptance criteria, not the same vague prompt.
4. Resume short fixes; use a fresh, precise spec for large revision rounds. Fresh Verifier sessions preserve independence.

Codex front uses these effort rules for itself and Claude tiers for workers. Specialist assignments remain unchanged unless approved separately. The human must make Codex front and ask it to orchestrate; its opt-in skill does not activate itself and remains [unvalidated](../STATE.md).

To add an agent, provide a shared-interface wrapper, evidence-linked profile, routing rows, and model-catalog entries. Catalog facts may be updated directly; routing changes need human approval and a PR under [AGENTS.md](../AGENTS.md).
