
def generate_insights(candidate: dict, job: dict, score_result: dict) -> dict:
    
    requirements = job.get("requirements", {})
    must_haves = requirements.get("mustHaveSkills", [])
    nice_to_haves = requirements.get("niceToHaveSkills", [])
    min_years = requirements.get("minYears", 0)

    candidate_years = candidate.get("yearsOfExperience", 0)
    matched_skills = score_result.get("matchedSkills", [])
    missing_must = score_result.get("missingMustHaveSkills", [])
    missing_nice = score_result.get("missingNiceToHaveSkills", [])

    strengths = []
    skill_gaps = []
    next_steps = []

    # ── Strengths ──────────────────────────────────────────
    if not missing_must:
        strengths.append("Covers all must-have skills for this role.")

    if candidate_years >= min_years + 2:
        strengths.append(f"Strong experience: {candidate_years} years (role requires {min_years}).")
    elif candidate_years >= min_years:
        strengths.append(f"Meets experience requirement: {candidate_years} years.")

    nice_matched_count = len(nice_to_haves) - len(missing_nice)
    if nice_matched_count >= 3:
        strengths.append(f"Matches {nice_matched_count} nice-to-have skills — well-rounded profile.")
    elif nice_matched_count >= 1:
        strengths.append(f"Matches {nice_matched_count} nice-to-have skill(s).")

    if score_result.get("score", 0) >= 0.85:
        strengths.append("Overall strong match for this role.")

    # ── Skill Gaps ─────────────────────────────────────────
    if missing_must:
        skill_gaps.append({
            "type": "must_have",
            "skills": missing_must,
            "impact": "High — these are required for the role."
        })

    if missing_nice:
        skill_gaps.append({
            "type": "nice_to_have",
            "skills": missing_nice,
            "impact": "Medium — would strengthen the application."
        })

    if candidate_years < min_years:
        skill_gaps.append({
            "type": "experience",
            "skills": [],
            "impact": f"Low experience: {candidate_years} years vs {min_years} required."
        })

    # ── Next Steps ─────────────────────────────────────────
    for skill in missing_must:
        next_steps.append(f"Learn {skill} — it is a must-have for this role.")

    if missing_nice:
        top_nice = missing_nice[:2]
        for skill in top_nice:
            next_steps.append(f"Consider adding {skill} to strengthen your profile.")

    if candidate_years < min_years:
        gap = min_years - candidate_years
        next_steps.append(f"Gain {gap} more year(s) of experience to meet the minimum requirement.")

    if not next_steps:
        next_steps.append("Strong profile — focus on showcasing your experience in interviews.")

    return {
        "strengths": strengths,
        "skillGaps": skill_gaps,
        "nextSteps": next_steps,
    }