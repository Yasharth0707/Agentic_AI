#this file will handle the indexing phase of the RAG pipeline. It will take in a list of documents and create embeddings for them using the OpenAI API. The embeddings will then be stored in a vector database (Qdrant) for later retrieval.
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

pdf_path=Path(__file__).parent / "nodejs.pdf"

#Load this file in python program
loader=PyPDFLoader(file_path=pdf_path)
docs=loader.load()

#Split the docs into smaller chunks
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# When you split a long document, if you cut it off rigidly at a specific character limit (e.g., exactly every 500 characters), you risk splitting a sentence, a thought, or an important relationship right down the middle. This can cause the retrieval system to lose crucial context.

# By introducing an overlap, the end of one chunk is repeated at the beginning of the next chunk. This ensures that semantic continuity and context are preserved across boundaries.
chunks=text_splitter.split_documents(documents=docs)

#Vector Embeddings
embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("Indexing completed. The documents have been embedded and stored in the Qdrant vector database.")


