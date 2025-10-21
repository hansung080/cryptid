import pytest
from fastapi.testclient import TestClient
from starlette import status

from cryptid.main import app
from cryptid.model.auth import AuthUser
from cryptid.model.user import PublicUser, SignInUser, PartialUser

from tests.common import count
from tests.full.common import assert_response, make_headers, admin_token, create_token

key_num = count()
client = TestClient(app)
mike_token: str | None = None
john_token: str | None = None

PublicUser.to_auth_user = lambda self: AuthUser(
    name=self.name,
    roles=self.roles,
)


@pytest.fixture
def mike() -> PublicUser:
    return PublicUser(
        name=f"Mike {key_num}",
        roles=["user"],
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


@pytest.fixture
def john_password() -> str:
    return "john1234"


def test_create_mike(mike: PublicUser, mike_password: str) -> None:
    global mike_token
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = client.post("/users", json=user.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=mike)

    mike_token = create_token(user).access


def test_create_and_delete_john(john: PublicUser, john_password: str) -> None:
    global john_token
    user = SignInUser(
        name=john.name,
        roles=john.roles,
        password=john_password,
    )
    resp = client.post("/users", json=user.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=john)

    john_token = create_token(user).access

    resp = client.delete(f"/users/me", headers=make_headers(token=john_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_get_me(mike: PublicUser) -> None:
    resp = client.get(f"/users/me", headers=make_headers(token=mike_token))
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_get_me_not_found() -> None:
    resp = client.get(f"/users/me", headers=make_headers(token=john_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace_me(john: PublicUser) -> None:
    resp = client.put(f"/users/me", headers=make_headers(token=mike_token), json=john.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=john)


def test_replace_me_not_found(mike: PublicUser) -> None:
    resp = client.put(f"/users/me", headers=make_headers(token=mike_token), json=mike.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify_me(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    user = PartialUser(roles=john.roles).model_dump(exclude_unset=True)
    resp = client.patch(f"/users/me", headers=make_headers(token=john_token), json=user)
    assert_response(resp, status_code=status.HTTP_200_OK, json=john)


def test_modify_me_not_found() -> None:
    user = PartialUser().model_dump(exclude_unset=True)
    resp = client.patch(f"/users/me", headers=make_headers(token=mike_token), json=user)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete_me_conflict() -> None:
    resp = client.delete(f"/users/me", headers=make_headers(token=john_token))
    assert_response(resp, status_code=status.HTTP_409_CONFLICT)


# FIXME: It must be HTTP_409_CONFLICT.
def test_delete_me_not_found(john: PublicUser) -> None:
    resp = client.delete(f"/users/me", headers=make_headers(token=john_token))
    print(f"KHS: {resp.status_code}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
