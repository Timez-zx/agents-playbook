# Writing for people

## Four rules for readable documents

1. **Every summary sentence must stand alone.** Name the subject, setting, finding with its key number, and comparison or consequence, so the reader learns something without reading the evidence. Use supplied numbers; never invent one. Prefer a complete, slightly longer sentence to an over-compressed topic label.

2. **Items at one level must be the same kind.** Group parallel points together, so the reader can follow the logic. A progress report has three groups: done (findings), not yet verified but needed (open questions parallel to those findings), and decisions for the reader. Keep open questions out of the findings group.

3. **Formatting must read comfortably.** Use a bold claim followed by one short evidence paragraph, so the page is easy to scan. Never put one sentence per line; use at most one list level and a blank line before headings. Tables compare the same measures across options.

4. **Use plain words and simple sentences everywhere.** Describe first and put the technical term in parentheses second, so the reader understands before learning the label. Use one idea per sentence; explain unfamiliar terms and internal labels before using them. Common terms such as GPU, PR, CLI, JSON, and API need no expansion.

## Process: structure → prose → cold read → checked fixes

Use the [long-document workflow](patterns.md#w6-structure--prose--cold-read--checked-fixes) for reports to the human over about 15 lines, PR descriptions, and README-level documents. Short replies follow the four rules directly.

1. Front writes the [pyramid skeleton](templates/skeleton-format.md): reader and question, one ANSWER sentence, GROUPS of same-kind POINTS with evidence, then DECISIONS. Front owns the logic.

2. Writer uses a fresh Codex sol high session with `-s ro --raw`, the [Writer template](templates/report-writer.md), and the skeleton to write prose. Keep the structure, facts, numbers, and uncertainty unchanged.

3. A fresh Codex luna medium session with `-s ro --raw` receives only the [cold-read template](templates/cold-read.md) and finished text. It restates the answer, groups, points, and decisions, then flags unclear wording, summaries that cannot stand alone, mixed-kind groups, and uncomfortable formatting.

4. Front triages the flags and asks Writer to fix real blockers via resume. Front checks that facts remain unchanged before delivery. Cold readers can over-flag; do not fix a wording flag already resolved in the item's evidence paragraph. Summary sentences must still stand alone.

Writer assignment is independent of front; accepted reassignment or a budget shift may change the Writer under [routing](routing.md). Keep the structure contract and independent cold read.

## Example: a topic label becomes a claim

Invented library-report example:

Before: **Speed is fine.**

After: **In the library's trial, the catalog search took 2 seconds instead of 5, so readers reached results sooner.**

The same set of catalog searches was timed before and after the change.

## Facts, actions, and ownership

Give the conclusion first, supporting points next, and detail only as needed. Preserve facts and uncertainty; explanation quality comes before token savings under [AGENTS.md](../AGENTS.md).

- Prefer concrete evidence: supplied numbers, safe paths, and commands. Never publish private paths or unpublished private measurements.

- Put required action on a separate `Action:` line; invent no action when none is needed.

- Use tables for comparisons, prose for a single line of reasoning.

- Always talk to the human in their preferred language, whatever the language of code, tool output, or worker reports; switch only when they explicitly ask for another language. Repo artifacts and commit messages are English.

Writer writes/rewrites persistent artifacts: READMEs, docs, PR text, lessons, review write-ups, and long reports. Front supplies structure and evidence, checks facts, and owns delivery. Small tasks and short replies skip Writer overhead but follow these rules. Worker coordination may be terse; human prose must stand on its own.

Explain what changed, why, verification, and remaining uncertainty. A worker claim needs a test, diff read, or other-model check before becoming a verified fact. Only new general principles or refinements get a short background Writer call after delivery; the human never waits for upkeep.
