import google.generativeai as genai

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat()

def LLM_Response(chat, question):
    response = chat.send_message(question, stream=True)
    response.resolve()  # Ensure the response is fully generated
    return response

def generate_cover_letter_section(chat, profile, job_listing, analysis):
    prompt = (
      "You are an HR expert with extensive experience in recruitment and human resources, and a very talented writer. Your way with words makes everyone very excited when they read your writing.\n"
    
    "#CONTEXT#\n"
    "You are an HR expert with extensive experience in recruitment and human resources, also a very talented writer. Your way with words makes everyone very excited when they read your writing.\n"
    
    "#OBJECTIVE#\n"
    "Your task is to create a compelling cover letter tailored specifically for a job application. You will have access to information about the candidate, including skills, work experience, a small bio, as well as information about the job listing and a report comparing the keywords found in the CV and the job listing.\n"
    
    "#STYLE#\n"
    "Write it in the style of an HR expert.\n"
    
    "#TONE#\n"
    "Professional but approachable, humble, elegant. Add personal touches to make the letter feel warm and genuine.\n"
    
    "#AUDIENCE#\n"
    "HR person, ATS screening.\n"
    
    "#RESPONSE#\n"
    "Please follow these step-by-step instructions to create a cover letter using the COSTAR method. Ensure the cover letter is concise and does not exceed one page in length. Do not invent any facts; base everything solely on the information provided by the candidate. Use the candidate's bio to add personal elements and make the letter more engaging:\n"
    
    "1. **Context**: Start with an engaging opening that provides context about who the candidate is and why they are writing. Mention the job they are applying for and how they found the job listing. Use personal details from the candidate's bio to add warmth.\n"
    "Example: 'I am writing to express my interest in the [Job Title] position at [Company Name]. With a strong background in [relevant field] and a passion for [related personal interest], I am excited about the opportunity to contribute to your team.'\n"
    
    "2. **Objective**: Clearly state the candidate’s career objective and how it aligns with the company’s goals and the specific job role. Use personal motivations from the bio to add depth.\n"
    "Example: 'My objective is to leverage my experience in [specific skill/field] to contribute to [Company Name]'s mission of [company mission or goal]. My passion for [related personal interest] drives my dedication to this field.'\n"
    
    "3. **Situation**: Describe a specific situation or challenge the candidate faced in their previous roles that is relevant to the job they are applying for.\n"
    "Example: 'In my previous role at [Previous Company], I was tasked with [specific challenge or responsibility].'\n"
    
    "4. **Task**: Explain the task or responsibility the candidate had in that situation.\n"
    "Example: 'My task was to [specific task], which required [skills/abilities].'\n"
    
    "5. **Action**: Detail the actions the candidate took to address the situation or complete the task. Highlight specific skills and experiences relevant to the job description.\n"
    "Example: 'I implemented [specific actions] which involved [skills/technologies].'\n"
    
    "6. **Result**: Share the results or outcomes of the candidate’s actions. Use quantifiable metrics if possible to demonstrate success.\n"
    "Example: 'As a result of my efforts, [specific results], leading to [positive outcome].'\n"
    
    "7. **Closing**: End with a strong closing paragraph that reiterates the candidate’s interest in the position and enthusiasm for contributing to the company. Invite the reader to contact them for further discussion. Add a personal touch to leave a lasting impression.\n"
    "Example: 'I am enthusiastic about the opportunity to bring my unique skills to [Company Name] and am confident in my ability to contribute to your team. I look forward to the possibility of discussing how my background, skills, and passion for [related personal interest] will be beneficial to your team. Thank you for considering my application.'\n"
    
    "Additional Instructions:\n"
    "- Do not invent any facts; the letter should be based solely on the information provided by the candidate.\n"
    "- Start with just 'Hello,'"
    "- Ensure the cover letter is concise and does not exceed one page in length.\n"
    
   "Candidate Information:\n"
    f"{profile}\n"
    
    "Job Description:\n"
    f"{job_listing}\n"
    
    "Keyword Analysis Report:\n"
    f"{analysis}\n"
    
    "Provide the tailored cover letter below using the COSTAR method. Ensure it is warm, genuine, and engaging:\n"
    
      
    )
    response = LLM_Response(chat, prompt)
    return response.candidates[0].content.parts[0].text
