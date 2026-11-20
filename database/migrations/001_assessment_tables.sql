-- Additive migration: keep your existing tutor.db unchanged.
CREATE TABLE IF NOT EXISTS benchmark_attempts (
  attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  assessment_type TEXT NOT NULL CHECK(assessment_type IN ('pre','post')),
  status TEXT NOT NULL DEFAULT 'in_progress' CHECK(status IN ('in_progress','submitted','expired')),
  answers_json TEXT,
  mcq_score INTEGER,
  practical_score INTEGER,
  total_score INTEGER,
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  submitted_at TEXT,
  time_spent_seconds INTEGER,
  FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
  UNIQUE(student_id,assessment_type)
);
CREATE TABLE IF NOT EXISTS pre_assessment_attempts (
  attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL UNIQUE,
  background TEXT NOT NULL,
  answers_json TEXT NOT NULL,
  score INTEGER NOT NULL CHECK(score BETWEEN 0 AND 10),
  status TEXT NOT NULL DEFAULT 'submitted' CHECK(status='submitted'),
  submitted_at TEXT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
