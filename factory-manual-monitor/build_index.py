from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import mlflow
from sentence_transformers import SentenceTransformer

mlflow.set_experiment("Factory_RAG_Pipeline")

with mlflow.start_run():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    with open("factory_manual.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # initialize Qdrant Client (local storage)
    client = QdrantClient(path="./qdrant_db")
    
    # create Collection
    if client.collection_exists(collection_name="factory_docs"):
        client.delete_collection(collection_name="factory_docs")
        
    client.create_collection(
        collection_name="factory_docs",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    
    # embed and store
    points = []
    for i, text in enumerate(lines):
        embedding = model.encode(text).tolist()
        # Qdrant stores the raw text in the payload
        points.append(
            PointStruct(id=i, vector=embedding, payload={"text": text})
        )
    
    client.upsert(collection_name="factory_docs", points=points)
    
    # explicitly close the client to release file locks (problem on windows :)
    client.close()
    
    # log to mlflow
    mlflow.log_param("embedding_model", "all-MiniLM-L6-v2")
    mlflow.log_artifact("./qdrant_db", "qdrant_store")
    print("Qdrant index built and logged successfully.")