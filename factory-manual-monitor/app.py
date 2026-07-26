from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks
from fastapi.responses import HTMLResponse
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import pandas as pd
import os
import datetime
from evidently.core.report import Report
from evidently.presets import DataDriftPreset
from evidently.presets import DataSummaryPreset

app = FastAPI()

# load model and connect to Qdrant
model = SentenceTransformer('all-MiniLM-L6-v2')
client = QdrantClient(path="./qdrant_db")

# setup drift monitoring logs
LOG_FILE = "query_logs.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["timestamp", "user_query"]).to_csv(LOG_FILE, index=False)

# What "normal" factory queries look like (act asbaseline)
REFERENCE_DATA = pd.DataFrame({
    "user_query": [
        "How often should I lubricate Pump 204?",
        "What is the tension for Conveyor Belt B?",
        "Hydraulic press temperature is too high",
        "Emergency cooling system procedures",
        "When is the next maintenance cycle?"
    ]
})

def log_query(query: str):
    """Background task to save incoming queries to a CSV."""
    new_data = pd.DataFrame([{"timestamp": datetime.datetime.now(), "user_query": query}])
    new_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

def verify_token(authorization: str = Header(None)):
    """Simulates SSO / API Gateway authentication."""
    if authorization != "Bearer secure_factory_token_123":
        raise HTTPException(status_code=401, detail="Unauthorized operator")

@app.post("/ask", dependencies=[Depends(verify_token)])
def ask_question(query: str, background_tasks: BackgroundTasks):
    # log query for drift detection wthout slowing down the API response
    background_tasks.add_task(log_query, query)
    
    # embed the query
    query_vector = model.encode(query).tolist()
    
    try:
        # retrieve answer from Qdrant using the updated query_points API
        # warning: query without threshold create hallucination
        # search_results = client.query_points(
        #     collection_name="factory_docs",
        #     query=query_vector,
        #     limit=1
        # ).points

        # query Qdrant with the score included
        search_results = client.query_points(
            collection_name="factory_docs",
            query=query_vector,
            limit=1,
            with_payload=True,
            with_vectors=False
            ).points
        
    except Exception as e:
        return {"query": query, "system_answer": f"Database Error: {str(e)}. Did you run build_index.py?"}
    
    THRESHOLD = 0.5
    if not search_results or search_results[0].score < THRESHOLD:
        return {"query": query, "system_answer": "No relevant info found."}
        
    context = search_results[0].payload["text"]
    
    return {
        "query": query,
        "retrieved_context": context,
        "system_answer": f"Based on the manual: {context}"
    }

@app.get("/monitor-drift")
def get_drift_metrics():
    try:
        current_data = pd.read_csv(LOG_FILE)
        
        baseline_len = 25 
        current_avg_len = current_data['user_query'].str.len().mean()
        
        # explicitly convert the numpy boolean to a standard Python bool
        drift_detected = bool(abs(current_avg_len - baseline_len) / baseline_len > 0.3)
        
        return {
            "status": "success",
            "drift_detected": drift_detected,
            "metrics": {
                "current_avg_length": float(current_avg_len),
                "baseline_avg_length": baseline_len
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}