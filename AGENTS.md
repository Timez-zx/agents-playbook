# How agents-playbook runs

This is the single source of truth for operating, updating, and improving this repo. The design is agent-agnostic: today's main pair is Claude Code + Codex CLI because the owner currently considers them the strongest, but more agents will appear. Add an agent with a `<agent>-task` wrapper using the shared interface, an `<AGENT>.md` profile, and rows in [routing.md](playbook/routing.md).

## Read order

For an agent arriving to work on this repo, read in this order:

1. `AGENTS.md`: operating and maintenance rules, so changes follow one policy.
2. [STATE.md](STATE.md): current front, validation status, and proposals, so an experiment is not mistaken for a proven mode.
3. The profile of each agent you will work with: [CLAUDE.md](CLAUDE.md), [CODEX.md](CODEX.md), or the added agent's profile. Evidence and mitigations explain the current assignments.
4. [playbook/roles.md](playbook/roles.md): authoritative assignments, so routing uses the agreed roles.
5. Lessons with `status: new` in [lessons/](lessons/README.md): recent evidence that may not yet be a rule.
6. Open files in [proposals/](proposals/README.md): pending trials and decisions, so sessions do not duplicate or contradict them.

This is the read order for repo work, not a preload list for every project task. During an ordinary installed-skill session, read only `repo/STATE.md` at startup and open other documents when the current step needs them. Bounded reading keeps the playbook out of the real task's way.

## Non-intrusive by design

The playbook serves the task. Small questions, edits below about 30 lines, and quick lookups just get done: no delegation, quota check, or lesson. Their coordination cost would exceed the benefit.

At session start, read only the short STATE file. Run `agent-quota` only when a task will be delegated. Never load the whole playbook up front; open a file only for the step at hand, so coordination does not consume the session.

Upkeep happens after delivery. Once the human has the result, use one short Writer call in the background to capture a general surprise; skip it if nothing general was learned. The human never waits for playbook upkeep because the session exists to complete their task.

Keep upkeep in this repo. It never touches the human's project repos, and project-task work never edits the playbook. Retry a maintenance failure later or drop it; a git conflict or network failure in upkeep is never reported as a failure of the delivered task. Isolation keeps optional learning from disrupting real work.

Improving the playbook itself becomes a task only when the human asks for it. Routine lesson capture does not authorize a broader redesign.

## Iteration loop

1. **Use:** Apply the playbook on real tasks. Real outcomes supply stronger evidence than speculative rules.
2. **Record:** After delivery, write one lesson per general surprise. Separate incidents stay traceable, and ordinary small tasks need no upkeep.
3. **Promote:** When at least two lessons agree, or one has strong evidence, open a PR folding the lesson into the playbook. This threshold keeps a local accident from becoming a universal rule.
4. **Approve:** The human approves behavior changes. Public instructions affect every user who installs them.
5. **Live:** Installation uses symlinks; the next session loads the updated clone without re-setup. Keep the clone fixed so those links remain valid.

## Front and specialist roles

The **front** is the agent the human is talking to, selected by which tool the human opens. The front is the Orchestrator: it talks to the human, routes work, integrates results, and owns outcomes. A front switch requires a proposal and human decision; the human then talks to the other agent, which continues iterating from this repo.

The specialist **roles** are Planner, Scout, Ideator, Executor, Verifier, and Writer. Any agent can hold any role, regardless of the front. Reassigning a role changes [roles.md](playbook/roles.md) through a PR; switching fronts does not automatically exchange all assignments.

Planner owns decomposition and design decisions. Today the front, Claude, also holds Planner. If evidence favors another planner, the front delegates planning while keeping coordination, verification, and the human conversation. This lets a better plan improve the work without forcing a conversation switch.

Raise a front-switch or role-reassignment proposal in chat when role evidence favors it. Evidence informs the proposal; the human decides, so neither agent can promote itself through an unsupported comparison.

## STATE.md

[STATE.md](STATE.md) is a short record of the current front, validated and partially validated modes, unvalidated modes, open proposals, and the last update date. Keep observations separate from expectations so later sessions know which paths have live evidence.

Update it in any session that changes a mode's validated status, opens or closes a proposal, or changes the front. Small STATE updates go directly to main like lessons because they record status; they do not authorize a behavior change. A decision marked `trial` stays open until the human resolves it.

## Proposals and decisions

Use `proposals/YYYY-MM-DD-<slug>.md` for front switches and role reassignments. Raise the proposal in chat with the human first; the file records that discussion. Give it a unique slug so concurrent sessions do not share a draft.

Use the [proposal template](proposals/README.md) with these sections:

- **Proposal:** The exact front or role change, so the decision has a bounded scope.
- **Evidence:** Links to lessons and quoted owner statements, so claims can be checked.
- **Expected benefit:** The outcome the change should improve, so a trial has a purpose.
- **Risks:** Costs and uncertainties, so acceptance does not imply certainty.
- **Trial plan:** A small, reversible test, so the comparison does not require a permanent switch.
- **Decision:** Filled by the human with `accepted`, `rejected`, or `trial`, and a date, so agents do not infer approval from silence.

After the human accepts a front switch:

1. Update roles.md and both profile files to reflect the accepted front and assignments. Align both skills' compact role tables if assignments changed, so installed instructions agree.
2. Run `./install.sh --with-codex-front` to install the opt-in Codex-side skill. Installation makes the entry available; it does not itself change who the human talks to.
3. Update STATE.md with the front and proposal decision. Preserve unvalidated status until a mode has actually been tested.
4. The human starts talking to the new front. The new front owns the next task and continues using this repo's evidence.

