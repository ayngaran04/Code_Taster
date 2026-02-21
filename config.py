import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
MAX_FILE_SIZE_KB = 100
MAX_TOKENS = 4000
SUPPORTED_EXTENSIONS = {".py", ".js", ".java"}
EXCLUDED_DIRS = {             
    "node_modules", ".git", "__pycache__",
    "venv", ".venv", "dist", "build", ".next"
}