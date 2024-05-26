import os
from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent

if os.getenv("ENVIRONMENT") == "dev":
    load_dotenv(basedir / ".env.dev", verbose=True)
elif os.getenv("ENVIRONMENT") == "docker":
    load_dotenv(basedir / ".env.docker", verbose=True)

SECRET_KEY = os.urandom(32)


DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
