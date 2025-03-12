import fitz  # PyMuPDF for PDF text extraction
import json
import os
from openai import OpenAI

def extract_resume_data_and_structure(pdf_path):
    """Extracts text from a PDF resume and processes it with GPT-4 Turbo to return structured JSON."""
    
    try:
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set 'OPENAI_API_KEY' in the environment.")

        client = OpenAI(api_key=api_key)
        print("[INFO] OpenAI client initialized successfully.")

        # Extract text from the PDF
        print(f"[INFO] Extracting text from PDF: {pdf_path}")
        try:
            doc = fitz.open(pdf_path)
            extracted_text = "\n".join(page.get_text("text") for page in doc)
        except Exception as e:
            raise RuntimeError(f"Error reading PDF file: {str(e)}")
        
        if not extracted_text.strip():
            raise ValueError("Extracted text is empty. Ensure the PDF contains selectable text.")

        print("[INFO] Successfully extracted text from PDF.")

        # Define the prompt
        prompt = f"""
        Extract the following details from this resume and return JSON:
        - Name
        - Email
        - Phone Number
        - Skills
        - Work Experience (Company, Role, Duration)
        - Education (Degree, Institution, Year)
        - Certifications
        - Projects
        - Gpa

        Resume Text:
        {extracted_text}
        """

        print("[INFO] Sending extracted text to GPT-4 Turbo for processing...")

        # Call GPT-4 Turbo
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You extract structured information from resumes and return JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
        except Exception as e:
            raise RuntimeError(f"Error calling OpenAI API: {str(e)}")

        print("[INFO] Received response from GPT-4 Turbo.")

        # Parse JSON response
        try:
            structured_data = json.loads(response.choices[0].message.content.strip("```json\n").rstrip("\n```"))
            print("[INFO] Successfully parsed structured data.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse GPT response. Error: {str(e)}")

        return structured_data

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": str(e)}

