
# HR Policy RAG Chatbot 🤖

An AI-powered HR Policy Chatbot built using Retrieval-Augmented Generation (RAG).

## Features
- PDF document text extraction
- Text chunking
- Vector storage using Pinecone
- Semantic search and retrieval
- Answer generation using Google Gemini
- Interactive chatbot interface using Streamlit

## Tech Stack
- Python
- Streamlit
- Pinecone
- Google Gemini
- RAG
- PyPDF

## Architecture

PDF → Text Extraction → Chunking → Vector Storage
→ Similarity Search → Gemini → Chatbot Response

## Installation

1. Clone the repository:

   git clone YOUR_REPOSITORY_URL

2. Install dependencies:

   pip install -r requirements.txt

3. Create a `.env` file and add:

   GEMINI_API_KEY=your_gemini_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=your_index_name

4. Run the application:

   streamlit run app.py

## Note
API keys are not included in this repository.
