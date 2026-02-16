from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from huggingface_hub import InferenceClient
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"


repo_dir = "Repo"

def q_n_a_repo(question: str) -> str:
    question = question.strip()

    if not question:
        raise ValueError("You did not enter any question")

    loader = DirectoryLoader(
        repo_dir,
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
    
    client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token="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"
)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(chunks, embeddings)

    relevant_docs = db.similarity_search(question, k=5)
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    print("\nThinking...\n")
    

    prompt = f"""
You are a helpful assistant analyzing a GitHub repository.
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}
"""
    print(prompt)
    response =  client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Ask a question about this repo: ").strip()
    answer = q_n_a_repo(question)
    print("\nAnswer:\n")
    print(answer)
