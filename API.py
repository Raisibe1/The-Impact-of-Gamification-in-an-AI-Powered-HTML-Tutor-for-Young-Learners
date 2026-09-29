import secrets
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, Response, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from connection import Database
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash

app = FastAPI(title = "Your Tutor API")

app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

password_hash = PasswordHash.recommended()
session_len = 1

def create_session(student_id: int):
    db = Database()
    conn = db.get_connection()

    session_id = secrets.token_urlsafe(32)
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(hours=session_len)
    )

    try:
        # Remove expired sessions
        conn.execute(
            """
            DELETE FROM sessions
            WHERE expires_at < ?
            """,
            (
                datetime.now(timezone.utc).isoformat(),
            )
        )

        # Create new session
        conn.execute(
            """
            INSERT INTO sessions (
                session_id,
                student_id,
                expires_at
            )
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                student_id,
                expires_at.isoformat()
            )
        )

        conn.commit()

    finally:
        conn.close()

    return session_id

def set_session_cookie(response: Response,session_id: str):
    """
    Sends the session ID to the browser using
    a secure HttpOnly cookie.
    """
    response.set_cookie(
        key="session_id",
        value=session_id,

        # JavaScript cannot read this cookie
        httponly=True,

        # change this to True when using HTTPS
        secure=False,

        # Helps protect against CSRF
        samesite="lax",
        max_age=session_len * 60 * 60,
        path="/"
    )

class RegisterRequest(BaseModel):
    name: str
    surname: str
    school: str
    email: EmailStr
    password: str
    age_group: str | None = None
    learning_style: str | None = None
    goal: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/login")
def login(user: LoginRequest,response: Response):
    db = Database()
    conn = db.get_connection()

    try:
        student = conn.execute(
            """
            SELECT
                student_id,
                name,
                email,
                password_hash
            FROM students
            WHERE email = ?
            """,
            (user.email,)
        ).fetchone()

    finally:
        conn.close()

    if not student:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password!")

    #verify p/w
    isValid = password_hash.verify(user.password,student["password_hash"])

    if not isValid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password")
    
    #create session
    session_id = create_session(student["student_id"])
    set_session_cookie(response,session_id)

    return {
        "message": "Login successful.",
        "student": {
            "student_id": student["student_id"],
            "name": student["name"],
            "email": student["email"]
        }
    }

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="test.html"
       )

@app.get("/test")
def test(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="test.html"
       )

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html")

@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html")


@app.get("/program")
def program(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="program.html"
    )

@app.get("/tutor")
def tutor(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tutor.html"
    )

@app.get("/registration")
def registration(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="registration.html")

def get_current_student(request: Request):
    """
    Reads the 'session_id' cookie, validates it against the sessions table,
    and returns the matching student row (sqlite3.Row) or None.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None

    db = Database()
    conn = db.get_connection()
    try:
        row = conn.execute(
            """
            SELECT s.student_id
            FROM sessions s
            WHERE s.session_id = ?
              AND s.expires_at > ?
            """,
            (session_id, datetime.now(timezone.utc).isoformat()),
        ).fetchone()

        if row is None:
            return None

        student = conn.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (row["student_id"],),
        ).fetchone()

        return student  # sqlite3.Row or None
    finally:
        conn.close()

@app.get("/profile")
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
        

@app.post("/register")
def register(user: RegisterRequest,response: Response):
    db = Database()
    conn = db.get_connection()

    if len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters."
        )

    try:
        # Check whether email already exists
        existing_student = conn.execute(
            """
            SELECT student_id
            FROM students
            WHERE email = ?
            """,
            (user.email,)
        ).fetchone()

        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="Email is already registered."
            )

        hashed_password = password_hash.hash(user.password)

        # Create student
        cursor = conn.execute(
            """
            INSERT INTO students (
                name,
                surname,
                school,
                email,
                age_group,
                learning_style,
                password_hash,
                goal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.name,
                user.surname,
                user.school,
                user.email,
                user.age_group,
                user.learning_style,
                hashed_password,
                user.goal
            )
        )

        conn.commit()
        student_id = cursor.lastrowid

    finally:
        conn.close()

    session_id = create_session(student_id)
    set_session_cookie(response,session_id)

    return {
        "message": "Registration successful.",
        "student_id": student_id
    }


@app.get("/me/edit")
def edit_profile_page(request: Request):
    student = get_current_student(request)
    if student is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit_profile.html",
        context={"student": dict(student)},
    )


@app.post("/me/edit")
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
#python -m uvicorn API:app --reload