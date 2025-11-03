from transformers import pipeline

qna = pipeline(
    "question-answering",
    model="timpal0l/mdeberta-v3-base-squad2"
    )

question = "How high is the building?"
context = "My height is 1.7 meters, the tree stands 3 meters and the building is 130 meters in height"

res = qna(question = question, context = context)

print(res)