import pytest
from fastapi.testclient import TestClient
from starlette import status

from cryptid.main import app
from cryptid.model.user import PublicUser, SignInUser, PartialUser

from tests.common import count
from tests.full.common import assert_response

key_num = count()
client = TestClient(app)


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
    resp = client.post("/user", json=user.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=mike)


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = client.post("/user", json=user.model_dump())
    assert_response(resp, status_code=status.HTTP_409_CONFLICT)


def test_get_all() -> None:
    resp = client.get("/user")
    assert_response(resp, status_code=status.HTTP_200_OK)


def test_get_one(mike: PublicUser) -> None:
    resp = client.get(f"/user/{mike.name}")
    assert_response(resp, status_code=status.HTTP_200_OK, json=mike)


def test_get_one_not_found(john: PublicUser) -> None:
    resp = client.get(f"/user/{john.name}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = client.put(f"/user/{mike.name}", json=john.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=john)


def test_replace_not_found(mike: PublicUser) -> None:
    resp = client.put(f"/user/{mike.name}", json=mike.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    user = PartialUser(roles=john.roles).model_dump(exclude_unset=True)
    resp = client.patch(f"/user/{john.name}", json=user)
    assert_response(resp, status_code=status.HTTP_200_OK, json=john)


def test_modify_not_found(mike: PublicUser) -> None:
    user = PartialUser().model_dump(exclude_unset=True)
    resp = client.patch(f"/user/{mike.name}", json=user)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete(john: PublicUser) -> None:
    resp = client.delete(f"/user/{john.name}")
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_delete_not_found(john: PublicUser) -> None:
    resp = client.delete(f"/user/{john.name}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
