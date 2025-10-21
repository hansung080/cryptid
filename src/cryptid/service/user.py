import os

from cryptid.data.init import get_conn
from cryptid.model.user import PublicUser, SignInUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import user as data
else:
    from cryptid.fake.data import user as data

_conn = get_conn()
_cursor = _conn.cursor()


def create(user: SignInUser) -> PublicUser:
    private_user = PrivateUser(
        name=user.name,
        roles=user.roles,
        hash=make_hash(user.password),
    )
    return data.create(_cursor, private_user)


def get_all() -> list[PublicUser]:
    return data.get_all(_cursor)


def get_one(name: str) -> PublicUser:
    return data.get_one(_cursor, name)


def replace(name: str, user: PublicUser) -> PublicUser:
    return data.replace(_cursor, name, user)


def modify(name: str, user: PartialUser) -> PublicUser:
    return data.modify(_cursor, name, user)


def delete(name: str) -> None:
    data.delete(_cursor, name)
