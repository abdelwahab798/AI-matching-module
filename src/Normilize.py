Skills = {
    "js":"JavaScript",
    "ts":"TypeScript",
    "reactjs": "React",
    "react.js": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "scss": "Sass",
    "testing-library": "Testing Library",
    "react-query": "React Query",
}

def normalize_skill(skill: str) -> str:
    cleaned = skill.strip().lower()
    for alias, canonical in Skills.items():
        if cleaned == alias.lower():
            return canonical
    return skill.strip()

def normalize_skills(skills: list[str]) -> list[str]:
    seen=set()
    result=[]
    for skill in skills:
        normalized=normalize_skill(skill)
        key=normalized.lower()
        if key not in seen:
            seen.add(key)
            result.append(normalized)
    return result

