Skills={
    "js":"JavaScript",
    "ts":"TypeScript",
    "reactjs": "React",
    "react.js": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "scss": "Sass",
    "testing-library": "Testing Library",
    "react-query": "React Query",}

def normalize_skill(skill:str)->str:
    cleaned=skill.lower().strip()
    for f,t in Skills.items():
        if cleaned==f:
            return t
    return skill.strip()

def normalize_skills(skills:list[str])->list[str]:
    final_Skills=set()
    results=[]
    for skill in skills:
        k=normalize_skill(skill)
        if k not in final_Skills:
            final_Skills.add(k)
            results.append(k)
    return results


