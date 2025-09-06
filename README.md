# ChatPDF – Conversational PDF Question Answering

ChatPDF is an AI-powered application that allows users to upload a PDF document and interact with it conversationally.  
It uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on the uploaded content, with a simple and interactive Streamlit frontend.

---

## Features
- Upload any PDF document.  
- Ask unlimited questions related to the document.  
- Retrieves the most relevant content using embeddings.  
- Uses LLMs to generate human-like answers grounded in the PDF.  
- Built with Streamlit for a smooth user interface.  

---

## Tech Stack
- Python  
- LangChain – for RAG pipeline (document loaders, embeddings, retrievers)  
- FAISS – vector database for efficient similarity search  
- OpenAI / LLMs – for generating answers  
- Streamlit – frontend web interface  

---

## Project Structure
app.py # Main Streamlit application entrypoint
├── function_chatbot_pdf.py # Core logic for PDF processing, embeddings, and QA
├── requirements.txt # Python dependencies
└── README.md 
