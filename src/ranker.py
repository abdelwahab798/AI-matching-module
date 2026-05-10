# matching/ranker.py

from datetime import datetime, timezone
from src.score import score_candidate


def rank_candidates(
    job: dict,
    candidates: list[dict],
    top_k: int = 10,
) -> dict:
    """
    بتاخد job + كل الـ candidates وترجع top-k مرتبين
    """
    results = []

    for candidate in candidates:
        # تجاهل الـ candidates الـ malformed
        if not candidate.get("id") or not candidate.get("skills") is not None:
            print(f"[WARN] Skipping malformed candidate: {candidate.get('id', 'unknown')}")
            continue

        try:
            scored = score_candidate(candidate, job)
            results.append(scored)
        except Exception as e:
            print(f"[WARN] Failed to score candidate {candidate.get('id')}: {e}")
            continue

    # ترتيب تنازلي بالـ score
    results.sort(key=lambda x: x["score"], reverse=True)

    # top-k
    top_results = results[:top_k]

    return {
        "jobId":   job["id"],
        "topK":    top_k,
        "results": top_results,
        "meta": {
            "approach":    "baseline-v1",
            "totalScored": len(results),
            "generatedAt": datetime.now(timezone.utc).isoformat(),
        },
    }


def rank_all_jobs(
    jobs: list[dict],
    candidates: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """
    بتشغل rank_candidates على كل الـ jobs
    """
    return [rank_candidates(job, candidates, top_k) for job in jobs]