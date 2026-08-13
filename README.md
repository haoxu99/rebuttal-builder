# RebuttalBuilder

> Build a focused, evidence-grounded rebuttal from complex reviewer feedback.

RebuttalBuilder is a Codex skill for systematically building focused, evidence-grounded academic rebuttals through a reviewable workflow. Instead of jumping directly from long review files to a polished response, it creates three auditable artifacts:

1. a reviewer-by-reviewer digest containing only verbatim praise and actionable concerns;
2. a prioritized cross-reviewer concern map that preserves the exact quotations;
3. an approximately 1,000-word rebuttal organized around the issues most likely to affect the decision.

The workflow keeps reviewer quotations, author analysis, and verified response evidence separate. It never permits invented results, citations, reviewer intent, or manuscript locations.

## 中文简介

RebuttalBuilder 是一个用于系统化构建学术论文 rebuttal 的 Codex skill。它通过提炼、归类、规划和撰写审稿回复，帮助作者生成重点明确、证据充分的 rebuttal。它不会直接跳到终稿，而是依次生成三份可供作者检查和修改的文件：

1. 按审稿人整理的逐字摘录，只保留赞赏和需要回应的问题；
2. 跨审稿人合并、标注来源并按重要程度排序的问题清单；
3. 基于已验证证据撰写的约 1,000 词 rebuttal。

前两份文件中的审稿人内容必须保留原话，不允许意译、翻译、润色、拼接或用省略号缩写。作者可以在每个阶段确认分类、优先级、实验可行性和回复策略。

## Why RebuttalBuilder?

Strong rebuttals require more than fluent writing. Authors must filter long review files, identify shared concerns, decide what evidence matters, prioritize feasible experiments, and compress the result into a strict response budget. RebuttalBuilder turns those steps into an explicit and testable build process.

- **Verbatim first:** reviewer wording is preserved before interpretation begins.
- **Cross-reviewer synthesis:** related questions are answered together instead of repeated reviewer by reviewer.
- **Decision-aware priority:** correctness, novelty, decisive baselines, and shared major concerns come first.
- **Human checkpoints:** authors can revise the digest and concern map before drafting.
- **Evidence discipline:** planned experiments remain distinct from completed results.
- **Executable audits:** bundled validation checks quote fidelity, concern coverage, and rebuttal length.
- **Maintainable case library:** prior rebuttals can be added as reusable structural references.

## Workflow

```text
Raw reviewer files
        │
        ▼
01_verbatim_review_digest.md
Reviewer-by-reviewer exact quotations
        │
        ▼  Author checkpoint 1
02_grouped_prioritized_concerns.md
Cross-reviewer clusters, P0–P3 priority, evidence and experiment plan
        │
        ▼  Author checkpoint 2
03_rebuttal.md
Direct Answer → Evidence → Revision
        │
        ▼
Quote, coverage, evidence, and word-count audit
```

Unless a venue specifies another limit, the final English rebuttal targets 900–1,100 words, centered near 1,000.

## Installation

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/YOUR-USERNAME/rebuttal-builder.git ~/.codex/skills/rebuttal-builder
```

Alternatively, clone it anywhere and provide the path to the skill explicitly when asking Codex to use it. Restart or refresh Codex if the newly installed skill is not immediately visible.

The repository folder should remain named `rebuttal-builder`, matching the `name` field in `SKILL.md`.

## Usage

Invoke the skill explicitly with `$rebuttal-builder` and attach or reference the review files:

```text
Use $rebuttal-builder to process these reviewer files.

First create the verbatim review digest and stop for my approval. Then group and
prioritize related concerns across reviewers. After I confirm the experiment
plan and provide the results, draft an approximately 1,000-word rebuttal.
```

Useful information to provide includes:

- all reviews and meta-reviews;
- scores and reviewer confidence;
- manuscript and supplementary material;
- venue, rebuttal deadline, and word or character limit;
- venue policy on new experiments;
- available compute, data, and author time;
- completed experiment results and exact settings.

Missing evidence is never silently filled. The skill uses visible markers such as `[RESULT NEEDED]`, `[MANUSCRIPT LOCATION NEEDED]`, and `[AUTHOR CONFIRMATION NEEDED]`.

## Output artifacts

### 1. `01_verbatim_review_digest.md`

Organizes each reviewer's praise and actionable concerns while removing greetings, boilerplate, empty form labels, and non-actionable narration. Every retained passage receives a stable ID such as `R1-P01` or `R2-Q03`.

Reviewer quotations must be exact, contiguous source text. Only extraction-related whitespace normalization is allowed.

### 2. `02_grouped_prioritized_concerns.md`

Regroups related questions across reviewers while retaining their exact wording and reviewer IDs. Each concern cluster receives a short neutral title and a priority:

- `P0 — Must address`
- `P1 — High value`
- `P2 — Address compactly`
- `P3 — Revision or resubmission`

Each cluster also records available evidence, missing evidence, feasible experiments or analyses, fallback wording, planned manuscript changes, and decisions required from the author.

### 3. `03_rebuttal.md`

Answers the prioritized concern clusters using:

```text
Direct Answer → Evidence → Revision
```

The draft is written for a neutral area chair or editor: concise, calm, specific, and grounded only in supplied or verified evidence.

## Validation

The validator supports plain text, Markdown, DOCX, and PDF review sources.

Check that Artifact 1 contains exact, contiguous source quotations:

```bash
python scripts/validate_artifacts.py quotes \
  --source path/to/reviews.docx \
  --artifact 01_verbatim_review_digest.md
