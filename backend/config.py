import os
from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent

SECRET_KEY = os.urandom(32)
SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.getenv("ENV") == "dev":
    load_dotenv(basedir / ".env", verbose=True)
    DEBUG = os.getenv("DEBUG")
elif os.getenv("ENV") == "docker":
    load_dotenv(basedir / ".env.docker", verbose=True)
    DEBUG = os.getenv("DEBUG")
else:
    load_dotenv()
    DEBUG = False

DATABASE_URI = os.getenv("DATABASE_URI")
