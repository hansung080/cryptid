import pytest
from fastapi import HTTPException

from cryptid.model.auth import AuthUser
from cryptid.model.user import PublicUser, SignInUser, PartialUser
from cryptid.web import user as web

from tests.common import count
from tests.unit.web.common import assert_not_found_error

key_num = count()

PublicUser.to_auth_user = lambda self: AuthUser(
    name=self.name,
    roles=self.roles,
)


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
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = web.create(user)
    assert resp == mike


def test_get_me(mike: PublicUser) -> None:
    resp = web.get_me(me=mike.to_auth_user())
    assert resp == mike


def test_get_me_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.get_me(me=john.to_auth_user())
        assert_not_found_error(e)


def test_replace_me(mike: PublicUser, john: PublicUser) -> None:
    resp = web.replace_me(john, me=mike.to_auth_user())
    assert resp == john


def test_replace_me_not_found(mike: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.replace_me(mike, me=mike.to_auth_user())
        assert_not_found_error(e)


def test_modify_me(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    resp = web.modify_me(PartialUser(roles=john.roles), me=john.to_auth_user())
    assert resp == john


def test_modify_me_not_found(mike: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.modify_me(PartialUser(), me=mike.to_auth_user())
        assert_not_found_error(e)


def test_delete_me(john: PublicUser) -> None:
    assert web.delete_me(me=john.to_auth_user()) is None


def test_delete_me_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        web.delete_me(me=john.to_auth_user())
        assert_not_found_error(e)
