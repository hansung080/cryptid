import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

__all__ = ["conn", "cursor", "IntegrityError"]

conn: Connection | None = None
cursor: Cursor | None = None


def init_db(name: str | None = None, reset: bool = False):
    global conn, cursor
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        top_dir = Path(__file__).resolve().parents[3]
        db_dir = top_dir / "db"
        db_dir.mkdir(exist_ok=True)
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    conn = connect(name, check_same_thread=False, isolation_level=None)
    cursor = conn.cursor()


init_db()
