def calculate_ats_score(resume_text, skills_found):

    score = 0

    if len(resume_text) > 1000:
        score += 20

    if len(skills_found) >= 5:
        score += 30

    if "experience" in resume_text.lower():
        score += 20

    if "education" in resume_text.lower():
        score += 15

    if "project" in resume_text.lower():
        score += 15

    return min(score, 100)
