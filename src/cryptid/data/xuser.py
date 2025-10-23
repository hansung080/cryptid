import json
from typing import Any, TypeAlias

from cryptid.data.init import transaction_with, Cursor, IntegrityError
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser

UserRow: TypeAlias = tuple[str, str, str]


@transaction_with(new_conn=False)
def _create_table(cursor: Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS xuser (
        name TEXT PRIMARY KEY,
        hash TEXT NOT NULL,
        roles TEXT NOT NULL CHECK(json_valid(roles))
    )
    """)


_create_table()


def model_to_dict(user: PublicUser | PrivateUser) -> dict[str, Any]:
    user_dict = user.model_dump(exclude={"roles"})
    user_dict["roles"] = json.dumps(user.roles)
    return user_dict


def row_to_model(row: UserRow, *, public: bool = True) -> PublicUser | PrivateUser:
    name, hash_, roles = row
    roles = json.loads(roles)
    if public:
        return PublicUser(name=name, roles=roles)
    else:
        return PrivateUser(name=name, roles=roles, hash=hash_)


def create(cursor: Cursor, user: PrivateUser, *, fetch: bool = True) -> PublicUser:
    sql = """
    INSERT INTO xuser (name, hash, roles)
    VALUES (:name, :hash, :roles)
    """
    try:
        cursor.execute(sql, model_to_dict(user))
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise EntityAlreadyExistsError(entity="xuser", key=user.name)
        raise e
    return get_one(cursor, user.name) if fetch else PublicUser(name=user.name)


def get_all(cursor: Cursor) -> list[PublicUser]:
    sql = """
    SELECT *
    FROM xuser
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(cursor: Cursor, name: str, *, public: bool = True) -> PublicUser | PrivateUser:
    sql = """
    SELECT *
    FROM xuser
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if row := cursor.fetchone():
        return row_to_model(row, public=public)
    else:
        raise EntityNotFoundError(entity="xuser", key=name)


def replace(cursor: Cursor, name: str, user: PublicUser, *, fetch: bool = True) -> PublicUser:
    sql = """
    UPDATE xuser
    SET name = :name,
        roles = :roles
    WHERE name = :name_old
    """
    params = model_to_dict(user)
    params["name_old"] = name
    cursor.execute(sql, params)
    if cursor.rowcount == 1:
        return get_one(cursor, user.name) if fetch else user
    else:
        raise EntityNotFoundError(entity="xuser", key=name)


def modify(cursor: Cursor, name: str, user: PartialUser, *, fetch: bool = True) -> PublicUser:
    updated = update_model(get_one(cursor, name), user)
    return replace(cursor, name, updated, fetch=fetch)


def update_model(user: PublicUser, update: PartialUser) -> PublicUser:
    update_dict = update.model_dump(exclude_unset=True)
    return user.model_copy(update=update_dict)


def delete(cursor: Cursor, name: str) -> None:
    sql = """
    DELETE FROM xuser
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount != 1:
        raise EntityNotFoundError(entity="xuser", key=name)
