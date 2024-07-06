from pathlib import Path
import joblib
from joblib import Memory
import pandas as pd

# from transformers import BertTokenizer, TFBertForSequenceClassification
from flask import jsonify
import json


# def load_model():
#     path = Path(__file__).parent / "chatbot"
#     model = TFBertForSequenceClassification.from_pretrained(path / "tmodels/")
#     tokenizer = BertTokenizer.from_pretrained(path / "tmodels/")

#     return model, tokenizer


# def chat(question, answer):
#     model, tokenizer = load_model()

#     inputs = tokenizer(
#         question, answer, return_tensors="tf", truncation=True, padding=True
#     )
#     outputs = model(inputs)  # type: ignore
#     prediction = tf.argmax(outputs.logits, axis=-1).numpy()[0]
#     return bool(prediction)


def load_df():
    path = Path(__file__).parent / "chatbot"
    df = pd.read_pickle(path / "flights_dataframe")
    return df


def validate(data):
    df_flights = load_df()
    question = data["question"].lower()
    answer = data["answer"].lower()
    payload = {}

    keyword = "compagnie"
    if keyword in question.lower():
        unique_values_all_columns = pd.concat(
            [
                pd.Series(df_flights["compagnie"].str.lower().unique()),
                pd.Series(df_flights["code_compagnie"].str.lower().unique()),
            ],
            ignore_index=True,
        )
        answer = [s for s in unique_values_all_columns.values if answer in s.lower()]
        if answer[0] not in unique_values_all_columns.values:
            return payload, {
                "valid": False,
                "error": "Cette compagnie n'existe pas, veuillez entrer une autre compagnie.",
            }
        else:
            payload = df_flights[
                (df_flights["compagnie"].str.lower() == answer[0])
                | (df_flights["code_compagnie"].str.lower() == answer[0])
            ]
            payload = payload["code_compagnie"].iloc[0]

    keyword = "aéroport ou la ville d'origine"
    if keyword in question.lower():
        unique_values_all_columns = pd.concat(
            [
                pd.Series(df_flights["aeroport_origine"].str.lower().unique()),
                pd.Series(df_flights["code_aeroport_origine"].str.lower().unique()),
                pd.Series(df_flights["ville_origine"].str.lower().unique()),
            ],
            ignore_index=True,
        )
        answer = [s for s in unique_values_all_columns.values if answer in s.lower()]
        if answer[0] not in unique_values_all_columns.values:
            return payload, {
                "valid": False,
                "error": "Cet aéroport ou cette ville n'existe pas, veuillez entrer un autre nom.",
            }
        else:
            payload = df_flights[
                (df_flights["aeroport_origine"].str.lower() == answer[0])
                | (df_flights["code_aeroport_origine"].str.lower() == answer[0])
                | (df_flights["ville_origine"].str.lower() == answer[0])
            ]["code_aeroport_origine"].iloc[0]

    keyword = "aéroport ou la ville de destination"
    if keyword in question.lower():
        unique_values_all_columns = pd.concat(
            [
                pd.Series(df_flights["aeroport_destination"].str.lower().unique()),
                pd.Series(df_flights["code_aeroport_destination"].str.lower().unique()),
                pd.Series(df_flights["ville_destination"].str.lower().unique()),
            ],
            ignore_index=True,
        )
        answer = [s for s in unique_values_all_columns.values if answer in s.lower()]
        if answer[0] not in unique_values_all_columns.values:
            return payload, {
                "valid": False,
                "error": "Cet aéroport ou cette ville n'existe pas, veuillez entrer un autre nom.",
            }
        else:
            payload = df_flights[
                (df_flights["aeroport_destination"].str.lower() == answer[0])
                | (df_flights["code_aeroport_destination"].str.lower() == answer[0])
                | (df_flights["ville_destination"].str.lower() == answer[0])
            ]["code_aeroport_destination"].iloc[0]
    # valid = chat(question, answer)

    return payload, {"valid": True, "error": ""}
