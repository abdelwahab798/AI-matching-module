# AI Matching Module

A deterministic candidate-ranking system that scores and explains candidate fits for job requirements.

## How to Run

### Install dependencies
pip install -r requirements.txt

### Rank candidates for a job
python -m app.rank --job-id j-001 --top-k 10

### Save results to file
python -m app.rank --job-id j-001 --top-k 10 --out outputs/j-001.json

### Explain a single candidate
python -m app.explain --job-id j-001 --candidate-id c-001

### Run demo for all jobs
python -m app.demo --out-dir outputs --top-k 10

## Approach
Baseline deterministic scoring (Option A) — no external APIs or embeddings required.

## Scoring Formula

| Component        | Weight |
|------------------|--------|
| Must-have skills | 50%    |
| Nice-to-have     | 20%    |
| Experience fit   | 20%    |
| Location match   | 10%    |

- Missing must-haves reduce score proportionally from the 50%.
- Experience below minYears applies a proportional penalty.
- Location mismatch loses the 10% but adds no extra penalty.

## Normalization Logic

Two layers:
1. **Alias mapping** — e.g. `"reactjs" → "React"`, `"ts" → "TypeScript"`, `"scss" → "Sass"`
2. **Evidence mapping** — e.g. `"D3"` and `"Recharts"` count as evidence for `"Data Visualization"`

All comparisons are case-insensitive with whitespace trimming and deduplication.

## Example Output

```json
{
  "candidateId": "c-001",
  "score": 0.755,
  "matchedSkills": ["React", "TypeScript", "CSS", "Accessibility", "Storybook"],
  "missingMustHaveSkills": ["React Router"],
  "missingNiceToHaveSkills": ["Vitest", "React Query", "Design Tokens"],
  "reasons": [
    { "type": "must_have_match", "Data": "React, TypeScript, CSS", "weight": 0.375 },
    { "type": "nice_to_have_match", "Data": "Accessibility, Storybook", "weight": 0.08 },
    { "type": "experience_fit", "Data": "4 years >= 3 required", "weight": 0.2 },
    { "type": "location_fit", "Data": "Cairo, Egypt", "weight": 0.1 }
  ]
}
```

## Trade-offs & Next Improvements

- **Tie-breaking** — candidates with equal scores are not differentiated beyond years of experience.
- **Semantic matching** — adding embeddings would catch skill synonyms not in the alias map.
- **Insights** — next steps are rule-based; an LLM could generate richer explanations.

## Time Spent
~ 5 hours