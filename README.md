# ResumeParserAI

ResumeParserAI is an intelligent resume parsing and retrieval system that uses **LLMs**, **OCR models**, and **vector embeddings** to process and search for ideal candidates based on user prompts. The system features a **FastAPI** backend, **React.js** frontend, **PostgreSQL** for structured data, and a **Vector DB** for semantic search.

## 🚀 Key Features

- **LLM-Powered Resume Parsing**: Parses resumes using **GPT + Pumice (pumdf)** and **Mistral OCR**, extracting structured data (name, skills, experience, etc.) from raw PDFs.
- **Vectorization & Embedding**: Extracted content is converted to embeddings using **OpenAI/GPT embedding models**, and stored in a **Vector DB** (e.g., Chroma/Weaviate/Pinecone).
- **Prompt-Based Candidate Search**: Users can enter a prompt describing their ideal candidate, and the system performs **semantic similarity search** using cosine similarity + keyword overlap.
- **Frontend Search Interface**: Built using React.js, allowing users to upload PDFs and search for matching candidates via prompt queries.
- **PostgreSQL Storage**: Structured metadata (e.g. candidate name, email, experience) is stored in PostgreSQL for relational queries.
- **Performance Comparison**: Compared **Mistral OCR** vs **GPT + Pumice** on accuracy, extraction time, and consistency across various resume formats.

## 🧱 Tech Stack

- **Backend**: FastAPI, Python, PyPDF2, LangChain, GPT APIs, Mistral OCR
- **Frontend**: React.js, Axios
- **Database**: PostgreSQL + Vector DB (Chroma/Pinecone)
- **DevOps**: Docker, GitHub Actions
- **Embedding Models**: OpenAI (text-embedding-ada-002) / GPT-4

## ⚙️ Setup & Installation

### 🐳 Prerequisites
- Python 3.9+
- Node.js + npm
- Docker
- PostgreSQL
- Vector DB (Chroma, Weaviate, or Pinecone)

### 🛠️ Backend Setup

```bash
git clone https://github.com/yourusername/resume-parser-ai.git
cd resume-parser-ai/backend
uvicorn main:app --reload
```

### 💻 Frontend Setup

```bash
cd ../frontend
npm start
```


## 📈 Pipeline Overview

1. **Resume Upload** (Frontend)
2. **Text Extraction** (Mistral OCR / GPT + Pumice)
3. **Data Parsing** (Extract name, email, skills, etc.)
4. **Vectorization** using GPT embeddings
5. **Store** vector in Vector DB, metadata in PostgreSQL
6. **Query Interface**: Accepts prompt input (e.g., “5+ years React developer with ML background”)
7. **Search & Scoring**: Performs cosine similarity + keyword relevance
8. **Result Display**: Returns top matching candidates to the user

## 🧪 Benchmark: Mistral OCR vs GPT + Pumice

| Method              | Accuracy | Extraction Time (Avg) | Strengths                  |
|---------------------|----------|------------------------|----------------------------|
| GPT + Pumice        | 92%      | ~1.6s per resume       | Context-aware parsing, clean JSON output |
| Mistral OCR         | 83%      | ~0.9s per resume       | Faster on raw scanned PDFs |

> GPT + Pumice yielded higher accuracy for clean PDF resumes with rich text, while Mistral was better suited for low-quality or scanned documents.

## 📊 Real-World Use Case

This system is ideal for **HR recruiters**, **job portals**, and **internal hiring tools**, allowing them to semantically search large pools of resumes using natural language rather than boolean keyword filters.

## ✨ Future Enhancements

- Multi-language resume support  
- Fine-tuning a custom LLM for better entity extraction  
- Admin dashboard for batch uploads and analytics  
- Integration with job portals and email parsing

## 🙏 Acknowledgments

- OpenAI GPT  
- Mistral AI  
- FastAPI  
- Pumice  
- LangChain  
- Chroma / Pinecone  
- PostgreSQL
