from cryptonamicon.data.init import cursor, IntegrityError
from cryptonamicon.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptonamicon.model.explorer import Explorer

cursor.execute("""
CREATE TABLE IF NOT EXISTS explorer (
    name TEXT PRIMARY KEY,
    country TEXT,
    description TEXT
)
""")


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row
    return Explorer(
        name=name,
        country=country,
        description=description,
    )


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump()


def create(explorer: Explorer, select: bool = True) -> Explorer:
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
    return get_one(explorer.name) if select else explorer


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
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise EntityNotFoundError(entity="explorer", key=name)


def modify(name: str, explorer: Explorer, select: bool = True) -> Explorer:
    sql = """
    UPDATE explorer
    SET name = :name,
        country = :country,
        description = :description
    WHERE name = :k_name
    """
    params = model_to_dict(explorer)
    params["k_name"] = name
    cursor.execute(sql, params)
    if cursor.rowcount == 1:
        return get_one(explorer.name) if select else explorer
    else:
        raise EntityNotFoundError(entity="explorer", key=name)


def delete(name: str) -> None:
    sql = """
    DELETE FROM explorer
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount != 1:
        raise EntityNotFoundError(entity="explorer", key=name)
