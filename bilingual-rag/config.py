import os

from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore

# Configure GenAI LLM and Embeddings
Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-2")
Settings.llm = GoogleGenAI(model_name="gemini-2.5-flash")

# Connect to Qdrant Vector DB
# client = QdrantClient(host="localhost", port=6333)
# vector_store = QdrantVectorStore(collection_name="bilingual_docs", client=client)

client = QdrantClient(path="./qdrant_db")
vector_store = QdrantVectorStore(client=client, collection_name="bilingual_rag")

print("System successfully connected to Qdrant and configured with modern Google GenAI!")
