---
date: 2026-10-04
tags: [environment, tooling]
status: new
agents: ["Claude haiku worker via claude-task"]
---

# Probe Claude worker permissions live

## Context

Live Linux tests checked Claude Code workers under `claude -p`, including read-only and writable tiers.

## What happened

Claude Code's Bash sandbox needed both bubblewrap and socat. Without socat it silently failed to engage. Every non-read-only Bash command then required approval; non-interactive `claude -p` could not approve it, so workers could not run tests.

With socat installed, `-s rw` behaved like Codex workspace-write: tests ran, writes inside the working directory succeeded, outside writes failed with “read-only file system,” network was blocked, and `AGENT_ROLE=worker` was visible.

The sandbox allowed working-directory writes even for a worker described as read-only: `touch` and Python created files. Corrected `claude-task ro` therefore explicitly disables the Bash sandbox. Claude Code still auto-allows read-only commands (`git diff`, `git log`, `grep`) and blocks writes. Trade-off: read-only Claude workers cannot run tests.

A `claude -p --resume <session>` follow-up served 97% of input tokens from cache reads.

## Lesson

Verify every permission tier with live write probes inside and outside the working directory before trusting it. Offline fake-binary tests cannot expose the real sandbox boundary or missing runtime dependencies.

## Evidence

The orchestrator supplied these live-test observations on 2026-10-04. The cache percentage is one measured follow-up, not a guarantee. Corrected flags were tested; re-test of the final wrapper is pending in [STATE](../STATE.md). The separate [read-only defect incident](2026-10-04-ro-tier-defect.md) records spec ownership and independent review.

## Applies when

Using Claude Code as a non-interactive Linux worker, selecting permission tiers, or validating wrapper behavior.
