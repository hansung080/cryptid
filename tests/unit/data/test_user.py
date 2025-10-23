import pytest

from cryptid.data import user as data, xuser
from cryptid.data.init import get_cursor, transaction_with, Cursor
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash

from tests.common import count

key_num = count()


@pytest.fixture
def mike() -> PublicUser:
    return PublicUser(
        name=f"Mike {key_num}",
        roles=["user", "admin"],
    )


@pytest.fixture
def mike_password() -> str:
    return "mike1234"


@pytest.fixture
def john() -> PublicUser:
    return PublicUser(
        name=f"John {key_num}",
        roles=["user"],
    )


def test_create(mike: PublicUser, mike_password: str) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        user = PrivateUser(
            name=mike.name,
            roles=mike.roles,
            hash=make_hash(mike_password),
        )
        resp = data.create(cursor, user)
        assert resp == mike
    inner()


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        user = PrivateUser(
            name=mike.name,
            roles=mike.roles,
            hash=make_hash(mike_password),
        )
        with pytest.raises(EntityAlreadyExistsError):
            _ = data.create(cursor, user)
    inner()


def test_get_all() -> None:
    resp = data.get_all(get_cursor())
    assert len(resp) > 0


def test_get_one(mike: PublicUser) -> None:
    resp = data.get_one(get_cursor(), mike.name)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(get_cursor(), john.name)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        resp = data.replace(cursor, mike.name, john)
        assert resp == john
    inner()


def test_replace_not_found(mike: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            _ = data.replace(cursor, mike.name, mike)
    inner()


def test_modify(john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        john.roles = ["user", "admin"]
        resp = data.modify(cursor, john.name, PartialUser(roles=john.roles))
        assert resp == john
    inner()


def test_modify_not_found(mike: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            _ = data.modify(cursor, mike.name, PartialUser())
    inner()


def test_delete(john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        assert data.delete(cursor, john.name) is None
        resp = xuser.get_one(cursor, john.name)
        john.roles = ["user", "admin"]
        assert resp == john
    inner()


def test_delete_not_found(john: PublicUser) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            data.delete(cursor, john.name)
    inner()
