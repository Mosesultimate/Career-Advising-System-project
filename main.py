import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from supabase import create_client
import re
import base64
from langchain.llms import HuggingFaceHub
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"]="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"




def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()



def has_numbers(string):
    pattern = r'\d+'  # Matches one or more digits
    return bool(re.search(pattern, string))

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: 100vw 100vh;
    background-repeat: no-repeat
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)







def create_supabase_client(supabase_key,supabase_url):
    supabase=create_client(supabase_url,supabase_key)
    return supabase



def create_app(openai_api_key,supabase):

    st.title("Career-Advising System")
    st.header("What are your main strengths and skills?")
    skills=st.text_input("Skills")
    st.header("What is your academic background")
    academic_background=st.text_input("Academic Background")
    st.header("What are your areas of interest or passion?")
    interests=st.text_input("Interests")
    st.header("What are your long term goals")
    goals=st.text_input("Goals")
    st.header("What industries or sectors are you interested in exploring?")
    industry=st.text_input("Industry")
    submit=st.button("Recommend Career")
    if submit:
        if skills and interests  and goals  and industry  and academic_background :
            
            if has_numbers(skills) or has_numbers(interests) or has_numbers(industry) or has_numbers(academic_background) :
                st.write("Ensure All fields are strings and not numbers")

            else:

                prompt = PromptTemplate(input_variables=["interests","skills","goals","industry"], template="Recommend career for someone who {goals} goals,{skills} skills,{interests} interessts and prefers to work in {industry} industry and has {academic_background} as academic background.Mention just the career,do not explain")

                llm=OpenAI(temperature=0.9,openai_api_key=openai_api_key)
                #llm = HuggingFaceHub( repo_id="tiiuae/falcon-7b-instruct")
                llm_chain = LLMChain(prompt=prompt, llm=llm)
                variables={"interests":interests,"skills":skills,"goals":goals,"industry":industry,"academic_background":academic_background}
                response=llm_chain.run(variables)
                if response:
                    st.write(response)
                    data=supabase.table("career").insert({"skills":skills,"interests":interests,"goals":goals,"industry":industry,"academic_background":academic_background,"recommended_career":response})
                    if data:
                        print(data.execute())
        
           
                
        else:
            st.write("Please fill all fields ")




def main():
    openai_api_key="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"  
    SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNraG9iYnR5ZmpjaGdmemJnYW10Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTAwNzA2ODIsImV4cCI6MjAyNTY0NjY4Mn0.KwHdoe8b_4YzJeVFoJbEE38m-Cb3H6juBZDEbt5cdY4"
    SUPABASE_URL="https://ckhobbtyfjchgfzbgamt.supabase.co"  
    set_background('./Generative-AI-and-Usecases-in-different-sectors-1.jpg')
    supabase=create_supabase_client(SUPABASE_KEY,SUPABASE_URL)
    create_app(openai_api_key,supabase)



if __name__=="__main__":
    main()
