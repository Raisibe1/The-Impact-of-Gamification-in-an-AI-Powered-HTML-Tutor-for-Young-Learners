"""Apply additive migrations to the existing SQLite file. Back up DB before calling."""
from pathlib import Path
from database.connection import Database
HERE = Path(__file__).resolve().parent

def apply_migrations():
    conn = Database().get_connection()
    try:
        for path in sorted((HERE / 'migrations').glob('*.sql')):
            conn.executescript(path.read_text(encoding='utf-8'))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    apply_migrations()
    print('Additive database migrations applied.')
