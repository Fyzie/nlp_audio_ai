# ingest urls-type docs and manual batching
import os
import time
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.web import SimpleWebPageReader

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

all_documents = []

# LOAD LOCAL FILES
print("Reading documents from the data directory...")
if os.path.exists("data"):
    # exclude reading urls.txt for first file ingestion
    local_docs = SimpleDirectoryReader(
        "data", 
        exclude=["urls.txt"]
    ).load_data()
    
    if local_docs:
        all_documents.extend(local_docs)

else:
    print("Error: The 'data' folder is missing or empty! Add a file first.")
    # exit(1) $ optional: exit or just create "data" folder and add files into it
    os.makedirs("data")

# READ URLS WITHIN .TXT AND INGEST
url_file_path = os.path.join("data", "urls.txt")
if os.path.exists(url_file_path):
    print(f"Found '{url_file_path}'. Reading target website lines...")
    
    with open(url_file_path, "r", encoding="utf-8") as f:
        target_urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        
    if target_urls:
        print(f"Scraping {len(target_urls)} web destinations sequentially...")
        try:
            web_docs = SimpleWebPageReader(html_to_text=True).load_data(urls=target_urls)
            all_documents.extend(web_docs)
            print(f"Scraped web context blocks successfully.")
        except Exception as e:
            print(f"Web Scraping Error: Could not process URLs: {e}")
    else:
        print("urls.txt empty")
else:
    print("urls.txt doesnt exist")

if not all_documents:
    print("No local files at all")
    exit(1)

##########################################################################################################
print("Parsing all unified text structures into semantic sentence chunks...")
splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=51
)

nodes = splitter.get_nodes_from_documents(all_documents)
total_nodes = len(nodes)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# qdratn empty vector index mapping
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

# manual loop and batching
batch_size = 16
for i in range(0, total_nodes, batch_size):
    batch_nodes = nodes[i : i + batch_size]
    
    for node in batch_nodes:
        node.embedding = Settings.embed_model.get_text_embedding(
            node.get_content(metadata_mode="embed")
        )
    
    storage_context.vector_store.add(batch_nodes)
    
    progress = min(i + batch_size, total_nodes)
    print(f"   Processed Chunks: {progress}/{total_nodes} ({(progress/total_nodes)*100:.1f}%)")
    
    if i + batch_size < total_nodes:
        print("Pacing API limit for seconds interval")
        time.sleep(3.0)

print("Ingestion done. Data metrics are chunked, vectorized, and securely stored in Qdrant.")

#### SHORTCUT INGESTION ######################################################################

# storage_context = StorageContext.from_defaults(vector_store=vector_store)

# index = VectorStoreIndex.from_documents(
#     all_documents, 
#     storage_context=storage_context, 
#     transformations=[splitter]
# )
