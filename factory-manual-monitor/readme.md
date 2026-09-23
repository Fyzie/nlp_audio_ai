### Step-by-Step Guide

1. **Open project folder in VS Code:** Setup.
Open VS Code, go to **File > Open Folder...**, and select the directory where both `app.py` and `simulate_traffic.py` are saved.


2. **Open the integrated terminal:**
New terminal on VSCode.   


```
uvicorn app:app --reload
```
OR
```
uvicorn {script_name}:app --reload --port 8000

```
OR for cloud deployment,   
**Start Command:**   
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
   
Should see output indicating that the server is running on http://127.0.0.1:8000. Leave this terminal window open.


```
python simulate_traffic.py

```
