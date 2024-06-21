import streamlit as st
import os
import json
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy
import google.generativeai as genai
from fpdf import FPDF

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Configure Gemini API
api_key = os.environ.get("API_KEY")

# Load pre-trained BERT model
bert_model = SentenceTransformer('bert-base-nli-mean-tokens')

# Load Spacy model for NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Custom stop words list
custom_stopwords = set(stopwords.words('english')).union({
    'https', 'www', 'com', 'edu', 'org', 'net', 'job', 'description', 'role', 'responsibilities', 'requirements'
})

lemmatizer = WordNetLemmatizer()

def list_json_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.json')]
    return files

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat()

def LLM_Response(chat, question):
    response = chat.send_message(question, stream=True)
    response.resolve()  # Ensure the response is fully generated
    return response

def extract_keywords_with_gemini(chat, text, num_keywords=10):
    response = LLM_Response(chat, 
         "You are an HR wizard with extensive experience in recruitment and human resources. "
        "Your task is to analyze job descriptions and CVs to identify the most relevant keywords. "
        "These keywords should include job titles, required skills, tools, technologies, and any other pertinent terms "
        "that an Applicant Tracking System (ATS) or a recruiter would focus on.\n"
        "For the given text, extract the keywords that best represent the essential qualifications, responsibilities, and skills. "
        "Ensure the keywords are highly relevant to the job role or candidate profile.\n"
        "If there is no text to analyze just answer with empty space \n"
        f"Extract up to {num_keywords} relevant keywords from the following text. Provide only the keywords without any explanations, labels, any message or additional text:\n{text}"
    )
    #print(response)
    keywords = response.candidates[0].content.parts[0].text.split(',')
    return [kw.strip().lower() for kw in keywords][:num_keywords]

def extract_profile_keywords(chat, profile, num_keywords=10):
    sections = {
        "skills": [],
        "certifications": [],
        "projects": [],
        "summary": [],
        "interests": []
    }
    all_keywords = set()
    # Extracting keywords for each section
    for section, content in sections.items():
        if section in profile:
            text = []
            for item in profile[section]:
                if isinstance(item, dict):
                    text.extend(item.values())
                else:
                    text.append(item)
            joined_text = " ".join(text)
            keywords = extract_keywords_with_gemini(chat, joined_text, num_keywords)
            unique_keywords = list(set(keywords) - all_keywords)
            sections[section] = unique_keywords
            all_keywords.update(unique_keywords)
    return sections

def extract_job_listing_keywords(chat, job_listing, num_keywords=10):
    sections = {
        "requirements": [],
        "responsibilities": [],
        "skills": [],
        "experience": []
    }
    all_keywords = set()
    # Extracting keywords for each section
    for section, content in sections.items():
        if section in job_listing:
            joined_text = " ".join(job_listing[section])
            keywords = extract_keywords_with_gemini(chat, joined_text, num_keywords)
            unique_keywords = list(set(keywords) - all_keywords)
            sections[section] = unique_keywords
            all_keywords.update(unique_keywords)
    return sections

def clean_keywords(keywords):
    cleaned_keywords = set()
    for kw in keywords:
        cleaned_kw = kw.strip().lower()
        if cleaned_kw:
            cleaned_keywords.add(cleaned_kw)
    return cleaned_keywords

def get_tfidf_similarity_score(profile_text, job_text):
    vectorizer = TfidfVectorizer().fit_transform([profile_text, job_text])
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)
    return cosine_matrix[0][1] * 100

def get_embedding_similarity_score(profile_text, job_text):
    profile_embedding = bert_model.encode(profile_text)
    job_embedding = bert_model.encode(job_text)
    similarity = cosine_similarity([profile_embedding], [job_embedding])
    return similarity[0][0] * 100

def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

def compare_entities(profile_text, job_text):
    profile_entities = set(extract_entities(profile_text))
    job_entities = set(extract_entities(job_text))
    common_entities = profile_entities.intersection(job_entities)
    return len(common_entities) / len(job_entities) * 100 if job_entities else 0

def analyze_job_listing(chat, profile, job_listing):
    profile_text = " ".join([" ".join(item.values()) for section in profile.values() for item in section if isinstance(item, dict)])
    job_listing_text = " ".join(job_listing.get('requirements', []) + job_listing.get('responsibilities', []))

    tfidf_score = get_tfidf_similarity_score(profile_text, job_listing_text)
    embedding_score = get_embedding_similarity_score(profile_text, job_listing_text)
    entity_score = compare_entities(profile_text, job_listing_text)
    
    profile_keywords = extract_profile_keywords(chat, profile)
    job_keywords = extract_job_listing_keywords(chat, job_listing)
    
    all_profile_keywords = clean_keywords([kw for section in profile_keywords.values() for kw in section])
    all_job_keywords = clean_keywords([kw for section in job_keywords.values() for kw in section])
    
    keyword_overlap = all_profile_keywords.intersection(all_job_keywords)
    keyword_score = len(keyword_overlap) / len(all_job_keywords) * 100 if all_job_keywords else 0

    final_score = (tfidf_score + embedding_score + entity_score + keyword_score) / 4

    return {
        "tfidf_score": tfidf_score,
        "embedding_score": embedding_score,
        "entity_score": entity_score,
        "keyword_score": keyword_score,
        "final_score": final_score,
        "profile_keywords": profile_keywords,
        "job_keywords": job_keywords,
        "keyword_overlap": list(keyword_overlap)
    }

