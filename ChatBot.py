import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


# 1st part


st.set_page_config(page_title="NoteBot🤖", page_icon="🤖")
st.title("NoteBot 🤖")
st.caption("Your intelligent assistant for PDF documents.")

with st.sidebar:
    st.title("My Notes")
    st.write("Upload a PDF and click 'Process' to start chatting.")
    file=st.file_uploader("",type = "pdf")


if file is not None:
    # extracting text from pdf
    my_pdf=PdfReader(file)
    text=""
    for page in my_pdf.pages:
        text+=page.extract_text()

    #converting into small chunks i.e. tokens
    splitter=RecursiveCharacterTextSplitter(separators=[""],chunk_size=250,chunk_overlap=50)
    chunks=splitter.split_text(text) # outputs as list of chunks like chunk 1,chunk 2....
    #st.write(chunks)

    # converting and giving embedded vectors of our file chunks to vector database
    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GEMINI_API_KEY")) #object creation

    vector_store=FAISS.from_texts(chunks,embedder)#creates vector db
    # stores embedding vectors of given doc

# 2nd part
    question=st.text_input("Ask a Question")

    if question:
        matching_chunks_ie_doc_objs=vector_store.similarity_search(question)
        #internally converts query to embeding vectors and then fetches matching chunks...

        #defining llm
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),

            temperature=0,
            max_output_tokens=300
        )

        # generate response

        #template for prompt to be given to llm after context ie doc objs /chunks are added
        customized_prompt = ChatPromptTemplate.from_template(
            """ You are my assistant tutor. Answer the question based on the following context and
            if you did not get the context still answer by your intelligence :
            {context}
            Question: {input}
            """)


        chain = create_stuff_documents_chain(llm, customized_prompt)
        # Corrected line
        output = chain.invoke({"input": question, "context": matching_chunks_ie_doc_objs})
        st.write(output)






