# Contributing

Keep lessons small, evidence-based, and safe to publish. Changes to behavior need a pull request (PR) and human approval because this public repo's installed skills affect every user.

## Work from one fixed clone

Keep the local clone in a fixed location. The default is a directory named `claude-codex-playbook` in your home directory. Installation links to that clone, so edits are live without reinstalling. Be deliberate about changes to skills and rules: later sessions will load them.

Write commit messages and all repo text in English. This gives contributors and agents one shared language. For direct conversation, match the user's language.

## Capture a lesson

At the end of every task, check whether anything deserves a general lesson. Write one when something surprised you: a failure mode, a routing choice that worked or failed with numbers, a tool quirk, or a human preference about output. Routine tasks with no new evidence need no forced lesson.

The orchestrator supplies terse facts. The Writer turns them into lesson prose using the [template](lessons/README.md). The orchestrator checks the facts before saving it. This separates clear writing from responsibility for accuracy.

Create one file per lesson: `lessons/YYYY-MM-DD-<slug>.md`. Choose a unique, specific slug so concurrent sessions do not edit the same file. Include the required front matter and five sections from the template.

Use `role-evidence` for comparisons of the agents: who found a bug, whose design was simpler, or whose writing the human preferred. Repeated observations can justify a role change; one preference is evidence to record, not a universal ranking.

## Publish lessons to main

Lessons go straight to main because recording evidence does not itself change the playbook's behavior. Run these commands from the fixed clone on main, replacing the placeholder with the new lesson:

```sh
git pull --rebase
git add lessons/YYYY-MM-DD-<slug>.md
git commit -m "Record lesson about <topic>"
git push
```

If a concurrent update causes a conflict or rejects the push, resolve the conflict, rebase again, and retry. Unique filenames reduce collisions; rebasing preserves other sessions' work. Workers never commit or push: the orchestrator owns publication after checking the Writer's facts and privacy.

## Change behavior through a PR

Use a branch and PR for changes to skills, scripts, playbook rules, or the roles table. The human approves merges because these changes alter the instructions or tooling other users rely on.

```sh
git pull --rebase
git switch -c <change-branch>
git add <changed-files>
git commit -m "Describe the behavior change"
git push -u origin <change-branch>
```

Open a PR with the concrete problem, resulting behavior, and validation. The Writer writes or rewrites its title and description; the orchestrator checks the facts. Clear review text lets the human assess the change without reconstructing a session.

Promote a lesson when at least two lessons agree, or one has strong evidence. Open a PR that folds the rule into the playbook. In the same change, mark the supporting lessons `status: promoted` and link to the promoted rule. This keeps the rule's evidence traceable. Use `retired` when a lesson no longer applies, and explain why rather than silently losing the history.

For a role swap, update the authoritative table in [roles.md](playbook/roles.md) and both skills' compact role tables in one PR. The user decides whether to swap; coordinated edits prevent sessions from loading contradictory assignments.

## Privacy before publication

Generalize every lesson and example. Never publish private repo names, paths under a user's home, emails, hostnames, credentials, account identifiers, session identifiers, or unpublished numbers from private work. Public evidence should explain the behavior without exposing the person or project behind it.

Use placeholders for paths and identifiers. Only include numbers already supplied as public lesson evidence or cleared for publication. Check lesson prose, command output, and excerpts before committing; logs can contain private data even when the conclusion does not.

## Review checklist

- Check the [writing guide](playbook/writing.md), so humans can follow the change.
- Resolve relative Markdown links and keep both skill `playbook` symlinks intact, so installed instructions can reach their details.
- Keep each skill within about 130 lines, so repeated session loading stays cheap.
- Validate the affected behavior with exact commands and expected results, so a worker's claim can be checked.
- Review the diff for scope and privacy, so unrelated changes or private data do not enter the public repo.
