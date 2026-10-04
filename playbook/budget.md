# Budget and efficiency

Quality of the outcome and explanation comes before token savings. Check both quotas only before delegation; compare usage with elapsed window time. Small tasks skip checks. Thresholds below remain [unvalidated](../STATE.md).

## Quota sources

`agent-quota [--json]` reports both quotas, burn-rate status, and routing advice; `--codex-line` is supported.

Codex: newest `sessions/YYYY/MM/DD/rollout-*.jsonl` in its data directory (default user's `.codex`), last `rate_limits` object:

- `primary.used_percent`: percentage used.
- `primary.window_minutes`: window length (`10080` = weekly).
- `primary.resets_at`: epoch-second reset time.
- `plan_type`, `credits.balance`: account budget context.

Claude desktop: `get_usage` exposes `percentUsed`/`resetsAt`. CLI: `claude -p --output-format stream-json --verbose` emits `rate_limit_event`; `rate_limit_info.unifiedWindows.<window>.utilization` is 0–1, and `resetsAt` is reset time. `claude-task` records these; convert utilization to percent.

## Burn rate and modes

```text
window_start = reset_time - window_length
elapsed_percent = 100 × fraction of window elapsed
over-burning = used_percent > elapsed_percent + 20
```

The margin is 20 percentage points: after 30% elapsed, above 50% used is over-burning. Raw usage thresholds still apply.

| State | Action |
|---|---|
| Both healthy | Default routing |
| Claude over-burning or >70% used | Codex also scouts/writes; fewer/cheaper Claude subagents; front coordinates/decides |
| Codex over-burning or >70% used | Claude sonnet routine execution; preserve Codex critical verification |
| Either >90% used | Critical work only on that side; tell human |

Above 90% takes priority for that side. If both are constrained, apply both restrictions. These are experimental starting thresholds, not account guarantees.

## Spend less without losing quality

1. Delegate large file/log reading; ask for compressed `file:line` summaries to protect front context.
2. Write terse, complete specs; omit irrelevant history the worker cannot use.
3. Follow [routing](routing.md): sol high for implementation/writing, sol xhigh for subtle logic/critical review; astra only escalation after sol failure/uncertainty or tie-breaks.
4. Resume short fixes, not large revision rounds. [One Codex follow-up](../lessons/2026-10-04-resume-cache.md) had 53k/58k cached input (~90%); [Claude resume](../lessons/2026-10-04-claude-worker-sandbox.md) had 97%. [Large resumed revisions](../lessons/2026-10-04-thread-growth-cost.md) still grew substantially; use fresh sessions and precise specs. Cache rates are observations, not guarantees.
5. Bound worker results to STATUS/CHANGES/VERIFICATION/RISKS, including unverified claims.
6. One verifier per aspect; intent/design and correctness differ. Critical tooling combines independent code review and live probes because they catch different defects.
7. Measure every run: both wrappers record tokens, and `ls` shows usage/status.

Budget shifts and front switches never waive verification, front responsibility, or the worker-delegation ban. Specialist assignments remain authoritative unless separately reassigned.
