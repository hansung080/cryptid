import pytest
from fastapi import HTTPException

from cryptid.model.user import PartialUser, PublicUser, SignInUser
from cryptid.web import user as web

from tests.common import count
from tests.unit.web.common import assert_already_exists_error, assert_not_found_error

key_num: int = count()

_mike: PublicUser = PublicUser(
    name=f"Mike {key_num}",
    roles=["user", "admin"],
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
    )


def test_create(mike: PublicUser, mike_password: str) -> None:
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = web.create(user)
    mike.id = resp.id
    mike.created_at = resp.created_at
    mike.updated_at = resp.updated_at
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
    resp = web.get_all(deleted=False)
    assert len(resp) > 0


def test_get_one(mike: PublicUser) -> None:
    resp = web.get_one(mike.id, deleted=False)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.get_one(john.id, deleted=False)
        assert_not_found_error(e)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = web.replace(mike.id, john)
    mike.name = john.name
    mike.roles = john.roles
    mike.updated_at = resp.updated_at
    assert resp == mike


def test_replace_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.replace(john.id, john)
        assert_not_found_error(e)


def test_modify(mike: PublicUser) -> None:
    mike.roles = ["user", "admin"]
    resp = web.modify(mike.id, PartialUser(roles=mike.roles))
    mike.updated_at = resp.updated_at
    assert resp == mike


def test_modify_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.modify(john.id, PartialUser())
        assert_not_found_error(e)


def test_delete(mike: PublicUser) -> None:
    assert web.delete(mike.id) is None


def test_delete_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        web.delete(john.id)
        assert_not_found_error(e)
