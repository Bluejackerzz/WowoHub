from flask import Flask, request, jsonify
from transformers import pipeline
import re
import emoji
import pandas as pd
from collections import Counter

app = Flask(__name__)

def remove_emoji(text):
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F" 
        "\U0001F300-\U0001F5FF" 
        "\U0001F680-\U0001F6FF"  
        "\U0001F1E0-\U0001F1FF"  
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_symbols(text):
    return re.sub(r'[^\w\s]+', '', text)

# Initialize the sentiment analysis pipeline
pipe = pipeline("text-classification", model="w11wo/indonesian-roberta-base-sentiment-classifier")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']
    
    # Clean the input text
    cleaned_text = remove_symbols(remove_emoji(text))
    
    # Run the sentiment analysis
    result = pipe(cleaned_text)
    label = result[0]['label']
    score = result[0]['score']
    
    # Return the sentiment result
    return jsonify({
        'sentiment': label,
        'score': score
    })

if __name__ == '__main__':
    app.run(debug=True)
