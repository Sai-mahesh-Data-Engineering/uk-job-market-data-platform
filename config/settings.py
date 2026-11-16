import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
REED_API_KEY = os.getenv("REED_API_KEY")

if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
    raise RuntimeError("Missing Adzuna credentials. Check your .env file.")

#print("Adzuna credentials loaded successfully.")