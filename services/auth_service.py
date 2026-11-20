"""Reusable authentication primitives, re-exported for future service-level use."""
from core.security import (create_session, set_session_cookie, get_current_student,
                           require_student_id, password_hash)
