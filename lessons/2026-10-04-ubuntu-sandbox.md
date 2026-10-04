---
date: 2026-10-04
tags: [environment, tooling]
status: new
agents: ["Claude Code orchestrator (tier not recorded)", "Codex CLI worker (tier not recorded)"]
---

# Ubuntu 24.04 can block Codex sandbox startup

## Context

The first session used Ubuntu 24.04 with `kernel.apparmor_restrict_unprivileged_userns=1`. Codex's bubblewrap sandbox needed a user namespace, an isolated operating-system environment controlled by that security setting.

## What happened

Every command failed in both read-only and workspace-write sandboxes. Only danger-full-access worked. The failure message was:

```text
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

The fix was to install bubblewrap, add an AppArmor profile for `/usr/bin/bwrap` granting `userns` with `flags=(unconfined)`, and load that profile with `apparmor_parser -r`. AppArmor is a Linux security system that restricts what a process may do.

Claude Code's auto-mode classifier blocked the agent from applying that fix unasked. The change relaxes a security policy and needs human approval.

## Lesson

Check the namespace policy when this exact startup error occurs. An approved bubblewrap profile can restore the sandbox without using full access for every task. Do not apply the policy change without the human's approval, because it changes a system security restriction.

Action: Ask the human to approve the AppArmor change before applying it.

After the fix, sandboxed commands had no graphics processing unit (GPU) device access and no network by default. Network access must be enabled per task. `$HOME` was readable. Account for those boundaries when planning experiments, so a successful startup is not mistaken for unrestricted access.

## Evidence

The session observed the same `bwrap` error in read-only and workspace-write modes, success in danger-full-access, and sandbox startup after the profile fix. The recorded policy value was `1`. These are observations from that Ubuntu 24.04 setup, not a claim about every installation.

## Applies when

Codex on Ubuntu 24.04 fails with the quoted bubblewrap error while unprivileged user namespaces are restricted. Review the local policy before applying this environment-specific fix.
