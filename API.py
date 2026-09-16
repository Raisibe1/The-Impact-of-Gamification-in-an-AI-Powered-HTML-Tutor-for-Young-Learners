import secrets
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, Response, HTTPException
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

#python -m uvicorn API:app --reload