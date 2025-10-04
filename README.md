# NoteBot - PDF Question Answering ChatBot

A Streamlit-based chatbot that allows you to upload PDF documents and ask questions about their content using Google's Gemini AI.

## Features

- 📄 Upload and process PDF documents
- 🤖 Ask questions about your PDF content
- 🔍 Semantic search using FAISS vector database
- ✨ Powered by Google Gemini AI
- 💬 Intelligent context-aware responses

## Prerequisites

- Python 3.8+
- Google AI API Key (Gemini)

## Installation

1. Clone the repository or download the files

2. Install required packages:
```bash
pip install streamlit PyPDF2 langchain langchain-openai langchain-google-genai langchain-community faiss-cpu
```

3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your Google AI API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit app:
```bash
streamlit run ChatBot.py
```

2. Upload a PDF file using the sidebar

3. Ask questions about the PDF content in the text input

4. Get AI-powered answers based on the document context

## How It Works

1. **PDF Processing**: Extracts text from uploaded PDF files
2. **Text Chunking**: Splits text into manageable chunks for processing
3. **Embedding**: Converts text chunks into vector embeddings
4. **Vector Storage**: Stores embeddings in FAISS vector database
5. **Similarity Search**: Finds relevant chunks based on user questions
6. **Answer Generation**: Uses Gemini AI to generate contextual answers

## Configuration

- **Chunk Size**: 250 characters (adjustable in code)
- **Chunk Overlap**: 50 characters
- **Model**: Gemini 2.5 Flash
- **Max Output Tokens**: 300

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your license here]
