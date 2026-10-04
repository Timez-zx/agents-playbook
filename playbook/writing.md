# Writing for people

## First rule: top-down, accurate, concise

Give the conclusion first, supporting points next, and detail only as needed. Preserve facts and uncertainty; remove words that do not help understanding. Explanation quality comes before token savings under [AGENTS.md](../AGENTS.md).

Before:

> We checked the logs, added a guard, and ran tests. W3 confirms the race; verifier ACK is pending.

After:

> The fix prevents two tasks from closing the same connection. Tests pass; independent correctness review is pending.

> Action: Wait for that review before merging.

## Other rules

- One idea per sentence; short sentences keep causes and evidence clear.
- Define unfamiliar terms for a capable engineer or avoid them. Leave GPU, PR, CLI, JSON, and API unexpanded.
- Prefer concrete evidence: numbers, safe paths, commands. Never publish private paths.
- Put required action on a separate `Action:` line; invent no action when none is needed.
- Use tables for comparisons, prose for a single line of reasoning.
- Explain internal labels rather than assume the human knows “P3” or “W1.”
- Match the human's language in conversation; repo artifacts and commit messages are English.

## Ownership and verification

Writer writes/rewrites persistent artifacts: READMEs, docs, PR text, lessons, review write-ups, and long reports. Front supplies facts and checks the prose. Worker coordination may be terse; human prose must stand on its own.

Small tasks and short replies skip Writer overhead but follow these rules. Reports over about 15 lines use the [report pass](patterns.md): verified facts → read-only Writer → front fact check → human.

Explain what changed, why, verification, and remaining uncertainty. A worker claim needs a test, diff read, or other-model check before becoming a verified fact. General lesson writing happens after delivery in one short background call; the human never waits for upkeep.
