import os
from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent
load_dotenv(basedir / ".env", verbose=True)

DEBUG = os.getenv("DEBUG")
# URL = ""

if os.getenv("ENV") == 'docker':
    URL = os.getenv("DOCKER_BACKEND_URL")
elif os.getenv("ENV") == 'dev':
    URL = os.getenv("LOCAL_BACKEND_URL")
else:
    load_dotenv()
    URL = os.getenv("RENDER_BACKEND_URL")
    DEBUG = False
