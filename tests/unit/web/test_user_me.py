from __future__ import annotations

import pytest
from fastapi import HTTPException

from cryptid.model.auth import AuthUser
from cryptid.model.user import PartialUser, PublicUser, SignInUser
from cryptid.web import user as web

from tests.common import count
from tests.unit.web.common import assert_not_found_error

key_num: int = count()

_mike: PublicUser = PublicUser(
    name=f"Mike {key_num}",
    roles=["user", "admin"],
)


def to_auth_user(user: PublicUser) -> AuthUser:
    assert user.id is not None
    return AuthUser(
        id=user.id,
        roles=user.roles,
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


def test_get_me(mike: PublicUser) -> None:
    resp = web.get_me(to_auth_user(mike))
    assert resp == mike


def test_get_me_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.get_me(to_auth_user(john))
        assert_not_found_error(e)


def test_replace_me(mike: PublicUser, john: PublicUser) -> None:
    resp = web.replace_me(to_auth_user(mike), john)
    mike.name = john.name
    mike.roles = john.roles
    mike.updated_at = resp.updated_at
    assert resp == mike


def test_replace_me_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.replace_me(to_auth_user(john), john)
        assert_not_found_error(e)


def test_modify_me(mike: PublicUser) -> None:
    mike.roles = ["user", "admin"]
    resp = web.modify_me(to_auth_user(mike), PartialUser(roles=mike.roles))
    mike.updated_at = resp.updated_at
    assert resp == mike


def test_modify_me_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.modify_me(to_auth_user(john), PartialUser())
        assert_not_found_error(e)


def test_delete_me(mike: PublicUser) -> None:
    assert web.delete_me(to_auth_user(mike)) is None


def test_delete_me_not_found(john: PublicUser) -> None:
    with pytest.raises(HTTPException) as e:
        web.delete_me(to_auth_user(john))
        assert_not_found_error(e)
