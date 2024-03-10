import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from supabase import create_client


import base64
import streamlit as st


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background('./careers.jpg')

SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNraG9iYnR5ZmpjaGdmemJnYW10Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTAwNzA2ODIsImV4cCI6MjAyNTY0NjY4Mn0.KwHdoe8b_4YzJeVFoJbEE38m-Cb3H6juBZDEbt5cdY4"
SUPABASE_URL="https://ckhobbtyfjchgfzbgamt.supabase.co"
supabase=create_client(SUPABASE_URL,SUPABASE_KEY)

data=supabase.table("career").select("*").execute()
print(data)

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

         llm=OpenAI(temperature=0.9,openai_api_key="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")
         llm_chain = LLMChain(prompt=prompt, llm=llm)
         variables={"interests":interests,"skills":skills,"goals":goals,"industry":industry,"academic_background":academic_background}
         response=llm_chain.run(variables)
         if response:
            st.write(response)
            data=supabase.table("career").insert({"skills":skills,"interests":interests,"goals":goals,"industry":industry,"academic_background":academic_background,"recommended_career":response})
            if data:
                print(data.execute())
    else:
        st.write("Please fill all fields")





