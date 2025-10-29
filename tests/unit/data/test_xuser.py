from datetime import datetime, timezone

import pytest

from cryptid.data import xuser as data
from cryptid.data.init import get_cursor, transaction_with, Cursor
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash

from tests.common import count

key_num = count()

_mike = PublicUser(
    id="100000",
    name=f"Mike {key_num}",
    roles=["user", "admin"],
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)


@pytest.fixture
def mike() -> PublicUser:
    return _mike


@pytest.fixture
def mike_password() -> str:
    return "mike1234"


@pytest.fixture
def john() -> PublicUser:
    return PublicUser(
        id="missing",
        name=f"John {key_num}",
        roles=["user"],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def test_create(mike: PublicUser, mike_password: str) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        user = PrivateUser(
            id=mike.id,
            name=mike.name,
            roles=mike.roles,
            created_at=mike.created_at,
            updated_at=mike.updated_at,
            hash=make_hash(mike_password),
        )
        resp = data.create(cursor, user)
        mike.deleted_at = resp.deleted_at
        assert resp == mike
    inner()


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        user = PrivateUser(
            id=mike.id,
            name=mike.name,
            roles=mike.roles,
            created_at=mike.created_at,
            updated_at=mike.updated_at,
            hash=make_hash(mike_password),
        )
        with pytest.raises(EntityAlreadyExistsError):
            _ = data.create(cursor, user)
    inner()


def test_get_all() -> None:
    resp = data.get_all(get_cursor())
    assert len(resp) > 0


def test_get_one(mike: PublicUser) -> None:
    resp = data.get_one(get_cursor(), mike.id)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(get_cursor(), john.id)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        resp = data.replace(cursor, mike.id, john)
        mike.name = john.name
        mike.roles = john.roles
        mike.updated_at = resp.updated_at
        assert resp == mike
    inner()


def test_replace_not_found(john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            _ = data.replace(cursor, john.id, john)
    inner()


def test_modify(mike: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        mike.roles = ["user", "admin"]
        resp = data.modify(cursor, mike.id, PartialUser(roles=mike.roles))
        mike.updated_at = resp.updated_at
        assert resp == mike
    inner()


def test_modify_not_found(john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            _ = data.modify(cursor, john.id, PartialUser())
    inner()


def test_delete(mike: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        assert data.delete(cursor, mike.id) is None
    inner()


def test_delete_not_found(john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            data.delete(cursor, john.id)
    inner()
