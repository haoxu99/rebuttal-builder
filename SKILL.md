---
name: rebuttal-builder
description: Prepare evidence-grounded academic paper rebuttals from reviewer files through a mandatory three-artifact workflow: (1) a reviewer-by-reviewer verbatim digest of praise and actionable questions, (2) a prioritized cross-reviewer grouping that preserves those exact quotations and reviewer labels, and (3) an approximately 1000-word rebuttal with feasible experiments, direct answers, and concrete revisions. Use when Codex needs to extract, organize, plan, draft, revise, or quality-check conference or journal review responses, author responses, rebuttals, or resubmission responses. Never fabricate or paraphrase reviewer quotations, results, citations, or manuscript locations.
---

# RebuttalBuilder

Create an auditable chain from the source reviews to the final response. Treat the first two artifacts as the author's control surface: pause for feedback after each one unless the user explicitly asks for a single uninterrupted run.

## Non-negotiable deliverables

Create these three files in the task workspace:

1. `01_verbatim_review_digest.md`
2. `02_grouped_prioritized_concerns.md`
3. `03_rebuttal.md`

Start from [the bundled templates](assets/templates/). Keep intermediate files even when the user requests a one-pass result. If the user requires DOCX, PDF, or another format, first create the Markdown artifacts, then export copies; do not replace the auditable Markdown sources.

## Evidence boundary

Maintain three distinct layers:

- **Reviewer text:** exact, contiguous quotations from the supplied review source.
- **Author/agent analysis:** titles, priorities, interpretations, proposed actions, and feasibility notes. Never place these inside a quotation.
- **Verified response evidence:** supplied manuscript facts, completed results, calculations, or author-confirmed commitments.

Never invent results, reviewer intent, citations, manuscript locations, venue rules, or promised changes. Use visible placeholders such as `[RESULT NEEDED]`, `[SETTING NEEDED]`, `[MANUSCRIPT LOCATION NEEDED]`, and `[AUTHOR CONFIRMATION NEEDED]`.

## Step 0: Intake and source preservation

1. Inventory every review, meta-review, score, confidence, manuscript, supplement, result, venue rule, deadline, and output limit supplied by the user.
2. Preserve the source files unchanged. Record source filenames and reviewer-label mapping at the top of Artifact 1.
3. Ask only for missing information that would materially change the work. Continue with explicit placeholders when safe.
4. If the reviews are in DOCX or PDF, use the applicable document/PDF workflow to extract all relevant text. Inspect tables, comments, footnotes, appendices, and page images when they may contain review content.
5. Treat a venue-specified word or character limit as authoritative. Otherwise target 900–1100 English words for the final rebuttal, centered near 1000.

## Step 1: Create the verbatim review digest

Create `01_verbatim_review_digest.md` reviewer by reviewer.

For each reviewer, retain only:

- explicit praise or positive assessment;
- questions;
- criticisms that require an answer;
- requested experiments, analyses, citations, clarifications, or revisions;
- decision-relevant limitations or concerns;
- relevant score/meta-review statements when supplied.

Omit greetings, boilerplate, repeated form labels, empty ratings, and non-actionable narration. Omission is filtering, not rewriting.

### Verbatim rules

- Copy exact contiguous text from the source. Preserve wording, spelling, capitalization, numbers, symbols, citations, and punctuation.
- Permit whitespace normalization caused by file extraction. Do not otherwise edit the quotation.
- Do not paraphrase, translate, grammar-correct, silently shorten, stitch non-contiguous fragments, or insert ellipses.
- When only part of a paragraph is relevant, quote one or more complete contiguous sentences. If sentence boundaries are ambiguous, retain the full paragraph.
- If one source passage contains several issues that cannot be separated without editing, keep it as one quote; split it analytically only in Artifact 2.
- Assign stable IDs: `R1-P01` for praise and `R1-Q01` for questions/actionable concerns. Use `MR` for a meta-review and keep the same reviewer mapping throughout.
- Keep source quotations in blockquotes. Put any neutral note outside the blockquote and label it `Note:`.

Run the quote audit:

```bash
python scripts/validate_artifacts.py quotes --source <review-file> --artifact 01_verbatim_review_digest.md
```

Repeat `--source` for multiple source files. The audit must pass before continuing. For unsupported source formats, manually verify every quote against the rendered source and record that manual verification in the artifact.

### Checkpoint 1

Show the user the file and briefly flag uncertain omissions, reviewer mapping, or source-extraction issues. Ask the user to correct or approve it before grouping. If the user requested uninterrupted execution, continue but mark the checkpoint `provisional` and preserve all uncertainties.

## Step 2: Group and prioritize without changing reviewer words

Create `02_grouped_prioritized_concerns.md` from Artifact 1, not from memory.

1. Reorder questions across reviewers by issue rather than reviewer.
2. Put substantially identical questions, or questions answerable by one shared explanation/experiment, in the same cluster.
3. Give every cluster a short neutral title written by the agent.
4. Prefix every quotation with its stable ID and reviewer label.
5. Copy the exact quotation from Artifact 1. Do not paraphrase it.
6. Assign each concern to one primary cluster so coverage is auditable. Cross-reference secondary relevance instead of duplicating or silently dropping it.
7. Include a coverage checklist mapping every `*-Q*` ID in Artifact 1 to exactly one primary cluster.

