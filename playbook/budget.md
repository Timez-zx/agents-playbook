# Budget and efficiency

Read both quotas before choosing a routing mode. Compare usage with elapsed time in the quota window, because the same percentage can mean a comfortable pace or a fast drain. Shift routine work toward the agent with headroom while preserving critical-path capacity.

## Quota sources

`agent-quota [--json]` reports both quotas, burn-rate status, and routing advice. Machine-readable sources allow routing to use evidence instead of estimates.

For Codex, read the newest `sessions/YYYY/MM/DD/rollout-*.jsonl` in the Codex data directory, then its last `"rate_limits"` object. The default data directory is the user's `.codex` directory. Relevant fields are:

- `primary.used_percent`: usage as a percentage, so the threshold can be compared directly.
- `primary.window_minutes`: window length; `10080` means a week, so pace must use that window rather than a day.
- `primary.resets_at`: reset time in epoch seconds, so elapsed time can be calculated.
- `plan_type` and `credits.balance`: plan and remaining credits, so the report includes the account's budget context.

In Claude Code desktop, use `get_usage`: plan windows expose `percentUsed` and `resetsAt`. From the command line, `claude -p --output-format stream-json --verbose` emits `rate_limit_event`; read `rate_limit_info.unifiedWindows.<window>.utilization` (0–1) and `resetsAt`. `claude-task` records these events' quota data. Convert utilization to percent before comparing it with the thresholds, so the scales match.

## Burn-rate rule

```text
window_start = reset_time - window_length
elapsed_percent = 100 × fraction of the window elapsed
over-burning = used_percent > elapsed_percent + 20
```

The margin is 20 percentage points. If 30% of a window has elapsed, usage above 50% is over-burning. Usage of 45% is not over-burning by this rule, although the raw usage thresholds below still apply. Pace catches a problem early enough to shift work.

## Routing modes

| State | Action | Why |
|---|---|---|
| Both healthy | Keep default routing | No evidence calls for a budget shift |
| Claude over-burning or above 70% used | Codex also takes Scout and Writer work; use fewer or cheaper Claude subagents; the orchestrator only decides | Reduce Claude's routine spending while keeping its coordination judgment |
| Codex over-burning or above 70% used | Claude sonnet subagents take routine Executor work; preserve Codex for critical-path verification | Spend remaining Codex capacity where its rigor matters most |
| Either above 90% used | Only critical-path work on that side; tell the user | Preserve the last capacity and make the constraint visible |

The above-90% rule takes priority for that side. If both sides are constrained, apply each side's restriction rather than assume one has spare capacity. These thresholds are starting rules for this experimental playbook, not guarantees about every account.

## Spend less without losing evidence

1. Delegate reading of large files and logs. Request compressed `file:line` summaries, because orchestrator context is the scarcest resource.
2. Write terse, complete specs. The worker cannot see the conversation, but repeating irrelevant history costs tokens without clarifying the task.
3. Use the cheapest plausible tier and escalate on failure. Critical-path review goes straight to the top tier because missing a defect can cost more than the review.
4. Use `resume` for follow-ups. One measured Codex follow-up served about 90% of input tokens from cache: 53k of 58k on the first follow-up turn in the same thread. This is observed evidence, not a promised cache rate; see the [lesson](../lessons/2026-10-04-resume-cache.md).
5. Keep worker final messages within the contract's status, changes, verification, and risks sections. Bounded results keep integration cheap while exposing unverified claims.
6. Assign one verifier per aspect. Intent/design and correctness can have different reviewers; reviewing the same aspect twice needs a reason beyond habit.
7. Measure every run. Both wrappers record token counts, and `ls` shows usage with run status. Measurements reveal whether a routing choice saved budget or merely moved it.

When the user swaps orchestration direction, preserve these rules and apply the authoritative role assignments. Budget shifts change who does routine work; they do not waive verification or the ban on worker delegation.
