import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI

import os


os.environ["OPENAI_API_KEY"] ="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"


st.title("Career-Advising System")
st.write("What are your main strengths and skills?")
skills=st.text_input("Skills")
st.write("What is your academic background")
academic_background=st.text_input("Academic Background")
st.write("What are your areas of interest or passion?")
interests=st.text_input("Interests")
st.write("What are your long term goals")
goals=st.text_input("Goals")
st.write("What industries or sectors are you interested in exploring?")
industry=st.text_input("Industry")
submit=st.button("Recommend Career")
if submit:
    if skills and interests and goals and industry and academic_background:
         prompt = PromptTemplate(input_variables=["interests","skills","goals","industry"], template="Recommend career for someone who {goals} goals,{skills} skills,{interests} interessts and prefers to work in {industry} industry and has {academic_background} as academic background.Mention just the career,do not explain")

         llm=OpenAI(temperature=0.9)
         llm_chain = LLMChain(prompt=prompt, llm=llm)
         variables={"interests":interests,"skills":skills,"goals":goals,"industry":industry,"academic_background":academic_background}
         response=llm_chain.run(variables)
         if response:
            st.write(response)
    else:
        st.write("Please fill all fields")
