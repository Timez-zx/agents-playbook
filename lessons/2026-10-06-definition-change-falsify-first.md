---
date: 2026-10-06
tags: [verification, pattern, budget]
status: new
agents: ["Claude Opus front/Planner", "Codex gpt-6.1-sol Executor", "Codex gpt-6.1-sol xhigh Verifier"]
---

# Changing a research definition needs a falsifying test before implementation

## Context

A research bitrate controller used a measured delay-spread ratio. An idealized model predicts that ratio equals 1/p, where p is service probability. An earlier dataset comparing the ratio with measured 1/p supported the claim.

## What happened

The front saw the metric rise with the flow's own bitrate even without competing load. It attributed this to packets waiting behind the flow's own earlier packets and redefined the metric to include only packets that found the flow's own queue empty.

The front routed the change as an ordinary feature (W1): spec → Executor → resume fix → fresh xhigh correctness review → installation into the owner's working tree. Unit tests passed, and replays matched reference values computed from the new definition. Review found three code-level issues; no step checked whether the new definition still satisfied the research claim.

After the owner clarified the baseline measurement, the front checked the dataset supporting the claim. The new metric's mean error against 1/p was roughly five times worse than the original, and under heavy load it barely rose. The front reverted the default that turn.

Root cause class: **spec/handoff**, owned and self-reported by the front. Tests and code review checked the implementation against the spec, not the spec against the research claim.

## Lesson

Suggested, not adopted: treat changes to research definitions as W2 ideation. Before writing a spec, run the cheapest falsifying test on the data defining the claim. Implement only after that check supports proceeding. This can also avoid spending worker tokens on a wrong idea.

## Evidence

The detour's worker runs used about 1.04M input tokens, including about 0.95M cached, and about 33k output tokens. An additional xhigh review's usage was not recorded by `codex-task review`; its metadata showed “unknown.” The front's falsifying check used one offline script, took about two minutes, and used no worker tokens.

This is one incident. The five-fold result comes from one comparison on archived data. The likely explanation—that waiting behind the flow's own packets carries contention signal, which filtering removed—was not separately tested. Related: [A faithful implementation can preserve a spec error](2026-10-04-ro-tier-defect.md).

## Applies when

A change alters what a metric, baseline, estimator, or threshold means, or which samples it uses, especially when a theory-versus-data relation already exists.