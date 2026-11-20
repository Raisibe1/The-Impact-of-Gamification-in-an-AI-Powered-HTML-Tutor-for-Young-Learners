"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
import secrets
from datetime import datetime, timezone, timedelta
from fastapi import Request, Response, HTTPException
from pwdlib import PasswordHash
from database.connection import Database
from core.config import SESSION_HOURS, COOKIE_SECURE
password_hash = PasswordHash.recommended()
session_len = SESSION_HOURS

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
        secure=COOKIE_SECURE,

        # Helps protect against CSRF
        samesite="lax",
        max_age=session_len * 60 * 60,
        path="/"
    )


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


def require_student_id(request: Request) -> int:
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail='Please log in to continue')
    return int(student['student_id'])
