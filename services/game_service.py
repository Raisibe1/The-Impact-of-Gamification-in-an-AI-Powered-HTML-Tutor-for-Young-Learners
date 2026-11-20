"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from datetime import datetime, timezone
from database.connection import Database

def _ensure_user_xp(conn, student_id: int) -> None:
    """Create a user_xp row if the student doesn't have one yet."""
    conn.execute(
        """
        INSERT OR IGNORE INTO user_xp
            (student_id, total_xp, level, current_streak, longest_streak, updated_at)
        VALUES (?, 0, 1, 0, 0, ?)
        """,
        (student_id, datetime.now(timezone.utc).isoformat()),
    )


def _resolve_challenge_id(conn, lesson_slug: str, challenge_slug: str | None):
    """Map (lesson_slug, challenge_slug) -> challenges.id, or None."""
    if not challenge_slug:
        return None

    row = conn.execute(
        """
        SELECT c.id
          FROM challenges c
          JOIN lessons l ON l.id = c.lesson_id
         WHERE l.slug = ? AND c.slug = ?
        """,
        (lesson_slug, challenge_slug),
    ).fetchone()

    if row is None:
        print(f"[warn] unknown challenge: lesson='{lesson_slug}' challenge='{challenge_slug}'")
        return None

    return row["id"] if row else None
