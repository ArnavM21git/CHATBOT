# NoteBot - PDF Question Answering ChatBot

[![Deployed on Streamlit](https://img.shields.io/badge/Deployed%20on-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://chatbot-sjdm6apoxgqrrakwvbt4zi.streamlit.app)
[![View on Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-sjdm6apoxgqrrakwvbt4zi.streamlit.app)

A Streamlit-based chatbot that allows you to upload PDF documents and ask questions about their content using Google's Gemini AI.

## 🚀 Live Demo

Try the live app here: **[NoteBot on Streamlit Cloud](https://chatbot-sjdm6apoxgqrrakwvbt4zi.streamlit.app)**

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

1. Clone the repository:
```bash
git clone https://github.com/ArnavM21git/CHATBOT.git
cd CHATBOT
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
.\venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate
```

3. Install required packages from requirements.txt:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
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
- **Embedding Model**: models/embedding-001
- **Vector Database**: FAISS

## Deployment on Streamlit Cloud

This app is deployed on Streamlit Cloud. To deploy your own version:

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your forked repository
5. Add your `GEMINI_API_KEY` in the Secrets section (Settings → Secrets):
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
6. Click Deploy!

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 ArnavM21git

---

**Made with ❤️ using Streamlit and Google Gemini AI**
