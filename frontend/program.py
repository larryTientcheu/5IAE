from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import os
import joblib
import helpers
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/validate_answer", methods=["POST"])
def validate_answers():
    data = request.json
    payload, valid = helpers.validate(data)
    valid["payload"] = payload
    return jsonify(valid)


@app.route("/save_flight_info", methods=["POST"])
def save_flight_info():
    sent_to_back = {}
    payload = request.json
    if payload:
        sent_to_back["prompt"] = payload["prompt"]
        sent_to_back["airline"] = payload["compagnie"]
        sent_to_back["departure"] = (
            payload["date_depart"] + " " + payload["heure_depart"] + ":00"
        )
        sent_to_back["origin"] = payload["origine"]
        sent_to_back["destination"] = payload["destination"]

    print(json.dumps(sent_to_back))
    # Call the backend api chat here
    url = "http://localhost:5005/chat"
    response = requests.post(url, sent_to_back, timeout=25)

    if response.status_code != 200:
        return {"message": "Une erreur s'est produite"}
    print("JSON Response ", response)

    return jsonify(
        {"message": "Les informations de vol ont été sauvegardées avec succès."}
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
