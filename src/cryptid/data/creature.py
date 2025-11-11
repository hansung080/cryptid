from __future__ import annotations

from typing import Any, TypeAlias

from cryptid.data.init import Cursor, IntegrityError, is_unique_constraint_failed, transaction_with
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.creature import Creature, PartialCreature

Row: TypeAlias = tuple[str, str, str, str, str]


@transaction_with(new_conn=False)
def _create_table(cursor: Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS creature (
        name TEXT PRIMARY KEY,
        country TEXT NOT NULL,
        area TEXT NOT NULL,
        description TEXT NOT NULL,
        aka TEXT NOT NULL
    )
    """)


_create_table()


def model_to_dict(creature: Creature) -> dict[str, Any]:
    return creature.model_dump()


def row_to_model(row: Row) -> Creature:
    name, country, area, description, aka = row
    return Creature(
        name=name,
        country=country,
        area=area,
        description=description,
        aka=aka,
    )


def create(cursor: Cursor, creature: Creature, *, fetch: bool = True) -> Creature | None:
    sql = """
    INSERT INTO creature (name, country, area, description, aka)
    VALUES (:name, :country, :area, :description, :aka)
    """
    try:
        cursor.execute(sql, model_to_dict(creature))
    except IntegrityError as e:
        if is_unique_constraint_failed(e):
            raise EntityAlreadyExistsError(entity="creature", key=creature.name)
        raise e
    return get_one(cursor, creature.name) if fetch else None


def get_all(cursor: Cursor) -> list[Creature]:
    sql = """
    SELECT *
    FROM creature
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(cursor: Cursor, name: str) -> Creature:
    sql = """
    SELECT *
    FROM creature
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if (row := cursor.fetchone()) is None:
        raise EntityNotFoundError(entity="creature", key=name)
    return row_to_model(row)


def replace(cursor: Cursor, name: str, creature: Creature, *, fetch: bool = True) -> Creature | None:
    sql = """
    UPDATE creature
    SET name = :name,
        country = :country,
        area = :area,
        description = :description,
        aka = :aka
    WHERE name = :name_old
    """
    params = model_to_dict(creature)
    params["name_old"] = name
    try:
        cursor.execute(sql, params)
    except IntegrityError as e:
        if is_unique_constraint_failed(e):
            raise EntityAlreadyExistsError(entity="creature", key=creature.name)
        raise e
    if cursor.rowcount == 0:
        raise EntityNotFoundError(entity="creature", key=name)
    return get_one(cursor, creature.name) if fetch else None


def modify(cursor: Cursor, name: str, creature: PartialCreature, *, fetch: bool = True) -> Creature | None:
    updated = update_model(get_one(cursor, name), creature)
    return replace(cursor, name, updated, fetch=fetch)


def update_model(creature: Creature, update: PartialCreature) -> Creature:
    update_dict = update.model_dump(exclude_unset=True)
    return creature.model_copy(update=update_dict)


def delete(cursor: Cursor, name: str) -> None:
    sql = """
    DELETE FROM creature
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount == 0:
        raise EntityNotFoundError(entity="creature", key=name)
