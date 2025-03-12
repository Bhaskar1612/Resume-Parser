from mistralai import Mistral
import json
import os

def extract_and_structure_resume(pdf_path: str):
    """Extracts text from a PDF resume using Mistral OCR and processes it to return structured JSON."""
    
    try:
        # Initialize Mistral client
        api_key = os.getenv('MISTRAL_API_KEY')
        if not api_key:
            raise ValueError("Missing MISTRAL API key. Set 'MISTRAL_API_KEY' in the environment.")
        
        client = Mistral(api_key=api_key)
        print("[INFO] Mistral client initialized successfully.")

        # Step 1: Upload PDF to Mistral
        print(f"[INFO] Uploading PDF: {pdf_path}")
        try:
            with open(pdf_path, "rb") as pdf_file:
                uploaded_pdf = client.files.upload(
                    file={"file_name": os.path.basename(pdf_path), "content": pdf_file},
                    purpose="ocr"
                )
        except Exception as e:
            raise RuntimeError(f"Error uploading PDF to Mistral: {str(e)}")

        print(f"[INFO] PDF uploaded successfully. File ID: {uploaded_pdf.id}")

        # Step 2: Get Signed URL
        try:
            signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
        except Exception as e:
            raise RuntimeError(f"Error fetching signed URL from Mistral: {str(e)}")

        print("[INFO] Successfully retrieved signed URL for OCR.")

        # Step 3: Perform OCR on PDF
        print("[INFO] Performing OCR on the uploaded PDF...")
        try:
            ocr_response = client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": signed_url.url}
            )
        except Exception as e:
            raise RuntimeError(f"Error performing OCR: {str(e)}")

        if not ocr_response.pages:
            raise ValueError("OCR extraction failed or returned no data.")

        extracted_text = "\n".join([page.markdown for page in ocr_response.pages])
        print("[INFO] OCR extraction completed successfully.")

        # Step 4: Prepare Prompt for Mistral Chat
        prompt = f"""
        Extract the following details from this resume and return JSON format:
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

        print("[INFO] Sending extracted text to Mistral for structured data processing...")

        # Step 5: Query Mistral Chat Model
        try:
            chat_response = client.chat.complete(
                model='mistral-large-latest',
                messages=[{"role": "user", "content": prompt}]
            )
        except Exception as e:
            raise RuntimeError(f"Error calling Mistral API for resume structuring: {str(e)}")

        response_text = chat_response.choices[0].message.content
        print("[INFO] Received response from Mistral.")

        # Step 6: Parse JSON Response
        try:
            structured_data = json.loads(response_text.strip("```json\n").rstrip("\n```"))
            print("[INFO] Successfully parsed structured resume data.")
        except json.JSONDecodeError:
            raise ValueError("Failed to parse Mistral response. Ensure the output is in JSON format.")

        return structured_data

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": str(e)}
