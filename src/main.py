import fnmatch
import os

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

from github_utils import fetch_mdx_contents, get_files_from_github_repo
from retriever_utils import get_chroma_db, get_source_chunks


def main():
    print("Starting...")
    print("Loading environment variables...")
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKENS")
    EXIT_COMMAND = "exit"
    REPO_OWNER = "RasaHQ"
    REPO_NAME = "rasa"
    CHROMA_DB_PATH = f"./chroma/{os.path.basename(REPO_NAME)}"
    DOCS_MDX_PATH = "src/all_mdx_contents.pkl"

    repo_files = get_files_from_github_repo(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
    mdx_files = [
        file
        for file in repo_files
        if file["type"] == "blob" and fnmatch.fnmatch(file["path"], "*.mdx")
    ]
    mdx_contents = fetch_mdx_contents(mdx_files, wait_for_renewal=False)

    if len(mdx_contents) < len(mdx_files):
        print()
        print(
            f"Warning: {len(mdx_contents)} of {len(mdx_files)} files were downloaded."
        )
        print(f"Please check your Github API rate limit.")
        print(f"Using old mdx files from disk.")

        import pickle

        with open(DOCS_MDX_PATH, "rb") as f:
            mdx_contents = pickle.load(f)
        print(f"Loaded {len(mdx_contents)} mdx files from disk.")

    source_chunks = get_source_chunks(mdx_contents)
    embedding_model = OpenAIEmbeddings()
    chroma_db = get_chroma_db(CHROMA_DB_PATH, source_chunks, embedding_model)

    qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    qa = RetrievalQA(
        combine_documents_chain=qa_chain, retriever=chroma_db.as_retriever()
    )
    input_text = f"Enter the question (If you want to exit, enter '{EXIT_COMMAND}')"
    while True:
        print()
        print(input_text)
        question = input(">>> ")
        if question == EXIT_COMMAND:
            break
        res = qa.run(question)
        print(res)


if __name__ == "__main__":
    main()
