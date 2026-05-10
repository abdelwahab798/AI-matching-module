# tests/test_scorer.py

from src.score import score_candidate

# بيانات تجريبية
MOCK_JOB = {
    "id": "j-test",
    "title": "Test Job",
    "requirements": {
        "mustHaveSkills": ["React", "TypeScript", "CSS"],
        "niceToHaveSkills": ["Storybook", "Vitest"],
        "minYears": 3,
        "location": "Cairo, Egypt"
    }
}

PERFECT_CANDIDATE = {
    "id": "c-test-1",
    "yearsOfExperience": 5,
    "location": "Cairo, Egypt",
    "skills": ["React", "TypeScript", "CSS", "Storybook", "Vitest"]
}

MISSING_MUST_CANDIDATE = {
    "id": "c-test-2",
    "yearsOfExperience": 4,
    "location": "Cairo, Egypt",
    "skills": ["React"]  # ناقص TypeScript و CSS
}

JUNIOR_CANDIDATE = {
    "id": "c-test-3",
    "yearsOfExperience": 1,
    "location": "Cairo, Egypt",
    "skills": ["React", "TypeScript", "CSS"]
}

WRONG_LOCATION_CANDIDATE = {
    "id": "c-test-4",
    "yearsOfExperience": 5,
    "location": "Alexandria, Egypt",
    "skills": ["React", "TypeScript", "CSS"]
}


def test_perfect_candidate_high_score():
    result = score_candidate(PERFECT_CANDIDATE, MOCK_JOB)
    assert result["score"] >= 0.9

def test_missing_must_have_reduces_score():
    perfect = score_candidate(PERFECT_CANDIDATE, MOCK_JOB)
    missing = score_candidate(MISSING_MUST_CANDIDATE, MOCK_JOB)
    assert perfect["score"] > missing["score"]

def test_missing_must_have_in_result():
    result = score_candidate(MISSING_MUST_CANDIDATE, MOCK_JOB)
    assert "TypeScript" in result["missingMustHaveSkills"]
    assert "CSS" in result["missingMustHaveSkills"]

def test_junior_penalty():
    perfect = score_candidate(PERFECT_CANDIDATE, MOCK_JOB)
    junior = score_candidate(JUNIOR_CANDIDATE, MOCK_JOB)
    assert perfect["score"] > junior["score"]

def test_location_mismatch_reduces_score():
    cairo = score_candidate(PERFECT_CANDIDATE, MOCK_JOB)
    alex = score_candidate(WRONG_LOCATION_CANDIDATE, MOCK_JOB)
    assert cairo["score"] > alex["score"]

def test_matched_skills_not_empty():
    result = score_candidate(PERFECT_CANDIDATE, MOCK_JOB)
    assert len(result["matchedSkills"]) > 0

def test_score_between_0_and_1():
    result = score_candidate(PERFECT_CANDIDATE, MOCK_JOB)
    assert 0.0 <= result["score"] <= 1.0