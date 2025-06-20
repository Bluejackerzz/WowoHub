import pandas as pd
from transformers import pipeline
from collections import Counter
import re
import emoji

# Helper functions
def remove_emoji(text):
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_symbols(text):
    return re.sub(r'[^\w\s]+', '', text)

# Load sentiment analysis pipeline
pipe = pipeline("text-classification", model="w11wo/indonesian-roberta-base-sentiment-classifier")

def analyze_texts(texts):
    # Clean texts
    cleaned_texts = [remove_symbols(remove_emoji(text)) for text in texts]
    
    # Get sentiment analysis results
    results = pipe(cleaned_texts)
    labels = [result['label'] for result in results]
    
    # Count the sentiment labels
    label_counts = Counter(labels)
    total_count = len(labels)
    label_percentages = {label: count / total_count * 100 for label, count in label_counts.items()}
    
    return label_percentages, results
