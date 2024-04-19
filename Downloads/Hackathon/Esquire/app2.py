import os
import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from llama_index.indices.managed.vectara import VectaraIndex
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core.readers import SimpleDirectoryReader
from vectara import Searching

from llama_index.core import PromptTemplate


import getpass
import openai






load_dotenv()
openai.api_key =  os.getenv('OPENAI_API_KEY')

  



searcher = Searching()
index = VectaraIndex()

st.set_page_config(
    page_title= "Esquire: The Nigerian Legal Counsellor",
    layout = "centered",
    initial_sidebar_state= "auto",
   
    
)

custom_html = """
<div class = "banner">
<img src = "https://img.freepik.com/premium-photo/wide-banner-with-many-random-square-hexagons-charcoal-dark-black-color_105589-1820.jpg" alt = "Banner Image">
</div>
<style>
   .banner {
        width: 160%;
       height: 200px;
       overflow:hidden;
   }
   .banner img {
       width: 100%;
       object-fit: cover;
   }
   </style>
   """
   
st.components.v1.html(custom_html)





st.title("Esquire: The Nigerian Legal Counsel")


load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo", temperature=0)



def extract_file_content(file_path):
    
    

    pdf_reader = PdfReader(file_path)
    
    documents_content = ""
    for page in pdf_reader.pages:
        documents_content += page.extract_text()
    
    return documents_content


with st.sidebar:
    st.info("")


with st.expander("Ask the Ai Esquire", expanded = True):
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Enter the legal brief", type = ["txt", "pdf", "doc", "docx"])
    with col2:
        query_text = st.text_input("Give me a brief", key= 'query_text')
        
    
    query = ""
        
    if uploaded_file is not None:
       
        file_text = extract_file_content(uploaded_file)
        query.join(file_text)
        if query_text is not None:
            query.join(query_text)
            
    else:
        query.join(query_text)
        
    text_qa_template_str = (
    "Context information is"
    " below.\n---------------------\n{context_str}\n---------------------\nUsing"
    " both the context information and also using your own knowledge, answer"
    " the question: {query_str}\nIf the context isn't helpful, you can also"
    " answer the question on your own.\n"
                )
    text_qa_template = PromptTemplate(text_qa_template_str)

    refine_template_str = (
    "The original question is as follows: {query_str}\nWe have provided an"
    " existing answer: {existing_answer}\nWe have the opportunity to refine"
    " the existing answer (only if needed) with some more context"
    " below.\n------------\n{context_msg}\n------------\nUsing both the new"
    " context and your own knowledge, update or repeat the existing answer.\n"  
                    )
    refine_template = PromptTemplate(refine_template_str)
        
    
        
        
    if st.button("Search"):
        with st.spinner("Searching..."):
           query_engine = index.as_query_engine(
    similarity_top_k=5,
    summary_enabled=False,
    vectara_query_mode="mmr",
    mmr_k=50,
    mmr_diversity_bias=0.5)
           
        response = query_engine.query(query)
            
        st.markdown(response)
        

            
  


    
    #remember to change to response
    
    
        
        
        
        


