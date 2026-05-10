# tests/test_normalization.py

from src.Normilize import normalize_skill, normalize_skills


def test_normalize_alias():
    assert normalize_skill("ReactJS") == "React"
    assert normalize_skill("ts") == "TypeScript"
    assert normalize_skill("js") == "JavaScript"
    assert normalize_skill("nodejs") == "Node.js"
    assert normalize_skill("node") == "Node.js"
    assert normalize_skill("scss") == "Sass"

def test_normalize_case_insensitive():
    assert normalize_skill("REACTJS") == "React"
    assert normalize_skill("TS") == "TypeScript"

def test_normalize_whitespace():
    assert normalize_skill("  React  ") == "React"
    assert normalize_skill("  ts  ") == "TypeScript"

def test_normalize_unknown_skill():
    assert normalize_skill("SomeUnknownSkill") == "SomeUnknownSkill"

def test_normalize_skills_deduplication():
    result = normalize_skills(["React", "ReactJS", "react"])
    assert result.count("React") == 1

def test_normalize_skills_list():
    result = normalize_skills(["ts", "ReactJS", "node"])
    assert "TypeScript" in result
    assert "React" in result
    assert "Node.js" in result