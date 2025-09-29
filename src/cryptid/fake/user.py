from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, SignInUser, PrivateUser

_users = [
    PublicUser(
        name="Mike",
        roles=["user", "admin"],
    ),
    PublicUser(
        name="John",
        roles=["user"],
    ),
]


def find(name: str) -> PublicUser | None:
    for _user in _users:
        if _user.name == name:
            return _user
    return None


def check_already_exists(name: str) -> None:
    if find(name):
        raise EntityAlreadyExistsError(entity="user", key=name)


def check_not_found(name: str) -> None:
    if not find(name):
        raise EntityNotFoundError(entity="user", key=name)


def create(user: SignInUser | PrivateUser) -> PublicUser:
    check_already_exists(user.name)
    return PublicUser(name=user.name, roles=user.roles)


def get_all() -> list[PublicUser]:
    return _users


def get_one(name: str) -> PublicUser:
    check_not_found(name)
    return find(name)


def replace(name: str, user: PublicUser) -> PublicUser:
    check_not_found(name)
    return user


def modify(name: str, user: PublicUser) -> PublicUser:
    check_not_found(name)
    return user


def delete(name: str) -> None:
    check_not_found(name)
