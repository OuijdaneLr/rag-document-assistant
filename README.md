# RAG Document Assistant

A document question-answering assistant built with Python, ChromaDB and Ollama.

## Project Overview

This project extracts text from PDF documents, splits the text into smaller chunks, stores them in a ChromaDB database, and retrieves relevant passages to answer questions.

## Features

- Extract text from PDF documents.
- Split text into smaller chunks.
- Store document chunks in ChromaDB.
- Search for relevant passages using semantic search.
- Run a local language model with Ollama.

## Technologies

- Python
- PyMuPDF
- ChromaDB
- Ollama
- Llama 3.2

## Project Structure

```text
rag-document-assistant/
├── data/               # PDF documents (local only)
├── chroma_db/          # Local vector database
├── importer_pdf.py     # Extract and store PDF chunks
├── recherche.py        # Search relevant passages
├── test_pdf.py         # Test PDF text extraction
├── tester_ollama.py    # Test Ollama connection
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/OuijdaneLr/rag-document-assistant.git
cd rag-document-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

Install the required Python libraries:

```bash
pip install pymupdf chromadb ollama
```

### 4. Install Ollama

Download Ollama from https://ollama.com/download/windows.

Then download the model:

```bash
ollama run llama3.2
```

### 5. Add a PDF document

Place your PDF file in the `data/` folder and name it `document.pdf`.

### 6. Import the PDF

```bash
python importer_pdf.py
```

### 7. Search the document

```bash
python recherche.py
```

## Current Status

The project currently supports PDF text extraction, chunking, vector storage and semantic search. Integration of retrieved passages with the language model for complete answers is in progress.

## Author

OuijdaneLr