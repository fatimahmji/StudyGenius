
import openai
import streamlit as st
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
import json
import time


load_dotenv()

openai.api_key = os.getenv("OPEN_API_KEY")

def extract_text_from_pdf(file):
    reader =PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
             text += content

    return text

def get_s(text, num_of_chapters):
    prompt = f"""
    act as a student and Generate a customized study schedule that distributes the workload evenly across the available time frame
    by analyzing the provided syllabus(Week Course Outline) based on the text delimted by four backquotes,
    and consider the user's preference for the number of chapters to study per day {num_of_chapters},
    Ensure that the study schedule covers all chapters/topics within the specified time period,
    Take into account any deadlines or milestones provided in the syllabus.
    each subject contains id, chapters.
    
    the text is : ````{text}````
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125", 
        messages=[{
            "role": "system", 
            "content": prompt,
            },],)
    
    return (response.choices[0].message.content)





def main(): 
    st.set_page_config(page_title="StudyGenius app",page_icon="🤖")
    st.title("StudyGenius")

    st.subheader('Unlock Your Academic Potential With :blue[StudyGenius]  app', divider='rainbow')
    st.write("This app generates personalized study schedule based on your syllabus, ensuring the most suitable plan for your academic success.")
    st.divider()


    with st.form(key="Upload_file"):
        uploaded_file= st.file_uploader("Upload a PDF file", type=["pdf"])
        num_of_chapters= st.number_input("how many chapters can you study in one day", min_value=1, max_value=10, value=3)



        submit_button= st.form_submit_button(label="Generate schedule", type="primary")


        if submit_button:
            if uploaded_file:
                text = extract_text_from_pdf(uploaded_file)
                st.write(get_s(text, num_of_chapters))
                #display_q(questions)
            else:
                st.error("Please upload a PDF file.")


    

if __name__ == "__main__":
    main()