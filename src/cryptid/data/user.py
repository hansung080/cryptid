import json
from typing import Any, TypeAlias

from cryptid.data.init import transaction_with, Cursor, IntegrityError
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser

UserRow: TypeAlias = tuple[str, str, str]


@transaction_with(new_conn=False)
def _create_tables(cursor: Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        name TEXT PRIMARY KEY,
        hash TEXT NOT NULL,
        roles TEXT NOT NULL CHECK(json_valid(roles))
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS xuser (
        name TEXT PRIMARY KEY,
        hash TEXT NOT NULL,
        roles TEXT NOT NULL CHECK(json_valid(roles))
    )
    """)


_create_tables()


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


def get_table_name(deleted_user: bool) -> str:
    return "xuser" if deleted_user else "user"


def create(cursor: Cursor, user: PrivateUser, *, deleted_user: bool = False, fetch: bool = True) -> PublicUser:
    table = get_table_name(deleted_user)
    sql = f"""
    INSERT INTO {table} (name, hash, roles)
    VALUES (:name, :hash, :roles)
    """
    try:
        cursor.execute(sql, model_to_dict(user))
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise EntityAlreadyExistsError(entity=table, key=user.name)
        raise e
    return get_one(cursor, user.name) if fetch else PublicUser(name=user.name)


def get_all(cursor: Cursor, *, deleted_user: bool = False) -> list[PublicUser]:
    sql = f"""
    SELECT *
    FROM {get_table_name(deleted_user)}
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(cursor: Cursor, name: str, *, public: bool = True, deleted_user: bool = False) -> PublicUser | PrivateUser:
    table = get_table_name(deleted_user)
    sql = f"""
    SELECT *
    FROM {table}
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if row := cursor.fetchone():
        return row_to_model(row, public=public)
    else:
        raise EntityNotFoundError(entity=table, key=name)


def replace(cursor: Cursor, name: str, user: PublicUser, *, deleted_user: bool = False, fetch: bool = True) -> PublicUser:
    table = get_table_name(deleted_user)
    sql = f"""
    UPDATE {table}
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
        raise EntityNotFoundError(entity=table, key=name)


def modify(cursor: Cursor, name: str, user: PartialUser, *, deleted_user: bool = False, fetch: bool = True) -> PublicUser:
    updated = update_model(get_one(cursor, name), user)
    return replace(cursor, name, updated, deleted_user=deleted_user, fetch=fetch)


def update_model(user: PublicUser, update: PartialUser) -> PublicUser:
    update_dict = update.model_dump(exclude_unset=True)
    return user.model_copy(update=update_dict)


def delete(cursor: Cursor, name: str, *, deleted_user: bool = False) -> None:
    user = get_one(cursor, name, public=False)
    table = get_table_name(deleted_user)
    sql = f"""
    DELETE FROM {table}
    WHERE name = :name
    """
    cursor.execute(sql, {"name": name})
    if cursor.rowcount == 1:
        create(cursor, user, deleted_user=True, fetch=False)
    else:
        raise EntityNotFoundError(entity=table, key=name)
