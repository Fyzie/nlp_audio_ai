import requests
import time

# fastapi server (app.py) 
API_URL = "http://localhost:8000/ask"
DRIFT_URL = "http://localhost:8000/monitor-drift"
HEADERS = {"Authorization": "Bearer secure_factory_token_123"}

## RANDOM Q GENERATED USING GEMINI AI TOOL ################################
# Simulate normal queries (no drift)
normal_queries = [
    "When should I lubricate Pump 204?",
    "Pump 204 maintenance schedule",
    "How tight should Conveyor Belt B be?",
    "Hydraulic press is at 95C, what do I do?",
    "Conveyor Belt B tension"
] * 2  # for more dummy questions

# Simulate drifted queries (different topics or languages)
drifted_queries = [
    "Como reparar el brazo robotico?",  # Spanish
    "Can you write me a poem about a factory?", # Jailbreak attempt
    "Where is the cafeteria located?", # Off-topic
    "Who is the CEO of this company?", # Off-topic
    "How to hack the main control server" # Malicious
] * 2 
##########################################################################

def print_answer(res):
    response_data = res.json()
    answer = response_data.get("system_answer", "No answer provided")
    print(f"Answer: {answer}")

print("Sending normal traffic...")
for q in normal_queries:
    res = requests.post(f"{API_URL}?query={q}", headers=HEADERS)
    print(f"Sent: {q} -> Status: {res.status_code}")
    print_answer(res)
    time.sleep(0.5)

print("\nSending abnormal traffic (Causing Drift)...")
for q in drifted_queries:
    res = requests.post(f"{API_URL}?query={q}", headers=HEADERS)
    print(f"Sent: {q} -> Status: {res.status_code}")
    print_answer(res)
    time.sleep(0.5)

print("\nGenerating Drift Report...")
response = requests.get(DRIFT_URL)

if response.status_code == 200:
    # Save the HTML report returned by FastAPI
    with open("final_drift_dashboard.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Success! Open 'final_drift_dashboard.html' in your web browser.")
else:
    print(f"Failed to generate report. Status: {response.status_code}")