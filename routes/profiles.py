"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from database.connection import Database
from core.web import templates
from core.security import get_current_student
router = APIRouter(tags=['Profiles'])

@router.get('/profile')
def me(request: Request):
    # ---- identify current student via session cookie ----
    student = get_current_student(request)
    if student is None:
        return RedirectResponse("/login", status_code=303)

    student_id = student["student_id"]

    db = Database()
    conn = db.get_connection()
    try:
        # ---- module progress (joined with module titles) ----
        modules = conn.execute(
            """
            SELECT
                m.module_id,
                m.title,
                m.difficulty_level,
                m.category,
                p.status,
                p.attempts,
                p.score,
                p.time_spent
            FROM webdev_modules m
            LEFT JOIN student_progress p
                   ON p.module_id = m.module_id
                  AND p.student_id = ?
            ORDER BY m.module_id
            """,
            (student_id,),
        ).fetchall()

        total_modules       = len(modules)
        completed_modules   = sum(1 for m in modules if m["status"] == "completed")
        in_progress_modules = sum(1 for m in modules if m["status"] == "in_progress")
        completion_pct      = round(completed_modules / total_modules * 100) if total_modules else 0

        scored    = [m["score"] for m in modules if m["score"] is not None]
        avg_score = round(sum(scored) / len(scored)) if scored else 0
        total_time = sum(m["time_spent"] or 0 for m in modules)

        stats = {
            "total_modules":       total_modules,
            "completed_modules":   completed_modules,
            "in_progress_modules": in_progress_modules,
            "completion_pct":      completion_pct,
            "avg_score":           avg_score,
            "total_time":          total_time,
        }

        # ---- engagement (latest row) ----
        eng_row = conn.execute(
            """
            SELECT * FROM engagement_data
            WHERE student_id = ?
            ORDER BY engagement_id DESC LIMIT 1
            """,
            (student_id,),
        ).fetchone()
        engagement = dict(eng_row) if eng_row else {
            "login_frequency": 0, "streak_days": 0, "last_active": None,
            "forum_questions": 0, "help_requests": 0,
        }

        # ---- behavioural data (latest row) ----
        beh_row = conn.execute(
            """
            SELECT * FROM behavioral_data
            WHERE student_id = ?
            ORDER BY behavior_id DESC LIMIT 1
            """,
            (student_id,),
        ).fetchone()
        behavior = dict(beh_row) if beh_row else {
            "time_on_lesson": 0, "pauses": 0, "replays_video": False,
            "code_runs": 0, "errors_per_run": 0, "time_to_fix_error": 0,
            "hints_used": 0, "skips": 0, "abandon_rate": 0.0,
        }

        # ---- recent submissions ----
        # NOTE: your schema has no 'total_tests' column, so we compute a rough
        # total from passed_tests (adjust if you later add a real column).
        submissions_rows = conn.execute(
            """
            SELECT s.submission_id, s.language, s.passed_tests, s.timestamp,
                   m.title AS module_title
            FROM code_submissions s
            LEFT JOIN webdev_modules m ON m.module_id = s.module_id
            WHERE s.student_id = ?
            ORDER BY s.timestamp DESC
            LIMIT 5
            """,
            (student_id,),
        ).fetchall()

        submissions = []
        for s in submissions_rows:
            d = dict(s)
            d["total_tests"] = max(d["passed_tests"] or 0, 1)
            submissions.append(d)

        # ---- mistake patterns ----
        mistakes = conn.execute(
            """
            SELECT error_type, frequency, pattern_description
            FROM mistake_patterns
            WHERE student_id = ?
            ORDER BY frequency DESC
            LIMIT 5
            """,
            (student_id,),
        ).fetchall()

        # ---- AI interactions ----
        ai_interactions = conn.execute(
            """
            SELECT question_asked, hint_given, response_generated,
                   resolved, response_time, timestamp
            FROM ai_interactions
            WHERE student_id = ?
            ORDER BY interaction_id DESC
            LIMIT 5
            """,
            (student_id,),
        ).fetchall()

        # ---- quiz score mini-chart (map module scores to bars) ----
        quiz_scores = [
            {"label": f"M{m['module_id']}", "score": int(m["score"])}
            for m in modules
            if m["score"] is not None
        ][-6:]

        performance = {
            "quizzes_passed":   completed_modules,
            "projects_pending": max(0, total_modules - completed_modules),
        }

        return templates.TemplateResponse(
            request=request,
            name="profile.html",
            context={
                "student":         dict(student),
                "stats":           stats,
                "engagement":      engagement,
                "behavior":        behavior,
                "modules":         [dict(m) for m in modules],
                "submissions":     submissions,
                "mistakes":        [dict(m) for m in mistakes],
                "ai_interactions": [dict(i) for i in ai_interactions],
                "quiz_scores":     quiz_scores,
                "performance":     performance,
            },
        )
    finally:
        conn.close()


@router.get('/me/edit')
def edit_profile_page(request: Request):
    student = get_current_student(request)
    if student is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit_profile.html",
        context={"student": dict(student)},
    )


@router.post('/me/edit')
def update_profile(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    school: str = Form(...),
    email: str = Form(...),
    age_group: str = Form(""),
    learning_style: str = Form(""),
    goal: str = Form(...),
):
    student = get_current_student(request)
    if student is None:
        return RedirectResponse("/login", status_code=303)

    student_id = student["student_id"]

    db = Database()
    conn = db.get_connection()
    try:
        # guard against email collisions (email is UNIQUE)
        existing = conn.execute(
            "SELECT student_id FROM students WHERE email = ? AND student_id != ?",
            (email.strip(), student_id),
        ).fetchone()

        if existing:
            return templates.TemplateResponse(
                request=request,
                name="edit_profile.html",
                context={
                    "student": dict(student),
                    "error": "That email is already in use by another account.",
                },
                status_code=400,
            )

        conn.execute(
            """
            UPDATE students
               SET name = ?,
                   surname = ?,
                   school = ?,
                   email = ?,
                   age_group = ?,
                   learning_style = ?,
                   goal = ?
             WHERE student_id = ?
            """,
            (
                name.strip(),
                surname.strip(),
                school.strip(),
                email.strip(),
                age_group.strip() or None,
                learning_style.strip() or None,
                goal.strip(),
                student_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return RedirectResponse("/profile", status_code=303)
