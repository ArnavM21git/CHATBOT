# Copilot Instructions for NoteBot ChatBot Project

## Scope
- This is a **Streamlit-based ChatBot** application using LangChain and Google Generative AI.
- Focus on enhancing PDF processing, Q&A capabilities, and user experience.
- Features include:
  - PDF text extraction and processing
  - Vector database integration with FAISS
  - Question-answering using Google Gemini AI
  - Streamlit web interface

## Technology Stack
- **Streamlit** for web interface
- **LangChain** for LLM orchestration
- **Google Generative AI (Gemini)** for embeddings and chat
- **FAISS** for vector storage
- **PyPDF2** for PDF processing

## Code Style
- Add **comments for complex LLM chains** and vector database operations
- Document API key usage and environment variables
- Keep code modular and easy to understand
- Use descriptive variable names for LangChain components

## Features to Implement
- PDF upload and text extraction
- Text chunking and embedding
- Similarity search and context retrieval
- Question answering with context
- Error handling for API calls
- Session state management
- Multiple file support
- Chat history

## Best Practices
- Always handle API key security properly
- Use environment variables for sensitive data
- Implement proper error handling for PDF processing
- Optimize chunk size and overlap parameters
- Test with various PDF formats and sizes
- Add user-friendly error messages

## Setup Instructions
- Include clear instructions for:
  - Installing required packages
  - Setting up Google AI API keys
  - Running the Streamlit app
  - Environment configuration
