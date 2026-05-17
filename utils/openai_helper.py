from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")


def get_ai_suggestions(resume_text, job_description):

    prompt = f"""
    Analyze this resume and compare it with the job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:
    1. ATS improvement suggestions
    2. Missing skills
    3. Better resume summary
    4. Stronger project descriptions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
