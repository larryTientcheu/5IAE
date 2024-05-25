import json
import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
import tensorflow as tf

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
        "question": "Quel est le nom de l'aéroport ou la ville d'origine ?",
        "answer": row['aeroport_origine'] if row['aeroport_origine'] else row['ville_origine']
    })
    training_data.append({
        "question": "Quel est le nom de l'aéroport ou la ville de destination ?",
        "answer": row['aeroport_destination'] if row['aeroport_destination'] else row['ville_destination']
    })

# Vérifier la cohérence des données
questions = [item['question'] for item in training_data]
answers = [item['answer'] for item in training_data]

# Assurez-vous que les longueurs correspondent
assert len(questions) == len(answers), "Le nombre de questions et de réponses doit être égal"

# Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Encoder les questions et les réponses séparément
encoded_questions = tokenizer(questions, padding=True, truncation=True, return_tensors='tf')
encoded_answers = tokenizer(answers, padding=True, truncation=True, return_tensors='tf')

# Nous allons utiliser les tokens des questions et des réponses ensemble comme features
features = {
    "input_ids": encoded_questions['input_ids'],
    "attention_mask": encoded_questions['attention_mask']
}
labels = tf.ones(len(encoded_questions['input_ids']))  # Labels pour classification binaire

# Vérifier la cohérence des tailles des inputs et labels
assert features['input_ids'].shape[0] == labels.shape[0], "Le nombre d'inputs et de labels doit être égal"

# Split des données
train_features, val_features, train_labels, val_labels = train_test_split(
    features["input_ids"].numpy(), labels.numpy(), test_size=0.2)

# Convertir les données en format TensorFlow
train_dataset = tf.data.Dataset.from_tensor_slices((train_features, train_labels)).shuffle(len(train_labels)).batch(8)
val_dataset = tf.data.Dataset.from_tensor_slices((val_features, val_labels)).batch(8)

# Charger le modèle BERT pour la classification
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Compiler le modèle
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5), 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['accuracy'])

# Entraîner le modèle
model.fit(train_dataset, validation_data=val_dataset, epochs=1)

# Sauvegarder le modèle
model_save_path = './saved_model/'
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)
