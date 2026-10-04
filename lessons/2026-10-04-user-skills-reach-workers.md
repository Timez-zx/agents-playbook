---
date: 2026-10-04
tags: [tooling]
status: new
agents: ["Codex sol"]
---

# User-level skills also reach delegated workers

## Context

A delegated Codex worker had a scoped handoff on a machine with user-level skills.

## What happened

The worker announced a user-level skill favoring minimal implementations. Delegation had not isolated it from those skills or instruction files.

## Lesson

Account for user-level instructions when delegating: they can reinforce or conflict with the contract. A clear handoff remains necessary but is not the sole instruction source. The announcement alone establishes no code-quality failure or agent weakness; its quality effect was not assessed.

## Evidence

The supplied Codex sol worker announcement establishes instruction reach. No code-quality outcome was supplied or independently assessed.

## Applies when

Delegating on a machine with user-level skills or instruction files.
