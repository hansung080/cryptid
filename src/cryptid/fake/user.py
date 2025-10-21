from cryptid.fake.data import user as data
from cryptid.model.user import PublicUser, SignInUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash


def create(user: SignInUser) -> PublicUser:
    private_user = PrivateUser(
        name=user.name,
        roles=user.roles,
        hash=make_hash(user.password),
    )
    return data.create(None, private_user)


def get_all() -> list[PublicUser]:
    return data.get_all(None)


def get_one(name: str) -> PublicUser:
    return data.get_one(None, name)


def replace(name: str, user: PublicUser) -> PublicUser:
    return data.replace(None, name, user)


def modify(name: str, user: PartialUser) -> PublicUser:
    return data.modify(None, name, user)


def delete(name: str) -> None:
    data.delete(None, name)
