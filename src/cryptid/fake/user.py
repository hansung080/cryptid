from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, SignInUser, PrivateUser

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


def create(user: SignInUser | PrivateUser) -> PublicUser:
    if find(user.name) is not None:
        raise EntityAlreadyExistsError(entity="user", key=user.name)
    public_user = PublicUser(name=user.name, roles=user.roles)
    _users[user.name] = public_user
    return public_user


def get_all() -> list[PublicUser]:
    return list(_users.values())


def get_one(name: str) -> PublicUser:
    if (user := find(name)) is None:
        raise EntityNotFoundError(entity="user", key=name)
    return user


def replace(name: str, user: PublicUser) -> PublicUser:
    if find(name) is None:
        raise EntityNotFoundError(entity="user", key=name)
    if name != user.name:
        del _users[name]
    _users[user.name] = user
    return user


def modify(name: str, user: PublicUser) -> PublicUser:
    return replace(name, user)


def delete(name: str) -> None:
    if find(name) is None:
        raise EntityNotFoundError(entity="user", key=name)
    del _users[name]
