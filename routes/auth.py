"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from fastapi import APIRouter, Request, Response, HTTPException
from datetime import datetime, timezone
from database.connection import Database
from core.security import (get_current_student, create_session,set_session_cookie, password_hash)
from schemas.auth import RegisterRequest, LoginRequest
router = APIRouter(tags=['Authentication'])

@router.post('/login')
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


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(
        key="session_id",
        path="/",
        httponly=True,
        samesite="lax"
    )
    return {"message": "Logged out successfully"}


@router.post('/register')
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


@router.get('/api/me')
def get_me(request: Request):
    # This uses your existing helper function!
    student = get_current_student(request)
    
    if student is None:
        # If no valid session, return a 401 Unauthorized
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Return JSON data to React (excluding the password hash for security)
    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "surname": student["surname"],
        "email": student["email"],
        "school": student["school"],
        "age_group": student["age_group"],
        "learning_style": student["learning_style"],
        "goal": student["goal"]
    }
