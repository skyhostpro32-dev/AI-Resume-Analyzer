import json


def extract_skills(resume_text):

    with open("skills.json", "r") as f:
        skills_data = json.load(f)

    skills_found = []

    for skill in skills_data["skills"]:
        if skill.lower() in resume_text.lower():
            skills_found.append(skill)

    return skills_found
