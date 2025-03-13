from openai import OpenAI
import os
from typing import List, Dict, Any, Optional

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

def extract_prompt_info(description: str) -> Dict[str, Any]:
    print("Generating information based on user prompt")
    prompt = f"""Analyze the following user prompt and extract relevant resume details if present.
    Extract the following fields:
    - Skills
    - Work experience
    - Education
    - Certifications
    - Projects
    - Gpa
    
    If a field is not mentioned, return it as an empty list. If no gpa, return sting of 0.
    
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