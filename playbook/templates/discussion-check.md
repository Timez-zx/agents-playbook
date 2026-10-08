# Discussion check

Template for the [W7](../patterns.md#w7-interactive-discussion) Verifier. Run it with `codex-task run -t sol -e medium -s ro --raw -f <brief>`, and use `resume` for follow-ups on the same topic. `--raw` omits the long work contract, so this template carries the worker rules itself.

## Brief (front fills in)

```text
Question: <one sentence>
Serves decision: <what the human will decide with the answer>
Data scope: <the newest relevant results; name the files or runs; nothing else>
Digest: <the computed numbers or tables, each with the script or command that produced it>
Claims: <the front's claims, numbered>
Time budget: about 10 minutes
```

## Worker rules (send with the brief)

```text
You are a worker. Do not delegate to other agents and do not run codex-task or claude-task. Do not modify files.
Check each numbered claim against the digest.
Recompute from raw data only to settle a disagreement, at most three numbers, and say which.
Do not widen the question, add new questions, or search the web.
If a point needs more work than this allows, write NEEDS DEEP CHECK with what and why, and do not do it.
Answer in at most ten points.
End with:
VERDICT: agree|partly|disagree
POINTS: for each claim, agree or disagree, confidence high|medium|low, and what would change it
RECOMPUTED: each number recomputed and its result, or none
NOT CHECKED: what was not checked
```
