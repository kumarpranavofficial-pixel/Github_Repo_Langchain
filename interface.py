import streamlit as st



st.set_page_config(page_title="GitSensei – GitHub Repo Q&A", page_icon="📦")

st.title("GitSensei – Ask Questions about any GitHub Repo")
st.write(
    "Enter a public GitHub repository URL and a natural language question. "
    "GitSensei will clone the repo (if needed), analyze the Python files"
)

repo_url = st.text_input(
    "GitHub repository URL",
    placeholder="https://github.com/owner/repo",
)

question = st.text_area(
    "Your question about the repository",
    placeholder="What does this project do? How is the main service structured?",
    height=150,
)

run_button = st.button("Ask GitSensei")

if run_button:
    if not repo_url or not question:
        st.warning("Please provide both a GitHub repository URL and a question.")
    else:
        with st.spinner("Analyzing repository and thinking with Llama 3.1 8B Instant..."):
            try:
                answer = answer_question_about_repo(repo_url, question)
                st.subheader("Answer")
                st.write(answer)
            except Exception as e:
                st.error("Something went wrong while analyzing the repository.")
                st.exception(e)

