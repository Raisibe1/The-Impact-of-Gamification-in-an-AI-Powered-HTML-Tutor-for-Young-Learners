"""Central configuration. Paths are independent of the current working directory."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / '.env')

_db_input = Path(os.getenv('CODEVERSE_DB_PATH', 'database/tutor.db'))

DATABASE_PATH = (_db_input if _db_input.is_absolute() else ROOT / _db_input).resolve()
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-flash-latest')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
SESSION_HOURS = int(os.getenv('SESSION_HOURS', '1'))
COOKIE_SECURE = os.getenv('COOKIE_SECURE', 'false').lower() == 'true'
FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')
ALLOWED_ORIGINS = [FRONTEND_ORIGIN, 'http://127.0.0.1:5173']
