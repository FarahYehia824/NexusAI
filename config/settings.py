from dotenv import load_dotenv
import os

# نحسب مسار المشروع الرئيسي (nexusai/) بشكل واضح
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "config", ".env")

load_dotenv(ENV_PATH)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(f"GROQ_API_KEY not found. Checked path: {ENV_PATH}")