import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Import session management modules
from session_manager import SessionManager


# Initialize session manager (singleton pattern)
@st.cache_resource
def get_session_manager():
    """Create or retrieve session manager instance."""
    return SessionManager()


# 1st part - Page Configuration and Session Initialization

# 1st part - Page Configuration and Session Initialization

st.set_page_config(page_title="NoteBot🤖", page_icon="🤖")

# Initialize session manager
session_mgr = get_session_manager()

st.title("NoteBot 🤖")
st.caption("Your intelligent assistant for PDF documents with conversation memory.")

# Sidebar with chat history
with st.sidebar:
    st.title("💬 Chat History")
    
    # Display session status
    status = session_mgr.get_session_status()
    
    # Status indicators with enhanced details
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", status['message_count'], 
                 delta=f"{status['message_count'] // 2} pairs" if status['message_count'] > 0 else None)
    with col2:
        if status['storage_status'] == 'active':
            st.success("✓ Saved", icon="💾")
        elif status['storage_status'] == 'degraded':
            st.warning("⚠ Degraded", icon="⚠")
        else:
            st.error("✗ Not Saved", icon="❌")
    
    # Document status
    if status['document_loaded']:
        doc_name = session_mgr.get_document_name()
        st.info(f"📄 {doc_name}")
        if status['vector_store_ready']:
            st.success("✓ Ready for questions", icon="✅")
    else:
        st.warning("No document loaded", icon="📄")
    
    st.divider()
    
    # Display chat history
    chat_history = session_mgr.chat_manager.get_chat_history()
    
    if chat_history:
        # Show warning if approaching limit
        if len(chat_history) >= 40:
            st.warning(f"⚠ Approaching message limit ({len(chat_history)}/50)", icon="⚠")
        
        for msg in chat_history:
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            role_label = "You" if msg['role'] == 'user' else "NoteBot"
            
            # Format timestamp (more readable)
            timestamp = msg['timestamp'][:16].replace('T', ' ')
            
            with st.expander(f"{role_icon} {role_label} - {timestamp}", expanded=False):
                st.write(msg['content'])
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear History", use_container_width=True):
                session_mgr.chat_manager.clear_history()
                st.rerun()
        with col2:
            # Future: Export button placeholder
            st.button("💾 Export", use_container_width=True, disabled=True, 
                     help="Export feature coming soon!")
    else:
        st.info("No messages yet. Upload a PDF and start chatting!")
    
    st.divider()
    
    # Debug mode toggle
    show_debug = st.checkbox("🔍 Debug Mode", value=False)
    if show_debug:
        with st.expander("Debug Information", expanded=True):
            st.caption(f"**Session ID:** {status['session_id']}")
            st.caption(f"**Storage Status:** {status['storage_status']}")
            st.caption(f"**Vector Store:** {'Ready' if status['vector_store_ready'] else 'Not Ready'}")
            st.caption(f"**Message Count:** {status['message_count']}")
    else:
        st.caption(f"Session: {status['session_id'][:12]}...")


# Main content area
with st.container():
    st.header("📄 Document Upload")
    file = st.file_uploader("Upload a PDF to start chatting", type="pdf")


if file is not None:
    # Handle new document upload - clear history if different document
    current_doc = session_mgr.get_document_name()
    if current_doc != file.name:
        session_mgr.handle_new_document_upload(file.name, file.size)
        st.success(f"✅ New document '{file.name}' uploaded! Previous chat history cleared.")
    
    # extracting text from pdf
    my_pdf = PdfReader(file)
    text = ""
    for page in my_pdf.pages:
        text += page.extract_text()

    # converting into small chunks i.e. tokens
    splitter = RecursiveCharacterTextSplitter(
        separators=[""],
        chunk_size=250,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)  # outputs as list of chunks

    # converting and giving embedded vectors of our file chunks to vector database
    embedder = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    vector_store = FAISS.from_texts(chunks, embedder)
    
    # Mark vector store as ready
    session_mgr.mark_vector_store_ready()
    
    # Store vector store in session state for reuse
    st.session_state.vector_store = vector_store

    
    # 2nd part - Chat Interface
    st.header("💬 Chat Interface")
    
    # Get conversation context for contextual responses
    conversation_context = session_mgr.chat_manager.get_conversation_context(last_n=5)
    
    # Message input
    question = st.text_input("Ask a question about the document:")

    if question:
        # Add user message to chat history
        session_mgr.chat_manager.add_message("user", question)
        
        # Retrieve vector store from session state
        vector_store = st.session_state.get('vector_store')
        
        if vector_store:
            # Get conversation context first
            conversation_context = session_mgr.chat_manager.get_conversation_context(last_n=5)
            
            # Get matching chunks from vector store
            matching_chunks_ie_doc_objs = vector_store.similarity_search(question)

            # defining llm
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0,
                max_output_tokens=300
            )

            # Build conversation history for context
            conversation_history = ""
            if conversation_context['recent_exchanges']:
                conversation_history = "\n\nPrevious conversation:\n"
                for exchange in conversation_context['recent_exchanges'][-3:]:  # Last 3 exchanges
                    conversation_history += f"User: {exchange['user']}\n"
                    conversation_history += f"Assistant: {exchange['assistant']}\n"

            # Enhanced template with conversation context
            customized_prompt = ChatPromptTemplate.from_template(
                """You are my assistant tutor. Answer the question based on the following context.
                If the user refers to previous parts of our conversation, use the conversation history below.
                
                Context from document:
                {context}
                """ + conversation_history + """
                
                Current Question: {input}
                
                Please provide a helpful answer. If this is a follow-up question, acknowledge the previous context.
                """)

            chain = create_stuff_documents_chain(llm, customized_prompt)
            
            # generate response
            try:
                output = chain.invoke({"input": question, "context": matching_chunks_ie_doc_objs})
                
                # LangChain returns the response directly as a string
                # Validate output before adding to chat history
                if output:
                    output_str = str(output).strip()
                    if output_str:
                        # Add AI response to chat history
                        session_mgr.chat_manager.add_message("assistant", output_str)
                        
                        # Display the response
                        st.markdown("### 🤖 NoteBot's Response:")
                        st.write(output_str)
                    else:
                        st.error("❌ Empty response received. Please try rephrasing your question.")
                        # Remove the user message if response failed
                        if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'user':
                            st.session_state.chat_history.pop()
                else:
                    st.error("❌ Failed to generate a response. Please try again.")
                    # Remove the user message if response failed
                    if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'user':
                        st.session_state.chat_history.pop()
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                # Remove the user message if response failed
                if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'user':
                    st.session_state.chat_history.pop()
            
            # Show context info
            with st.expander("ℹ️ Context Info"):
                st.write(f"**Messages in conversation:** {conversation_context['total_messages']}")
                st.write(f"**Recent exchanges used:** {len(conversation_context['recent_exchanges'])}")
                if conversation_context['conversation_summary']:
                    st.write(f"**Summary:** {conversation_context['conversation_summary']}")
        else:
            st.error("❌ Vector store not ready. Please wait for document processing to complete.")
else:
    st.info("👆 Please upload a PDF document to start chatting!")






