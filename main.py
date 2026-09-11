import sqlite3

from connection import Database
from student_repo import StudentRepository
from progress_repo import ProgressRepository
from submission_repo import SubmissionRepository
from AI_repo import AIDataRepository
from module_repo import ModuleRepository

def main():

    print("=" * 60)
    print("THE MAGIC IS IN THE INVISIBLE")
    print("TUTOR DATABASE BACKEND TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. DATABASE CONNECTION
    # ---------------------------------------------------------

    print("\n[1] Testing database connection...")

    db = Database()
    conn = db.get_connection()

    print("Database connection successful!")
    conn.close()


    # ---------------------------------------------------------
    # 2. CREATE REPOSITORY OBJECTS
    # ---------------------------------------------------------

    print("\n[2] Creating repository objects...")

    student_repo = StudentRepository()
    module_repo = ModuleRepository()
    progress_repo = ProgressRepository()
    submission_repo = SubmissionRepository()
    ai_repo = AIDataRepository()

    print("All repositories loaded successfully!")


    # ---------------------------------------------------------
    # 3. CREATE STUDENT
    # ---------------------------------------------------------

    print("\n[3] Testing StudentRepository...")

    try:

        student_id = student_repo.create_student(
            name="Test Student",
            surname="Ndabezitha",
            school="SBHS",
            email="test@student.com",
            age_group="16-18",
            learning_style="visual",
            password="test_password",
            goal="excellence"
        )

        print("Student created!")
        print("Student ID:", student_id)

    except sqlite3.IntegrityError:

        print("Student already exists.")

        student = student_repo.get_by_email(email)

        if student:

            student_id = student["student_id"]

            print("Existing Student ID:", student_id)

        else:

            print("Could not find student.")
            return


    # ---------------------------------------------------------
    # 4. CREATE MODULE
    # ---------------------------------------------------------

    print("\n[4] Testing ModuleRepository...")

    module_id = module_repo.create_module(
        title="HTML Basics",
        description="Introduction to HTML",
        difficulty_level="beginner",
        estimated_time=30,
        category="Frontend",
        content_url="html-basics.html"
    )

    print("Module created!")
    print("Module ID:", module_id)


    # ---------------------------------------------------------
    # 5. CREATE PROGRESS
    # ---------------------------------------------------------

    print("\n[5] Testing ProgressRepository...")

    progress_id = progress_repo.create_progress(
        student_id=student_id,
        module_id=module_id,
        status="in_progress",
        attempts=1,
        score=75,
        time_spent=600
    )

    print("Progress record created!")
    print("Progress ID:", progress_id)


    # ---------------------------------------------------------
    # 6. CREATE CODE SUBMISSION
    # ---------------------------------------------------------

    print("\n[6] Testing SubmissionRepository...")

    submission_id = submission_repo.create_submission(
        student_id=student_id,
        module_id=module_id,
        code_text="<h1>Hello World</h1>",
        passed_tests=3,
        error_log=None,
        language="html"
    )

    print("Code submission created!")
    print("Submission ID:", submission_id)


    # ---------------------------------------------------------
    # 7. READ STUDENT PROGRESS
    # ---------------------------------------------------------

    print("\n[7] Reading student progress...")

    progress = progress_repo.get_student_progress(
        student_id
    )

    for record in progress:

        print(
            f"Module: {record['module_title']}"
        )

        print(
            f"Status: {record['status']}"
        )

        print(
            f"Score: {record['score']}"
        )

        print(
            f"Time spent: {record['time_spent']} seconds"
        )


    # ---------------------------------------------------------
    # 8. READ STUDENT SUBMISSIONS
    # ---------------------------------------------------------

    print("\n[8] Reading student submissions...")

    submissions = submission_repo.get_student_submissions(
        student_id
    )

    for submission in submissions:

        print(
            f"Language: {submission['language']}"
        )

        print(
            f"Code: {submission['code_text']}"
        )

        print(
            f"Tests passed: {submission['passed_tests']}"
        )


    # ---------------------------------------------------------
    # 9. AI REPOSITORY TEST
    # ---------------------------------------------------------

    print("\n[9] Testing AIRepository...")

    print("AI repository loaded successfully.")

    # We will test the actual AI repository methods
    # once we confirm exactly what methods you have inside it.

    print("\n" + "=" * 60)
    print("BACKEND TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()