def save_analysis_as_pdf(analysis, profile_name, job_name, candidate_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Compatibility Analysis Report", ln=True, align="C")
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Candidate: {candidate_name}", ln=True)
    pdf.cell(200, 10, txt=f"Profile: {profile_name}", ln=True)
    pdf.cell(200, 10, txt=f"Job Listing: {job_name}", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Scores", ln=True, align="L")
    pdf.cell(200, 10, txt=f"TF-IDF Similarity Score: {analysis['tfidf_score']:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Embedding Similarity Score: {analysis['embedding_score']:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Entity Matching Score: {analysis['entity_score']:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Keyword Overlap Score: {analysis['keyword_score']:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Final Compatibility Score: {analysis['final_score']:.2f}%", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Profile Keywords", ln=True, align="L")
    for section, keywords in analysis["profile_keywords"].items():
        pdf.cell(200, 10, txt=f"{section.capitalize()}: {', '.join(keywords)}", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Job Listing Keywords", ln=True, align="L")
    for section, keywords in analysis["job_keywords"].items():
        pdf.cell(200, 10, txt=f"{section.capitalize()}: {', '.join(keywords)}", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Keyword Overlap", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Overlap Keywords: {', '.join(analysis['keyword_overlap'])}", ln=True)
    
    if not os.path.exists("Data/analysis"):
        os.makedirs("Data/analysis")
    
    pdf.output(f"Data/analysis/{profile_name[:10]}_{job_name[:10]}_analysis.pdf")

def save_analysis_as_json(analysis, profile_name, job_name):
    if not os.path.exists("Data/analysis"):
        os.makedirs("Data/analysis")
    
    with open(f"Data/analysis/{profile_name[:10]}_{job_name[:10]}_analysis.json", 'w') as f:
        json.dump(analysis, f, indent=4)

def show_job_listing_analysis():
    st.markdown("<h1>Analyze Job Listing</h1>", unsafe_allow_html=True)
    
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")
    
    if api_key:
        chat = configure_gemini(api_key)
    
    profile_files = list_json_files("Data/user_profiles/")
    job_desc_files = list_json_files("Data/JobDescription/")
    
    selected_profile = st.selectbox("Select Profile", profile_files)
    selected_job_desc = st.selectbox("Select Job Description", job_desc_files)
    
    if st.button("Analyze"):
        if not api_key:
            st.error("Please enter your Gemini API Key.")
            return
        
        if selected_profile and selected_job_desc:
            profile = load_json_file(os.path.join("Data/user_profiles", selected_profile))
            job_listing = load_json_file(os.path.join("Data/JobDescription", selected_job_desc))
            
            # Extract candidate name from profile
            candidate_name = profile.get('name', 'Unknown Candidate')
            
            analysis = analyze_job_listing(chat, profile, job_listing)
            
            st.markdown("### Compatibility Analysis Results")

            col1, col2 = st.columns(2)

            with col1:
                with st.expander("TF-IDF Similarity Score"):
                    st.write(f"**Score:** {analysis['tfidf_score']:.2f}%")
                    st.write("Measures how often terms appear in the profile and job description and how unique those terms are.")

            with col2:
                with st.expander("Embedding Similarity Score"):
                    st.write(f"**Score:** {analysis['embedding_score']:.2f}%")
                    st.write("Uses BERT embeddings to measure semantic similarity between the profile and job listing, capturing the meaning of the text.")

            col3, col4 = st.columns(2)

            with col3:
                with st.expander("Entity Matching Score"):
                    st.write(f"**Score:** {analysis['entity_score']:.2f}%")
                    st.write("Compares important entities (like skills, job titles) in both texts to ensure key entities mentioned in the job listing are also present in the profile.")

            with col4:
                with st.expander("Keyword Overlap Score"):
                    st.write(f"**Score:** {analysis['keyword_score']:.2f}%")
                    st.write("Uses keyword extraction to measure the overlap between the profile and job listing, checking how many important keywords from the job listing are found in the profile.")

            st.markdown("### Final Compatibility Score")
            st.write(f"**Score:** {analysis['final_score']:.2f}%")

            with st.expander("Profile Keywords"):
                for section, keywords in analysis["profile_keywords"].items():
                    st.write(f"**{section.capitalize()}**: {', '.join(keywords)}")
            
            with st.expander("Job Listing Keywords"):
                for section, keywords in analysis["job_keywords"].items():
                    st.write(f"**{section.capitalize()}**: {', '.join(keywords)}")

            with st.expander("Keyword Overlap"):
                st.write(f"**Overlap Keywords**: {', '.join(analysis['keyword_overlap'])}")

            # Save analysis as PDF and JSON
            profile_name = os.path.splitext(selected_profile)[0]
            job_name = os.path.splitext(selected_job_desc)[0]
            save_analysis_as_pdf(analysis, profile_name, job_name, candidate_name)
            save_analysis_as_json(analysis, profile_name, job_name)

            st.success("Analysis saved as PDF and JSON files.")

        else:
            st.error("Please select both a profile and a job description for analysis.")

if __name__ == "__main__":
    show_job_listing_analysis()
