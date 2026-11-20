"""CodeVerse lesson-progress FastAPI router.

IMPORTANT: This router requires the host app's authenticated session resolver.
Use the original tutor.db file. Never infer student IDs from client JSON.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Callable, Awaitable
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

HERE = Path(__file__).resolve().parent
COURSE = [
    ('T001', 'Introduction to HTML and Web Basics'),
    ('T002', 'HTML Tags and Document Structure'),
    ('T003', 'Headings and Paragraphs'),
    ('T004', 'Hyperlinks'),
    ('T005', 'Images and Multimedia'),
    ('T006', 'Hyperlinks (Intermediate)'),
    ('T007', 'Images and Tags'),
    ('T008', 'Lists and Tables'),
    ('T009', 'Forms and User Input'),
    ('T010', 'Semantic HTML and Accessibility'),
]
LESSON_IDS = [item[0] for item in COURSE]
PASS_PERCENT = 70
QUIZ_BANK = json.loads((HERE / 'quiz_bank.json').read_text(encoding='utf-8'))

class QuizSubmit(BaseModel):
    attempt_id: int = Field(gt=0)
    answers: list[int] = Field(min_length=1, max_length=100)

class ChatQuestion(BaseModel):
    lesson_id: str
    message: str = Field(min_length=1, max_length=2000)

class QuizStart(BaseModel):
    lesson_id: str

class QuizAbandon(BaseModel):
    attempt_id: int = Field(gt=0)

class LessonViewed(BaseModel):
    lesson_id: str


def initialize_learning_db(db_path: str | Path):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path, timeout=10) as db:
        db.execute('PRAGMA foreign_keys=ON')
        db.executescript((HERE / 'learning_schema.sql').read_text(encoding='utf-8'))


def is_quiz_active(db_path: str | Path, student_id: int) -> bool:
    with sqlite3.connect(db_path, timeout=10) as db:
        return db.execute(
            "SELECT 1 FROM cv_quiz_attempts WHERE student_id=? AND status='active' LIMIT 1",
            (student_id,),
        ).fetchone() is not None


def learning_router(
    db_path: str | Path,
    get_student_id: Callable,
    chat_reply: Callable[[str, str, str], Awaitable[str]] | None = None,
) -> APIRouter:
    """get_student_id MUST be a FastAPI dependency validated using existing session_id cookie.

    chat_reply(lesson_id, lesson_title, learner_question) is an async adapter for
    the EXISTING AI model provider. Do not send client-authored tutor instructions to it.
    """
    router = APIRouter(prefix='/api/learning', tags=['Learning'])
    db_path = str(Path(db_path).resolve())

    def connect():
        db = sqlite3.connect(db_path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA busy_timeout=5000')
        return db

    def require_lesson(lesson_id):
        if lesson_id not in LESSON_IDS:
            raise HTTPException(404, 'Unknown lesson')

    def unlocked(db, student_id, lesson_id):
        # The official pre-test gates ALL lessons, including T001.
        benchmark_done = db.execute(
            """SELECT 1 FROM pre_assessment_attempts
               WHERE student_id=? AND status='submitted'
               LIMIT 1""",
            (student_id,),
        ).fetchone()
        if benchmark_done is None:
            return False

        idx = LESSON_IDS.index(lesson_id)
        if idx == 0:
            return True
        previous = db.execute(
            'SELECT passed_at FROM cv_lesson_progress WHERE student_id=? AND lesson_id=?',
            (student_id, LESSON_IDS[idx - 1]),
        ).fetchone()
        return bool(previous and previous['passed_at'])

    def check_no_active(db, student_id):
        if db.execute("SELECT 1 FROM cv_quiz_attempts WHERE student_id=? AND status='active'", (student_id,)).fetchone():
            raise HTTPException(423, 'Quiz active; AI tutoring and lesson navigation disabled')

    @router.get('/state')
    def state(student_id: int = Depends(get_student_id)):
        with connect() as db:
            progress_rows = db.execute('SELECT * FROM cv_lesson_progress WHERE student_id=?', (student_id,)).fetchall()
            attempt_rows = db.execute("SELECT lesson_id, COUNT(*) n FROM cv_quiz_attempts WHERE student_id=? AND status='submitted' GROUP BY lesson_id", (student_id,)).fetchall()
            active = db.execute("SELECT attempt_id, lesson_id FROM cv_quiz_attempts WHERE student_id=? AND status='active'", (student_id,)).fetchone()
            progress = {r['lesson_id']: dict(r) for r in progress_rows}
            counts = {r['lesson_id']: r['n'] for r in attempt_rows}
            return {
                'lessons': [
                    {'id': lid, 'title': title,
                     'unlocked': unlocked(db, student_id, lid),
                     'viewed': bool(progress.get(lid, {}).get('viewed_at')),
                     'passed': bool(progress.get(lid, {}).get('passed_at')),
                     'best_score': progress.get(lid, {}).get('best_score', 0),
                     'attempt_count': counts.get(lid, 0)}
                    for i, (lid, title) in enumerate(COURSE)
                ],
                'active_quiz': dict(active) if active else None,
            }

    @router.post('/viewed')
    def viewed(body: LessonViewed, student_id: int = Depends(get_student_id)):
        require_lesson(body.lesson_id)
        with connect() as db:
            check_no_active(db, student_id)
            if not unlocked(db, student_id, body.lesson_id):
                raise HTTPException(403, 'Pass the previous quiz first')
            db.execute('''INSERT INTO cv_lesson_progress (student_id,lesson_id,viewed_at)
                VALUES (?,?,CURRENT_TIMESTAMP) ON CONFLICT(student_id,lesson_id)
                DO UPDATE SET viewed_at=COALESCE(cv_lesson_progress.viewed_at, CURRENT_TIMESTAMP),
                updated_at=CURRENT_TIMESTAMP''', (student_id, body.lesson_id))
        return {'viewed': True}

    @router.post('/quiz/start')
    def start(body: QuizStart, student_id: int = Depends(get_student_id)):
        require_lesson(body.lesson_id)
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if not unlocked(db, student_id, body.lesson_id):
                raise HTTPException(403, 'Lesson locked')
            row = db.execute('SELECT viewed_at FROM cv_lesson_progress WHERE student_id=? AND lesson_id=?', (student_id, body.lesson_id)).fetchone()
            if not row or not row['viewed_at']:
                raise HTTPException(403, 'Finish studying the lesson before testing')
            existing = db.execute("SELECT attempt_id,lesson_id FROM cv_quiz_attempts WHERE student_id=? AND status='active'", (student_id,)).fetchone()
            if existing and existing['lesson_id'] != body.lesson_id:
                raise HTTPException(409, 'Finish or exit the existing quiz first')
            if existing:
                attempt_id = existing['attempt_id']
            else:
                cur = db.execute('INSERT INTO cv_quiz_attempts(student_id,lesson_id) VALUES (?,?)', (student_id,body.lesson_id))
                attempt_id = cur.lastrowid
        return {'attempt_id': attempt_id, 'lesson_id': body.lesson_id,
                'pass_percent': PASS_PERCENT,
                'questions': [{'question':q['question'], 'options':q['options']} for q in QUIZ_BANK[body.lesson_id]]}

    @router.post('/quiz/submit')
    def submit(body: QuizSubmit, student_id: int = Depends(get_student_id)):
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            attempt = db.execute("SELECT * FROM cv_quiz_attempts WHERE attempt_id=? AND student_id=? AND status='active'", (body.attempt_id,student_id)).fetchone()
            if attempt is None:
                raise HTTPException(404, 'Active quiz attempt not found')
            questions = QUIZ_BANK[attempt['lesson_id']]
            if len(body.answers)!=len(questions) or any(a < 0 or a >= len(q['options']) for a,q in zip(body.answers,questions)):
                raise HTTPException(422, 'Provide exactly one valid answer per question')
            correct = sum(a == q['correct'] for a,q in zip(body.answers,questions))
            score = round(100*correct/len(questions))
            passed = score >= PASS_PERCENT
            db.execute('''UPDATE cv_quiz_attempts SET finished_at=CURRENT_TIMESTAMP,
                correct_count=?,total_count=?,score_percent=?,passed=?,response_json=?,status='submitted'
                WHERE attempt_id=?''', (correct,len(questions),score,int(passed),json.dumps(body.answers),body.attempt_id))
            db.execute('''INSERT INTO cv_lesson_progress(student_id,lesson_id,best_score,passed_at)
                VALUES(?,?,?,CASE WHEN ? THEN CURRENT_TIMESTAMP ELSE NULL END)
                ON CONFLICT(student_id,lesson_id) DO UPDATE SET
                best_score=MAX(cv_lesson_progress.best_score, excluded.best_score),
                passed_at=COALESCE(cv_lesson_progress.passed_at,excluded.passed_at),updated_at=CURRENT_TIMESTAMP''',
                (student_id,attempt['lesson_id'],score,int(passed)))
        return {'lesson_id': attempt['lesson_id'], 'correct_count':correct, 'total_count':len(questions),
                'score_percent':score, 'passed':passed, 'pass_percent': PASS_PERCENT}

    @router.post('/quiz/abandon')
    def abandon(body: QuizAbandon, student_id: int = Depends(get_student_id)):
        with connect() as db:
            db.execute("UPDATE cv_quiz_attempts SET status='abandoned',finished_at=CURRENT_TIMESTAMP WHERE attempt_id=? AND student_id=? AND status='active'", (body.attempt_id,student_id))
        return {'abandoned':True}

    @router.post('/chat')
    async def chat(body: ChatQuestion, student_id: int = Depends(get_student_id)):
        require_lesson(body.lesson_id)
        with connect() as db:
            if not unlocked(db, student_id, body.lesson_id):
                raise HTTPException(403, 'Lesson locked')
            check_no_active(db, student_id)
        if chat_reply is None:
            raise HTTPException(503, 'AI provider not connected. Wire existing /chat model into chat_reply.')
        title = dict(COURSE)[body.lesson_id]
        answer = await chat_reply(body.lesson_id, title, body.message)
        if not isinstance(answer, str):
            raise HTTPException(502, 'AI provider returned invalid output')
        with connect() as db:
            # Check again so a quiz started during an AI call cannot receive a tutor answer.
            db.execute('BEGIN IMMEDIATE')
            check_no_active(db,student_id)
            db.execute('INSERT INTO cv_lesson_ai_interactions(student_id,lesson_id,question,answer) VALUES(?,?,?,?)',
                       (student_id,body.lesson_id,body.message,answer))
        return {'reply':answer}

    return router
