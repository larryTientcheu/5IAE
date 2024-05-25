from datetime import datetime
import config
from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
import json
from models import db, Prompts
import src.funcs as helper_functions
from flask_cors import CORS

import ai_model.helpers.helpers as ai_helpers

app = Flask(__name__)
app.config.from_object("config")

# connect to a local postgresql database
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

# Database Migration
migrate = Migrate(app, db)

CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add(
        "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
    )
    return response


@app.route("/chats", methods=["GET"])
def chat():
    prompts = Prompts.query.all()
    if not prompts:
        abort(404)
    prompts = [prompt.format() for prompt in prompts]
    return jsonify({"success": True, "prompts": prompts})


@app.route("/chat", methods=["POST"])
def add_chat():
    if not request.json:
        return abort(406)

    _json: dict = request.json
    if (
        "prompt" or "airline" or "departure" or "origin" or "destination"
    ) not in _json.keys():
        return abort(406)
    else:
        try:
            prompt = _json["prompt"]
            airline = _json["airline"]
            departure = _json["departure"]
            origin = _json["origin"]
            destination = _json["destination"]

            departure = datetime.strptime(departure, "%Y-%m-%d %H:%M:%S")

            input_data = helper_functions.format_input(
                airline, departure, origin, destination
            )

            price = ai_helpers.make_prediction(input_data)

            new_chat = Prompts(
                prompt=prompt,
                airline=airline,
                scheduled_departure=departure,
                origin_airport=origin,
                destination_airport=destination,
            )
            new_chat.insert()
            db.session.commit()
            return jsonify(
                {
                    "success": True,
                    "price": str(price),
                    "prompt": new_chat.format(),
                }
            )
        except Exception as e:
            # print(e)
            db.session.rollback()
            return abort(500)
        finally:
            db.session.close()


@app.route("/chat/<int:del_id>", methods=["DELETE"])
def remove_chat(del_id):
    try:
        Prompts.query.filter_by(id=del_id).delete()
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return abort(404)
    finally:
        db.session.close()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.register_blueprint(swaggerui_blueprint)
        app.run(debug=True)
