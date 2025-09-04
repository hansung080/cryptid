from cryptonamicon.data.init import cursor, IntegrityError
from cryptonamicon.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptonamicon.model.creature import Creature

cursor.execute("""
CREATE TABLE IF NOT EXISTS creature (
    name TEXT PRIMARY KEY,
    country TEXT,
    area TEXT,
    description TEXT,
    aka TEXT
)
""")


def row_to_model(row: tuple) -> Creature:
    name, country, area, description, aka = row
    return Creature(
        name=name,
        country=country,
        area=area,
        description=description,
        aka=aka,
    )


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def create(creature: Creature, select: bool = True) -> Creature:
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
    return get_one(creature.name) if select else creature


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
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise EntityNotFoundError(entity="creature", key=name)


def modify(name: str, creature: Creature, select: bool = True) -> Creature:
    sql = """
    UPDATE creature
    SET name = :name,
        country = :country,
        area = :area,
        description = :description,
        aka = :aka
    WHERE name = :k_name
    """
    params = model_to_dict(creature)
    params["k_name"] = name
    cursor.execute(sql, params)
    if cursor.rowcount == 1:
        return get_one(creature.name) if select else creature
    else:
        raise EntityNotFoundError(entity="creature", key=name)


def delete(name: str) -> None:
    sql = """
    DELETE FROM creature
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount != 1:
        raise EntityNotFoundError(entity="creature", key=name)
