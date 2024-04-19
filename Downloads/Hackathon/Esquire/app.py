import os
import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from llama_index.indices.managed.vectara import VectaraIndex
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core.readers import SimpleDirectoryReader
from vectara import Searching


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
        
        
    if st.button("Search"):
        with st.spinner("Searching..."):
            texts = searcher.send_query(
                corpus_id=int(os.getenv('VECTARA_CORPUS_ID')),
                query_text=query_text,
                num_results=2,
                summarizer_prompt_name="vectara-summary-ext-v1.3.0",
                response_lang='en',
            
                max_summarized_results=5  
                
                
            )
            st.write(texts)
  


    
    #remember to change to response
    
    
        
        
        
        


