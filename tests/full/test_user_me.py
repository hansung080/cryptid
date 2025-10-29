import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette import status

from cryptid.main import app
from cryptid.model.auth import AuthUser
from cryptid.model.user import SignInUser, PartialUser

from tests.common import count
from tests.full.common import assert_response, make_headers, create_token

key_num = count()
client = TestClient(app)
mike_token: str | None = None
john_token: str | None = None


class PublicUser(BaseModel):
    id: str | None = None
    name: str
    roles: list[str] = ["user"]
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None

    def to_auth_user(self) -> AuthUser:
        return AuthUser(
            id=self.id,
            roles=self.roles,
        )


_mike = PublicUser(
    name=f"Mike {key_num}",
    roles=["user"],
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
    resp_dict = resp.json()
    mike.id = resp_dict["id"]
    mike.created_at = resp_dict["created_at"]
    mike.updated_at = resp_dict["updated_at"]
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=mike)

    user.id = resp_dict["id"]
    mike_token = create_token(user).access


def test_create_and_delete_john(john: PublicUser, john_password: str) -> None:
    global john_token
    user = SignInUser(
        name=john.name,
        roles=john.roles,
        password=john_password,
    )
    resp = client.post("/users", json=user.model_dump())
    resp_dict = resp.json()
    john.id = resp_dict["id"]
    john.created_at = resp_dict["created_at"]
    john.updated_at = resp_dict["updated_at"]
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=john)

    user.id = resp_dict["id"]
    john_token = create_token(user).access

    resp = client.delete(f"/users/me", headers=make_headers(token=john_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_get_me(mike: PublicUser) -> None:
    resp = client.get(f"/users/me", headers=make_headers(token=mike_token))
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_get_me_not_found() -> None:
    resp = client.get(f"/users/me", headers=make_headers(token=john_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace_me(mike: PublicUser, john: PublicUser) -> None:
    resp = client.put(f"/users/me", headers=make_headers(token=mike_token), json=john.model_dump())
    resp_dict = resp.json()
    mike.name = resp_dict["name"]
    mike.roles = resp_dict["roles"]
    mike.updated_at = resp_dict["updated_at"]
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_replace_me_not_found(john: PublicUser) -> None:
    resp = client.put(f"/users/me", headers=make_headers(token=john_token), json=john.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify_me(mike: PublicUser) -> None:
    mike.roles = ["user", "admin"]
    user = PartialUser(roles=mike.roles).model_dump(exclude_unset=True)
    resp = client.patch(f"/users/me", headers=make_headers(token=mike_token), json=user)
    resp_dict = resp.json()
    mike.updated_at = resp_dict["updated_at"]
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_modify_me_not_found() -> None:
    user = PartialUser().model_dump(exclude_unset=True)
    resp = client.patch(f"/users/me", headers=make_headers(token=john_token), json=user)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete_me() -> None:
    resp = client.delete(f"/users/me", headers=make_headers(token=mike_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT)


def test_delete_me_not_found() -> None:
    resp = client.delete(f"/users/me", headers=make_headers(token=mike_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
