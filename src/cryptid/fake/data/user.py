from datetime import datetime, timezone

from cryptid.data.init import Cursor
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PartialUser, PrivateUser, PublicUser

_users: dict[str, PublicUser] = {
    "1": PublicUser(
        id="1",
        name="Mike",
        roles=["user", "admin"],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    ),
    "2": PublicUser(
        id="2",
        name="John",
        roles=["user"],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    ),
}

_last_id: int = len(_users)


def get_next_id() -> int:
    global _last_id
    _last_id += 1
    return int(_last_id)


def find(id_: str) -> PublicUser | None:
    return _users.get(id_)


def find_by_name(name: str) -> PublicUser | None:
    return next((v for k, v in _users.items() if v.name == name), None)


def create(_: Cursor | None, user: PrivateUser) -> PublicUser:
    if find_by_name(user.name) is not None:
        raise EntityAlreadyExistsError(entity="user", key=user.name)
    id_ = str(get_next_id())
    now = datetime.now(timezone.utc)
    public_user = PublicUser(
        id=id_,
        name=user.name,
        roles=user.roles,
        created_at=now,
        updated_at=now,
    )
    _users[id_] = public_user
    return public_user


def get_all(_: Cursor | None) -> list[PublicUser]:
    return list(_users.values())


def get_one(_: Cursor | None, id_: str) -> PublicUser:
    if (user := find(id_)) is None:
        raise EntityNotFoundError(entity="user", key=id_)
    return user


def replace(_: Cursor | None, id_: str, user: PublicUser) -> PublicUser:
    if (existing_user := find(id_)) is None:
        raise EntityNotFoundError(entity="user", key=id_)
    existing_user.name = user.name
    existing_user.roles = user.roles
    existing_user.updated_at = datetime.now(timezone.utc)
    return existing_user


def modify(cursor: Cursor | None, id_: str, user: PartialUser) -> PublicUser:
    updated = update_model(get_one(cursor, id_), user)
    return replace(cursor, id_, updated)


def update_model(user: PublicUser, update: PartialUser) -> PublicUser:
    update_dict = update.model_dump(exclude_unset=True)
    return user.model_copy(update=update_dict)


def delete(_: Cursor | None, id_: str) -> None:
    if find(id_) is None:
        raise EntityNotFoundError(entity="user", key=id_)
    del _users[id_]
