import matplotlib.pyplot as plt
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from safetensors.torch import load_file
import joblib

model_path = r'C:\Users\WINDOWS 10\Downloads\Project AI\AI model' #ubah file path disini
safetensors_path = f'{model_path}/model.safetensors'
label_encoder_path = r'C:\Users\WINDOWS 10\Downloads\Project AI\AI model/label_encoder.joblib' #ini juga ubah sesuai dimana joblib ditaruh

tokenizer = AutoTokenizer.from_pretrained(model_path)


model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=len(joblib.load(label_encoder_path).classes_))
state_dict = load_file(safetensors_path)
model.load_state_dict(state_dict)


label_encoder = joblib.load(label_encoder_path)

def predict_political_leaning(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
    return predictions.cpu().numpy()[0], label_encoder.classes_


comment = input("Enter a comment about the headline: ")


probabilities, labels = predict_political_leaning(comment)


# print("Political Leaning Prediction Probabilities:")
# for i, prob in enumerate(probabilities):
#     print(f"{labels[i]}: {prob * 100:.2f}%")


# plt.figure(figsize=(8, 8))
# plt.pie(probabilities, autopct='%1.1f%%', startangle=90)
# plt.title('Political Leaning Prediction Probabilities')
# plt.axis('equal')

# plt.show()

max_prob_index = probabilities.argmax()
predicted_label = labels[max_prob_index]
max_prob = probabilities[max_prob_index]


plt.figure(figsize=(8, 8))
plt.pie(probabilities, autopct='%1.1f%%', startangle=90)  
plt.title(f'Political Leaning: {predicted_label} ({max_prob * 100:.1f}%)')
plt.axis('equal')

plt.show()