"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
import time
import logging
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from core.config import GEMINI_API_KEY, GEMINI_MODEL
from google import genai
from lessons import get_lesson_by_slug
logger = logging.getLogger('tutor')
_client = None

def client():
    global _client
    if not GEMINI_API_KEY:
        raise HTTPException(503, 'AI tutor not configured: GEMINI_API_KEY is missing')
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client

def _build_tutor_prompt(student, message: str, lesson_context: str) -> str:
    level          = (student["age_group"]      if student else None) or "Beginner"
    learning_style = (student["learning_style"] if student else None) or "general"
    goal           = (student["goal"]           if student else None) or "learn HTML fundamentals"

    context_block = (
        f"Lesson material the student is currently studying:\n{lesson_context}\n\n"
        if lesson_context else ""
    )

    return f"""You are a patient, encouraging HTML tutor.
        Student level: {level}
        Preferred learning style: {learning_style}
        Student's stated goal: {goal}

        {context_block}Student question:
        {message}

        Rules:
        - Explain step by step at the student's level.
        - Give a short code example when relevant.
        - Keep answers under ~200 words unless the student asks for depth.
        - End with one short check-for-understanding question.
        """


async def codeverse_lesson_reply(lesson_id: str, lesson_title: str, question: str) -> str:
    prompt = _build_tutor_prompt(None, question,
        f'Current lesson {lesson_id}: {lesson_title}. Focus on explaining the lesson concept, not on grading an assessment.')
    def _request():
        response = client().models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return (response.text or '').strip()
    try:
        answer = await run_in_threadpool(_request)
    except HTTPException:
        raise
    except Exception:
        logger.exception('CodeVerse lesson tutor request failed')
        raise HTTPException(502, 'AI tutor temporarily unavailable')
    if not answer:
        raise HTTPException(502, 'AI tutor returned an empty response')
    return answer
