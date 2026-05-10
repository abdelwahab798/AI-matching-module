# app/explain.py

import argparse
import json
import sys
from pathlib import Path
from src.insights import generate_insights

from src.score import score_candidate


def load_json(path: Path) -> any:
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_explanation(candidate: dict, job: dict, result: dict,insights: dict) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append(f"Candidate : {candidate['fullName']} ({candidate['id']})")
    lines.append(f"Job       : {job['title']} ({job['id']})")
    lines.append(f"Score     : {result['score']}")
    lines.append("=" * 60)

    lines.append("\n Matched Skills:")
    if result["matchedSkills"]:
        for s in result["matchedSkills"]:
            lines.append(f"   {s}")
    else:
        lines.append("  None")

    lines.append("\n Missing Must-Have Skills:")
    if result["missingMustHaveSkills"]:
        for s in result["missingMustHaveSkills"]:
            lines.append(f"   {s}")
    else:
        lines.append("  None — all must-haves covered!")

    lines.append("\n  Missing Nice-to-Have Skills:")
    if result["missingNiceToHaveSkills"]:
        for s in result["missingNiceToHaveSkills"]:
            lines.append(f"    {s}")
    else:
        lines.append("  None")

    lines.append("\n Score Breakdown:")
    for reason in result["reasons"]:
        lines.append(f"  [{reason['type']}] weight={reason['weight']} | {reason['Data']}")

    lines.append("=" * 60)
    
    lines.append("\n Insights:")
    for s in insights["strengths"]:
        lines.append(f"   {s}")

    lines.append("\n Next Steps:")
    for s in insights["nextSteps"]:
     lines.append(f"  → {s}")
    return "\n".join(lines)



def main():
    parser = argparse.ArgumentParser(description="Explain candidate match for a job")
    parser.add_argument("--job-id",       required=True, help="Job ID e.g. j-001")
    parser.add_argument("--candidate-id", required=True, help="Candidate ID e.g. c-002")
    args = parser.parse_args()

    base       = Path(__file__).parent.parent
    candidates = load_json(base / "Data_json" / "candidates.json")
    jobs       = load_json(base / "Data_json" / "jobs.json")

    job = next((j for j in jobs if j["id"] == args.job_id), None)
    if not job:
        print(f"[ERROR] Job '{args.job_id}' not found")
        sys.exit(1)

    candidate = next((c for c in candidates if c["id"] == args.candidate_id), None)
    if not candidate:
        print(f"[ERROR] Candidate '{args.candidate_id}' not found")
        sys.exit(1)

    result = score_candidate(candidate, job)
    insights = generate_insights(candidate, job, result)
    print(format_explanation(candidate, job, result, insights))

if __name__ == "__main__":
    main()