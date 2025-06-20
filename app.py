from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
from sentiment_analysis import analyze_texts # Make sure this function exists
from political_model import predict_political_leaning

# Initialize Flask app
app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Existing /predict Route for Political Model
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get data from frontend
    text = data.get('text', '')  # Get the text input

    # Get prediction results from the AI model
    probabilities, labels = predict_political_leaning(text)
    
    # Prepare the prediction result to be sent to the frontend
    prediction = {
        "probabilities": probabilities.tolist(),
        "labels": labels.tolist(),
        "predicted_label": labels[probabilities.argmax()],
        "max_prob": probabilities.max().item()
    }

    return jsonify(prediction)


@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        text_input = request.form.get('text', '')  # Get the text input
        if not text_input:
            return render_template('sentiment.html', error="Please enter text for analysis.")
        
        # Analyze the text
        texts = [text_input]  # Single text input wrapped in a list
        percentages, results = analyze_texts(texts)
        return render_template('sentiment.html', percentages=percentages, results=results)

    return render_template('sentiment.html')
    
if __name__ == '__main__':
    app.run(debug=True)
