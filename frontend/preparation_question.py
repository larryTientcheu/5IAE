import json
import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os

# Charger les données du fichier JSON
with open('larger_flight_data.json', 'r') as f:
    flights_data = json.load(f)

# Convertir les données en DataFrame pour faciliter la manipulation
df = pd.DataFrame(flights_data)

# Créer un dataset pour l'entraînement
training_data = []

# Générer des paires question-réponse
for index, row in df.iterrows():
    training_data.append({
        "question": "Pouvez-vous me donner la compagnie aérienne ?",
        "answer": row['compagnie']
    })
    training_data.append({
        "question": "Quelle est la date de départ (YYYY-MM-DD) ?",
        "answer": row['date_depart']
    })
    training_data.append({
        "question": "Quelle est l'heure de départ (HH:MM) ?",
        "answer": row['heure_depart']
    })
    training_data.append({
        "question": "Quel est le nom de l'aéroport d'origine ?",
        "answer": row['aeroport_origine']
    })
    training_data.append({
        "question": "Quelle est la ville d'origine ?",
        "answer": row['ville_origine']
    })
    training_data.append({
        "question": "Quel est le nom de l'aéroport de destination ?",
        "answer": row['aeroport_destination']
    })
    training_data.append({
        "question": "Quelle est la ville de destination ?",
        "answer": row['ville_destination']
    })

# Vérifier la cohérence des données
questions = [item['question'] for item in training_data]
answers = [item['answer'] for item in training_data]

assert len(questions) == len(answers), "Le nombre de questions et de réponses doit être égal"

# Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Encoder les données
inputs = tokenizer(questions, answers, return_tensors='tf', padding=True, truncation=True)

# Créer les labels (1 pour valide, 0 pour invalide)
labels = [1] * len(answers)  # En supposant que toutes les réponses sont valides dans les données d'entraînement

# Split des données
train_inputs, val_inputs, train_labels, val_labels = train_test_split(inputs, labels, test_size=0.2)

# Convertir les données en format TensorFlow
train_dataset = tf.data.Dataset.from_tensor_slices((dict(train_inputs), train_labels)).shuffle(len(train_inputs)).batch(8)
val_dataset = tf.data.Dataset.from_tensor_slices((dict(val_inputs), val_labels)).batch(8)

# Charger le modèle BERT pour la classification
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Compiler le modèle
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5), 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['accuracy'])

# Entraîner le modèle
model.fit(train_dataset, validation_data=val_dataset, epochs=3)
