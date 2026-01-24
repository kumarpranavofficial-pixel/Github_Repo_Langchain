import os
import subprocess
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_openai import ChatOpenAI


load_dotenv()


rep_url = input("Enter GitHub repository URL: ").strip()
question = input("Ask a question about this repo: ").strip()

REPO_DIR = "repo"


if not os.path.exists(REPO_DIR):
    print("\nCloning repository...")
    subprocess.run(["git", "clone", rep_url, REPO_DIR], check=True)
else:
    print("\nRepository already exists. Using local copy.")


print("\nReading repository files...")

loader = DirectoryLoader(
    REPO_DIR,
    glob="**/*.py",
    loader_cls=TextLoader
)

documents = loader.load()
print(f"Loaded {len(documents)} files")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")


print("\nIndexing code...")
embeddings = FakeEmbeddings(size=768)
db = FAISS.from_documents(chunks, embeddings)


relevant_docs = db.similarity_search(question, k=5)

context = "\n\n".join(doc.page_content for doc in relevant_docs)


print("\nThinking...\n")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

prompt = f"""
You are a helpful assistant analyzing a GitHub repository.

Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}
"""

response = llm.invoke(prompt)

print("Answer:\n")
print(response.content)