```

Check exact quote transfer and complete concern coverage between Artifacts 1 and 2:

```bash
python scripts/validate_artifacts.py grouping \
  --digest 01_verbatim_review_digest.md \
  --grouped 02_grouped_prioritized_concerns.md
```

Check the default rebuttal word-count range:

```bash
python scripts/validate_artifacts.py count \
  --artifact 03_rebuttal.md \
  --min 900 \
  --max 1100
```

Run all checks together:

```bash
python scripts/validate_artifacts.py all \
  --source path/to/reviews.docx \
  --digest 01_verbatim_review_digest.md \
  --grouped 02_grouped_prioritized_concerns.md \
  --rebuttal 03_rebuttal.md \
  --min 900 \
  --max 1100
```

Run the validator regression tests with:

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
```

## Repository structure

```text
rebuttal-builder/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── templates/
│       ├── 01_verbatim_review_digest.md
│       ├── 02_grouped_prioritized_concerns.md
│       └── 03_rebuttal.md
├── references/
│   ├── drafting-guidance.md
│   └── cases/
│       ├── INDEX.md
│       ├── infuse/
│       └── simplix/
└── scripts/
    ├── validate_artifacts.py
    └── test_validate_artifacts.py
```

## Reference cases

The bundled case library is used only to learn workflow structure, grouping, response organization, tone, and compression. Its facts, reviewer wording, results, and manuscript locations must never be reused as evidence for another paper.

- **InFuse:** a complete raw reviews → grouped concerns → rebuttal case.
- **SimpliX:** a grouped concerns → rebuttal case; the original reviewer-by-reviewer source is not included, so it cannot validate first-stage quote fidelity.

See [`references/cases/INDEX.md`](references/cases/INDEX.md) for details and maintenance conventions.

## Adding a new reference case

Create a lowercase folder under `references/cases/` and prefer the following filenames:

```text
01-raw-reviews.<ext>
02-grouped-concerns.<ext>
03-rebuttal.<ext>
```

Then register the case in `references/cases/INDEX.md`, including:

- whether all three stages are present;
- the final rebuttal word count;
- evidence or quote-fidelity caveats;
- the workflow patterns worth learning from the case.

Preserve original source files unchanged.

## Privacy and publication warning

Reviewer reports, manuscripts, scores, and rebuttal materials may be confidential or subject to venue policies. Before publishing a case in a public repository:

1. confirm that the authors and applicable venue policies permit disclosure;
2. remove personal data and confidential identifiers where necessary;
3. consider replacing sensitive cases with synthetic or fully authorized examples;
4. use a private repository when permission is uncertain.

The bundled validation tools verify textual fidelity; they do not determine whether publication is legally or ethically permitted.

## Contributing

Contributions are welcome, especially:

- additional authorized or synthetic reference cases;
- support for more review-file formats;
- stronger quote and coverage audits;
- venue-specific length or formatting adapters;
- improvements to experiment-planning and evidence-validation guidance.

Please keep `SKILL.md` concise, put detailed guidance under `references/`, add regression tests for validator changes, and never include confidential review material without permission.

## Project status and license

RebuttalBuilder is an early-stage research workflow and should be used with author review at every checkpoint. It assists with organization and drafting; it does not guarantee acceptance or replace scientific judgment.

No open-source license is included yet. Add a `LICENSE` file before public release so users know how they may use, modify, and redistribute the project.

## Acknowledgment

RebuttalBuilder was developed from practical academic rebuttal workflows and emphasizes structured construction, author control, and evidence-grounded responses.
