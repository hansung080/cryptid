from __future__ import annotations

import os

from cryptid.data.init import Cursor, get_cursor, transaction
from cryptid.model.user import PartialUser, PrivateUser, PublicUser, SignInUser
from cryptid.service.auth import make_hash

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import user as data, xuser
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


def get_all(*, deleted: bool = False) -> list[PublicUser]:
    if deleted:
        return xuser.get_all(get_cursor())
    return data.get_all(get_cursor())


def get_one(id_: str, *, deleted: bool = False) -> PublicUser:
    if deleted:
        return xuser.get_one(get_cursor(), id_)
    return data.get_one(get_cursor(), id_)


@transaction
def replace(cursor: Cursor, id_: str, user: PublicUser) -> PublicUser:
    return data.replace(cursor, id_, user)


@transaction
def modify(cursor: Cursor, id_: str, user: PartialUser) -> PublicUser:
    return data.modify(cursor, id_, user)


@transaction
def delete(cursor: Cursor, id_: str) -> None:
    data.delete(cursor, id_)
