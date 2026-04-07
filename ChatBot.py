import streamlit as st
import os
from importlib import import_module
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

try:
    create_stuff_documents_chain = import_module("langchain.chains.combine_documents").create_stuff_documents_chain
except ModuleNotFoundError:
    create_stuff_documents_chain = import_module("langchain_classic.chains.combine_documents").create_stuff_documents_chain


def get_gemini_api_key():
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY")
        if secret_key:
            return secret_key
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


# 1st part


st.set_page_config(page_title="NoteBot🤖", page_icon="🤖")
st.title("NoteBot 🤖")
st.caption("Your intelligent assistant for PDF documents.")

with st.sidebar:
    st.title("My Notes")
    st.write("Upload a PDF and click 'Process' to start chatting.")
    file=st.file_uploader("Upload a PDF", type="pdf", label_visibility="collapsed")


api_key = get_gemini_api_key()
if not api_key:
    st.error("Set GEMINI_API_KEY in Streamlit Secrets or your local environment before uploading a PDF.")
    st.stop()


if file is not None:
    # extracting text from pdf
    my_pdf=PdfReader(file)
    text=""
    for page in my_pdf.pages:
        text += page.extract_text() or ""

    #converting into small chunks i.e. tokens
    splitter=RecursiveCharacterTextSplitter(separators=[""],chunk_size=250,chunk_overlap=50)
    chunks=splitter.split_text(text) # outputs as list of chunks like chunk 1,chunk 2....
    #st.write(chunks)


    #converting and giving embedded vectors of our file chunks to vector database
    embedder = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=api_key) #object creation

    vector_store=FAISS.from_texts(chunks,embedder)#creates vector db by faiss class object and
    # stores embedding vectors of given doc

# 2nd part
    question=st.text_input("Ask a Question")

    if question:
        matching_chunks_ie_doc_objs=vector_store.similarity_search(question)
        #internally converts query to embeding vectors and then fetches matching chunks...

        #defining llm
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=api_key,

            temperature=0,
            max_output_tokens=300
        )


        

        #template for prompt to be given to llm after context ie doc objs /chunks are added
        customized_prompt = ChatPromptTemplate.from_template(
            """ You are my assistant tutor. Answer the question based on the following context and
            if you did not get the context still answer by your intelligence :
            {context}
            Question: {input}
            """)


        chain = create_stuff_documents_chain(llm, customized_prompt)
        
        # generate response
        output = chain.invoke({"input": question, "context": matching_chunks_ie_doc_objs})
        st.write(output)






