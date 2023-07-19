import fnmatch
import os

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings

from github_utils import (
    fetch_mdx_contents,
    get_files_from_github_repo,
    load_mdx_contents,
    save_mdx_content,
)
from retriever_utils import (
    get_chroma_db,
    get_source_chunks,
    ask_question,
    chain_type_kwargs,
)
from langchain.chat_models import ChatOpenAI
import argparse


def input_loop(qa, exit_command="exit"):
    input_text = f"Enter the question (If you want to exit, enter '{exit_command}')"
    while True:
        print()
        print(input_text)
        question = input(">>> ")
        if question == exit_command:
            break
        # res = qa.run(question)
        res = ask_question(question, qa)
        print(res)


def get_arguments(args):
    if not args.load_from_env:
        github_token = args.github_token
        openai_api_key = args.openai_api_key
    else:
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        openai_api_key = os.getenv("OPENAI_API_KEY")
    wait_for_renewal = args.wait_for_renewal
    version = args.version
    return github_token, openai_api_key, wait_for_renewal, version


def get_mdx_contents(repo_files, mdx_path, wait_for_renewal=False):
    mdx_files = [
        file
        for file in repo_files
        if file["type"] == "blob" and fnmatch.fnmatch(file["path"], "*.mdx")
    ]
    mdx_contents = fetch_mdx_contents(mdx_files, wait_for_renewal=wait_for_renewal)

    if len(mdx_contents) < len(mdx_files):
        print()
        print(
            f"Warning: {len(mdx_contents)} of {len(mdx_files)} files were downloaded."
        )
        print(f"Please check your Github API rate limit.")
        mdx_contents = load_mdx_contents(mdx_path)
        print(f"Loaded {len(mdx_contents)} mdx files from disk.")
    elif len(mdx_contents) == len(mdx_files):
        save_mdx_content(mdx_path, mdx_contents)
        print(f"Saved {len(mdx_contents)} mdx files to disk.")

    return mdx_contents


def main(args):
    print("Starting...")
    print("Loading environment variables...")

    github_token, openai_api_key, wait_for_renewal, version = get_arguments(args)
    os.environ["OPENAI_API_KEY"] = openai_api_key

    REPO_OWNER = "RasaHQ"
    REPO_NAME = "rasa"
    EXIT_COMMAND = "exit"

    version_path = version.replace(".", "_")
    DOCS_MDX_PATH = f"docs_cache/mdx_{version_path}.pkl"
    CHROMA_DB_PATH = f"./chroma/{REPO_NAME}/{version_path}"

    repo_files = get_files_from_github_repo(REPO_OWNER, REPO_NAME, github_token)
    mdx_contents = get_mdx_contents(repo_files, DOCS_MDX_PATH, wait_for_renewal)
    source_chunks = get_source_chunks(mdx_contents)

    embedding_model = OpenAIEmbeddings()
    chroma_db = get_chroma_db(CHROMA_DB_PATH, source_chunks, embedding_model)

    qa = RetrievalQA.from_chain_type(
        chain_type="stuff",
        retriever=chroma_db.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        llm=ChatOpenAI(),
    )
    input_loop(qa, exit_command=EXIT_COMMAND)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--load_from_env", type=bool, default=False, help="Load environment variables"
    )
    argparser.add_argument(
        "--github_token", type=str, default=None, help="Github token"
    )
    argparser.add_argument(
        "--openai_api_key", type=str, default=None, help="OpenAI API key"
    )
    argparser.add_argument(
        "--wait_for_renewal", type=bool, default=False, help="Wait for token renewal"
    )
    argparser.add_argument("--version", type=str, default="main", help="Github tag")

    args = argparser.parse_args()
    main(args)
