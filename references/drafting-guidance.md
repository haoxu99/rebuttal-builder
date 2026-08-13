# Rebuttal Drafting Guidance

## Contents

1. Viability and scope
2. Concern diagnosis
3. Experiment planning
4. Response patterns
5. Tone and integrity
6. Compression and resubmission

## 1. Viability and scope

Assess whether rebuttal work has a plausible decision payoff. Consider scores only after identifying the venue scale and approximate boundary.

- `PROMISING`: concerns are answerable misunderstandings or missing evidence; no fatal flaw; one or two resolutions may change the decision.
- `BORDERLINE / UNCERTAIN`: a decisive clarification or experiment may help, but interpretation or feasibility is uncertain.
- `LOW EXPECTED RETURN`: multiple reviewers question correctness, novelty, or empirical validity; all scores are below the boundary; or the required work needs redesign or substantial new data.

Do not declare rejection certain. In a low-return case, correct material factual errors professionally, then provide a revision/resubmission backlog rather than encouraging rushed experiments.

## 2. Concern diagnosis

Keep the exact reviewer quote separate from analysis. For each cluster, diagnose the decision question, alternative interpretations, confidence, and evidence that would answer all plausible readings.

Common classes include correctness, novelty, empirical support, fair comparison, missing baseline, generalization, robustness, statistical reliability, efficiency, scalability, reproducibility, significance, overclaiming, related work, clarity, and presentation.

Distinguish severity from decision impact:

- `FATAL`: the main claim fails if the concern is valid and unresolved.
- `MAJOR`: the paper can survive, but the concern could drive rejection.
- `MODERATE`: affects confidence or scope.
- `MINOR`: local clarity, formatting, or citation issue.

Shared concerns generally outrank equally severe single-reviewer concerns. Mark reviewer-intent inference as high, medium, or low confidence.

## 3. Experiment planning

Use qualitative judgment guided by:

`decision impact × sharedness × severity × information gain × feasibility ÷ cost`

For each proposed experiment or analysis specify:

- quoted concern IDs;
- hypothesis or decision question;
- baseline and control conditions;
- data or evaluation subset;
- metric;
- compute/data/tuning matching;
- runs, seeds, and uncertainty when relevant;
- minimum interpretable result;
- implication of positive, negative, mixed, and null results;
- fallback response if unfinished.

Prefer information-dense experiments: matched-compute comparisons can address fairness and efficiency; multi-seed tests can address variance and cherry-picking; cross-domain evaluations can address realism and generalization; component ablations can address mechanism and novelty.

Do not run work that duplicates evidence, lacks controls, cannot finish reliably, or does not answer the underlying question.

## 4. Response patterns

### Correct a misunderstanding

> **The method does not require `[assumption]`; it requires only `[actual assumption]`.** Our presentation may have obscured this distinction. We will revise `[location]` and add `[clarification]`.

### Acknowledge a valid limitation

> **We agree that the current evidence does not establish `[broad claim]`.** It supports `[narrow claim]` under `[conditions]`. We will narrow the abstract/conclusion and state this limitation explicitly.

### Report a completed experiment

> **The requested comparison confirms `[specific answer]`.** Under matched `[conditions]`, our method obtains `[result]` versus `[baseline]` over `[N]` runs (`[uncertainty]`). We will add the protocol and result to `[location]`.

### Experiment cannot be completed reliably

> We agree that this experiment would be informative. Completing it reliably requires `[reason]`, and we do not want to report an under-validated result. Current evidence supports `[narrow claim]`; we will clarify the scope and add the experiment to the revision plan.

### Novelty

Build a private delta table first: prior work, capability/assumption, this paper's difference, and why it matters. State specific formulation, capability, guarantee, or finding; do not argue novelty only from combining known components.

### Missing baseline or unfair comparison

Align split, data, budget, backbone, selection protocol, and tuning. State what is and is not matched.

### Statistical reliability

Report metric, independent runs, mean and uncertainty, and a valid test only when actually performed. Never call a result statistically significant without one.

### Negative or mixed result

Use it to support a narrower credible claim. State conditions where the gain holds and where it does not, then revise the claim and limitation accordingly.

## 5. Tone and integrity

Prefer: “We agree,” “We clarify,” “Our presentation may have obscured,” “The intended claim is,” “The result shows,” “We will narrow,” and “We will revise.”

Avoid blaming reviewers, calling criticism unfair or obvious, speculating about motives, pressuring score changes, or repeating ceremonial thanks. Write for a neutral chair.

Allowed evidence includes supplied manuscript text, verified locations, completed experiments and analyses, corrected derivations, reproducible summaries, and policy-permitted citations. Never invent values, quotations, locations, reviewer agreement, or future success; never hide negative results.

## 6. Compression and resubmission

When over the limit, remove in this order:

1. repeated thanks;
2. repeated quotations;
3. generic background;
4. adjectives and rhetoric;
5. duplicate responses;
6. low-impact minor comments;
7. nonessential implementation detail.

Preserve direct answers, key numbers, controls, uncertainty, assumptions, claim narrowing, revisions, and unresolved limitations.

For resubmission, diagnose the dominant rejection mechanism and create a ranked backlog:

- `R0`: blocks resubmission;
- `R1`: strongly recommended;
- `R2`: improves completeness;
- `R3`: optional polish.

Separate work feasible during rebuttal from longer-horizon method, evaluation, framing, organization, related-work, and reproducibility changes.
