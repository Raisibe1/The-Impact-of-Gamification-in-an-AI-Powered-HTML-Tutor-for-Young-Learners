import sqlite3
import datetime

DB_NAME = "tutor.db"

conn = sqlite3.connect(DB_NAME, timeout=10)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# 1. STUDENTS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        school TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age_group TEXT,
        learning_style TEXT,
        password_hash TEXT NOT NULL,
        goal TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

# 2. WEBDEV_MODULES TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS webdev_modules (
        module_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        difficulty_level TEXT,
        estimated_time INTEGER,
        category TEXT,
        content_url TEXT
    )
""")

# 3. STUDENT_PROGRESS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS student_progress (
        progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        module_id INTEGER,
        status TEXT,
        attempts INTEGER DEFAULT 0,
        score REAL,
        time_spent INTEGER,
        completion_date TEXT,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id),
        FOREIGN KEY (module_id)
            REFERENCES webdev_modules(module_id)
    )
""")

# 4. CODE_SUBMISSIONS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS code_submissions (
        submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        module_id INTEGER,
        code_text TEXT,
        passed_tests INTEGER,
        error_log TEXT,
        language TEXT,
        timestamp TEXT,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id),
        FOREIGN KEY (module_id)
            REFERENCES webdev_modules(module_id)
    )
""")

# 5. PROJECTS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        title TEXT NOT NULL,
        code_url TEXT,
        dataset_id_used INTEGER,
        is_public BOOLEAN DEFAULT 0,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
    )
""")

# 6. BEHAVIORAL_DATA TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS behavioral_data (
        behavior_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        module_id INTEGER,
        time_on_lesson INTEGER,
        pauses INTEGER,
        replays_video BOOLEAN,
        code_runs INTEGER,
        errors_per_run INTEGER,
        time_to_fix_error INTEGER,
        hints_used INTEGER,
        skips INTEGER,
        abandon_rate REAL,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id),
        FOREIGN KEY (module_id)
            REFERENCES webdev_modules(module_id)
    )
""")

# 7. ENGAGEMENT_DATA TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS engagement_data (
        engagement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        login_frequency INTEGER,
        streak_days INTEGER,
        last_active TEXT,
        forum_questions INTEGER,
        help_requests INTEGER,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
    )
""")

# 8. PERFORMANCE_DATA TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS performance_data (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        quiz_scores TEXT,
        project_scores TEXT,
        rubric_breakdown TEXT,
        mistake_pattern TEXT,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
    )
""")

# 9. AI_INTERACTIONS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS ai_interactions (
        interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        module_id INTEGER,
        question_asked TEXT,
        hint_given TEXT,
        response_generated TEXT,
        resolved BOOLEAN,
        response_time INTEGER,
        timestamp TEXT,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id),
        FOREIGN KEY (module_id)
            REFERENCES webdev_modules(module_id)
    )
""")

# 10. MISTAKE_PATTERNS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS mistake_patterns (
        pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER,
        student_id INTEGER,
        module_id INTEGER,
        error_type TEXT,
        frequency INTEGER,
        pattern_description TEXT,
        FOREIGN KEY (submission_id)
            REFERENCES code_submissions(submission_id),
        FOREIGN KEY (student_id)
            REFERENCES students(student_id),
        FOREIGN KEY (module_id)
            REFERENCES webdev_modules(module_id)
    )
""")

# 11. DATASETS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        file_url TEXT,
        size TEXT
    )
""")

# 12. ML_MODELS TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS ml_models (
        model_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        framework TEXT,
        model_url TEXT,
        training_code_url TEXT,
        metrics_json TEXT,
        dataset_id INTEGER,
        FOREIGN KEY (dataset_id)
            REFERENCES datasets(dataset_id)
    )
""")

# 13. SESSION TABLE
c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        student_id INTEGER NOT NULL,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
            ON DELETE CASCADE
    )
""")

conn.commit()
conn.close()
print("Database and all tables created!")