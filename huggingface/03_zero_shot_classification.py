from transformers import pipeline
from transformers.utils.logging import set_verbosity_error

set_verbosity_error()

zsc = pipeline(
    "zero-shot-classification",
    model = 'cross-encoder/nli-deberta-v3-base'
)

text = "Gravity on earth much heavier than on mars"

candidate_labels = ['politics', 'sports', 'science']

res = zsc(
    text,
    candidate_labels
)

print(res)