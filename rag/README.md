## Package Installation

``` 
pip install llama-index-llms-google-genai llama-index-embeddings-google-genai llama-index llama-index-vector-stores-qdrant llama-index-llms-gemini llama-index-embeddings-gemini qdrant-client streamlit spacy
```

#### Create Docker for Database Container and Boot It
After docker-compose.yaml created, boot:   
```
docker-compose up -d
```
The qdrant storage will be created within the folder, otherwise:   

1. Restart database container (if needed)
```
docker-compose up -d --force-recreate
```
2. Run diagnose check on the container engine
```
docker ps -a
```
If the status is up w.r.t. the ports, then GOOD

Get Gemini API Key
1. Go to Google AI Studio and log in
2. Go to `Get API Key`
3. Click `Create API Key`

Set Key as Environment Variable
On CMD,   
```
set GEMINI_API_KEY="generated API key"
```

Verify:   
```
echo %GEMINI_API_KEY%
```

## Data Ingestion
Verify vector data inside Qdrant dashboard   
1. On web browser,
```
http://localhost:6333/dashboard
```
2. Go to `Collections`

