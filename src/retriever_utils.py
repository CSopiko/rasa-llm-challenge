import os

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate


def get_source_chunks(mdx_contents):
    source_chunks = []
    splitter = CharacterTextSplitter(separator="\n", chunk_size=2048, chunk_overlap=0)

    for source in mdx_contents:
        for chunk in splitter.split_text(source.page_content):
            source_chunks.append(Document(page_content=chunk, metadata=source.metadata))

    return source_chunks


def get_chroma_db(chromadb_path, source_chunks, embedding_model):
    if not os.path.exists(chromadb_path):
        print(f"Creating new chroma db at {chromadb_path}")
        chroma = Chroma.from_documents(
            source_chunks, embedding_model, persist_directory=chromadb_path
        )
        chroma.persist()
    else:
        print(f"Loading chroma db from {chromadb_path}")
        chroma = Chroma(persist_directory=chromadb_path)
    return chroma


prompt_template = """
You should act like Rasa (open source framework for building conversational ai) assistant, 
who is well known with the documentation.
You must be helpful and answer the questions of the user with the help of the documentation.
Provide code snippets and links to the documentation if needed.
Do not mention context and reply as human would write.

Context: {context} 

Question: {question}
Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
