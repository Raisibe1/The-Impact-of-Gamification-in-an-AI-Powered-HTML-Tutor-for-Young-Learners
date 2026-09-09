from connection import Database


class AIDataRepository:

    def __init__(self):
        self.db = Database()

    def get_student_features(self, student_id):

        conn = self.db.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                time_on_lesson,
                pauses,
                code_runs,
                errors_per_run,
                time_to_fix_error,
                hints_used,
                skips,
                abandon_rate
            FROM behavioral_data
            WHERE student_id = ?
        """, (student_id,))

        behavioral = cursor.fetchone()

        conn.close()

        return behavioral