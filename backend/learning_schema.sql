-- Additive schema only: do not drop or recreate existing students/users tables.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS cv_lesson_progress (
  student_id INTEGER NOT NULL,
  lesson_id TEXT NOT NULL,
  viewed_at TEXT,
  passed_at TEXT,
  best_score INTEGER NOT NULL DEFAULT 0 CHECK(best_score BETWEEN 0 AND 100),
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(student_id, lesson_id)
);
CREATE TABLE IF NOT EXISTS cv_quiz_attempts (
  attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  lesson_id TEXT NOT NULL,
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT,
  correct_count INTEGER,
  total_count INTEGER,
  score_percent INTEGER CHECK(score_percent BETWEEN 0 AND 100),
  passed INTEGER CHECK(passed IN (0,1)),
  response_json TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','submitted','abandoned'))
);
CREATE INDEX IF NOT EXISTS ix_cv_quiz_student_lesson ON cv_quiz_attempts(student_id,lesson_id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_cv_active_quiz_per_student ON cv_quiz_attempts(student_id) WHERE status='active';
CREATE TABLE IF NOT EXISTS cv_lesson_ai_interactions (
  interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  lesson_id TEXT NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_cv_chat_student_lesson ON cv_lesson_ai_interactions(student_id,lesson_id);
