from typing import Any, TypeAlias

from cryptid.data.init import cursor, IntegrityError
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer, PartialExplorer

cursor.execute("""
CREATE TABLE IF NOT EXISTS explorer (
    name TEXT PRIMARY KEY,
    country TEXT NOT NULL,
    description TEXT NOT NULL
)
""")

ExplorerRow: TypeAlias = tuple[str, str, str]


def model_to_dict(explorer: Explorer) -> dict[str, Any]:
    return explorer.model_dump()


def row_to_model(row: ExplorerRow) -> Explorer:
    name, country, description = row
    return Explorer(
        name=name,
        country=country,
        description=description,
    )


def create(explorer: Explorer, *, fetch: bool = True) -> Explorer:
    sql = """
    INSERT INTO explorer (name, country, description)
    VALUES (:name, :country, :description)
    """
    try:
        cursor.execute(sql, model_to_dict(explorer))
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise EntityAlreadyExistsError(entity="explorer", key=explorer.name)
        else:
            raise e
    return get_one(explorer.name) if fetch else explorer


def get_all() -> list[Explorer]:
    sql = """
    SELECT *
    FROM explorer
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(name: str) -> Explorer:
    sql = """
    SELECT *
    FROM explorer
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if row := cursor.fetchone():
        return row_to_model(row)
    else:
        raise EntityNotFoundError(entity="explorer", key=name)


def replace(name: str, explorer: Explorer, *, fetch: bool = True) -> Explorer:
    sql = """
    UPDATE explorer
    SET name = :name,
        country = :country,
        description = :description
    WHERE name = :name_old
    """
    params = model_to_dict(explorer)
    params["name_old"] = name
    cursor.execute(sql, params)
    if cursor.rowcount == 1:
        return get_one(explorer.name) if fetch else explorer
    else:
        raise EntityNotFoundError(entity="explorer", key=name)


def modify(name: str, explorer: PartialExplorer, *, fetch: bool = True) -> Explorer:
    updated = update_model(get_one(name), explorer)
    return replace(name, updated, fetch=fetch)


def update_model(explorer: Explorer, update: PartialExplorer) -> Explorer:
    update_dict = update.model_dump(exclude_unset=True)
    return explorer.model_copy(update=update_dict)


def delete(name: str) -> None:
    sql = """
    DELETE FROM explorer
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount != 1:
        raise EntityNotFoundError(entity="explorer", key=name)
