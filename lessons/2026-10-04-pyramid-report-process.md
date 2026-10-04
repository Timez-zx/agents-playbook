---
date: 2026-10-04
tags: [writing, pattern, role-evidence]
status: promoted
agents: ["Claude front", "Codex sol high Writer", "Codex luna medium cold reader"]
---

# Front supplies structure; Writer supplies prose; cold reader checks understanding

## Context

Earlier reports used a flat handoff: front supplied facts, Writer wrote prose, and front checked facts. The owner found the language easier but the logic hard to follow. This extends the earlier [readability incident](2026-10-04-writer-readability.md) with new evidence about structure.

## What happened

The flat fact list left Writer to invent the structure. Root cause class: spec/handoff; front owns the structure and delivered report. The owner identified structure and logic as the front's strength and wording as Writer's, then approved a process tested on one real progress report on 2026-10-04.

Front wrote a pyramid skeleton: reader and question, one answer, groups of parallel points with evidence, and decisions. Fresh Codex sol high wrote prose without changing that structure. Fresh Codex luna medium read only the finished text and recovered the complete answer, groups, points, and decisions exactly.

The cold reader caught real readability issues but also flagged wording explained in the next sentence. Front triaged the flags, Writer fixed real blockers via resume, and front checked facts unchanged. The owner sharpened rules for standalone summaries, same-kind groups, comfortable formatting, and plain language.

While preparing the PR, the front also identified an installation hazard: installed skills are symlinks into the fixed clone, so switching branches there silently changes the live skill.

## Lesson

Give Writer the logic before asking for prose. Use an independent cold read to check what a reader understands, then triage its flags rather than accepting every suggestion. Keep the fixed clone on main and develop behavior changes in separate worktrees so live skills stay stable.

The owner approved promotion into [writing.md](../playbook/writing.md), [W6](../playbook/patterns.md#w6-structure--prose--cold-read--checked-fixes), and the [behavior-change worktree rule](../AGENTS.md#behavior-approval-branch-and-pr). Implementation remains subject to PR merge review.

## Evidence

The orchestrator supplied the owner's feedback, explicit approval, exact structure recovery, real flags, and over-flagging on 2026-10-04. The process used fresh read-only Writer and cold-reader sessions with `-s ro --raw`. Token use and elapsed time were measured; private measurements and report content are omitted.

This is one validated report and this owner's role preference, not a controlled model comparison or proof across document types. [STATE](../STATE.md) records that limit. The worktree hazard was identified during PR preparation; no live branch-switch probe is claimed here.

## Applies when

Writing reports to the human over about 15 lines, PR descriptions, or README-level documents; preparing behavior changes in a clone used by installed skill symlinks. Short replies follow writing.md directly.
