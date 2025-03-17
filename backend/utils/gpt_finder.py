from openai import OpenAI
import os
from typing import List, Dict, Any, Optional

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

def extract_prompt_info(description: str) -> Dict[str, Any]:
    print("Generating information based on user prompt")
    prompt = f"""Extract relevant resume details from the given user description. 
The user may provide explicit or implicit information about their skills, work experience, education, certifications, projects, or GPA.

Extract and classify the following fields:
- Skills: Includes programming languages, frameworks, libraries, tools, technologies, methodologies, and relevant technical or domain-specific expertise.
- Work Experience: Job roles, companies, internships, or professional experiences.
- Education: Degrees, institutions, and areas of study.
- Certifications: Any relevant certifications or professional qualifications.
- Projects: Names or descriptions of personal, academic, or professional projects.
- GPA: If mentioned, extract it; otherwise, return "0".

If a field is not mentioned, return it as an empty list.
    
    User Prompt:
    {description}
    
    Return the extracted information in JSON format without explanations or extra text.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing user descriptions to extract resume-related information."},
            {"role": "user", "content": prompt}
        ]
    )
    
    extracted_data = response.choices[0].message.content.strip()
    print(extracted_data)
    
    try:
        resume_info = eval(extracted_data) if extracted_data.startswith("{") else {}
    except Exception:
        resume_info = {}
    
    return {
        "skills": resume_info.get("Skills", []),
        "work_experience": resume_info.get("Work_experience", []),
        "education": resume_info.get("Education", []),
        "certifications": resume_info.get("Certifications", []),
        "projects": resume_info.get("Projects", []),
        "gpa": resume_info.get("Gpa", "0")
    }