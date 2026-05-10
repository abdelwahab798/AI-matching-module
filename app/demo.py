# app/demo.py

import argparse
import json
import sys
from pathlib import Path

from src.ranker import rank_all_jobs


def load_json(path: Path) -> any:
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_summary(results: list[dict]) -> None:
    for job_result in results:
        print(f"\n{'=' * 60}")
        print(f"Job: {job_result['jobId']} | Top {job_result['topK']} Candidates")
        print(f"{'=' * 60}")
        for i, r in enumerate(job_result["results"], 1):
            missing = len(r["missingMustHaveSkills"])
            print(
                f"  {i:2}. [{r['score']:.3f}] {r['ID']}"
                f" | matched={len(r['matchedSkills'])}"
                f" | missing_must={missing}"
            )


def main():
    parser = argparse.ArgumentParser(description="Run demo for all jobs")
    parser.add_argument("--out-dir", default="outputs", help="Output directory")
    parser.add_argument("--top-k",   type=int, default=10, help="Top K per job")
    args = parser.parse_args()

    base       = Path(__file__).parent.parent
    candidates = load_json(base / "Data_json" / "candidates.json")
    jobs       = load_json(base / "Data_json" / "jobs.json")

    print(f"[INFO] Scoring {len(candidates)} candidates across {len(jobs)} jobs...")

    all_results = rank_all_jobs(jobs, candidates, top_k=args.top_k)

    # save each job result to file
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for result in all_results:
        out_path = out_dir / f"{result['jobId']}.json"
        out_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"[OK] Saved {out_path}")

    # print summary in terminal
    print_summary(all_results)
    print(f"\n[DONE] Results saved to '{args.out_dir}/'")


if __name__ == "__main__":
    main()