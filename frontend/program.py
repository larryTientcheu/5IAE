from flask import Flask, render_template, request, jsonify
import requests
import config
import helpers

app = Flask(__name__)
app.config.from_object("config")

URL = app.config.get("URL")

@app.route("/")
def index():
    try:
        chats = requests.get(f"{URL}chats", timeout=60)
        all_chats = chats.json()
        prompts = [prompt for prompt in all_chats["prompts"]]
        # get a list of prompts and pass to the index
        return render_template("index.html", chats=prompts)
    except Exception as e:
        return render_template("index.html", chats=[])


@app.route("/validate_answer", methods=["POST"])
def validate_answers():
    data = request.json
    payload, valid = helpers.validate(data)
    valid["payload"] = payload
    return jsonify(valid)


@app.route("/save_flight_info", methods=["POST"])
def save_flight_info():
    try:
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

        print(sent_to_back)
        # Call the backend api chat here
        response = requests.post(f"{URL}chat", json=sent_to_back, timeout=120)

        if response.status_code != 200:
            return {"message": "Une erreur s'est produite"}
        result = response.json()
        return jsonify(
            {
                "message": f"Le prix du vol de {result['prompt']['origin_airport']} à {result['prompt']['destination_airport']}, le {result['prompt']['scheduled_departure']} avec la compagnie {result['prompt']['airline']} est: ${result['price']}"
            }
        )
    except Exception as e:
        return {"message": f"Une erreur s'est produite {e}"}


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG"), host="0.0.0.0", port=5000)