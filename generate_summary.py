import google.generativeai as genai

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat()

def LLM_Response(chat, question):
    response = chat.send_message(question, stream=True)
    response.resolve()  # Ensure the response is fully generated
    return response

def generate_summary_section(api_key, profile, job_listing, analysis):
    chat = configure_gemini(api_key)
    prompt = (
      "You are an HR expert with extensive experience in recruitment and human resources, and a very talented writer. "
      "Your way with words makes everyone very excited when they read your writing.\n"
      
      "#CONTEXT#\n"
      "You are an HR expert with extensive experience in recruitment and human resources, also a very talented writer. "
      "Your way with words makes everyone very excited when they read your writing.\n"
      
      "#OBJECTIVE#\n"
      "Your task is to create a compelling Summary section for a CV, tailored specifically for a job application. "
      "You will have access to information about the candidate, including skills, work experience, a small bio, as well as information about the job listing and a report comparing the keywords found in the CV and the job listing.\n"
      
      "#STYLE#\n"
      "Write it in the style of an HR expert.\n"
      
      "#TONE#\n"
      "Professional but approachable, humble, elegant. Add personal touches to make the summary feel warm and genuine.\n"
      
      "#AUDIENCE#\n"
      "HR person, ATS screening.\n"
      
      "#RESPONSE#\n"
      "Please follow these step-by-step instructions to create a compelling Summary section. Ensure the summary is concise and does not exceed a few sentences in length. Do not invent any facts; base everything solely on the information provided by the candidate. Use the candidate's bio to add personal elements and make the summary more engaging. Keep the summary short, around 60 to 70 words, and not more than 600 characters:\n"
      
      "1. Carefully analyze the job description to identify the most relevant keywords. These keywords should include job titles, required skills, tools, technologies, and any other pertinent terms that an Applicant Tracking System (ATS) or a recruiter would focus on.\n"
      
      "2. Compare the identified keywords with the keywords found in the candidate's CV to determine the gaps and overlaps.\n"
      
      "3. Review the candidate's information in detail, including their skills, work experience, and bio. Ensure you understand the candidate's background fully.\n"
      
      "4. Using the candidate's information and the keyword analysis, craft a Summary section that highlights the candidate's most relevant skills, experiences, and qualifications that align with the job requirements. Ensure the summary is concise, impactful, and tailored to the specific job application. Use personal details from the candidate's bio to add warmth.\n"
      
      "5. Ensure the Summary section is concise and not very long, using a professional but approachable tone. Reflect the candidate's unique strengths and how they meet the essential qualifications and responsibilities listed in the job description.\n"
      
      "6. Do not invent any facts; the summary should be based solely on the information provided by the candidate.\n"
      
      "Candidate Information:\n"
      f"{profile}\n"
      
      "Job Description:\n"
      f"{job_listing}\n"
      
      "Keyword Analysis Report:\n"
      f"{analysis}\n"
      
      "Provide the tailored Summary section below. Ensure it is warm, genuine, and engaging, and does not exceed 70 words or 600 characters:\n"
    )
    response = LLM_Response(chat, prompt)
    return response.candidates[0].content.parts[0].text
