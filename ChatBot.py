import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings#OpenAIEmbeddings is a class
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
# 1st part
OpenAI_API_Key= "sk-proj-z8fcSSSEuixrmg7q_EOxlS0aKcRZB8ecnIxw-_LBi8LDjqHGqeRzoIOmsGYZ6WoYFY9M2UaAE2T3BlbkFJwNZ9V0MLRBh4n6zHuyq4zqgDdxt3D7HmhKvzxGaWDNYNTR6YWoF-P3n3Kq4HbyMPfvc6ckin8Ass\""

st.title("NoteBot")

with st.sidebar:
    st.title("My Notes")
    file=st.file_uploader("UPLOAD REFERENCE PDF",type = "pdf")


if file is not None:
    # extracting text from pdf
    my_pdf=PdfReader(file)
    text=""
    for page in my_pdf.pages:
        text+=page.extract_text()

    #converting into small chunks i.e. tokens
    splitter=RecursiveCharacterTextSplitter(separators=[""],chunk_size=250,chunk_overlap=50)
    chunks=splitter.split_text(text) # outputs as list of chunks like chunk 1,chunk 2....

    # converting and giving embedded vectors of our file chunks to vector database
    embedder=OpenAIEmbeddings(api_key=OpenAI_API_Key) #object creation

    vector_store=FAISS.from_texts(chunks,embedder)

# 2nd part


