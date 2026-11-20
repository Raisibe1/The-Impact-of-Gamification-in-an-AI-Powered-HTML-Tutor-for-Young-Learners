#.\.venv313\Scripts\python.exe -m uvicorn API:app --reload --port 8000
"""CodeVerse FastAPI application composition root.
Run: uvicorn API:app --reload --port 8000

"""
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import ROOT, DATABASE_PATH, ALLOWED_ORIGINS
from database.migrate import apply_migrations
from database.seed import seed_lessons
from routes.admin_analytics import router as analytics_router
from routes import (auth, profiles, pages, assessments, gamification,
                    ai_tutor, ml_prediction)
from backend.learning_routes import initialize_learning_db, learning_router
from core.security import require_student_id
from services.gemini_service import codeverse_lesson_reply

logging.basicConfig(level=logging.INFO)
app = FastAPI(title='CodeVerse API', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS,
                   allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.mount('/static', StaticFiles(directory=str(ROOT / 'static')), name='static')

@app.on_event('startup')
def prepare_database():
    apply_migrations()
    initialize_learning_db(DATABASE_PATH)
    seed_lessons()
    seed_legacy_games()

app.include_router(auth.router)
app.include_router(analytics_router)
app.include_router(profiles.router)
app.include_router(pages.router)
app.include_router(assessments.router)
app.include_router(gamification.router)
app.include_router(ai_tutor.router)
app.include_router(ml_prediction.router)
app.include_router(learning_router(DATABASE_PATH, require_student_id,chat_reply=codeverse_lesson_reply))
