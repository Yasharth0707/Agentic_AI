#Retrieval Phase 


from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()
openai_client = OpenAI()


embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db=QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

#Take the user input
user_input = input("Enter your question: ")

#Retrieve the relevant documents from the vector database based on the user input
search_results = vector_db.similarity_search(query=user_input)

context="".join([f"Page {i+1}: {doc.page_content}\nPage Number: {doc.metadata.get('page_number', 'Unknown')}\nFile Location: {doc.metadata.get('file_location', 'Unknown')}\n" for i, doc in enumerate(search_results)])

SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions based on the context provided along with the page_contents and page number.

You should only answer the user based on the following context and navigate the user to open the right page number to know more.

Context:{context}
"""

response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":user_input}
    ]
)

print("Answer:", response.choices[0].message.content)
