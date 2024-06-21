import streamlit as st
import os
import atexit
from home import show_home
from profile_maker import profile_m
from job_listing_pdf import show_job_listing_pdf
from job_listing_analysis import show_job_listing_analysis
from personalized_cv import show_personalized_cv

# Directory to store user profiles temporarily
USER_PROFILES_DIR = "Data/user_profiles/"
JOB_DESC_DIR = "Data/JobDescription/"
JOB_ANALYSIS_DIR = "Data/analysis/"

PAGES = {
    "Home": show_home,
    "Profile Management": profile_m,
    "Save Job Listing as PDF": show_job_listing_pdf,
    "Analyze Job Listing": show_job_listing_analysis,
    "Create Personalized CV": show_personalized_cv
}

def list_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

def file_manager():
    st.sidebar.title("File Manager")
    
    profile_files = list_files(USER_PROFILES_DIR)
    job_desc_files = list_files(JOB_DESC_DIR)
    job_analysis_files = list_files(JOB_ANALYSIS_DIR)
    
    with st.sidebar.expander("Profiles", expanded=False):
        if profile_files:
            for profile in profile_files:
                col1, col2 = st.columns([3, 1])
                col1.write(profile)
                with col2:
                    st.download_button(label="Download", data=open(os.path.join(USER_PROFILES_DIR, profile), "rb").read(), file_name=profile)
                    if st.button(f"Delete", key=f"del_profile_{profile}"):
                        os.remove(os.path.join(USER_PROFILES_DIR, profile))
                        st.success(f"Deleted {profile}")
                        st.rerun()
        else:
            st.write("No profiles found.")
    
    with st.sidebar.expander("Job Descriptions", expanded=False):
        if job_desc_files:
            for job_desc in job_desc_files:
                col1, col2 = st.columns([3, 1])
                col1.write(job_desc)
                with col2:
                    st.download_button(label="Download", data=open(os.path.join(JOB_DESC_DIR, job_desc), "rb").read(), file_name=job_desc)
                    if st.button(f"Delete", key=f"del_job_{job_desc}"):
                        os.remove(os.path.join(JOB_DESC_DIR, job_desc))
                        st.success(f"Deleted {job_desc}")
                        st.rerun()
        else:
            st.write("No job descriptions found.")
    
    with st.sidebar.expander("Analysis", expanded=False):
        if job_analysis_files:
            for job_analysis in job_analysis_files:
                col1, col2 = st.columns([3, 1])
                col1.write(job_analysis)
                with col2:
                    st.download_button(label="Download", data=open(os.path.join(JOB_ANALYSIS_DIR, job_analysis), "rb").read(), file_name=job_analysis)
                    if st.button(f"Delete", key=f"del_job_{job_analysis}"):
                        os.remove(os.path.join(JOB_ANALYSIS_DIR, job_analysis))
                        st.success(f"Deleted {job_analysis}")
                        st.rerun()
        else:
            st.write("No Analysis found.")

def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page()
    file_manager()

def cleanup_files():
    for directory in [USER_PROFILES_DIR, JOB_DESC_DIR, JOB_ANALYSIS_DIR]:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

atexit.register(cleanup_files)

if __name__ == "__main__":
    main()
