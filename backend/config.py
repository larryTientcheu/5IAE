import os
from pathlib import Path

SECRET_KEY = os.urandom(32)

basedir = Path(__file__).parent

DATABASE_URI = "postgresql://postgres:grimm@localhost:5432/chatbot"
SQLALCHEMY_TRACK_MODIFICATIONS = False
