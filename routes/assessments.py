"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
import json
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request, HTTPException
from database.connection import Database
from schemas.assessments import BenchmarkSubmitRequest, PreAssessmentSubmission, FinalAssessmentSubmission
from services.assessment_service import require_completed_benchmark, _assessment_student, _require_course_complete
from services.grading_service import BENCHMARK_MCQ_KEY, _PRE_ANSWERS, _PRE_BACKGROUNDS, _FINAL_MCQ_ANSWERS
from core.security import (get_current_student, create_session,set_session_cookie, password_hash)


router = APIRouter(tags=['Assessments'])

@router.get('/api/benchmark/status')
def benchmark_status(request: Request):

    student = get_current_student(request)
    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Please log in to access the benchmark."
        )

    student_id = student["student_id"]
    db = Database()
    conn = db.get_connection()

    try:
        #get the learner's pre-test record
        pre_test = conn.execute(
            """
            SELECT
                attempt_id,
                status,
                mcq_score,
                practical_score,
                total_score,
                submitted_at
            FROM benchmark_attempts
            WHERE student_id = ?
              AND assessment_type = 'pre'
            """,
            (student_id,)
        ).fetchone()

        #Check assessment completion
        completed = (
            pre_test is not None
            and pre_test["status"] == "submitted"
        )

        return {
            "student_id": student_id,
            "pre_test_completed": completed,
            "lessons_unlocked": completed,
            "pre_test": {
                "attempt_id": pre_test["attempt_id"],
                "status": pre_test["status"],
                "mcq_score": pre_test["mcq_score"],
                "practical_score": pre_test["practical_score"],
                "total_score": pre_test["total_score"],
                "submitted_at": pre_test["submitted_at"]
            } if pre_test else None
        }

    finally:
        conn.close()


@router.post('/api/benchmark/start')
def start_benchmark(request: Request):
    student = get_current_student(request)

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Please log in to start the benchmark."
        )

    student_id = student["student_id"]
    db = Database()
    conn = db.get_connection()

    try:
        # Create only one official pre-test per learner.
        conn.execute(
            """
            INSERT OR IGNORE INTO benchmark_attempts
                (student_id, assessment_type, status, started_at)
            VALUES (?, 'pre', 'in_progress', ?)
            """,
            (
                student_id,
                datetime.now(timezone.utc).isoformat()
            )
        )

        conn.commit()
        attempt = conn.execute(
            """
            SELECT attempt_id, status, started_at
            FROM benchmark_attempts
            WHERE student_id = ?
              AND assessment_type = 'pre'
            """,
            (student_id,)
        ).fetchone()

        if attempt is None:
            raise HTTPException(
                status_code=500,
                detail="Unable to create benchmark."
            )

        if attempt["status"] == "submitted":
            raise HTTPException(
                status_code=409,
                detail="You have already submitted your pre-test."
            )

        started_at = datetime.fromisoformat(
            attempt["started_at"]
        )

        if started_at.tzinfo is None:
            started_at = started_at.replace(
                tzinfo=timezone.utc
            )

        deadline = started_at + timedelta(minutes=30)
        now = datetime.now(timezone.utc)

        if attempt["status"] == "expired" or now >= deadline:

            if attempt["status"] == "in_progress":
                conn.execute(
                    """
                    UPDATE benchmark_attempts
                    SET status = 'expired'
                    WHERE attempt_id = ?
                      AND status = 'in_progress'
                    """,
                    (attempt["attempt_id"],)
                )
                conn.commit()

            raise HTTPException(
                status_code=410,
                detail="Your benchmark session has expired."
            )

        return {
            "message": "Benchmark session ready.",
            "attempt_id": attempt["attempt_id"],
            "student_id": student_id,
            "assessment_type": "pre",
            "status": "in_progress",
            "started_at": started_at.isoformat(),
            "expires_at": deadline.isoformat(),
            "time_remaining_seconds": max(
                0, int((deadline - now).total_seconds())
            )
        }

    finally:
        conn.close()


