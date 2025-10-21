import pytest
from fastapi.testclient import TestClient
from starlette import status

from cryptid.main import app
from cryptid.model.user import PublicUser, SignInUser, PartialUser

from tests.common import count
from tests.full.common import assert_response, make_headers, admin_token, create_token

key_num = count()
client = TestClient(app)
mike_token: str | None = None


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


def test_create(mike: PublicUser, mike_password: str) -> None:
    global mike_token
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = client.post("/users", json=user.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=mike)
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
    resp = client.get(f"/users/{mike.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_get_one_not_found(john: PublicUser) -> None:
    resp = client.get(f"/users/{john.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = client.put(f"/users/{mike.name}", headers=make_headers(token=admin_token), json=john.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=john)


def test_replace_not_found(mike: PublicUser) -> None:
    resp = client.put(f"/users/{mike.name}", headers=make_headers(token=admin_token), json=mike.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    user = PartialUser(roles=john.roles).model_dump(exclude_unset=True)
    resp = client.patch(f"/users/{john.name}", headers=make_headers(token=admin_token), json=user)
    assert_response(resp, status_code=status.HTTP_200_OK, json=john)


def test_modify_not_found(mike: PublicUser) -> None:
    user = PartialUser().model_dump(exclude_unset=True)
    resp = client.patch(f"/users/{mike.name}", headers=make_headers(token=admin_token), json=user)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete(john: PublicUser) -> None:
    resp = client.delete(f"/users/{john.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_delete_not_found(john: PublicUser) -> None:
    resp = client.delete(f"/users/{john.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
