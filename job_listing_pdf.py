import streamlit as st
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from xhtml2pdf import pisa
import json
import os

# Directory to save job descriptions
JOB_PATH = "Data/JobDescription/"
if not os.path.exists(JOB_PATH):
    os.makedirs(JOB_PATH)

def linkedin_to_pdf(job_url: str):
    files_number = len([f for f in os.listdir(JOB_PATH) if os.path.isfile(os.path.join(JOB_PATH, f))])

    try:
        page = requests.get(job_url)

        if page.status_code != 200:
            st.error(f"Failed to retrieve the job posting at {job_url}. Status code: {page.status_code}")
            return

        # Parse the HTML content of the job posting using BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")

        # Find the job title element and get the text
        job_title = soup.find("h1", {"class": "topcard__title"}).text.strip()

        # Find the organization name element (try both selectors)
        organization_element = soup.find("span", {"class": "topcard__flavor"})
        if not organization_element:
            organization_element = soup.find("a", {"class": "topcard__org-name-link"})
        organization = organization_element.text.strip()

        # Find the location element
        location_element = soup.find("span", {"class": "topcard__flavor--bullet"})
        location = location_element.text.strip() if location_element else "Not specified"

        # Find the job description element
        job_description_element = soup.find("div", {"class": "show-more-less-html__markup"})
        job_description_html = str(job_description_element) if job_description_element else "No description provided"

        # Extract granular data from the job description
        job_description_text = job_description_element.get_text(separator="\n").strip() if job_description_element else "No description provided"
        requirements, responsibilities, skills, benefits, other_details = extract_granular_data(job_description_text)

        # Set file_path and sanitize organization name and job title
        sanitized_filename = sanitize_filename(f"{organization}__{job_title}_{files_number}")
        pdf_path = os.path.join(JOB_PATH, f"{sanitized_filename}.pdf")
        json_path = os.path.join(JOB_PATH, f"{sanitized_filename}.json")

        # Create a PDF file and write the job description to it
        with open(pdf_path, "wb") as pdf_file:
            pisa.CreatePDF(job_description_html, dest=pdf_file, encoding="utf-8")

        # Save the job description and metadata as a JSON file
        job_data = {
            "organization": organization,
            "job_title": job_title,
            "location": location,
            "requirements": requirements,
            "responsibilities": responsibilities,
            "skills": skills,
            "benefits": benefits,
            "other_details": other_details
        }
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(job_data, json_file, indent=4, ensure_ascii=False)

        st.success(f"Job description saved as {pdf_path} and {json_path}")

    except Exception as e:
        st.error(f"Could not get the description from the URL: {job_url}")
        st.error(str(e))

def extract_granular_data(job_description: str):
    requirements = []
    responsibilities = []
    skills = []
    benefits = []
    other_details = []
    sections = {"requirements": requirements, "responsibilities": responsibilities, "skills": skills, "benefits": benefits, "other_details": other_details}

    current_section = "other_details"
    lines = job_description.split('\n')

    for line in lines:
        line_lower = line.lower().strip()
        if "requirement" in line_lower or "qualification" in line_lower or "education" in line_lower:
            current_section = "requirements"
        elif "responsibilit" in line_lower or "duties" in line_lower or "role" in line_lower:
            current_section = "responsibilities"
        elif "skill" in line_lower:
            current_section = "skills"
        elif "benefit" in line_lower or "we offer" in line_lower or "compensation" in line_lower:
            current_section = "benefits"
        else:
            sections[current_section].append(line.strip())
    
    # Clean up empty strings from lists
    sections = {k: [item for item in v if item] for k, v in sections.items()}

    return requirements, responsibilities, skills, benefits, other_details

def create_pdf(content: str, file_path: str):
    with open(file_path, "wb") as pdf_file:
        pisa.CreatePDF(content, dest=pdf_file, encoding="utf-8")

def show_job_listing_pdf():
    st.markdown("<h1>Save Job Listing as PDF and JSON</h1>", unsafe_allow_html=True)
    job_url = st.text_input("Enter the URL of the LinkedIn Job Posting:")
    job_description = st.text_area("Or paste the job description here:")

    if st.button("Save Job Listing"):
        if job_url:
            linkedin_to_pdf(job_url)
        elif job_description:
            # Use a placeholder organization and job title for manually pasted descriptions
            organization = "Manual_Entry"
            job_title = "Job_Description"
            location = "Not specified"  # Define location for manual entries
            files_number = len([f for f in os.listdir(JOB_PATH) if os.path.isfile(os.path.join(JOB_PATH, f))])
            sanitized_filename = sanitize_filename(f"{organization}__{job_title}_{files_number}")
            pdf_path = os.path.join(JOB_PATH, f"{sanitized_filename}.pdf")
            json_path = os.path.join(JOB_PATH, f"{sanitized_filename}.json")

            # Extract granular data from the job description
            requirements, responsibilities, skills, benefits, other_details = extract_granular_data(job_description)

            # Prepare content for the PDF
            pdf_content = f"""
            <h1>{organization}</h1>
            <h2>{job_title}</h2>
            <h3>Location: {location}</h3>
            <h3>Requirements:</h3>
            <ul>
                {"".join(f"<li>{req}</li>" for req in requirements)}
            </ul>
            <h3>Responsibilities:</h3>
            <ul>
                {"".join(f"<li>{resp}</li>" for resp in responsibilities)}
            </ul>
            <h3>Skills:</h3>
            <ul>
                {"".join(f"<li>{skill}</li>" for skill in skills)}
            </ul>
            <h3>Benefits:</h3>
            <ul>
                {"".join(f"<li>{benefit}</li>" for benefit in benefits)}
            </ul>
            <h3>Other Details:</h3>
            <ul>
                {"".join(f"<li>{detail}</li>" for detail in other_details)}
            </ul>
            """

            # Create a PDF file and write the job description to it
            create_pdf(pdf_content, pdf_path)

            # Save the job description and metadata as a JSON file
            job_data = {
                "organization": organization,
                "job_title": job_title,
                "location": location,
                "requirements": requirements,
                "responsibilities": responsibilities,
                "skills": skills,
                "benefits": benefits,
                "other_details": other_details
            }
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(job_data, json_file, indent=4, ensure_ascii=False)

            st.success(f"Job description saved as {pdf_path} and {json_path}")
        else:
            st.error("Please enter a URL or paste a job description.")

if __name__ == "__main__":
    show_job_listing_pdf()
