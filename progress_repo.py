from connection import Database
import datetime


class ProgressRepository:

    def __init__(self):
        self.db = Database()

    # ---------------------------------------------------------
    # CREATE PROGRESS RECORD
    # ---------------------------------------------------------

    def create_progress(
        self,
        student_id,
        module_id,
        status,
        attempts=1,
        score=None,
        time_spent=None
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        completion_date = None

        if status == "completed":
            completion_date = datetime.datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO student_progress
            (
                student_id,
                module_id,
                status,
                attempts,
                score,
                time_spent,
                completion_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            module_id,
            status,
            attempts,
            score,
            time_spent,
            completion_date
        ))

        conn.commit()

        progress_id = cursor.lastrowid

        conn.close()

        return progress_id

    # ---------------------------------------------------------
    # GET ALL PROGRESS FOR A STUDENT
    # ---------------------------------------------------------

    def get_student_progress(self, student_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.*,
                m.title AS module_title
            FROM student_progress p
            JOIN webdev_modules m
                ON p.module_id = m.module_id
            WHERE p.student_id = ?
            ORDER BY p.completion_date DESC
        """, (student_id,))

        results = cursor.fetchall()

        conn.close()

        return results

    # ---------------------------------------------------------
    # GET PROGRESS FOR ONE MODULE
    # ---------------------------------------------------------

    def get_module_progress(
        self,
        student_id,
        module_id
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM student_progress
            WHERE student_id = ?
            AND module_id = ?
            ORDER BY progress_id DESC
        """, (
            student_id,
            module_id
        ))

        results = cursor.fetchall()

        conn.close()

        return results

    # ---------------------------------------------------------
    # GET LATEST PROGRESS
    # ---------------------------------------------------------

    def get_latest_progress(
        self,
        student_id,
        module_id
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM student_progress
            WHERE student_id = ?
            AND module_id = ?
            ORDER BY progress_id DESC
            LIMIT 1
        """, (
            student_id,
            module_id
        ))

        result = cursor.fetchone()

        conn.close()

        return result

    # ---------------------------------------------------------
    # UPDATE PROGRESS
    # ---------------------------------------------------------

    def update_progress(
        self,
        progress_id,
        status=None,
        attempts=None,
        score=None,
        time_spent=None
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE student_progress
            SET
                status = COALESCE(?, status),
                attempts = COALESCE(?, attempts),
                score = COALESCE(?, score),
                time_spent = COALESCE(?, time_spent),
                completion_date =
                    CASE
                        WHEN ? = 'completed'
                        THEN ?
                        ELSE completion_date
                    END
            WHERE progress_id = ?
        """, (
            status,
            attempts,
            score,
            time_spent,
            status,
            datetime.datetime.now().isoformat(),
            progress_id
        ))

        conn.commit()

        updated = cursor.rowcount

        conn.close()

        return updated

    # ---------------------------------------------------------
    # DELETE PROGRESS
    # ---------------------------------------------------------

    def delete_progress(self, progress_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM student_progress
            WHERE progress_id = ?
        """, (progress_id,))

        conn.commit()

        deleted = cursor.rowcount

        conn.close()

        return deleted