import streamlit as st
import os
from home import show_home
from profile_maker import profile_m
from job_listing_pdf import show_job_listing_pdf
from job_listing_analysis import show_job_listing_analysis
from personalized_cv import show_personalized_cv
from cover_letter import show_cover_letter

PAGES = {
    "Home": show_home,
    "Profile Management": profile_m,
    "Save Job Listing as PDF": show_job_listing_pdf,
    "Analyze Job Listing": show_job_listing_analysis,
    "Create Personalized CV": show_personalized_cv,
    "Cover Letter": show_cover_letter
}

def list_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

def file_manager():
    st.sidebar.title("File Manager")
    
    profile_dir = "Data/user_profiles/"
    job_desc_dir = "Data/JobDescription/"
    job_analysis_dir = "Data/analysis/"
    gen_dir = "Data/Gen/"
    
    profile_files = list_files(profile_dir)
    job_desc_files = list_files(job_desc_dir)
    job_analysis = list_files(job_analysis_dir)
    gen_files = list_files(gen_dir)
    
    with st.sidebar.expander("Profiles", expanded=False):
        if profile_files:
            for profile in profile_files:
                st.write(profile)
                cols = st.columns([2, 1])
                with cols[0]:
                    st.download_button(label="Download", data=open(os.path.join(profile_dir, profile), "rb").read(), file_name=profile)
                with cols[1]:
                    if st.button(f"Delete", key=f"del_profile_{profile}"):
                        os.remove(os.path.join(profile_dir, profile))
                        st.success(f"Deleted {profile}")
                        st.rerun()
        else:
            st.write("No profiles found.")
    
    with st.sidebar.expander("Job Descriptions", expanded=False):
        if job_desc_files:
            for job_desc in job_desc_files:
                st.write(job_desc)
                cols = st.columns([2, 1])
                with cols[0]:
                    st.download_button(label="Download", data=open(os.path.join(job_desc_dir, job_desc), "rb").read(), file_name=job_desc)
                with cols[1]:
                    if st.button(f"Delete", key=f"del_job_{job_desc}"):
                        os.remove(os.path.join(job_desc_dir, job_desc))
                        st.success(f"Deleted {job_desc}")
                        st.rerun()
        else:
            st.write("No job descriptions found.")
    
    with st.sidebar.expander("Analysis", expanded=False):
        if job_analysis:
            for job_analys in job_analysis:
                st.write(job_analys)
                cols = st.columns([2, 1])
                with cols[0]:
                    st.download_button(label="Download", data=open(os.path.join(job_analysis_dir, job_analys), "rb").read(), file_name=job_analys)
                with cols[1]:
                    if st.button(f"Delete", key=f"del_analysis_{job_analys}"):
                        os.remove(os.path.join(job_analysis_dir, job_analys))
                        st.success(f"Deleted {job_analys}")
                        st.rerun()
        else:
            st.write("No Analysis found.")
    
    with st.sidebar.expander("Generated CVs / CL", expanded=False):
        if gen_files:
            for gen_file in gen_files:
                st.write(gen_file)
                cols = st.columns([2, 1])
                with cols[0]:
                    st.download_button(label="Download", data=open(os.path.join(gen_dir, gen_file), "rb").read(), file_name=gen_file)
                with cols[1]:
                    if st.button(f"Delete", key=f"del_gen_{gen_file}"):
                        os.remove(os.path.join(gen_dir, gen_file))
                        st.success(f"Deleted {gen_file}")
                        st.rerun()
        else:
            st.write("No Generated CVs found.")

def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page()
    file_manager()

if __name__ == "__main__":
    main()
