# 🏔️ SikkimRAG

### AI-Powered Sikkim Travel Assistant using RAG

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![RAG](https://img.shields.io/badge/AI-RAG-purple)
![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-red)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 📌 Overview

**SikkimRAG** is an AI-powered travel information system developed as an **MCA academic project** using **Retrieval-Augmented Generation (RAG)**.

It retrieves relevant information from a Sikkim travel guide using **semantic search and Qdrant Vector Database**, then uses an LLM to generate context-aware answers.

---

## 🎯 Objectives

* Build a domain-specific AI travel assistant.
* Implement a complete RAG pipeline.
* Extract and process PDF travel information.
* Generate text embeddings.
* Store and retrieve information using Qdrant.
* Integrate an LLM for answer generation.

---

## 🏗️ Architecture

```text
Sikkim Travel PDF
       ↓
PDF Extraction
       ↓
Text Chunking
       ↓
Embeddings
       ↓
Qdrant Vector DB
       ↓
User Query
       ↓
Semantic Retrieval
       ↓
Relevant Context
       ↓
LLM
       ↓
AI Response
```

---

## 🛠️ Tech Stack

| Technology            | Purpose         |
| --------------------- | --------------- |
| Python                | Development     |
| PyPDF                 | PDF extraction  |
| Sentence Transformers | Embeddings      |
| all-MiniLM-L6-v2      | Embedding model |
| Qdrant                | Vector database |
| Nugen                 | LLM integration |
| Git & GitHub          | Version control |

---

## 📂 Project Structure

```text
sikkim-rag/
├── app/
├── data/
│   └── Sikkim_Travel_Guide.pdf
├── scripts/
│   ├── test_pdf.py
│   ├── chunk_pdf.py
│   ├── ingest.py
│   ├── query.py
│   └── check_nugen.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 RAG Workflow

1. Extract text from the Sikkim travel PDF.
2. Split the document into smaller chunks.
3. Generate embeddings using `all-MiniLM-L6-v2`.
4. Store embeddings in Qdrant.
5. Convert the user's query into an embedding.
6. Retrieve relevant document chunks.
7. Pass the retrieved context to the LLM.
8. Generate the final response.

---

## 💬 Example Queries

```text
What are the best places to visit in Sikkim?

What is the best time to visit Sikkim?

How can I plan a 3-day Sikkim trip?

What are the major tourist attractions?
```

---

## ✅ Current Status

* ✅ PDF Extraction
* ✅ Text Chunking
* ✅ Embeddings
* ✅ Qdrant Ingestion
* ✅ Semantic Retrieval
* ✅ Nugen Authentication
* 🔄 LLM Generation
* 🔮 Web Interface

---

## 🚀 Future Scope

* AI chatbot interface
* Personalized itineraries
* Budget-based trip planning
* Interactive maps
* Weather integration
* Travel recommendations

---

## 🎓 Academic Project

**Program:** Master of Computer Applications (MCA)

**Domain:** Artificial Intelligence / Generative AI / NLP

**Author:** **Prasad Kamble**

GitHub: https://github.com/prasad-kamble330

---

⭐ **SikkimRAG — Making travel information smarter with RAG.**