Changes to roles, profiles, and skills follow the behavior-change PR process below. A proposal records a decision; it does not bypass review of the implementation.

## Profiles and accountability

Profiles contain Strengths, Weaknesses, Roles held now, Candidates, Mitigations in force, and Evidence links. Candidate entries name a possible alternative for each held specialist role and the evidence that would decide the comparison. Keep environment and tooling quirks in Operating notes, not agent weaknesses, so the profile describes the agent rather than a machine's restrictions.

The owner requires agents not to keep shifting blame onto each other ("不能反复推锅"). Apply these firm rules:

1. **The front owns the outcome.** Anything delivered to the human is the front's responsibility, whichever worker produced it. A defect that reaches the human is also a front verification miss. One accountable coordinator prevents responsibility from disappearing between agents.
2. **Fix the process, not the agent.** Classify the root cause as spec/handoff, execution, verification, tooling, or environment. Change the template, contract, test, or tool that let it through. A process fix prevents recurrence; a label about an agent does not.
3. **One incident, one lesson.** Record it once; every profile discussing it cites that same lesson. No rebuttal lessons. Settle a dispute once through a fresh tie-break session in [patterns.md](playbook/patterns.md), or by the human. The outcome stands unless new evidence appears, so competing narratives do not become an endless blame loop.
4. **Weaknesses need evidence above a threshold.** Require at least two independent incidents or an explicit human statement. Single incidents stay in lessons only. This prevents one failure from becoming a permanent reputation.
5. **Self-report first.** The agent that finds its own error records it; this counts in its favor. Workers supply the facts through their result rather than edit the playbook outside their scope. Rewarding disclosure makes errors easier to find and fix.
6. **Evidence only.** Every profile claim links a lesson or quotes the human. Either agent may edit any profile only by adding or removing evidence-linked claims. Unsupported opinions cannot change an assignment or profile.

Profile changes use PRs because they can affect routing. A candidate is a testable possibility, not an established capability claim.

## Git, PRs, and publication

Keep one fixed local clone; the default is `~/agents-playbook`. Symlinked installation makes edits live, so later sessions can load a change without reinstalling. The installer interface is `install.sh [--with-codex-front] [--uninstall]`; the Codex-front skill is opt-in because that mode is not validated.

Install backups are moved outside skill directories into `~/.agent-runs/install-backups/`. A backed-up skill must never be loaded, because it may contain obsolete instructions.

Write all repo text and commit messages in English so contributors and agents share one language. In conversation, match the human's language. The Writer writes or rewrites persistent human-facing text; the front supplies facts and checks the prose before publication.

### Lessons and STATE: small direct commits to main

After delivery, capture a lesson for a surprising failure, measured routing choice, tool quirk, or human output preference. Use one unique `lessons/YYYY-MM-DD-<slug>.md` file per incident and the [lesson template](lessons/README.md). The front supplies facts, the Writer writes, and the front checks facts and privacy. The split preserves readability without shifting responsibility.

Use `role-evidence` for concrete comparisons: who found a bug, whose design was simpler, or whose text the human preferred. Record a preference as evidence from this user, not a universal brand ranking.

From the playbook clone on main, replace the illustrative filename and topic below:

```sh
git pull --rebase
git add lessons/YYYY-MM-DD-topic.md
git commit -m "Record lesson about topic"
git push
```

Use the same sequence with `git add STATE.md` for a small status update. Resolve a conflict, rebase again, and retry a rejected push when appropriate. Unique lesson names reduce collisions; rebasing preserves concurrent work. If background upkeep fails, retry later or drop it without making the human wait.

Workers never commit or push. The front owns publication after checking facts and privacy, so a worker cannot accidentally publish raw session material.

### Behavior changes: branch and PR

Use a branch and PR for skills, scripts, playbook rules, role assignments, profiles, and their proposal records. The human approves merges because these changes affect shared behavior. Replace the branch and file placeholders before running:

```sh
git pull --rebase
git switch -c change-branch
git add changed-file.md
git commit -m "Describe the behavior change"
git push -u origin change-branch
```

Open a PR describing the concrete problem, resulting behavior, and validation. The Writer writes its title and description; the front checks facts. Review text should let a human assess the change without reconstructing a session.

Promote when at least two lessons agree or one has strong evidence. Fold the rule into the playbook through a PR, mark supporting lessons `status: promoted`, and link to the adopted rule. This makes the rule's basis traceable. Mark obsolete lessons `retired` with a reason, rather than discard the evidence history.

### Privacy before publication

Generalize every lesson, proposal, profile, and example. Never publish private repo names, paths under a user's home, emails, hostnames, credentials, account IDs, session IDs, or unpublished numbers from private work. The generic installation paths and variable templates in these docs are public configuration examples, not private user paths.

Use placeholders and safe excerpts. Include numbers only when supplied as public lesson evidence or cleared for publication. Check command output and logs as well as prose, because the evidence can identify private work even when the conclusion does not.

### Review checklist

- Follow [writing.md](playbook/writing.md), so readers can understand the change.
- Resolve relative Markdown links and both skill `repo` symlinks, so installed instructions reach the clone rather than the install directory.
- Route every skill link through `repo/...`; use `git -C "$REPO"` for skill maintenance commands. The install directory is a symlink and must not determine repository paths.
- Keep the Claude skill within 120 lines and the Codex skill within about 130, so repeated session loading stays cheap.
- Validate affected behavior with exact commands and expected results, so “done” remains checkable.
- Review the diff for scope and privacy, so unrelated work and private data stay out of the public repo.
