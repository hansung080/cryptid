import os

from cryptid.data.init import get_cursor, transaction, Cursor
from cryptid.model.user import PublicUser, SignInUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import user as data
else:
    from cryptid.fake.data import user as data


@transaction
def create(cursor: Cursor, user: SignInUser) -> PublicUser:
    private_user = PrivateUser(
        name=user.name,
        roles=user.roles,
        hash=make_hash(user.password),
    )
    return data.create(cursor, private_user)


def get_all() -> list[PublicUser]:
    return data.get_all(get_cursor())


def get_one(name: str) -> PublicUser:
    return data.get_one(get_cursor(), name)


@transaction
def replace(cursor: Cursor, name: str, user: PublicUser) -> PublicUser:
    return data.replace(cursor, name, user)


@transaction
def modify(cursor: Cursor, name: str, user: PartialUser) -> PublicUser:
    return data.modify(cursor, name, user)


@transaction
def delete(cursor: Cursor, name: str) -> None:
    data.delete(cursor, name)
