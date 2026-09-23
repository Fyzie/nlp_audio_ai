### Step-by-Step Guide

1. **Open your project folder in VS Code:** Setup.
Open VS Code, go to **File > Open Folder...**, and select the directory where you saved both `app.py` and `simulate_traffic.py`.


2. **Open the integrated terminal:**
New terminal on VSCode.   


```
uvicorn app:app --reload

```

Should see output indicating that the server is running on http://127.0.0.1:8000. Leave this terminal window open.


```
python simulate_traffic.py

```
