"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from database.connection import Database
from lessons import LESSON_CONTENT

def seed_lessons():
    db = Database()
    conn = db.get_connection()
    try:
        for lesson in LESSON_CONTENT:
            existing = conn.execute(
                "SELECT id FROM lessons WHERE slug = ?",
                (lesson["slug"],),
            ).fetchone()

            if existing is None:
                conn.execute(
                    """
                    INSERT INTO lessons (
                        slug, title, subtitle, description, icon,
                        order_index, xp_reward, is_locked
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        lesson["slug"],
                        lesson["title"],
                        lesson["subtitle"],
                        lesson["description"],
                        lesson["icon"],
                        lesson["order"],          # maps to order_index
                        lesson["xp_reward"],
                        0 if lesson["order"] == 1 else 1,
                    ),
                )
                print(f"[seed] inserted lesson: {lesson['slug']}")
            else:
                conn.execute(
                    """
                    UPDATE lessons
                       SET title       = ?,
                           subtitle    = ?,
                           description = ?,
                           icon        = ?,
                           order_index = ?,
                           xp_reward   = ?
                     WHERE slug        = ?
                    """,
                    (
                        lesson["title"],
                        lesson["subtitle"],
                        lesson["description"],
                        lesson["icon"],
                        lesson["order"],
                        lesson["xp_reward"],
                        lesson["slug"],
                    ),
                )

        conn.commit()
    finally:
        conn.close()


LESSON_SEED = [
    ("first-page","first-page","Challenge: Build Your First Page","HTML",0,88,1),
    ("html",           "HTML Foundations",   "Structure of the Web",   "HTML", 1, 40,  0),
    ("html-links",     "Portal Maker",       "You can link websites",  "🔗",   2, 50,  1),
    ("html-media",     "Media Lab",          "Images, audio and video","🖼️",  3, 50,  1),
    ("html-lists",     "Data Vault",         "Lists and tables",       "📊",   4, 50,  1),
    ("html-forms",     "Form Forge",         "Build accessible forms", "📝",   5, 50,  1),
    ("html-semantics", "Structure Sanctum",  "Semantic HTML layouts",  "🏛️",  6, 60,  1),
    ("journey",        "User Journeys",      "Investigations",         "JRN",  7, 200, 0),
    ("design",         "Design",             "Design on the Web",      "DSN",  8, 150, 0),
    ("css",            "CSS",                "Styling the Web",        "CSS",  9, 150, 0),
    ("js",             "JavaScript Logic",   "The Brain of the Web",   "JS",   10, 350, 0),
    ("react",          "React",              "Components and State",   "RCT",  11, 400, 1),
]

CHALLENGE_SEED = {

    "first-page":[(1,"first-page","Challenge: Build Your Website","code",40),
    ],
    "html": [
        (1, "first-page", "Challenge: Build Your First Page", "code", 40),
    ],
    "html-links": [
        (1, "html-links", "Create a linked Component", "code", 50),
        (2, "link-hub", "Boss Challenge: The Link Hub", "code", 50),
    ],
    "html-media": [
        (1, "media-showcase", "Boss Challenge: The Media Showcase", "code", 50),
    ],
    "html-lists": [
        (1, "leaderboard", "Boss Challenge: The Leaderboard", "code", 50),
    ],
    "html-forms": [
        (1, "guild-form", "Boss Challenge: Join the Build", "code", 50),
    ],
    "html-semantics": [
        (1, "semantic-layout", "Boss Challenge: Rebuild the Sanctum", "code", 50),
    ],
    "design": [
        (1, "visual-match", "Visual Design Match", "dragdrop", 25),
        (2, "goal-match", "User vs Site Goals", "matching", 25),
    ],
    "journey": [
        (1, "log", "Documentation Log", "reflection", 25),
        (2, "reflections", "Reflection and Review", "reflection", 15),
        (3, "final-reflections", "Learning Experience", "reflection", 25),
    ],
    "js": [
        (1, "js", "Write a Greeting function", "quiz", 15),
        (2, "step1", "What is JavaScript?", "quiz", 15),
        (3, "step2", "Variables", "code", 15),
        (4, "step3", "Data Types", "matching", 20),
        (5, "step4", "Operators and Conditionals", "code", 20),
        (6, "step5", "Functions", "code", 15),
        (7, "step6", "Arrays and Loops", "code", 15),
        (8, "step7", "DOM Manipulation", "reflection", 15),
        (9, "match-var", "Match Variables", "matching", 20),
        (10, "match-type", "Match Data Types", "matching", 20),
        (11, "match-op", "Match Operators", "matching", 20),
        (12, "dom-reflection", "DOM Reflection", "reflection", 15),
    ],
    "react": [
        (1, "welcome-component", "Create a React Component", "code", 100),
    ],
}

BADGE_SEED = [
    # (slug, name, description, icon, xp_bonus, criteria)
    ("html-lists","html-lists","Learn how to order data and set as lists","LL",66,"complete list challenge"),
    ("html-forms","html-forms","Learn how to input data into your site","HF",88,"create your form"),
    ("html-media","html-media","include videos and images into your website","HM",33,"images linked"),
    ("html-links","html-links","Know how to connect links","HL",33,"structured connections"),
    ("html",      "First Steps",      "Complete your first challenge.",              "STA", 10,  "complete_any_challenge"),
    ("css", "Design Detective", "Complete all Design challenges.",             "DSN", 25,  "complete_lesson:design"),
    ("code-wizard",      "Code Wizard",      "Complete all JavaScript challenges.",         "JS",  50,  "complete_lesson:javascript"),
    ("level-5",          "Rising Star",      "Reach Level 5.",                              "LVL", 20,  "reach_level:5"),
    ("streak-7",         "On Fire",          "Maintain a 7-day streak.",                    "STR", 30,  "streak:7"),
]

def seed_db(conn):
    for (slug, title, subtitle, icon, order_index, xp_reward, is_locked) in LESSON_SEED:
        conn.execute(
            """
            INSERT INTO lessons (slug, title, subtitle, icon, order_index, xp_reward, is_locked)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO NOTHING
            """,
            (slug, title, subtitle, icon, order_index, xp_reward, is_locked),
        )

    # Challenges - look up lesson_id by slug
    for lesson_slug, challenges in CHALLENGE_SEED.items():
        row = conn.execute(
            "SELECT id FROM lessons WHERE slug = ?", (lesson_slug,)
        ).fetchone()
        if not row:
            continue
        lesson_id = row["id"]
        for (step_number, slug, title, ctype, xp_reward) in challenges:
            conn.execute(
                """
                INSERT INTO challenges (lesson_id, slug, step_number, title, type, xp_reward)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(lesson_id, slug) DO NOTHING
                """,
                (lesson_id, slug, step_number, title, ctype, xp_reward),
            )

    # Badges
    for (slug, name, desc, icon, xp_bonus, criteria) in BADGE_SEED:
        conn.execute(
            """
            INSERT INTO badges (slug, name, description, icon, xp_bonus, criteria)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO NOTHING
            """,
            (slug, name, desc, icon, xp_bonus, criteria),
        )

def seed_legacy_games():
    db = Database()
    conn = db.get_connection()
    try:
        seed_db(conn)
        conn.commit()
    finally:
        conn.close()
