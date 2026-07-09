import os

from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from llama_index.core import SimpleDirectoryReader, Settings, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.qdrant import QdrantVectorStore

# Ensure can read the API Key set
if "GEMINI_API_KEY" not in os.environ:
    print("Error: GEMINI_API_KEY environment variable is missing!")
    exit(1)

# Import configuration settings from config.py
print("Initializing embedding models and engine connectivity...")
from config import client, vector_store, Settings # get config from config.py

# if manually configure the client and vector store
# client = QdrantClient(path="./qdrant_db")
# vector_store = QdrantVectorStore(client=client, collection_name="bilingual_rag")
data_folder = "D:/Github/rag/bilingual-rag-pro/single_data"
# load docs from local data folder
print("Reading documents from the data directory...")
if not os.path.exists(data_folder) or len(os.listdir(data_folder)) == 0:
    print("Error: The 'data' folder is missing or empty! Add a text file first.")
    exit(1)

print("Ingesting source files from data directory")
documents = SimpleDirectoryReader(data_folder).load_data()

print("Parsing text using structured sentence splitting...")
splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=51
)

# create the storage context pipeline configuration
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# generate embeddings and write them into qdrant
print("Generating gemini-embedding-2 vectors and saving to Qdrant...")
index = VectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context, 
    transformations=[splitter]
)

print("Ingestion done. Documents are chunked, vectorized, and securely stored in Qdrant.")