from flask import Flask, render_template, request, jsonify
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import json
import numpy as np
import os

app = Flask(__name__)

# Charger le modèle BERT pour la validation des réponses
model_save_path = './saved_model/'  # spécifiez le même chemin que celui utilisé pour la sauvegarde
tokenizer = BertTokenizer.from_pretrained(model_save_path)
model = TFBertForSequenceClassification.from_pretrained(model_save_path)

# Charger les données du fichier JSON pour la validation
with open('larger_flight_data.json', 'r') as f:
    flights_data = json.load(f)

# Extraire les listes valides de compagnies, aéroports et villes
valid_companies = set(row['compagnie'] for row in flights_data)
valid_airports = set(row['aeroport_origine'] for row in flights_data) | set(row['aeroport_destination'] for row in flights_data)
valid_cities = set(row['ville_origine'] for row in flights_data) | set(row['ville_destination'] for row in flights_data)

# Fonction pour valider les réponses en utilisant le modèle entraîné
def validate_answer(question, answer):
    inputs = tokenizer(question, answer, return_tensors='tf', truncation=True, padding=True)
    outputs = model(inputs)
    prediction = tf.argmax(outputs.logits, axis=-1).numpy()[0]
    return bool(prediction)

# Route pour la validation des réponses
@app.route('/validate_answer', methods=['POST'])
def validate_answer_route():
    data = request.json
    question = data['question']
    answer = data['answer']

    if "compagnie" in question.lower() and answer not in valid_companies:
        return jsonify({'valid': False, 'error': 'Cette compagnie n\'existe pas, veuillez entrer une autre compagnie.'})
    elif "aéroport ou la ville d'origine" in question.lower() and answer not in valid_airports and answer not in valid_cities:
        return jsonify({'valid': False, 'error': 'Cet aéroport ou cette ville n\'existe pas, veuillez entrer un autre nom.'})
    elif "aéroport ou la ville de destination" in question.lower() and answer not in valid_airports and answer not in valid_cities:
        return jsonify({'valid': False, 'error': 'Cet aéroport ou cette ville n\'existe pas, veuillez entrer un autre nom.'})
    
    valid = validate_answer(question, answer)
    return jsonify({'valid': valid})

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour sauvegarder les informations de vol
@app.route('/save_flight_info', methods=['POST'])
def save_flight_info():
    flight_info = request.json
    
    if not os.path.exists('flights_data.json'):
        flights_data = []
    else:
        with open('flights_data.json', 'r') as f:
            flights_data = json.load(f)
    
    flights_data.append(flight_info)
    
    with open('flights_data.json', 'w', encoding='utf-8') as f:
        json.dump(flights_data, f, ensure_ascii=False, indent=4)
    
    return jsonify({'message': 'Les informations de vol ont été sauvegardées avec succès.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
