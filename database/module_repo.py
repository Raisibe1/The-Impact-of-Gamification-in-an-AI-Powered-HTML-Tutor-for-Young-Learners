from connection import Database


class ModuleRepository:

    def __init__(self):
        self.db = Database()

    # ---------------------------------------------------------
    # CREATE MODULE
    # ---------------------------------------------------------

    def create_module(
        self,
        title,
        description=None,
        difficulty_level=None,
        estimated_time=None,
        category=None,
        content_url=None
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO webdev_modules
            (
                title,
                description,
                difficulty_level,
                estimated_time,
                category,
                content_url
            )
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

        module_id = cursor.lastrowid

        conn.close()

        return module_id

    # ---------------------------------------------------------
    # GET MODULE BY ID
    # ---------------------------------------------------------

    def get_by_id(self, module_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM webdev_modules
            WHERE module_id = ?
        """, (module_id,))

        module = cursor.fetchone()

        conn.close()

        return module

    # ---------------------------------------------------------
    # GET MODULE BY TITLE
    # ---------------------------------------------------------

    def get_by_title(self, title):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM webdev_modules
            WHERE title = ?
        """, (title,))

        module = cursor.fetchone()

        conn.close()

        return module

    # ---------------------------------------------------------
    # GET ALL MODULES
    # ---------------------------------------------------------

    def get_all(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM webdev_modules
            ORDER BY module_id
        """)

        modules = cursor.fetchall()

        conn.close()

        return modules

    # ---------------------------------------------------------
    # GET MODULES BY CATEGORY
    # ---------------------------------------------------------

    def get_by_category(self, category):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM webdev_modules
            WHERE category = ?
            ORDER BY module_id
        """, (category,))

        modules = cursor.fetchall()

        conn.close()

        return modules

    # ---------------------------------------------------------
    # UPDATE MODULE
    # ---------------------------------------------------------

    def update_module(
        self,
        module_id,
        title=None,
        description=None,
        difficulty_level=None,
        estimated_time=None,
        category=None,
        content_url=None
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE webdev_modules
            SET
                title = COALESCE(?, title),
                description = COALESCE(?, description),
                difficulty_level = COALESCE(?, difficulty_level),
                estimated_time = COALESCE(?, estimated_time),
                category = COALESCE(?, category),
                content_url = COALESCE(?, content_url)
            WHERE module_id = ?
        """, (
            title,
            description,
            difficulty_level,
            estimated_time,
            category,
            content_url,
            module_id
        ))

        conn.commit()

        updated = cursor.rowcount

        conn.close()

        return updated

    # ---------------------------------------------------------
    # DELETE MODULE
    # ---------------------------------------------------------

    def delete_module(self, module_id):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM webdev_modules
            WHERE module_id = ?
        """, (module_id,))

        conn.commit()

        deleted = cursor.rowcount

        conn.close()

        return deleted