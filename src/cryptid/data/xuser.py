import json
from datetime import datetime, timezone
from typing import Any, TypeAlias

from cryptid.data.init import transaction_with, is_unique_constraint_failed, Cursor, IntegrityError
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser

Row: TypeAlias = tuple[int, str, str, str, str, str, str]


@transaction_with(new_conn=False)
def _create_table(cursor: Cursor) -> None:
    # CURRENT_TIMESTAMP or DATETIME('now') creates the UTC time.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS xuser (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        hash TEXT NOT NULL,
        roles TEXT NOT NULL CHECK(JSON_VALID(roles)),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)


_create_table()


def model_to_dict(
    user: PublicUser | PrivateUser,
    *,
    for_create: bool = False,
    for_update: bool = False,
) -> dict[str, Any]:
    user_dict = user.model_dump(exclude={"id", "roles", "created_at", "updated_at", "deleted_at"})
    user_dict["roles"] = json.dumps(user.roles)
    if for_create or for_update:
        now = datetime.now(timezone.utc).isoformat()
        if for_create:
            user_dict["id"] = int(user.id)
            user_dict["created_at"] = user.created_at.isoformat()
            user_dict["updated_at"] = user.updated_at.isoformat()
            user_dict["deleted_at"] = now
        else:
            user_dict["updated_at"] = now
    return user_dict


def row_to_model(row: Row, *, public: bool = True) -> PublicUser | PrivateUser:
    id_, name, hash_, roles, created_at, updated_at, deleted_at = row
    id_ = str(id_)
    roles = json.loads(roles)
    # Without the following conversions, pydantic.BaseModel automatically converts the type from str to datetime,
    # but I prefer the explicit conversion.
    created_at = datetime.fromisoformat(created_at)
    updated_at = datetime.fromisoformat(updated_at)
    deleted_at = datetime.fromisoformat(deleted_at)
    if public:
        return PublicUser(
            id=id_,
            name=name,
            roles=roles,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )
    else:
        return PrivateUser(
            id=id_,
            name=name,
            roles=roles,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            hash=hash_,
        )


def create(cursor: Cursor, user: PrivateUser, *, fetch: bool = True) -> PublicUser | None:
    sql = """
    INSERT INTO xuser (id, name, hash, roles, created_at, updated_at, deleted_at)
    VALUES (:id, :name, :hash, :roles, :created_at, :updated_at, :deleted_at)
    """
    try:
        cursor.execute(sql, model_to_dict(user, for_create=True))
    except IntegrityError as e:
        if is_unique_constraint_failed(e):
            raise EntityAlreadyExistsError(entity="xuser", key=user.id)
        raise e
    return get_one(cursor, user.id) if fetch else None


def get_all(cursor: Cursor) -> list[PublicUser]:
    sql = """
    SELECT *
    FROM xuser
    """
    cursor.execute(sql)
    return [row_to_model(row) for row in cursor.fetchall()]


def get_one(cursor: Cursor, id_: str, *, public: bool = True) -> PublicUser | PrivateUser:
    sql = """
    SELECT *
    FROM xuser
    WHERE id = :id
    """
    cursor.execute(sql, {"id": id_})
    if (row := cursor.fetchone()) is None:
        raise EntityNotFoundError(entity="xuser", key=id_)
    return row_to_model(row, public=public)


def replace(cursor: Cursor, id_: str, user: PublicUser, *, fetch: bool = True) -> PublicUser | None:
    sql = """
    UPDATE xuser
    SET name = :name,
        roles = :roles,
        updated_at = :updated_at
    WHERE id = :id
    """
    params = model_to_dict(user, for_update=True)
    params["id"] = id_
    cursor.execute(sql, params)
    if cursor.rowcount == 0:
        raise EntityNotFoundError(entity="xuser", key=id_)
    return get_one(cursor, id_) if fetch else None


def modify(cursor: Cursor, id_: str, user: PartialUser, *, fetch: bool = True) -> PublicUser | None:
    updated = update_model(get_one(cursor, id_), user)
    return replace(cursor, id_, updated, fetch=fetch)


def update_model(user: PublicUser, update: PartialUser) -> PublicUser:
    update_dict = update.model_dump(exclude_unset=True)
    return user.model_copy(update=update_dict)


def delete(cursor: Cursor, id_: str) -> None:
    sql = """
    DELETE FROM xuser
    WHERE id = :id
    """
    cursor.execute(sql, {"id": id_})
    if cursor.rowcount == 0:
        raise EntityNotFoundError(entity="xuser", key=id_)
