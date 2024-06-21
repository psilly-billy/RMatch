import google.generativeai as genai

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat()

def LLM_Response(chat, question):
    response = chat.send_message(question, stream=True)
    response.resolve()  # Ensure the response is fully generated
    return response

def generate_experience_section(api_key, profile, job_listing, analysis):
    chat = configure_gemini(api_key)
    prompt = (
     "You are an HR expert with extensive experience in recruitment and human resources. "
    "Your task is to create a comprehensive Work Experience section for a CV, tailored specifically for a certain job application. "
    "You will have access to information about the candidate's work experience, skills, and a small bio, as well as information about the job listing and a report comparing the keywords found in the CV and the job listing.\n"
    
    "Please follow these step-by-step instructions to ensure a concise and accurate Work Experience section:\n"
    
    "1. Analyze the job description to identify the most relevant responsibilities, qualifications, and skills required for the role. Focus on job titles, duties, and skills that an Applicant Tracking System (ATS) or a recruiter would prioritize.\n"
    
    "2. Compare the identified responsibilities and qualifications with the candidate's work experience to determine gaps and overlaps.\n"
    
    "3. Review the candidate's work experience, skills, and bio in detail to fully understand their background.\n"
    
    "4. Modify the descriptions of the candidate's work experience to highlight the most relevant skills, responsibilities, and achievements that align with the job requirements. Ensure each description is concise, impactful, and limited to 2-3 bullet points per role. Suggest additional responsibilities or achievements that could enhance the candidate's alignment with the job description, if applicable.\n"
    
    "5. Ensure the Work Experience section is in reverse chronological order (most recent experience first). Use the following template with placeholders to structure the section appropriately based on the candidate's field and the job description:\n"
    "6. Format the first line of each job experience entry in bold. The first line should include the job title, company name, location, and dates of employment. Follow this template for each job experience entry:\n"

    "Template:\n"
    "{Job_Title},  {Company},  {Location},        {Start_Date} - {End_Date}\n"
    "• {Responsibility_1}\n"
    "• {Responsibility_2}\n"
    "• {Responsibility_3}\n"
    "\n"
    
   
    
    "7. Ensure the Work Experience section is concise, well-structured, and tailored to the specific job application. Aim for brevity without sacrificing important details. Limit each job description to a maximum of 3 bullet points.\n"
    
    "9. Do not invent any facts; the section should be based solely on the information provided by the candidate. Adapt the language and focus to better match the job description. Suggest additional relevant responsibilities or achievements if they can enhance the candidate's fit for the job.\n"
    "9. Do not start with the phrase  '## Work Experience' \n"

    "Candidate Information:\n"
    f"{profile}\n"
    
    "Job Description:\n"
    f"{job_listing}\n"
    
    "Keyword Analysis Report:\n"
    f"{analysis}\n"

    "Provide the tailored Work Experience section below in reverse chronological order. Keep each job description concise and focused on key responsibilities and achievements, with a maximum of 3 bullet points per role and each bullet point no more than 50 words:\n"
    
    )
    response = LLM_Response(chat, prompt)
    return response.candidates[0].content.parts[0].text
