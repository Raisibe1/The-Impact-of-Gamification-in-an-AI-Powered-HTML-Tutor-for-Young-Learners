from connection import Database


class StudentRepository:

    def __init__(self):
        self.db = Database()

    def create_student(
        self,
        name,
        email,
        password,
        age_group=None,
        learning_style=None
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (name, email, password, age_group, learning_style, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            name,
            email,
            password,
            age_group,
            learning_style
        ))

        conn.commit()
        student_id = cursor.lastrowid
        conn.close()
        return student_id

    def get_by_email(self, email):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM students
            WHERE email = ?
        """, (email,))

        student = cursor.fetchone()
        conn.close()

        return student