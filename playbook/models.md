# Model catalog

This catalog records facts, not routing decisions. The seed below uses the supplied wrapper interface, session model metadata, and dated owner evidence; no independent model research has run. “Last checked” is the seed evidence date, not an availability guarantee. Unknown details are **not yet researched**. Routing policy lives in [routing.md](routing.md).

## Codex models

Effort levels below are exposed in this session where supplied; they do not guarantee support in every CLI/account. The playbook prohibits `ultra` even where available.

| Model | Provider | Tier / effort levels known | Capability evidence and date | Last checked |
|---|---|---|---|---|
| `gpt-6-luna` | OpenAI | `luna`, default medium; session: low, medium, high, xhigh, max | Session calls it fast/affordable for easier tasks, 2026-10-04; independent research pending | 2026-10-04 |
| `gpt-reserve` | OpenAI | `reserve`, medium; other efforts not yet researched | Cheap agentic coding is the supplied routing use, not a measured capability; not yet researched | 2026-10-04 |
| `gpt-6.1-sol` | OpenAI | `sol` (default), high; session: low, medium, high, xhigh, max, ultra | [Owner: close to astra on most tasks, lower cost](../lessons/2026-10-04-sol-routing-default.md), 2026-10-04; [Writer run measurements](../lessons/2026-10-04-thread-growth-cost.md) | 2026-10-04 |
| `gpt-6-astra` | OpenAI | `astra`, xhigh; session: low, medium, high, xhigh, max, ultra | [Independent review found five high-severity defects](../lessons/2026-10-04-ro-tier-defect.md), 2026-10-04; no same-task comparison with sol | 2026-10-04 |
| `gpt-6-sol` (legacy) | OpenAI | No wrapper tier; session: low, medium, high, xhigh, max, ultra | Session lists previous-generation workhorse; capabilities not yet researched | 2026-10-04 |
| `gpt-5.6-sol` (legacy) | OpenAI | No wrapper tier; session: low, medium, high, xhigh, max, ultra | Session lists older-generation workhorse; capabilities not yet researched | 2026-10-04 |

“Legacy” means outside this playbook's current tier defaults, not a claim of provider deprecation.

## Claude models

These are owner-supplied model names. Exact provider IDs, effort support, and alias resolution are not yet researched; do not invent IDs for the startup check. Tier names are the wrapper's `haiku`, `sonnet` (default), and `opus`; mapping each alias to a version still needs research.

| Model | Provider | Tier / effort levels known | Capability evidence and date | Last checked |
|---|---|---|---|---|
| Fable 5.1 | Anthropic | No supplied wrapper tier; efforts not yet researched | Not yet researched; name supplied 2026-10-04 | 2026-10-04 |
| Opus 5.5 | Anthropic | Opus family; exact alias/efforts not yet researched | Version-specific capability not yet researched; [spec incident](../lessons/2026-10-04-ro-tier-defect.md) identifies Opus without version, 2026-10-04 | 2026-10-04 |
| Sonnet 5.5 | Anthropic | Sonnet family; exact alias/efforts not yet researched | Not yet researched; name supplied 2026-10-04 | 2026-10-04 |
| Haiku 4.5 | Anthropic | Haiku family; exact alias/efforts not yet researched | Version-specific capability not yet researched; [live sandbox tests](../lessons/2026-10-04-claude-worker-sandbox.md) identify Haiku without version, 2026-10-04 | 2026-10-04 |

The [Claude profile](../CLAUDE.md) holds owner observations about Claude generally; they do not establish version-specific capabilities.

## Event-driven updates

```text
model-review --if-stale [DAYS] [--claude-models ids] [--force] [--dry-run]
```

At Claude-front startup: `model-review --if-stale 3 --claude-models "<Claude model ids known from system context>"`. Three days controls the list-check freshness, not a recurring research schedule. The check is free and silent when model lists have not changed. Only changed lists start one background Codex sol `--search` research run.

Read the result when finished; update facts here directly with source links, evidence dates, and last-checked dates. Mention the update to the human in one line at a natural point. Any proposed routing change follows [AGENTS.md](../AGENTS.md): short evidence-based proposal after delivery, human approval, then a behavior-change PR. Catalog updates cannot silently change routing.
