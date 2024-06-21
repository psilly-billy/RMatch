import streamlit as st
import json
import os
from datetime import datetime

# Directory to store user profiles temporarily
USER_PROFILES_DIR = "Data/user_profiles/"

def save_details(username, details):
    if not os.path.exists(USER_PROFILES_DIR):
        os.makedirs(USER_PROFILES_DIR)
    with open(os.path.join(USER_PROFILES_DIR, f"{username}.json"), 'w') as file:
        json.dump(details, file, indent=4)

def load_details(username):
    filepath = os.path.join(USER_PROFILES_DIR, f"{username}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return {}

def save_uploaded_profile(uploaded_file):
    with open(os.path.join(USER_PROFILES_DIR, uploaded_file.name), 'wb') as file:
        file.write(uploaded_file.getbuffer())

def load_details_from_file(file):
    return json.load(file)

def profile_m():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Build Profile</h1>", unsafe_allow_html=True)

    # User management
    st.sidebar.header("User Management")
    username = st.sidebar.text_input("Username")

    if st.sidebar.button("Create New Profile"):
        if username:
            st.sidebar.success(f"Profile '{username}' created. You can now enter your details.")
        else:
            st.sidebar.error("Please enter a username to create a profile.")

    uploaded_file = st.sidebar.file_uploader("Upload Profile", type="json")
    if uploaded_file:
        details = load_details_from_file(uploaded_file)
        st.sidebar.success("Profile loaded from file.")
    else:
        details = {}

    if st.sidebar.button("Load Profile"):
        if username:
            details = load_details(username)
            if details:
                st.sidebar.success(f"Profile '{username}' loaded.")
            else:
                st.sidebar.error(f"No profile found for '{username}'.")
        else:
            st.sidebar.error("Please enter a username to load a profile.")

    if username or uploaded_file:
        # Load existing details if available
        if not uploaded_file:
            details = load_details(username) if username else {}

        with st.expander("Personal Details", expanded=False):
            st.markdown("<h2>Personal Details</h2>", unsafe_allow_html=True)
            name = st.text_input("Full Name", details.get("name", ""))
            location = st.text_input("Location", details.get("location", ""))
            email = st.text_input("Email Address", details.get("email", ""))
            phone = st.text_input("Phone Number", details.get("phone", ""))
            linkedin = st.text_input("LinkedIn Profile", details.get("linkedin", ""))
            github = st.text_input("GitHub Profile", details.get("github", ""))
            website = st.text_input("Personal Website/Portfolio", details.get("website", ""))

            if st.button("Save Personal Details"):
                details["name"] = name
                details["location"] = location
                details["email"] = email
                details["phone"] = phone
                details["linkedin"] = linkedin
                details["github"] = github
                details["website"] = website
                save_details(username, details)
                st.success("Personal details saved successfully!")
        
        with st.expander("Professional Summary", expanded=False):
            st.markdown("<h2>Professional Summary</h2>", unsafe_allow_html=True)
            summary = st.text_area("Professional Summary", details.get("summary", ""), help="Provide a brief summary about your professional background.")

            if st.button("Save Professional Summary"):
                details["summary"] = summary
                save_details(username, details)
                st.success("Professional summary saved successfully!")

        with st.expander("Work Experience", expanded=False):
            st.markdown("<h2>Work Experience</h2>", unsafe_allow_html=True)
            experiences = details.get("experience", [])
            if "experience" not in details:
                details["experience"] = []

            # Form to add a new experience
            with st.form("experience_form", clear_on_submit=True):
                st.markdown("<h3>Add New Experience</h3>", unsafe_allow_html=True)
                job_title = st.text_input("Job Title")
                company_name = st.text_input("Company Name")
                location = st.text_input("Location")
                start_date = st.date_input("Start Date", min_value=datetime(1900, 1, 1), max_value=datetime.now())
                current_job = st.checkbox("I currently work here")
                end_date = st.date_input("End Date", min_value=datetime(1900, 1, 1), max_value=datetime.now()) if not current_job else st.text("Present")
                job_description = st.text_area("Job Description")
                add_experience = st.form_submit_button("Add Experience")

            if add_experience:
                experience = {
                    "job_title": job_title,
                    "company_name": company_name,
                    "location": location,
                    "start_date": start_date.strftime('%Y-%m-%d'),
                    "end_date": "Present" if current_job else end_date.strftime('%Y-%m-%d'),
                    "job_description": job_description
                }
                details["experience"].append(experience)
                save_details(username, details)
                st.success("Experience added successfully!")
                st.rerun()

            # Display added experiences with delete and modify options
            for i, exp in enumerate(details["experience"]):
                st.markdown(f"<h3>{exp['job_title']} at {exp['company_name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Location:</b> {exp['location']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Period:</b> {exp['start_date']} - {exp['end_date']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Description:</b> {exp['job_description']}</p>", unsafe_allow_html=True)
                if st.button(f"Delete Experience {i+1}"):
                    details["experience"].pop(i)
                    save_details(username, details)
                    st.rerun()

                with st.form(f"modify_experience_form_{i}", clear_on_submit=True):
                    new_job_title = st.text_input("Job Title", exp['job_title'], key=f"job_title_{i}")
                    new_company_name = st.text_input("Company Name", exp['company_name'], key=f"company_name_{i}")
                    new_location = st.text_input("Location", exp['location'], key=f"location_{i}")
                    new_start_date = st.date_input("Start Date", datetime.strptime(exp['start_date'], '%Y-%m-%d'), min_value=datetime(1900, 1, 1), max_value=datetime.now(), key=f"start_date_{i}")
                    new_current_job = st.checkbox("I currently work here", exp['end_date'] == "Present", key=f"current_job_{i}")
                    new_end_date = st.date_input("End Date", datetime.strptime(exp['end_date'], '%Y-%m-%d'), min_value=datetime(1900, 1, 1), max_value=datetime.now(), key=f"end_date_{i}") if not new_current_job else st.text("Present")
                    new_job_description = st.text_area("Job Description", exp['job_description'], key=f"job_description_{i}")
                    save_modification = st.form_submit_button("Save Changes")

                    if save_modification:
                        details["experience"][i]["job_title"] = new_job_title
                        details["experience"][i]["company_name"] = new_company_name
                        details["experience"][i]["location"] = new_location
                        details["experience"][i]["start_date"] = new_start_date.strftime('%Y-%m-%d')
                        details["experience"][i]["end_date"] = "Present" if new_current_job else new_end_date.strftime('%Y-%m-%d')
                        details["experience"][i]["job_description"] = new_job_description
                        save_details(username, details)
                        st.success("Experience modified successfully!")
                        st.rerun()
                st.markdown("---")

        with st.expander("Education", expanded=False):
            st.markdown("<h2>Education</h2>", unsafe_allow_html=True)
            education_entries = details.get("education", [])
            if "education" not in details:
                details["education"] = []

            # Form to add a new education entry
            with st.form("education_form", clear_on_submit=True):
                st.markdown("<h3>Add New Education</h3>", unsafe_allow_html=True)
                degree = st.text_input("Degree")
                institution = st.text_input("Institution")
                edu_location = st.text_input("Location")
                edu_start_date = st.date_input("Start Date", min_value=datetime(1900, 1, 1), max_value=datetime.now(), key="edu_start")
                edu_end_date = st.date_input("End Date", min_value=datetime(1900, 1, 1), max_value=datetime.now(), key="edu_end")
                edu_description = st.text_area("Description", key="edu_desc")
                add_education = st.form_submit_button("Add Education")

            if add_education:
                education = {
                    "degree": degree,
                    "institution": institution,
                    "location": edu_location,
                    "start_date": edu_start_date.strftime('%Y-%m-%d'),
                    "end_date": edu_end_date.strftime('%Y-%m-%d'),
                    "description": edu_description
                }
                details["education"].append(education)
                save_details(username, details)
                st.success("Education added successfully!")
                st.rerun()

            # Display added education entries with delete and modify options
            for i, edu in enumerate(details["education"]):
                st.markdown(f"<h3>{edu['degree']} at {edu['institution']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Location:</b> {edu['location']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Period:</b> {edu['start_date']} - {edu['end_date']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Description:</b> {edu['description']}</p>", unsafe_allow_html=True)
                if st.button(f"Delete Education {i+1}"):
                    details["education"].pop(i)
                    save_details(username, details)
                    st.rerun()

                with st.form(f"modify_education_form_{i}", clear_on_submit=True):
                    new_degree = st.text_input("Degree", edu['degree'], key=f"degree_{i}")
                    new_institution = st.text_input("Institution", edu['institution'], key=f"institution_{i}")
                    new_edu_location = st.text_input("Location", edu['location'], key=f"edu_location_{i}")
                    new_edu_start_date = st.date_input("Start Date", datetime.strptime(edu['start_date'], '%Y-%m-%d'), min_value=datetime(1900, 1, 1), max_value=datetime.now(), key=f"new_edu_start_{i}")
                    new_edu_end_date = st.date_input("End Date", datetime.strptime(edu['end_date'], '%Y-%m-%d'), min_value=datetime(1900, 1, 1), max_value=datetime.now(), key=f"new_edu_end_{i}")
                    new_edu_description = st.text_area("Description", edu['description'], key=f"new_edu_desc_{i}")
                    save_modification = st.form_submit_button("Save Changes")

                    if save_modification:
                        details["education"][i] = {
                            "degree": new_degree,
                            "institution": new_institution,
                            "location": new_edu_location,
                            "start_date": new_edu_start_date.strftime('%Y-%m-%d'),
                            "end_date": new_edu_end_date.strftime('%Y-%m-%d'),
                            "description": new_edu_description
                        }
                        save_details(username, details)
                        st.success("Education modified successfully!")
                        st.rerun()
                st.markdown("---")

        with st.expander("Skills", expanded=False):
            st.markdown("<h2>Skills</h2>", unsafe_allow_html=True)
            skills_entries = details.get("skills", [])
            if "skills" not in details:
                details["skills"] = []

            # Soft Skills options
            soft_skills_options = [
                "Communication", "Teamwork", "Problem Solving", "Time Management", "Critical Thinking", 
                "Decision Making", "Organizational", "Stress Management", "Adaptability", "Creativity",
                "Interpersonal", "Work Ethic", "Attention to Detail", "Leadership", "Customer Service", 
                "Conflict Resolution", "Negotiation", "Presentation", "Self-motivation", "Flexibility"
            ]

            # Form to add a new soft skill
            with st.form("soft_skills_form", clear_on_submit=True):
                st.markdown("<h3>Add Soft Skill</h3>", unsafe_allow_html=True)
                soft_skill = st.selectbox("Select Soft Skill", soft_skills_options)
                custom_soft_skill = st.text_input("Or type a custom soft skill")
                add_soft_skill = st.form_submit_button("Add Soft Skill")

            if add_soft_skill:
                skill_entry = {
                    "skill": custom_soft_skill if custom_soft_skill else soft_skill,
                    "level": "N/A"  # No proficiency level for soft skills
                }
                details["skills"].append(skill_entry)
                save_details(username, details)
                st.success("Soft Skill added successfully!")
                st.rerun()

            # Form to add a new hard skill
            with st.form("hard_skills_form", clear_on_submit=True):
                st.markdown("<h3>Add Hard Skill</h3>", unsafe_allow_html=True)
                hard_skill = st.text_input("Hard Skill")
                skill_level = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
                add_hard_skill = st.form_submit_button("Add Hard Skill")

            if add_hard_skill:
                skills_entry = {
                    "skill": hard_skill,
                    "level": skill_level
                }
                details["skills"].append(skills_entry)
                save_details(username, details)
                st.success("Hard Skill added successfully!")
                st.rerun()

            # Display added skills in a compact format with delete and modify options
            cols = st.columns(2)
            for i, skl in enumerate(details["skills"]):
                col = cols[i % 2]
                with col:
                    st.markdown(f"**{skl['skill']}** - {skl['level']}")
                    if st.button(f"Delete Skill {i+1}", key=f"delete_skill_{i}"):
                        details["skills"].pop(i)
                        save_details(username, details)
                        st.rerun()

                    with st.form(f"modify_skill_form_{i}", clear_on_submit=True):
                        new_skill = st.text_input("Skill", skl['skill'], key=f"skill_{i}")
                        new_skill_level = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=["Beginner", "Intermediate", "Advanced", "Expert"].index(skl['level']), key=f"skill_level_{i}") if skl['level'] != "N/A" else "N/A"
                        save_modification = st.form_submit_button("Save Changes")

                        if save_modification:
                            details["skills"][i] = {
                                "skill": new_skill,
                                "level": new_skill_level
                            }
                            save_details(username, details)
                            st.success("Skill modified successfully!")
                            st.rerun()

        with st.expander("Certifications", expanded=False):
            st.markdown("<h2>Certifications</h2>", unsafe_allow_html=True)
            certifications_entries = details.get("certifications", [])
            if "certifications" not in details:
                details["certifications"] = []

            # Form to add a new certification
            with st.form("certifications_form", clear_on_submit=True):
                st.markdown("<h3>Add Certification</h3>", unsafe_allow_html=True)
                certification = st.text_input("Certification")
                certifying_body = st.text_input("Certifying Body")
                cert_date = st.date_input("Date Awarded", min_value=datetime(1900, 1, 1), max_value=datetime.now())
                cert_description = st.text_area("Description", key="cert_desc")
                add_certification = st.form_submit_button("Add Certification")

            if add_certification:
                certification_entry = {
                    "certification": certification,
                    "certifying_body": certifying_body,
                    "date_awarded": cert_date.strftime('%Y-%m-%d'),
                    "description": cert_description
                }
                details["certifications"].append(certification_entry)
                save_details(username, details)
                st.success("Certification added successfully!")
                st.rerun()

            # Display added certifications with delete and modify options
            for i, cert in enumerate(details["certifications"]):
                st.markdown(f"<h3>{cert['certification']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Certifying Body:</b> {cert['certifying_body']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Date Awarded:</b> {cert['date_awarded']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Description:</b> {cert['description']}</p>", unsafe_allow_html=True)
                if st.button(f"Delete Certification {i+1}"):
                    details["certifications"].pop(i)
                    save_details(username, details)
                    st.rerun()

                with st.form(f"modify_certification_form_{i}", clear_on_submit=True):
                    new_certification = st.text_input("Certification", cert['certification'], key=f"certification_{i}")
                    new_certifying_body = st.text_input("Certifying Body", cert['certifying_body'], key=f"certifying_body_{i}")
                    new_cert_date = st.date_input("Date Awarded", datetime.strptime(cert['date_awarded'], '%Y-%m-%d'), min_value=datetime(1900, 1, 1), max_value=datetime.now(), key=f"new_cert_date_{i}")
                    new_cert_description = st.text_area("Description", cert['description'], key=f"new_cert_desc_{i}")
                    save_modification = st.form_submit_button("Save Changes")

                    if save_modification:
                        details["certifications"][i] = {
                            "certification": new_certification,
                            "certifying_body": new_certifying_body,
                            "date_awarded": new_cert_date.strftime('%Y-%m-%d'),
                            "description": new_cert_description
                        }
                        save_details(username, details)
                        st.success("Certification modified successfully!")
                        st.rerun()
                st.markdown("---")

        with st.expander("Projects", expanded=False):
            st.markdown("<h2>Projects</h2>", unsafe_allow_html=True)
            projects_entries = details.get("projects", [])
            if "projects" not in details:
                details["projects"] = []

            # Form to add a new project
            with st.form("projects_form", clear_on_submit=True):
                st.markdown("<h3>Add Project</h3>", unsafe_allow_html=True)
                project_title = st.text_input("Project Title")
                project_description = st.text_area("Project Description", key="proj_desc")
                project_url = st.text_input("Project URL")
                add_project = st.form_submit_button("Add Project")

            if add_project:
                project_entry = {
                    "title": project_title,
                    "description": project_description,
                    "url": project_url
                }
                details["projects"].append(project_entry)
                save_details(username, details)
                st.success("Project added successfully!")
                st.rerun()

            # Display added projects with delete and modify options
            for i, proj in enumerate(details["projects"]):
                st.markdown(f"<h3>{proj['title']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Description:</b> {proj['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>URL:</b> {proj['url']}</p>", unsafe_allow_html=True)
                if st.button(f"Delete Project {i+1}"):
                    details["projects"].pop(i)
                    save_details(username, details)
                    st.rerun()

                with st.form(f"modify_project_form_{i}", clear_on_submit=True):
                    new_project_title = st.text_input("Project Title", proj['title'], key=f"project_title_{i}")
                    new_project_description = st.text_area("Project Description", proj['description'], key=f"new_proj_desc_{i}")
                    new_project_url = st.text_input("Project URL", proj['url'])
                    save_modification = st.form_submit_button("Save Changes")

                    if save_modification:
                        details["projects"][i] = {
                            "title": new_project_title,
                            "description": new_project_description,
                            "url": new_project_url
                        }
                        save_details(username, details)
                        st.success("Project modified successfully!")
                        st.rerun()
                st.markdown("---")

        with st.expander("Interests", expanded=False):
            st.markdown("<h2>Interests</h2>", unsafe_allow_html=True)
            interests = st.text_area("Interests", details.get("interests", ""), help="Provide a brief summary of your interests.")
            details["interests"] = interests

            if st.button("Save Interests"):
                details["interests"] = interests
                save_details(username, details)
                st.success("Interests saved successfully!")

        with st.expander("Short Bio", expanded=False):
            st.markdown("<h2>Short Bio</h2>", unsafe_allow_html=True)
            short_bio = st.text_area("Short Bio", details.get("short_bio", ""), help="Provide a brief summary about yourself.")
            details["short_bio"] = short_bio

            if st.button("Save Short Bio"):
                details["short_bio"] = short_bio
                save_details(username, details)
                st.success("Short Bio saved successfully!")

        st.download_button(
            label="Download Profile as JSON",
            data=json.dumps(details, indent=4),
            file_name=f"{username}_profile.json",
            mime="application/json",
        )

        if uploaded_file:
            if st.button("Save Uploaded Profile"):
                save_uploaded_profile(uploaded_file)
                st.success("Uploaded profile saved successfully!")

if __name__ == "__main__":
    profile_m()
