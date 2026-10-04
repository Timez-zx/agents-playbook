# Proposals

Use proposals for front switches and specialist-role reassignments. Raise the change in chat with the human first, then record it in one unique `YYYY-MM-DD-<slug>.md` file here. The file makes the evidence, trial, and human decision available to later sessions.

## Template

```markdown
# A specific proposed change

## Proposal

Name the exact front switch or role reassignment.

## Evidence

Link the supporting lessons. Quote owner statements and give their dates.
Separate observations from expectations.

## Expected benefit

State what should improve and how the trial will measure it.

## Risks

List costs, uncertainties, and what could get worse.

## Trial plan

Describe a small, reversible test, acceptance criteria, and how to revert.

## Decision

Filled by the human: accepted | rejected | trial
Date: YYYY-MM-DD
```

Each section makes the decision checkable: scope bounds the change, evidence supports it, expected benefit defines success, risks expose uncertainty, and a reversible trial limits the cost of being wrong. Only the human fills the decision; silence is not approval.

Follow [AGENTS.md](../AGENTS.md) for PRs, privacy, front-switch steps, and STATE updates. Keep `trial` proposals open until the human resolves them. Switching fronts does not automatically exchange specialist roles.
