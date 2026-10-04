---
date: 2026-10-04
tags: [environment, tooling]
status: new
agents: ["Claude Code orchestrator (tier not recorded)", "Codex CLI worker (tier not recorded)"]
---

# Ubuntu 24.04 can block Codex sandbox startup

## Context

Ubuntu 24.04 had `kernel.apparmor_restrict_unprivileged_userns=1`. Bubblewrap needed a user namespace, an isolated OS environment restricted by that setting.

## What happened

Every command failed in read-only and workspace-write; only danger-full-access worked:

```text
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

The fix installed bubblewrap, added an AppArmor profile for `/usr/bin/bwrap` granting `userns` with `flags=(unconfined)`, and loaded it with `apparmor_parser -r`. AppArmor restricts process access. Claude Code's auto-mode classifier blocked the unapproved policy change.

## Lesson

Check namespace policy for this exact error. A human-approved profile can restore the sandbox; full access is not a routine substitute. The change relaxes security policy.

Action: Obtain human approval before changing AppArmor policy.

After the fix, sandboxed commands had no GPU access, no network by default, and readable `$HOME`. Enable network per task; startup success does not imply unrestricted access. Current Linux prerequisites for both workers are bubblewrap and socat; see [install notes](../playbook/handoff.md).

## Evidence

The session recorded policy value `1`, the error in both sandbox modes, full-access success, and sandbox startup after the profile fix. These are observations from that setup, not all installations.

## Applies when

Codex on Ubuntu 24.04 shows this error with restricted unprivileged user namespaces. Review local policy first.
