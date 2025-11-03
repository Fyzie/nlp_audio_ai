from transformers import pipeline
from transformers.utils.logging import set_verbosity_error

set_verbosity_error()

summarizer = pipeline(
    task="summarization",
    model="facebook/bart-large-cnn"
    )

text = """
The science of ocean level, also known as sea level science, studies the height of the ocean surface 
and how it changes over time. These changes are influenced by factors such as melting glaciers, thermal 
expansion of seawater due to global warming, and natural climate patterns like El Niño. Scientists use 
satellites, tide gauges, and computer models to monitor and predict these variations. Rising ocean levels 
pose serious risks to coastal communities, ecosystems, and infrastructure worldwide. Understanding sea 
level science helps governments and researchers plan better strategies to reduce the impacts of climate change.
"""

res = summarizer(
    text,
    max_length = 100,
    min_length = 50,
    do_sample = False
    )

print(res)