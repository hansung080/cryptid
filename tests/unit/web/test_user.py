import pytest
from fastapi import HTTPException

from cryptid.model.user import PublicUser, SignInUser, PartialUser
from cryptid.web import user as web

from tests.common import count
from tests.unit.web.common import assert_already_exists_error, assert_not_found_error

key_num = count()


@pytest.fixture
def mike() -> PublicUser:
    return PublicUser(
        name=f"Mike {key_num}",
        roles=["user", "admin"],
    )


@pytest.fixture
def mike_password() -> str:
    return "1234"


@pytest.fixture
def john() -> PublicUser:
    return PublicUser(
        name=f"John {key_num}",
        roles=["user"],
    )


def test_create(mike: PublicUser, mike_password: str) -> None:
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = web.create(user)
    assert resp == mike


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    with pytest.raises(HTTPException) as e:
        _ = web.create(user)
        assert_already_exists_error(e)


def test_get_all() -> None:
    resp = web.get_all()
    assert len(resp) > 0


def test_get_one(mike: PublicUser) -> None:
    resp = web.get_one(mike.name)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.get_one(john.name)
        assert_not_found_error(e)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = web.replace(mike.name, john)
    assert resp == john


def test_replace_not_found(mike: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.replace(mike.name, mike)
        assert_not_found_error(e)


def test_modify(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    resp = web.modify(john.name, PartialUser(roles=john.roles))
    assert resp == john


def test_modify_not_found(mike: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.modify(mike.name, PartialUser())
        assert_not_found_error(e)


def test_delete(john: PublicUser) -> None:
    assert web.delete(john.name) is None


def test_delete_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        web.delete(john.name)
        assert_not_found_error(e)
