from __future__ import annotations

from typing import Any, TypeAlias

from cryptid.data.init import Cursor, IntegrityError, is_unique_constraint_failed, transaction_with
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer, PartialExplorer

Row: TypeAlias = tuple[str, str, str]


@transaction_with(new_conn=False)
def _create_table(cursor: Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS explorer (
        name TEXT PRIMARY KEY,
        country TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)


_create_table()


def model_to_dict(explorer: Explorer) -> dict[str, Any]:
    return explorer.model_dump()


def row_to_model(row: Row) -> Explorer:
    name, country, description = row
    return Explorer(
        name=name,
        country=country,
        description=description,
    )


def create(cursor: Cursor, explorer: Explorer, *, fetch: bool = True) -> Explorer | None:
    sql = """
    INSERT INTO explorer (name, country, description)
    VALUES (:name, :country, :description)
    """
    try:
        cursor.execute(sql, model_to_dict(explorer))
    except IntegrityError as e:
        if is_unique_constraint_failed(e):
            raise EntityAlreadyExistsError(entity="explorer", key=explorer.name)
        raise e
    return get_one(cursor, explorer.name) if fetch else None


def get_all(cursor: Cursor) -> list[Explorer]:
    sql = """
    SELECT *
    FROM explorer
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(cursor: Cursor, name: str) -> Explorer:
    sql = """
    SELECT *
    FROM explorer
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if (row := cursor.fetchone()) is None:
        raise EntityNotFoundError(entity="explorer", key=name)
    return row_to_model(row)


def replace(cursor: Cursor, name: str, explorer: Explorer, *, fetch: bool = True) -> Explorer | None:
    sql = """
    UPDATE explorer
    SET name = :name,
        country = :country,
        description = :description
    WHERE name = :name_old
    """
    params = model_to_dict(explorer)
    params["name_old"] = name
    try:
        cursor.execute(sql, params)
    except IntegrityError as e:
        if is_unique_constraint_failed(e):
            raise EntityAlreadyExistsError(entity="explorer", key=explorer.name)
        raise e
    if cursor.rowcount == 0:
        raise EntityNotFoundError(entity="explorer", key=name)
    return get_one(cursor, explorer.name) if fetch else None


def modify(cursor: Cursor, name: str, explorer: PartialExplorer, *, fetch: bool = True) -> Explorer | None:
    updated = update_model(get_one(cursor, name), explorer)
    return replace(cursor, name, updated, fetch=fetch)


def update_model(explorer: Explorer, update: PartialExplorer) -> Explorer:
    update_dict = update.model_dump(exclude_unset=True)
    return explorer.model_copy(update=update_dict)


def delete(cursor: Cursor, name: str) -> None:
    sql = """
    DELETE FROM explorer
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount == 0:
        raise EntityNotFoundError(entity="explorer", key=name)
