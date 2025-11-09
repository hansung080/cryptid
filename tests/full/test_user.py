import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette import status

from cryptid.main import app
from cryptid.model.user import PartialUser, SignInUser

from tests.common import count
from tests.full.common import admin_token, assert_response, create_token, make_headers

key_num: int = count()
client: TestClient = TestClient(app)
mike_token: str | None = None


class PublicUser(BaseModel):
    id: str | None = None
    name: str
    roles: list[str] = ["user"]
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


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
        id="missing",
        name=f"John {key_num}",
        roles=["user"],
    )


def test_create(mike: PublicUser, mike_password: str) -> None:
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


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = client.post("/users", json=user.model_dump())
    assert_response(resp, status_code=status.HTTP_409_CONFLICT)


def test_get_all() -> None:
    resp = client.get("/users", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_200_OK)


def test_get_all_unauthorized() -> None:
    resp = client.get("/users")
    assert_response(resp, status_code=status.HTTP_401_UNAUTHORIZED)


def test_get_all_forbidden() -> None:
    resp = client.get("/users", headers=make_headers(token=mike_token))
    assert_response(resp, status_code=status.HTTP_403_FORBIDDEN)


def test_get_one(mike: PublicUser) -> None:
    resp = client.get(f"/users/{mike.id}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_get_one_not_found(john: PublicUser) -> None:
    resp = client.get(f"/users/{john.id}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = client.put(f"/users/{mike.id}", headers=make_headers(token=admin_token), json=john.model_dump())
    resp_dict = resp.json()
    mike.name = resp_dict["name"]
    mike.roles = resp_dict["roles"]
    mike.updated_at = resp_dict["updated_at"]
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_replace_not_found(john: PublicUser) -> None:
    resp = client.put(f"/users/{john.id}", headers=make_headers(token=admin_token), json=john.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify(mike: PublicUser) -> None:
    mike.roles = ["user", "admin"]
    user = PartialUser(roles=mike.roles).model_dump(exclude_unset=True)
    resp = client.patch(f"/users/{mike.id}", headers=make_headers(token=admin_token), json=user)
    resp_dict = resp.json()
    mike.updated_at = resp_dict["updated_at"]
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_modify_not_found(john: PublicUser) -> None:
    user = PartialUser().model_dump(exclude_unset=True)
    resp = client.patch(f"/users/{john.id}", headers=make_headers(token=admin_token), json=user)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete(mike: PublicUser) -> None:
    resp = client.delete(f"/users/{mike.id}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_delete_not_found(john: PublicUser) -> None:
    resp = client.delete(f"/users/{john.id}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
