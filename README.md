# 🇱🇰 Sri Lankan SME Business Advisor (Agentic AI)

An enterprise-grade Agentic AI application providing Sri Lankan SMEs with regulatory, tax, and financial advisory services grounded in official Sri Lankan frameworks.

## Agentic Architecture
1. **Orchestrator Agent**: Categorizes intent into domain buckets (`TAX`, `LOANS`, `REGISTRATION`).
2. **RAG Search Agent**: Retrieves grounded legal clauses from local ChromaDB vector store.
3. **Financial Advisor**: Performs two-pass reflection & self-critique over tax/loan rules.
4. **Report Generator**: Synthesizes intermediate findings into a professional Markdown report.

## Method 1: Auto-Ingestion
This application utilizes a clean Git architecture. Raw PDF documents are stored in `data/sme_docs/`. Upon the initial boot of the Streamlit application, the system automatically ingests, chunks, and creates vector embeddings, storing them in a local `.chroma_db` index that is safely excluded from version control.