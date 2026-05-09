
from Normilize import normalize_skills

SKILL_EVIDENCE= {
    "Data Visualization": ["D3", "Recharts", "Chart.js"],
    "Performance":        ["Lighthouse", "Code Splitting", "Vite"],
    "Forms":              ["React Hook Form", "Zod", "Formik"],
    "Testing Library":    ["Vitest", "Jest", "Cypress", "Testing"],
    "Accessibility":      ["ARIA", "Keyboard UX"],
    "CSS":                ["CSS Modules", "Sass", "SCSS", "Tailwind"],
    }


def candidate_has_skill(candidate_skills: list[str],required_skill: str) -> tuple[bool, str | None]:

    normalized=normalize_skills(candidate_skills)
    normalized_lower=[s.lower() for s in normalized]

    if required_skill.lower() in normalized_lower:
        return True,"direct"

    evidence_skills=SKILL_EVIDENCE.get(required_skill, [])
    matched=[s for s in evidence_skills if s.lower() in normalized_lower]
    if matched:
        return True,f"via {', '.join(matched)}"

    return False, None