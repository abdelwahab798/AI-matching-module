# app/rank.py

import argparse
import json
import sys
from pathlib import Path

from src.ranker import rank_candidates


def load_json(path: Path) -> any:
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Rank candidates for a job")
    parser.add_argument("--job-id",  required=True,  help="Job ID e.g. j-001")
    parser.add_argument("--top-k",type=int, default=10, help="Number of top candidates")
    parser.add_argument("--out",required=False, help="Output file e.g. outputs/j-001.json")
    args = parser.parse_args()

    
    base = Path(__file__).parent.parent
    candidates = load_json(base / "Data_json" / "candidates.json")
    jobs       = load_json(base / "Data_json" / "jobs.json")

    
    job = next((j for j in jobs if j["id"] == args.job_id), None)
    if not job:
        print(f"[ERROR] Job '{args.job_id}' not found")
        sys.exit(1)

    # rank
    result = rank_candidates(job, candidates, top_k=args.top_k)

    # output
    output_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_str, encoding="utf-8")
        print(f"[OK] Saved to {args.out}")
    else:
        print(output_str)

if __name__ == "__main__":
    main()