from connection import Database
import datetime


class SubmissionRepository:

    def __init__(self):
        self.db = Database()

    # ---------------------------------------------------------
    # CREATE CODE SUBMISSION
    # ---------------------------------------------------------

    def create_submission(
        self,
        student_id,
        module_id,
        code_text,
        passed_tests=None,
        error_log=None,
        language="python"
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO code_submissions
            (
                student_id,
                module_id,
                code_text,
                passed_tests,
                error_log,
                language,
                timestamp
            )
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

        submission_id = cursor.lastrowid

        conn.close()

        return submission_id

    # ---------------------------------------------------------
    # GET ONE SUBMISSION
    # ---------------------------------------------------------

    def get_submission(self, submission_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM code_submissions
            WHERE submission_id = ?
        """, (submission_id,))

        result = cursor.fetchone()

        conn.close()

        return result

    # ---------------------------------------------------------
    # GET ALL STUDENT SUBMISSIONS
    # ---------------------------------------------------------

    def get_student_submissions(self, student_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.*,
                m.title AS module_title
            FROM code_submissions s
            JOIN webdev_modules m
                ON s.module_id = m.module_id
            WHERE s.student_id = ?
            ORDER BY s.timestamp DESC
        """, (student_id,))

        results = cursor.fetchall()

        conn.close()

        return results

    # ---------------------------------------------------------
    # GET SUBMISSIONS FOR MODULE
    # ---------------------------------------------------------

    def get_module_submissions(
        self,
        student_id,
        module_id
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM code_submissions
            WHERE student_id = ?
            AND module_id = ?
            ORDER BY timestamp DESC
        """, (
            student_id,
            module_id
        ))

        results = cursor.fetchall()

        conn.close()

        return results

    # ---------------------------------------------------------
    # GET LATEST SUBMISSION
    # ---------------------------------------------------------

    def get_latest_submission(
        self,
        student_id,
        module_id
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM code_submissions
            WHERE student_id = ?
            AND module_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (
            student_id,
            module_id
        ))

        result = cursor.fetchone()

        conn.close()

        return result

    # ---------------------------------------------------------
    # UPDATE SUBMISSION
    # ---------------------------------------------------------

    def update_submission(
        self,
        submission_id,
        passed_tests=None,
        error_log=None
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE code_submissions
            SET
                passed_tests = COALESCE(?, passed_tests),
                error_log = COALESCE(?, error_log)
            WHERE submission_id = ?
        """, (
            passed_tests,
            error_log,
            submission_id
        ))

        conn.commit()

        updated = cursor.rowcount

        conn.close()

        return updated

    # ---------------------------------------------------------
    # DELETE SUBMISSION
    # ---------------------------------------------------------

    def delete_submission(self, submission_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM code_submissions
            WHERE submission_id = ?
        """, (submission_id,))

        conn.commit()

        deleted = cursor.rowcount

        conn.close()

        return deleted