### Priority order

Order clusters from most to least decision-critical:

- `P0 — Must address`: correctness, core novelty, invalid evaluation, missing decisive baseline, or shared rejection-driving concern.
- `P1 — High value`: major evidence, generalization, robustness, fairness, scalability, or reproducibility concern.
- `P2 — Address compactly`: useful clarification, local limitation, presentation, related work, or minor requested analysis.
- `P3 — Revision/resubmission`: valuable but infeasible or low-return within the response period.

Judge priority from severity, sharedness, likely decision impact, available evidence, feasibility, and cost. Explain uncertain judgments; do not claim certainty about reviewer intent.

For each cluster add an analysis block outside the quotes:

- decision-relevant concern;
- shared answer strategy;
- evidence already available;
- evidence missing;
- feasible experiment/analysis and minimum viable protocol, if needed;
- fallback if it cannot be completed;
- planned manuscript change;
- confidence and author decision needed.

Prefer one information-dense experiment that resolves several quoted questions. Do not recommend an experiment merely to signal effort. Never present planned work as completed.

Run the cross-artifact audit:

```bash
python scripts/validate_artifacts.py grouping --digest 01_verbatim_review_digest.md --grouped 02_grouped_prioritized_concerns.md
```

The audit must confirm that every grouped quote is copied exactly from Artifact 1 and every actionable ID has one primary placement.

### Checkpoint 2

Show the user the grouped file. Request feedback on clustering, priority, interpretation, experiment feasibility, available results, and commitments. Do not launch costly, long-running, or externally consequential experiments without the required authority. Incorporate feedback into Artifact 2 before drafting.

## Step 3: Build evidence, then draft the rebuttal

Create `03_rebuttal.md` in the cluster order from Artifact 2.

Before drafting, validate every new result:

- Does it answer the quoted concern?
- Are baselines, data, compute, tuning, metrics, and controls matched?
- Are runs, seeds, and uncertainty adequate?
- Is the result positive, negative, mixed, or inconclusive?
- What exact claim can it support?
- What limitation or narrower claim follows?

If a feasible local analysis or experiment can be performed from the provided code/data within scope, do it and record the protocol and result. Otherwise request the needed result or use a visible placeholder/fallback. Never turn an inconclusive result into a positive claim.

### Rebuttal structure

1. Open with a brief, factual summary of genuine reviewer praise and the main response themes. Attribute praise accurately.
2. Respond by prioritized cluster, merging reviewers who raised the same issue.
3. Label each heading with the relevant reviewers, for example `Core novelty and distinction (R1, R3)`.
4. For every major cluster use **Direct answer → Evidence → Revision**:
   - answer in the first sentence;
   - provide verified evidence and conditions;
   - state the exact manuscript change or defensible scope limitation.
5. Group minor corrections compactly.
6. Keep confidential process concerns separate when an appropriate chair channel exists.

Write for a neutral area chair or editor: calm, precise, self-contained, and easy to audit. Acknowledge valid limitations. Correct misunderstandings without blaming the reviewer. Do not repeatedly thank reviewers or ask aggressively for score changes.

Read [drafting guidance](references/drafting-guidance.md) when planning experiments, handling common concern types, compressing, or considering resubmission.

### Length gate

Follow the venue limit when known. Otherwise keep the English rebuttal between 900 and 1100 words. Count only the rebuttal body, excluding the audit metadata after `<!-- AUDIT START -->`:

```bash
python scripts/validate_artifacts.py count --artifact 03_rebuttal.md --min 900 --max 1100
```

Report the exact count at the end of the file. When above the limit, remove repeated thanks, repeated quotations, generic background, rhetoric, duplicate answers, and low-impact detail before removing direct answers, key numbers, controls, uncertainty, claim narrowing, or concrete revisions.

## Step 4: Final audit and user handoff

Run:

```bash
python scripts/validate_artifacts.py all \
  --source <review-file> \
  --digest 01_verbatim_review_digest.md \
  --grouped 02_grouped_prioritized_concerns.md \
  --rebuttal 03_rebuttal.md \
  --min 900 --max 1100
```

Before delivery confirm:

- Artifact 1 contains only verbatim contiguous source quotations plus clearly separated metadata/notes.
- Artifact 2 preserves every quotation exactly, labels every reviewer, groups related concerns, prioritizes clusters, and covers every actionable ID once.
- Artifact 3 answers P0/P1 concerns first and contains no unsupported evidence or invented locations.
- Added experiments are feasible, interpretable, and honestly reported.
- The response follows the venue limit or the default 900–1100-word band.
- All placeholders and decisions needing user input are visible.
- The user receives all three files and a concise list of remaining choices.

If the user changes Artifact 1 or 2, propagate the change downstream and rerun the audits. Never overwrite a user-approved artifact silently.

## Reference case library

Use [the case index](references/cases/INDEX.md) selectively. Consult cases for workflow, grouping, response organization, tone, and compression—not as factual evidence or prose to copy into a new paper. The library is maintainable: future cases can be added as new subfolders and registered in the index.
