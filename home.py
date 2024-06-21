import streamlit as st

def show_home():
    st.title("Welcome to the Job Application Companion")
    st.write("Navigate through the different functionalities using the sidebar.")
    st.markdown("""
        ### Features:
        - **Profile Management**: 
            - Create and manage profiles.
            - Enter and save personal details, professional summaries, work experiences, education, skills, certifications, projects, interests, and a short bio.
            - Upload and download profiles as JSON files.
        - **Save Job Listing as PDF**: 
            - Upload job listing documents (DOCX or PDF) and convert them to PDF for consistent and easy sharing.
        - **Analyze Job Listing**: 
            - Upload job listing JSON files and analyze their compatibility with your profile using various scores and metrics.
        - **Create Personalized CV**: 
            - Use the Gemini API to generate personalized summary, skills, and experience sections for your CV.
            - Automatically format the CV sections for better readability and ATS compatibility.
            - Download the personalized CV as a Word document.
        - **Create Personalized Cover Letter**: 
            - Use the Gemini API to generate personalized cover letters tailored to specific job applications.
            - Download the generated cover letter as a Word document.
        - **File Manager**: 
            - View, download, and delete files in the user profiles, job descriptions, and analysis directories.

        ### Requirements:
        To use the Gemini API for free, you need:
        - **Gemini API Key**: Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
        - **VPN**: Use a VPN to emulate that you are in the USA to access the Gemini API for free.
    """)

if __name__ == "__main__":
    show_home()
