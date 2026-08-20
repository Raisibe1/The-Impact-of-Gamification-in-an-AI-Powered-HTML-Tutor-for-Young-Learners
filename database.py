import sqlite3
import datetime

DB_NAME = "tutor.db"

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():
    conn = get_connection()
    c = conn.cursor()

    # 1. STUDENTS TABLE
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age_group TEXT,
            learning_style TEXT,
            password TEXT NOT NULL,
            created_at TEXT
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

    conn.commit()
    conn.close()
    print("Database and all tables created!")


# ============================================================
# ADD STUDENT 
# ============================================================

def add_student(name, email, password, age_group=None, learning_style=None):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO students
        (name, email, password, age_group, learning_style, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        password,
        age_group,
        learning_style,
        datetime.datetime.now().isoformat()
    ))

    conn.commit()
    student_id = c.lastrowid
    conn.close()
    return student_id


# ============================================================
# ADD MODULE 
# ============================================================

def add_module(title, description=None, difficulty_level=None, 
               estimated_time=None, category=None, content_url=None):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO webdev_modules
        (title, description, difficulty_level, estimated_time, category, content_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        difficulty_level,
        estimated_time,
        category,
        content_url
    ))

    conn.commit()
    module_id = c.lastrowid
    conn.close()
    return module_id


# ============================================================
# LOG STUDENT PROGRESS
# ============================================================

def log_progress(student_id, module_id, status, attempts=1, score=None, time_spent=None):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO student_progress
        (student_id, module_id, status, attempts, score, time_spent, completion_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        module_id,
        status,
        attempts,
        score,
        time_spent,
        datetime.datetime.now().isoformat() if status == 'completed' else None
    ))

    conn.commit()
    conn.close()


# ============================================================
# LOG CODE SUBMISSION
# ============================================================

def log_code_submission(student_id, module_id, code_text, passed_tests=None, 
                        error_log=None, language="python"):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO code_submissions
        (student_id, module_id, code_text, passed_tests, error_log, language, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        module_id,
        code_text,
        passed_tests,
        error_log,
        language,
        datetime.datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# ============================================================
# LOG BEHAVIORAL DATA
# ============================================================

def log_behavioral_data(student_id, module_id, time_on_lesson=None, pauses=None,
                        replays_video=None, code_runs=None, errors_per_run=None,
                        time_to_fix_error=None, hints_used=None, skips=None,
                        abandon_rate=None):

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO behavioral_data
        (student_id, module_id, time_on_lesson, pauses, replays_video,
         code_runs, errors_per_run, time_to_fix_error, hints_used,
         skips, abandon_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        module_id,
        time_on_lesson,
        pauses,
        replays_video,
        code_runs,
        errors_per_run,
        time_to_fix_error,
        hints_used,
        skips,
        abandon_rate
    ))

    conn.commit()
    conn.close()


# ============================================================
# LOG AI INTERACTION
# ============================================================

def log_ai_interaction(student_id, module_id, question_asked, hint_given=None,
                       response_generated=None, resolved=False, response_time=None):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO ai_interactions
        (student_id, module_id, question_asked, hint_given,
         response_generated, resolved, response_time, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        module_id,
        question_asked,
        hint_given,
        response_generated,
        resolved,
        response_time,
        datetime.datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# ============================================================
# GET STUDENT BY EMAIL
# ============================================================

def get_student_by_email(email):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        SELECT * FROM students
        WHERE email = ?
    """, (email,))
    
    result = c.fetchone()
    conn.close()
    
    return result


# ============================================================
# GET MODULE BY TITLE
# ============================================================

def get_module_by_title(title):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        SELECT * FROM webdev_modules
        WHERE title = ?
    """, (title,))
    
    result = c.fetchone()
    conn.close()
    
    return result


# ============================================================
# GET STUDENT PROGRESS
# ============================================================

def get_student_progress(student_id):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        SELECT p.*, m.title as module_title
        FROM student_progress p
        JOIN webdev_modules m ON p.module_id = m.module_id
        WHERE p.student_id = ?
        ORDER BY p.completion_date DESC
    """, (student_id,))
    
    results = c.fetchall()
    conn.close()
    
    return results


# ============================================================
# GET STUDENT AI INTERACTIONS
# ============================================================

def get_student_ai_interactions(student_id, limit=10):
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        SELECT ai.*, m.title as module_title
        FROM ai_interactions ai
        JOIN webdev_modules m ON ai.module_id = m.module_id
        WHERE ai.student_id = ?
        ORDER BY ai.timestamp DESC
        LIMIT ?
    """, (student_id, limit))
    
    results = c.fetchall()
    conn.close()
    
    return results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_tables()

    # Create a test student
    try:
        student_id = add_student(
            name="Thabo Mokoena",
            email="thabo13@example.com",
            password="hashed_password_here",
            age_group="13-15",
            learning_style="visual"
        )
        print("New student ID:", student_id)

    except sqlite3.IntegrityError:
        print("Student already exists.")
        
        # Get the existing student
        student = get_student_by_email("thabo13@example.com")
        if student:
            student_id = student["student_id"]
            print(f"Found existing student: {student['name']} (ID: {student_id})")
        else:
            print("Error: Student not found!")
            exit()
    
    # Create a test module
    module_id = add_module(
        title="Introduction to HTML & CSS",
        description="Learn the basics of HTML structure and CSS styling",
        difficulty_level="beginner",
        estimated_time=45,
        category="Frontend",
        content_url="https://example.com/html-css-module"
    )
    print("Module ID:", module_id)

    # Log progress
    log_progress(
        student_id=student_id,
        module_id=module_id,
        status="in_progress",
        attempts=1,
        time_spent=600  # 10 minutes
    )
    print("Progress logged!")

    # Log a code submission
    log_code_submission(
        student_id=student_id,
        module_id=module_id,
        code_text="<div><h1>Hello World</h1></div>",
        passed_tests=3,
        language="html"
    )
    print("Code submission logged!")

    # Log behavioral data
    log_behavioral_data(
        student_id=student_id,
        module_id=module_id,
        time_on_lesson=600,
        pauses=2,
        replays_video=0,
        code_runs=5,
        errors_per_run=0,
        hints_used=1,
        skips=0
    )
    print("Behavioral data logged!")

    # Log an AI interaction
    log_ai_interaction(
        student_id=student_id,
        module_id=module_id,
        question_asked="How do I center a div?",
        hint_given="Try using margin: auto with a fixed width",
        response_generated="Here's how to center a div...",
        resolved=True,
        response_time=3
    )
    print("AI interaction logged!")

    print("\nAll test data successfully recorded!")
    print("\nDatabase schema includes all 12 tables from the specification.")