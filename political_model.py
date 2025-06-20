from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import joblib
from safetensors.torch import load_file

# Model paths
model_path = r'C:\Users\WINDOWS 10\Downloads\Project AI2\AI model2'
safetensors_path = f'{model_path}/model.safetensors'
label_encoder_path = r'C:\Users\WINDOWS 10\Downloads\Project AI2\AI model2/label_encoder.joblib'

# Load model, tokenizer, and label encoder
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
state_dict = load_file(safetensors_path)
model.load_state_dict(state_dict)
label_encoder = joblib.load(label_encoder_path)

# Define the prediction function
def predict_political_leaning(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
    return predictions.cpu().numpy()[0], label_encoder.classes_
