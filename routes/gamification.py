"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from core.security import get_current_student
from database.connection import Database
from services.game_service import _ensure_user_xp, _resolve_challenge_id
from schemas.gamification import XPRequest, ProgressRequest, BadgeRequest
router = APIRouter(tags=['Gamification'])
XP_PER_LEVEL = 100

@router.get('/api/state')
def api_state(request: Request):
    """Return the full game state for the logged-in student."""
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sid = student["student_id"]
    db = Database()
    conn = db.get_connection()
    try:
        _ensure_user_xp(conn, sid)
        conn.commit()

        xp_row = conn.execute(
            """
            SELECT total_xp, level, current_streak, longest_streak, last_active
              FROM user_xp
             WHERE student_id = ?
            """,
            (sid,),
        ).fetchone()

        badges = conn.execute(
            """
            SELECT b.slug, b.name, b.description, b.icon, ub.earned_at
              FROM user_badges ub
              JOIN badges b ON b.id = ub.badge_id
             WHERE ub.student_id = ?
            """,
            (sid,),
        ).fetchall()

        progress = conn.execute(
            """
            SELECT l.slug AS lesson_slug,
                   c.slug AS challenge_slug,
                   up.completed,
                   up.score,
                   up.response_data,
                   up.attempts
              FROM user_progress up
              LEFT JOIN lessons    l ON l.id = up.lesson_id
              LEFT JOIN challenges c ON c.id = up.challenge_id
             WHERE up.student_id = ?
            """,
            (sid,),
        ).fetchall()

        return {
            "xp": dict(xp_row),
            "badges": [dict(b) for b in badges],
            "progress": [dict(p) for p in progress],
        }
    finally:
        conn.close()


@router.post('/api/xp')
def api_award_xp(request: Request, payload: XPRequest):
    """Insert an xp_event, add to user_xp.total_xp, recompute level."""
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sid = student["student_id"]
    db = Database()
    conn = db.get_connection()

    print("Trying to reward a student")
    print("---------------------------")
    print(payload.lesson_slug)
    print(payload.challenge_slug)
    print("-----------------------")
    try:
        challenge_id = _resolve_challenge_id(
            conn, payload.lesson_slug, payload.challenge_slug
        )

        if payload.challenge_slug and challenge_id is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown challenge '{payload.challenge_slug}' for lesson '{payload.lesson_slug}'"
            )
            
        now = datetime.now(timezone.utc).isoformat()

        _ensure_user_xp(conn, sid)

        conn.execute(
            """
            INSERT INTO xp_events (student_id, amount, reason, challenge_id, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sid, payload.amount, payload.reason, challenge_id, now),
        )

        conn.execute(
            """
            UPDATE user_xp
               SET total_xp = total_xp + ?,
                   updated_at = ?
             WHERE student_id = ?
            """,
            (payload.amount, now, sid),
        )

        row = conn.execute(
            "SELECT total_xp FROM user_xp WHERE student_id = ?", (sid,)
        ).fetchone()
        new_total = row["total_xp"]
        new_level = (new_total // XP_PER_LEVEL) + 1

        conn.execute(
            "UPDATE user_xp SET level = ? WHERE student_id = ?",
            (new_level, sid),
        )
        conn.commit()

        return {"total_xp": new_total, "level": new_level, "awarded": payload.amount}
    finally:
        conn.close()


@router.post('/api/progress')
def api_save_progress(request: Request, payload: ProgressRequest):
    """Upsert a row in user_progress for (student, lesson[, challenge])."""
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sid = student["student_id"]
    db = Database()
    conn = db.get_connection()
    print("Server looking for this slug!")
    print("----------------------------------")
    print(payload.lesson_slug)
    print(payload.challenge_slug)
    print("---------------------------------")
    
    try:
        lesson = conn.execute(
            "SELECT id FROM lessons WHERE slug = ?", (payload.lesson_slug,)
        ).fetchone()

        if not lesson:
            print("This lesson DO NOT EXIST, challenge?")
            print(payload.lesson_slug)
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        else:
            print("HERES WHATS |REAL")
            print(lesson)
            print(lesson["id"])


        lesson_id = lesson["id"]
        challenge = conn.execute(
            """
            SELECT id
            FROM challenges
            WHERE slug = ?
            """,
            (payload.challenge_slug,),
        ).fetchone()

        if challenge is None:
            print(payload.challenge_slug)
            print("AGAIN its not even a real challenge")
            raise HTTPException(
                status_code=404,
                detail=f"Challenge '{payload.challenge_slug}' not found for lesson '{payload.lesson_slug}'."
            )

        challenge_id = challenge["id"]
        now = datetime.now(timezone.utc).isoformat()

        existing = conn.execute(
            """
            SELECT id FROM user_progress
             WHERE student_id = ?
               AND lesson_id = ?
               AND (challenge_id IS ? OR challenge_id = ?)
            """,
            (sid, lesson_id, challenge_id, challenge_id),
        ).fetchone()

        if existing:
            conn.execute(
                """
                UPDATE user_progress
                   SET completed     = ?,
                       score         = COALESCE(?, score),
                       response_data = COALESCE(?, response_data),
                       attempts      = attempts + 1,
                       completed_at  = CASE WHEN ? = 1 THEN ? ELSE completed_at END,
                       updated_at    = ?
                 WHERE id = ?
                """,
                (
                    1 if payload.completed else 0,
                    payload.score,
                    payload.response_data,
                    1 if payload.completed else 0,
                    now,
                    now,
                    existing["id"],
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO user_progress
                    (student_id, challenge_id, lesson_id, completed, score,
                     attempts, response_data, first_started_at, completed_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
                """,
                (
                    sid,
                    challenge_id,
                    lesson_id,
                    1 if payload.completed else 0,
                    payload.score,
                    payload.response_data,
                    now,
                    now if payload.completed else None,
                    now,
                ),
            )

        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


