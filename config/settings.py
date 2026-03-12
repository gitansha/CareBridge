import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# WHO ICD API
ICD_CLIENT_ID = os.getenv("ICD_CLIENT_ID", "")
ICD_CLIENT_SECRET = os.getenv("ICD_CLIENT_SECRET", "")

DEPARTMENTS = [
    "cardiology",
    "orthopedics",
    "general_medicine",
    "neurology",
    "emergency",
    "oncology",
]

MAX_AGENT_ITERATIONS = 10
