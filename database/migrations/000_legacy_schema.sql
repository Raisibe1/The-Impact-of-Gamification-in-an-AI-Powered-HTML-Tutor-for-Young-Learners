-- Preserved schema, additive only.
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
    );

CREATE TABLE IF NOT EXISTS webdev_modules (
        module_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        difficulty_level TEXT,
        estimated_time INTEGER,
        category TEXT,
        content_url TEXT
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        title TEXT NOT NULL,
        code_url TEXT,
        dataset_id_used INTEGER,
        is_public BOOLEAN DEFAULT 0,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS performance_data (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        quiz_scores TEXT,
        project_scores TEXT,
        rubric_breakdown TEXT,
        mistake_pattern TEXT,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS datasets (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        file_url TEXT,
        size TEXT
    );

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
    );

CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        student_id INTEGER NOT NULL,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
            ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS lessons (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        slug          TEXT    NOT NULL UNIQUE,      -- e.g. 'javascript'
        title         TEXT    NOT NULL,             -- e.g. 'JavaScript'
        subtitle      TEXT,                         -- e.g. 'The Brain of the Web'
        description   TEXT,
        icon          TEXT,                         -- short label like 'JS'
        order_index   INTEGER NOT NULL,             -- 1..N for sorting
        xp_reward     INTEGER NOT NULL DEFAULT 0,   -- XP for finishing the whole lesson
        is_locked     INTEGER NOT NULL DEFAULT 1,   -- 1 = locked until previous is done
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS challenges (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id     INTEGER NOT NULL,
    slug          TEXT    NOT NULL,             -- e.g. 'js-step-2-vars'
    step_number   INTEGER NOT NULL,             -- 1..N within the lesson
    title         TEXT    NOT NULL,
    type          TEXT    NOT NULL,             -- see comment above
    prompt        TEXT,
    xp_reward     INTEGER NOT NULL DEFAULT 15,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    UNIQUE (lesson_id, slug)
    );

CREATE TABLE IF NOT EXISTS badges (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT    NOT NULL UNIQUE,      -- e.g. 'code-wizard'
    name          TEXT    NOT NULL,             -- e.g. 'Code Wizard'
    description   TEXT,
    icon          TEXT,                         -- short label like 'WIZ'
    xp_bonus      INTEGER NOT NULL DEFAULT 0,
    criteria      TEXT,                         -- human-readable rule
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS user_progress (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id           INTEGER NOT NULL,
    challenge_id      INTEGER ,
    lesson_id         INTEGER NOT NULL,          -- denormalized for fast lookups
    completed         INTEGER NOT NULL DEFAULT 0,
    score             INTEGER DEFAULT 0,         -- optional: 0-100
    attempts          INTEGER NOT NULL DEFAULT 0,
    response_data     TEXT,                      -- JSON blob: reflections, drop data, etc.
    first_started_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at      TIMESTAMP,
    updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id)      REFERENCES students(student_id)      ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id)    REFERENCES lessons(id)    ON DELETE CASCADE,
    UNIQUE (student_id, challenge_id)
    );

CREATE TABLE IF NOT EXISTS user_xp (
    student_id        INTEGER PRIMARY KEY,
    total_xp       INTEGER NOT NULL DEFAULT 0,
    level          INTEGER NOT NULL DEFAULT 1,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_active    DATE,                          -- YYYY-MM-DD for streak math
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS user_badges (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id     INTEGER NOT NULL,
    badge_id    INTEGER NOT NULL,
    earned_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id)  REFERENCES students(student_id)  ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE,
    UNIQUE (student_id, badge_id)
    );

CREATE TABLE IF NOT EXISTS xp_events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    amount       INTEGER NOT NULL,
    reason       TEXT,                           -- e.g. 'completed js-step-2-vars'
    challenge_id INTEGER,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id)      REFERENCES students(student_id)      ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS benchmark_attempts (
        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        assessment_type TEXT NOT NULL CHECK (assessment_type IN ('pre', 'post')),
        status TEXT NOT NULL DEFAULT 'in_progress'
            CHECK (status IN (
                'in_progress',
                'submitted',
                'expired'
            )),

        answers_json TEXT,
        mcq_score INTEGER,
        practical_score INTEGER,
        total_score INTEGER,
        started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        submitted_at TEXT,
        time_spent_seconds INTEGER,

        FOREIGN KEY (student_id)
            REFERENCES students(student_id)
            ON DELETE CASCADE,

        UNIQUE(student_id, assessment_type)
    );
