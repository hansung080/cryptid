from cryptid.data.init import Cursor
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser

_users = {
    "Mike": PublicUser(
        name="Mike",
        roles=["user", "admin"],
    ),
    "John": PublicUser(
        name="John",
        roles=["user"],
    ),
}


def find(name: str) -> PublicUser | None:
    return _users.get(name)


def create(_: Cursor | None, user: PrivateUser) -> PublicUser:
    if find(user.name) is not None:
        raise EntityAlreadyExistsError(entity="user", key=user.name)
    public_user = PublicUser(name=user.name, roles=user.roles)
    _users[user.name] = public_user
    return public_user


def get_all(_: Cursor | None) -> list[PublicUser]:
    return list(_users.values())


def get_one(_: Cursor | None, name: str) -> PublicUser:
    if (user := find(name)) is None:
        raise EntityNotFoundError(entity="user", key=name)
    return user


def replace(_: Cursor | None, name: str, user: PublicUser) -> PublicUser:
    if find(name) is None:
        raise EntityNotFoundError(entity="user", key=name)
    if name != user.name:
        del _users[name]
    _users[user.name] = user
    return user


def modify(cursor: Cursor | None, name: str, user: PartialUser) -> PublicUser:
    updated = update_model(get_one(cursor, name), user)
    return replace(cursor, name, updated)


def update_model(user: PublicUser, update: PartialUser) -> PublicUser:
    update_dict = update.model_dump(exclude_unset=True)
    return user.model_copy(update=update_dict)


def delete(_: Cursor | None, name: str) -> None:
    if find(name) is None:
        raise EntityNotFoundError(entity="user", key=name)
    del _users[name]
