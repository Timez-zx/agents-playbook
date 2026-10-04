# Writing for people

Lead with the result, then give the evidence a reader needs to understand it. The Writer owns persistent human-facing prose; the orchestrator follows the same rules for short direct replies. Coordination messages may be terse, but a human should not need to decode internal shorthand to understand the result.

## Style rules and why

- **Conclusion first.** State the outcome before the process, so the reader knows what the details explain.
- **One idea per sentence; short sentences.** Split causes, changes, and evidence into clear steps, so the reader does not have to unpack a dense paragraph.
- **Define terms and abbreviations on first use, or avoid them.** Familiar language reduces the chance that an unexplained label hides the meaning.
- **Prefer concrete facts.** Use numbers, public or generalized file paths, and commands when they help, so claims can be checked. Keep private paths out of public artifacts.
- **Put required action on a separate, clearly marked line.** Use `Action:` when the reader must do something, so the request does not disappear inside an explanation. Do not invent an action when none is needed.
- **Use tables only for comparisons.** A table helps compare roles or alternatives; connected prose explains a single line of reasoning more naturally.
- **Do not expose unexplained internal labels.** Explain the workflow or principle instead of expecting a human to know identifiers such as “P3” or “W1,” so the text stands on its own.
- **Match the reader's language.** Direct replies may be in Chinese if the user writes in Chinese; repo artifacts and commit messages stay in English, so the public project has a consistent shared language.

## Before and after

Before:

> W3 confirms the race; mitigation gates teardown pending verifier ACK.

After:

> The logs show two tasks closing the same connection. The fix lets only one task close it. The correctness review is still pending.

> Action: Wait for that review before merging.

The rewrite states the result, explains the behavior, and separates the reader's action. It also makes the remaining uncertainty visible.

## Who writes which text

The Writer writes or rewrites every persistent human-facing artifact: READMEs, docs, pull request descriptions, lessons, review write-ups, and long end-of-task reports. The orchestrator supplies facts and checks that the final prose preserves them. This keeps readability from depending on the coordinator's preferred shorthand.

For an end-of-task report longer than about 15 lines, use the [report pass](patterns.md): terse facts → read-only Writer → orchestrator fact check → user. For shorter replies, the orchestrator writes directly with the rules above. A handoff should buy better writing, not cost more than the reply itself.

Report what changed, why, how it was verified, and what remains uncertain. Do not turn a worker's claim into a verified fact without a test, diff read, or other-model check. Clear writing must preserve the limits of the evidence.
