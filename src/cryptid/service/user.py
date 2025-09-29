import os

from cryptid.model.user import PublicUser, SignInUser, PrivateUser
from cryptid.service.auth import make_hash

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import user as data
else:
    from cryptid.fake import user as data


def create(user: SignInUser) -> PublicUser:
    private_user = PrivateUser(
        name=user.name,
        roles=user.roles,
        hash=make_hash(user.password),
    )
    return data.create(private_user)


def get_all() -> list[PublicUser]:
    return data.get_all()


def get_one(name: str) -> PublicUser:
    return data.get_one(name)


def replace(name: str, user: PublicUser) -> PublicUser:
    return data.replace(name, user)


def modify(name: str, user: PublicUser) -> PublicUser:
    return data.modify(name, user)


def delete(name: str) -> None:
    data.delete(name)
