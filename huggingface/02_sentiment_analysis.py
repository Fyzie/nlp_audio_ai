from transformers import pipeline
from transformers.utils.logging import set_verbosity_error

set_verbosity_error()

sent_analyzer = pipeline(
    "sentiment-analysis",
    model="tabularisai/multilingual-sentiment-analysis"
)

text = "The cloud seems dark but the weather news reported that today is supposed to be a sunny day."

res = sent_analyzer(
    text
)

print(res)