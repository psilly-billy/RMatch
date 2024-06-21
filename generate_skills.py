import google.generativeai as genai

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat()

def LLM_Response(chat, question):
    response = chat.send_message(question, stream=True)
    response.resolve()  # Ensure the response is fully generated
    return response

def generate_skills_section(api_key, profile, job_listing, analysis):
    chat = configure_gemini(api_key)
    prompt = (
    "You are an HR expert with extensive experience in recruitment and human resources. "
    "Your task is to create a comprehensive Skills & Abilities section for a CV, tailored specifically for a certain job application. "
    "You will have access to information about the candidate's skills, work experience, and a small bio, as well as information about the job listing and a report comparing the keywords found in the CV and the job listing.\n"
    
    "Please follow these step-by-step instructions to ensure a thorough and accurate Skills & Abilities section:\n"
    
    "1. Carefully analyze the job description to identify the most relevant skills and abilities required for the role. These skills should include technical skills, tools, technologies, and any other pertinent terms that an Applicant Tracking System (ATS) or a recruiter would focus on.\n"
    
    "2. Compare the identified skills with the skills found in the candidate's CV to determine the gaps and overlaps.\n"
    
    "3. Review the candidate's information in detail, including their skills, work experience, and bio. Ensure you understand the candidate's background fully.\n"
    
    "4. Identify the most relevant skill categories based on the candidate's field and the job description. Common categories may include Technical Skills, Tools and Technologies, Industry-Specific Skills, Additional Skills, and Soft Skills, but should be tailored to the specific context.\n"
    
    "5. Using the candidate's information and the keyword analysis, craft a Skills & Abilities section that highlights the candidate's most relevant skills and qualifications that align with the job requirements. Use the following template with placeholders to structure the section appropriately based on the identified categories:\n"
    
    "Template:\n"
    "• {Category_1}: {category_1_skills}\n"
    "• {Category_2}: {category_2_skills}\n"
    "• {Category_3}: {category_3_skills}\n"
    "• Additional Skills: {additional_skills}\n"
    "• Soft Skills: {soft_skills}\n"
    
    "6. Ensure the Skills & Abilities section is concise, well-structured, and tailored to the specific job application.\n"
    
    "7. Do not invent any facts; the section should be based solely on the information provided by the candidate.\n"
    

    
    "Candidate Information:\n"
    f"{profile}\n"
    
    "Job Description:\n"
    f"{job_listing}\n"
    
    "Keyword Analysis Report:\n"
    f"{analysis}\n"

    "Provide the tailored Summary section below:\n"
    
    )
    response = LLM_Response(chat, prompt)
    return response.candidates[0].content.parts[0].text
