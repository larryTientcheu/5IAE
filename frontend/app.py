from flask import Flask, render_template, request, jsonify
import json
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

app = Flask(__name__)

# Charger les données du fichier JSON
with open('chats.json', 'r') as f:
    data = json.load(f)
chats = data['chats']

# Charger le tokenizer et le modèle BERT pré-entraîné
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(chats))

# Préparer les données d'entraînement
questions = [chat['prompt'] for chat in chats]
responses = [chat['response'] for chat in chats]

train_encodings = tokenizer(questions, truncation=True, padding=True)
train_labels = tf.convert_to_tensor([i for i in range(len(chats))])

# Convertir les données en format TensorFlow Dataset
train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings),
    train_labels
))

# Compiler le modèle
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

# Entraîner le modèle
model.fit(train_dataset.shuffle(1000).batch(8), epochs=50, batch_size=20)

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour obtenir la réponse prédite à partir d'une question de l'utilisateur
@app.route('/get_response', methods=['POST'])
def get_response():
    user_question = request.json['question']
    
    # Prétraitement de la question de l'utilisateur
    inputs = tokenizer(user_question, return_tensors='tf', truncation=True, padding=True)
    
    # Prédiction de la réponse par le modèle
    outputs = model(inputs)
    prediction = tf.argmax(outputs.logits, axis=-1).numpy()[0]
    predicted_response = responses[prediction]
    
    return jsonify({'response': predicted_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
