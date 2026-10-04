# Current state

- **Current front:** Claude (Claude Code).
- **Validated (live, 2026-10-04):** Claude front + Codex workers via `codex-task` (`run`, `resume`, `review`, `peek`, `watch`, `ls`, `--search`); `claude-task` final wrapper (`run` with ro and rw write probes inside/outside the working directory, `resume`); `agent-quota`; `model-review` (forced dry-run, silent fresh re-check); `install.sh` (first real install: skill and command links, Codex-front skill correctly skipped).
- **Partially validated:** `model-review` research run (offline tests only).
- **Not validated:** Codex front (opt-in skill), budget thresholds, and human preference for the report pass (W6).
- **Open proposals:** None.
- **Last updated:** 2026-10-04.

Update validation, proposals, and front here under [AGENTS.md](AGENTS.md). Status records evidence; it does not approve behavior changes.
