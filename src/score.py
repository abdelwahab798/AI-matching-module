
from src.macthing import candidate_has_skill

WEIGHTS={
    "must_have":    0.50,
    "nice_to_have": 0.20,
    "experience":   0.20,
    "location":     0.10,}


def score_candidate(candidate: dict, job: dict):
    requirements=job.get("requirements",{})
    must_have=requirements.get("mustHaveSkills",[])
    nice_to_have=requirements.get("niceToHaveSkills",[])
    min_years=requirements.get("minYears",0)
    location=requirements.get("location",None)

    candidate_skills=candidate.get("skills",[])
    candidate_location=candidate.get("location",None)
    candidate_years= candidate.get("yearsOfExperience", 0)

    reasons=[]
    matched_skills=[]
    missing_must=[]
    missing_nice=[]
    must_matched=[]
    nice_matched=[]

######################## Must to have ############################
    for skill in must_have:
        found,refrence=candidate_has_skill(candidate_skills,skill)
        if found:
            matched_skills.append(skill)
            must_matched.append(skill)
        else:
            missing_must.append(skill)
        
    if must_have:
        must_score=(len(must_matched)/len(must_have))* WEIGHTS["must_have"]
    else:
        must_score=0

    if must_matched:
        reasons.append({
            "type": "must_have_match",
            "Data": ", ".join(must_matched),
            "weight": round(must_score,3)
            
            })
        
    if missing_must:
        reasons.append({
            "type": "Must_have_missing",
            "Data": ", ".join(missing_must),
            "weight":0
            
        })

######################## Nice to have ############################ 

    for skill in nice_to_have:
        found,refrence=candidate_has_skill(candidate_skills,skill)
        if found:
            nice_matched.append(skill)
            matched_skills.append(skill)
        else:
            missing_nice.append(skill)

    if nice_to_have:
        nice_score=(len(nice_matched)/len(nice_to_have)) * WEIGHTS["nice_to_have"]
    else:
        nice_score=0
    
    if nice_matched:
        reasons.append({
            "type": "nice_to_have_match",
            "Data":", ".join(nice_matched),
            "weight": round(nice_score,3),

        })
    
    
######################## Experience ############################ 

    if candidate_years>=min_years:
        exp_score=WEIGHTS["experience"]
        reasons.append({
            "type": "Experince_fit",
            "Data":f"{candidate_years} years => {min_years} years",
            "weight":round(exp_score,3)

        })
    else:
        if min_years==0:
            exp_score=WEIGHTS["experience"]
        else:
            ratio=candidate_years/min_years
            exp_score=ratio*WEIGHTS["experience"]
            reasons.append({
            "type": "Experince_miss",
            "Data":f"{candidate_years} years < {min_years} years",
            "weight":round(exp_score,3)
            
        })
######################## Location ############################ 

    if location:
        if candidate_location.lower() in location.lower():
            loc_score=WEIGHTS["location"]
            reasons.append({
            "type": "Location_fit",
            "Data":f"{candidate_location} fit with {location}",
            "weight":round(loc_score,3)
            })
        else:
            loc_score=0
            reasons.append({
            "type": "Location_miss",
            "Data":f"{candidate_location} miss with {location}",
            "weight":0
            })
    else:
        loc_score=WEIGHTS["location"]
    
######################## Location ############################ 
    total=round(must_score+exp_score+loc_score+nice_score,4)

    return{
        "ID": candidate["id"],
        "score": total,
        "matchedSkills": list(dict.fromkeys(matched_skills)),
        "missingMustHaveSkills":  missing_must,
        "missingNiceToHaveSkills":missing_nice,
        "yearsOfExperience": candidate_years,
        "reasons":                reasons,
    }

    
    

    
    
    



    





    


    




    

    
        