@router.post('/api/badges/unlock')
def api_unlock_badge(request: Request, payload: BadgeRequest):
    """Award a badge by slug (idempotent — one user_badges row per badge)."""
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sid = student["student_id"]
    db = Database()
    conn = db.get_connection()
    try:
        badge = conn.execute(
            "SELECT id, name, description FROM badges WHERE slug = ?",
            (payload.slug,),
        ).fetchone()

        print("--S--L--U--G-------")
        print("select id, name, description from badges where slug = ?(payload.slug,)")
        print(payload.slug)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")

        already = conn.execute(
            "SELECT id FROM user_badges WHERE student_id = ? AND badge_id = ?",
            (sid, badge["id"]),
        ).fetchone()

        if already:
            return {"unlocked": False, "name": badge["name"]}

        conn.execute(
            """
            INSERT INTO user_badges (student_id, badge_id, earned_at)
            VALUES (?, ?, ?)
            """,
            (sid, badge["id"], datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return {
            "unlocked": True,
            "name": badge["name"],
            "description": badge["description"],
        }
    finally:
        conn.close()


@router.post('/api/reset')
def api_reset(request: Request):
    """Wipe the logged-in student's game state (dev / start-over)."""
    student = get_current_student(request)
    if student is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sid = student["student_id"]
    db = Database()
    conn = db.get_connection()
    try:
        conn.execute("DELETE FROM user_progress WHERE student_id = ?", (sid,))
        conn.execute("DELETE FROM user_badges   WHERE student_id = ?", (sid,))
        conn.execute("DELETE FROM xp_events     WHERE student_id = ?", (sid,))
        conn.execute(
            """
            UPDATE user_xp
               SET total_xp = 0, level = 1, current_streak = 0,
                   longest_streak = 0, updated_at = ?
             WHERE student_id = ?
            """,
            (datetime.now(timezone.utc).isoformat(), sid),
        )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()
