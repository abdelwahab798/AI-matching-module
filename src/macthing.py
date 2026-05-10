
from src.Normilize import normalize_skills

skill_refrence= {
    "Data Visualization": ["D3", "Recharts", "Chart.js"],
    "Performance":        ["Lighthouse", "Code Splitting", "Vite"],
    "Forms":              ["React Hook Form", "Zod", "Formik"],
    "Testing Library":    ["Vitest", "Jest", "Cypress", "Testing"],
    "Accessibility":      ["ARIA", "Keyboard UX"],
    "CSS":                ["CSS Modules", "Sass", "SCSS", "Tailwind"],
    }

def candidate_has_skill(candidate_skills: list[str],required_skill: str) -> tuple[bool, str | None]:
    normlized=normalize_skills(candidate_skills)
    normlized=[s.lower() for s in normlized]
    
    if required_skill.lower() in normlized:
        return True,"direct"
    
    skills=skill_refrence.get(required_skill,[])
    matched=[s for s in skills if s.lower() in normlized]
    if matched:
        return True,f"via: {matched}"
    
    return False, None
    

    

