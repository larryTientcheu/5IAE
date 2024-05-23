from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import DateTime

db = SQLAlchemy()


class Prompts(db.Model):
    __tablename__ = "prompts"

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String)
    airline = db.Column(db.String)
    scheduled_departure = db.Column(DateTime(timezone=False))
    origin_airport = db.Column(db.String)
    destination_airport = db.Column(db.String)

    def __init__(
        self,
        prompt,
        airline,
        scheduled_departure,
        origin_airport,
        destination_airport,
    ):
        self.prompt = prompt
        self.airline = airline
        self.scheduled_departure = scheduled_departure
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "airline": self.airline,
            "scheduled_departure": self.scheduled_departure,
            "origin_airport": self.origin_airport,
            "destination_airport": self.destination_airport,
        }
