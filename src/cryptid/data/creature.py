from typing import Any, TypeAlias

from cryptid.data.init import cursor, IntegrityError
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.creature import Creature, PartialCreature

cursor.execute("""
CREATE TABLE IF NOT EXISTS creature (
    name TEXT PRIMARY KEY,
    country TEXT NOT NULL,
    area TEXT NOT NULL,
    description TEXT NOT NULL,
    aka TEXT NOT NULL
)
""")

CreatureRow: TypeAlias = tuple[str, str, str, str, str]


def model_to_dict(creature: Creature) -> dict[str, Any]:
    return creature.model_dump()


def row_to_model(row: CreatureRow) -> Creature:
    name, country, area, description, aka = row
    return Creature(
        name=name,
        country=country,
        area=area,
        description=description,
        aka=aka,
    )


def create(creature: Creature, *, fetch: bool = True) -> Creature:
    sql = """
    INSERT INTO creature (name, country, area, description, aka)
    VALUES (:name, :country, :area, :description, :aka)
    """
    try:
        cursor.execute(sql, model_to_dict(creature))
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise EntityAlreadyExistsError(entity="creature", key=creature.name)
        else:
            raise e
    return get_one(creature.name) if fetch else creature


def get_all() -> list[Creature]:
    sql = """
    SELECT *
    FROM creature
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(name: str) -> Creature:
    sql = """
    SELECT *
    FROM creature
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if row := cursor.fetchone():
        return row_to_model(row)
    else:
        raise EntityNotFoundError(entity="creature", key=name)


def replace(name: str, creature: Creature, *, fetch: bool = True) -> Creature:
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
    cursor.execute(sql, params)
    if cursor.rowcount == 1:
        return get_one(creature.name) if fetch else creature
    else:
        raise EntityNotFoundError(entity="creature", key=name)


def modify(name: str, creature: PartialCreature, *, fetch: bool = True) -> Creature:
    updated = update_model(get_one(name), creature)
    return replace(name, updated, fetch=fetch)


def update_model(creature: Creature, update: PartialCreature) -> Creature:
    update_dict = update.model_dump(exclude_unset=True)
    return creature.model_copy(update=update_dict)


def delete(name: str) -> None:
    sql = """
    DELETE FROM creature
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount != 1:
        raise EntityNotFoundError(entity="creature", key=name)
