from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.core import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

# Pickup and align settings from config.py
from config import client, vector_store, Settings

# manual configure
# Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-2")
# Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
# client = QdrantClient(path="./qdrant_db")  # or url="http://localhost:6333" if using Docker
# vector_store = QdrantVectorStore(client=client, collection_name="bilingual_rag")

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

query_engine = index.as_query_engine(similarity_top_k=3)

def send_query(text, lang):
    print(f"\n[Query {lang}]: {text}")
    print(query_engine.query(text))

# Bilingual test
# Test 1: english
query_en = "How do I reset the camera feed mechanism?"
send_query(query_en, "EN")

print("-" * 30)

# Test 2: malay
query_bm = "Apakah filter yang digunakan untuk mencari kerosakan lens?"
send_query(query_bm, "BM")