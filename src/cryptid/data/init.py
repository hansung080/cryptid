from __future__ import annotations

import os
from pathlib import Path
from sqlite3 import Connection, Cursor, IntegrityError, connect
from typing import Callable, Concatenate, ParamSpec, TypeAlias, TypeVar

__all__ = [
    "Connection",
    "Cursor",
    "IntegrityError",
    "database",
    "get_conn",
    "get_cursor",
    "is_unique_constraint_failed",
    "transaction",
    "transaction_with",
]

database: str | None = None
_conn: Connection | None = None


def _init_db(path: str | None = None, reset: bool = False):
    global database, _conn
    if _conn:
        if not reset:
            return
        _conn = None
    if not path:
        top_dir = Path(__file__).resolve().parents[3]
        db_dir = top_dir / "db"
        db_dir.mkdir(exist_ok=True)
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        path = os.getenv("CRYPTID_SQLITE_DB", db_path)

    # isolation_level=None, "DEFERRED" (default), "IMMEDIATE", "EXCLUSIVE"
    # - None: autocommit mode, in which every write SQL is committed immediately.
    # - DEFERRED: auto-transaction mode, in which a transaction acquires a write lock on first write.
    # - IMMEDIATE: auto-transaction mode, in which a transaction acquires a write lock on begin.
    # - EXCLUSIVE: auto-transaction mode, in which a transaction acquires a read/write lock on begin.
    # * Auto-transaction mode implicitly begins the `isolation_level` transaction on the first write SQL
    #   not in a transaction, and needs explicit COMMIT/ROLLBACK or the `with conn:` syntax to commit or rollback it.
    # * Explicit BEGIN <isolation_level>/COMMIT/ROLLBACK creates the <isolation_level> transaction
    #   regardless of the `isolation_level` argument.
    # * The `with conn:` syntax begins the `isolation_level` transaction if `isolation_level` is not None and
    #   not in a transaction, and commits or rollbacks it if `isolation_level` is not None.
    database = path
    _conn = connect(database, isolation_level="DEFERRED", check_same_thread=False)


_init_db()

# This is the rough implementation of sqlite3.Connection.ContextManager.
# class Connection:
#     def __enter__(self):
#         if self.isolation_level is not None and self.in_transaction == False:
#             self.execute("BEGIN")
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         if self.isolation_level is None:
#             return
#         if exc_type is None:
#             self.commit()
#         else:
#             self.rollback()


def get_conn(*, new: bool = False) -> Connection:
    if new:
        return connect(database, isolation_level="DEFERRED", check_same_thread=False)
    else:
        return _conn


def get_cursor(*, new_conn: bool = False) -> Cursor:
    return get_conn(new=new_conn).cursor()


P = ParamSpec("P")
R = TypeVar("R")
TxFunc: TypeAlias = Callable[Concatenate[Cursor, P], R]
TxWrapper: TypeAlias = Callable[P, R]


def transaction(func: TxFunc) -> TxWrapper:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        with get_conn() as conn:
            result = func(conn.cursor(), *args, **kwargs)
            return result
    return wrapper


def transaction_with(*, new_conn: bool) -> Callable[[TxFunc], TxWrapper]:
    def decorator(func: TxFunc) -> TxWrapper:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with get_conn(new=new_conn) as conn:
                result = func(conn.cursor(), *args, **kwargs)
                return result
        return wrapper
    return decorator


def is_unique_constraint_failed(error: IntegrityError) -> bool:
    return "UNIQUE constraint failed" in str(error)
