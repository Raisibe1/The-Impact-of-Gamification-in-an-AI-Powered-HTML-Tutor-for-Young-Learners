"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from fastapi import Request, HTTPException
from database.connection import Database
from core.security import get_current_student

def require_completed_benchmark(student_id: int):
    db = Database()
    conn = db.get_connection()

    try:
        completed = conn.execute(
            """
            SELECT 1
            FROM benchmark_attempts
            WHERE student_id = ?
              AND assessment_type = 'pre'
              AND status = 'submitted'
            LIMIT 1
            """,
            (student_id,)
        ).fetchone()

        if completed is None:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Complete your HTML benchmark "
                    "before accessing lessons."
                )
            )

        return True

    finally:
        conn.close()


def _assessment_student(request: Request) -> int:
    student = get_current_student(request)
    if student is None:
        raise HTTPException(401, 'Please log in to use assessments.')
    return int(student['student_id'])


def _require_course_complete(conn, student_id: int):
    passed = conn.execute('''SELECT COUNT(*) FROM cv_lesson_progress
        WHERE student_id=? AND lesson_id IN
        ('T001','T002','T003','T004','T005','T006','T007','T008','T009','T010')
        AND passed_at IS NOT NULL''', (student_id,)).fetchone()[0]
    if passed != 10:
        raise HTTPException(403, 'Complete all ten lesson quizzes before taking the final assessment.')
