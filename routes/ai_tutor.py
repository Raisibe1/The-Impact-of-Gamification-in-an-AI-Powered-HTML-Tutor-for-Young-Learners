"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
import time
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from database.connection import Database
from core.security import get_current_student
from core.config import GEMINI_MODEL, DATABASE_PATH as CODEVERSE_DB_PATH
from services.gemini_service import client, _build_tutor_prompt
from backend.learning_routes import is_quiz_active
from lessons import get_lesson_by_slug
logger = logging.getLogger('tutor')
router = APIRouter(tags=['AI Tutor'])
# Gemini client is created lazily to avoid disabling the rest of the platform.
class _GeminiProxy:
    @property
    def models(self):
        return client().models
gemini = _GeminiProxy()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    lesson_slug: str | None = None   # optional, for lesson-aware answers


class ChatResponse(BaseModel):
    reply: str


@router.post('/chat')
def chat_with_tutor(request: Request, payload: ChatRequest):
    # 1. Require login (matches your session-cookie system)
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Please log in to chat with your tutor.")

    # No AI support while any CodeVerse unlock quiz is active.
    if is_quiz_active(CODEVERSE_DB_PATH, student["student_id"]):
        raise HTTPException(status_code=423, detail="AI tutoring is disabled during an active quiz.")

    # 2. Optionally pull lesson context
    lesson_context = ""
    if payload.lesson_slug:
        try:
            lesson = get_lesson_by_slug(payload.lesson_slug)
            if lesson:
                # adjust these keys to match your LESSON_CONTENT structure
                lesson_context = (
                    lesson.get("title")
                    or lesson.get("description")
                    or lesson.get("subtitle")
                    or ""
                )
        except Exception:
            logger.warning("Could not load lesson %s", payload.lesson_slug)

    prompt = _build_tutor_prompt(student, payload.message, lesson_context)

    # Generate the lesson-aware response using the Gemini Developer API.
    started = time.time()
    try:
        response = gemini.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        reply = (response.text or "").strip()
        if not reply:
            raise HTTPException(status_code=502, detail="AI tutor returned an empty response")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Gemini call failed")
        raise HTTPException(status_code=502, detail="AI tutor is temporarily unavailable")

    elapsed = time.time() - started

    # 4. Persist to ai_interactions (already exists in your schema)
    try:
        db = Database()
        conn = db.get_connection()
        try:
            conn.execute(
                """
                INSERT INTO ai_interactions
                    (student_id, question_asked, response_generated,
                     response_time, timestamp, resolved)
                VALUES (?, ?, ?, ?, ?, 0)
                """,
                (
                    student["student_id"],
                    payload.message,
                    reply,
                    elapsed,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()
        finally:
            conn.close()
    except Exception:
        # Never let logging kill the user's reply
        logger.exception("Failed to log ai_interaction")

    return ChatResponse(reply=reply)