@router.post('/api/benchmark/submit')
def submit_benchmark(
    request: Request,
    payload: BenchmarkSubmitRequest
):
    student = get_current_student(request)
    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Please log in."
        )

    student_id = student["student_id"]
    now = datetime.now(timezone.utc)

    # Validate the question IDs.
    valid_mcq = {str(i) for i in range(1, 41)}
    valid_text = {str(i) for i in range(41, 51)}

    if not set(payload.answers).issubset(valid_mcq):
        raise HTTPException(
            status_code=422,
            detail="Invalid multiple-choice question ID."
        )

    if not set(payload.text_answers).issubset(valid_text):
        raise HTTPException(
            status_code=422,
            detail="Invalid practical question ID."
        )

    if any(
        len(answer) > 10000
        for answer in payload.text_answers.values()
    ):
        raise HTTPException(
            status_code=422,
            detail="A practical answer is too long."
        )

    db = Database()
    conn = db.get_connection()

    try:
        # Acquire a write lock to prevent concurrent
        # submissions from both being accepted.
        conn.execute("BEGIN IMMEDIATE")

        attempt = conn.execute(
            """
            SELECT attempt_id, status, started_at
            FROM benchmark_attempts
            WHERE attempt_id = ?
              AND student_id = ?
              AND assessment_type = 'pre'
            """,
            (payload.attempt_id, student_id)
        ).fetchone()

        if attempt is None:
            raise HTTPException(
                status_code=404,
                detail="Benchmark attempt not found."
            )

        if attempt["status"] != "in_progress":
            raise HTTPException(
                status_code=409,
                detail="Benchmark is no longer active."
            )

        started = datetime.fromisoformat(
            attempt["started_at"]
        )

        if started.tzinfo is None:
            started = started.replace(
                tzinfo=timezone.utc
            )

        deadline = started + timedelta(minutes=30)

        if now >= deadline:
            conn.execute(
                """
                UPDATE benchmark_attempts
                SET status = 'expired'
                WHERE attempt_id = ?
                """,
                (payload.attempt_id,)
            )
            conn.commit()

            raise HTTPException(
                status_code=410,
                detail="Benchmark time has expired."
            )

        # Missing MCQ answers score zero.
        mcq_score = sum(
            payload.answers.get(str(number))
            == correct
            for number, correct
            in BENCHMARK_MCQ_KEY.items()
        )

        saved_answers = json.dumps({
            "mcq": payload.answers,
            "practical": payload.text_answers
        })

        conn.execute(
            """
            UPDATE benchmark_attempts
            SET
                answers_json = ?,
                mcq_score = ?,
                practical_score = NULL,
                total_score = NULL,
                status = 'submitted',
                submitted_at = ?,
                time_spent_seconds = ?
            WHERE attempt_id = ?
            """,
            (
                saved_answers,
                mcq_score,
                now.isoformat(),
                max(0, int(
                    (now - started).total_seconds()
                )),
                payload.attempt_id
            )
        )

        conn.commit()

        return {
            "message": "Benchmark submitted successfully.",
            "attempt_id": payload.attempt_id,
            "status": "submitted",
            "mcq_score": mcq_score,
            "mcq_total": 40,
            "practical_score": None,
            "total_score": None,
            "grading_status": "pending_review",
            "pre_test_completed": True,
            "lessons_unlocked": True
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


@router.get('/api/pre-assessment/status')
def pre_assessment_status(request: Request):
    sid = _assessment_student(request)
    db = Database()
    conn = db.get_connection()
    try:
        row = conn.execute('''SELECT attempt_id, score, submitted_at FROM pre_assessment_attempts
                              WHERE student_id=? AND status='submitted' ''', (sid,)).fetchone()
        completed = row is not None
        return {
            'student_id': sid,
            'pre_test_completed': completed,
            'lessons_unlocked': completed,
            'pre_test': dict(row) if row else None,
        }
    finally:
        conn.close()


@router.post('/api/pre-assessment/submit')
def pre_assessment_submit(request: Request, payload: PreAssessmentSubmission):
    sid = _assessment_student(request)
    if payload.background not in _PRE_BACKGROUNDS:
        raise HTTPException(422, 'Select one valid background response.')
    if set(payload.answers) != set(_PRE_ANSWERS):
        raise HTTPException(422, 'Answer all ten HTML diagnostic questions (2 through 11).')
    score = sum(payload.answers[n] == correct for n, correct in _PRE_ANSWERS.items())
    db = Database()
    conn = db.get_connection()
    try:
        conn.execute('BEGIN IMMEDIATE')
        if conn.execute('SELECT 1 FROM pre_assessment_attempts WHERE student_id=?', (sid,)).fetchone():
            raise HTTPException(409, 'Your official diagnostic has already been submitted.')
        now = datetime.now(timezone.utc).isoformat()
        cur = conn.execute('''INSERT INTO pre_assessment_attempts
            (student_id, background, answers_json, score, status, submitted_at)
            VALUES (?,?,?,?, 'submitted', ?)''',
            (sid, payload.background, json.dumps(payload.answers), score, now))
        conn.commit()
        return {'attempt_id': cur.lastrowid, 'status': 'submitted', 'score': score,
                'total': 10, 'pre_test_completed': True, 'lessons_unlocked': True}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@router.get('/api/final-assessment/status')
def final_assessment_status(request: Request):
    sid = _assessment_student(request)
    db = Database()
    conn = db.get_connection()
    try:
        row = conn.execute('''SELECT attempt_id, status, mcq_score, practical_score,
            total_score, submitted_at FROM benchmark_attempts
            WHERE student_id=? AND assessment_type='post' ''', (sid,)).fetchone()
        return {'final_test_completed': bool(row and row['status'] == 'submitted'),
                'final_test': dict(row) if row else None}
    finally:
        conn.close()


@router.post('/api/final-assessment/start')
def final_assessment_start(request: Request):
    sid = _assessment_student(request)
    db = Database()
    conn = db.get_connection()
    try:
        conn.execute('BEGIN IMMEDIATE')
        _require_course_complete(conn, sid)
        now = datetime.now(timezone.utc)
        conn.execute('''INSERT OR IGNORE INTO benchmark_attempts
            (student_id, assessment_type, status, started_at)
            VALUES (?, 'post', 'in_progress', ?)''', (sid, now.isoformat()))
        attempt = conn.execute('''SELECT attempt_id, status, started_at
            FROM benchmark_attempts WHERE student_id=? AND assessment_type='post' ''', (sid,)).fetchone()
        started = datetime.fromisoformat(attempt['started_at'])
        if started.tzinfo is None: started = started.replace(tzinfo=timezone.utc)
        deadline = started + timedelta(minutes=30)
        if attempt['status'] == 'submitted':
            raise HTTPException(409, 'Your official final assessment has already been submitted.')
        if attempt['status'] == 'expired' or now >= deadline:
            conn.execute("UPDATE benchmark_attempts SET status='expired' WHERE attempt_id=?", (attempt['attempt_id'],))
            conn.commit()
            raise HTTPException(410, 'Your final assessment session has expired.')
        conn.commit()
        return {'attempt_id': attempt['attempt_id'], 'status': 'in_progress',
                'assessment_type': 'post', 'started_at': started.isoformat(),
                'expires_at': deadline.isoformat(),
                'time_remaining_seconds': max(0, int((deadline-now).total_seconds()))}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@router.post('/api/final-assessment/submit')
def final_assessment_submit(request: Request, payload: FinalAssessmentSubmission):
    sid = _assessment_student(request)
    if not set(payload.answers).issubset({str(i) for i in range(1,41)}):
        raise HTTPException(422, 'Invalid multiple-choice question ID.')
    if not set(payload.text_answers).issubset({str(i) for i in range(41,51)}):
        raise HTTPException(422, 'Invalid written question ID.')
    if any(len(s)>10000 for s in payload.text_answers.values()):
        raise HTTPException(422, 'A written answer exceeds the length limit.')
    db = Database()
    conn = db.get_connection()
    try:
        conn.execute('BEGIN IMMEDIATE')
        _require_course_complete(conn, sid)
        attempt = conn.execute('''SELECT attempt_id,status,started_at FROM benchmark_attempts
            WHERE attempt_id=? AND student_id=? AND assessment_type='post' ''',
            (payload.attempt_id,sid)).fetchone()
        if not attempt: raise HTTPException(404, 'Final assessment attempt not found.')
        if attempt['status'] != 'in_progress': raise HTTPException(409, 'Final assessment is no longer active.')
        started = datetime.fromisoformat(attempt['started_at'])
        if started.tzinfo is None: started = started.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if now >= started + timedelta(minutes=30):
            conn.execute("UPDATE benchmark_attempts SET status='expired' WHERE attempt_id=?", (payload.attempt_id,))
            conn.commit()
            raise HTTPException(410, 'Final assessment time has expired.')
        score = sum(payload.answers.get(str(n)) == answer for n,answer in _FINAL_MCQ_ANSWERS.items())
        conn.execute('''UPDATE benchmark_attempts SET answers_json=?, mcq_score=?,
            practical_score=NULL, total_score=NULL, status='submitted',
            submitted_at=?, time_spent_seconds=? WHERE attempt_id=?''',
            (json.dumps({'mcq':payload.answers,'practical':payload.text_answers}),
             score, now.isoformat(), int((now-started).total_seconds()), payload.attempt_id))
        conn.commit()
        return {'attempt_id': payload.attempt_id, 'status': 'submitted',
                'mcq_score': score, 'mcq_total': 40, 'practical_score': None,
                'total_score': None, 'grading_status':'pending_review',
                'final_test_completed': True}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
