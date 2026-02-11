# GitSensei – GitHub Repo Q&A

GitSensei is a Streamlit + LangChain app that lets you ask natural language questions about any public GitHub repository.  
It clones the repo, indexes Python files, and answers using Hugging Face 

---

Features
- Clone and analyze public GitHub repositories
- Index Python files with FAISS vector store
- Embed code using sentence-transformers
- Answer questions with Hugging Face models (Mistral, Llama, etc.)
- Streamlit UI for easy interaction

---

Installation

```bash
git clone https://github.com/your-username/gitsensei.git
cd gitsensei
pip install -r requirements.txt

