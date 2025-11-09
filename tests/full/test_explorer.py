import pytest
from fastapi.testclient import TestClient
from starlette import status

from cryptid.main import app
from cryptid.model.explorer import Explorer, PartialExplorer

from tests.common import count
from tests.full.common import admin_token, assert_response, make_headers

key_num: int = count()
client: TestClient = TestClient(app)


@pytest.fixture
def claude() -> Explorer:
    return Explorer(
        name=f"Claude Hande {key_num}",
        country="FR",
        description="Hard to meet when the full moon rises",
    )


@pytest.fixture
def noah() -> Explorer:
    return Explorer(
        name=f"Noah Weiser {key_num}",
        country="DE",
        description="Has poor eyesight and carries an axe",
    )


def test_create(claude: Explorer) -> None:
    resp = client.post("/explorers", headers=make_headers(token=admin_token), json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=claude)


def test_create_already_exists(claude: Explorer) -> None:
    resp = client.post("/explorers", headers=make_headers(token=admin_token), json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_409_CONFLICT)


def test_get_all() -> None:
    resp = client.get("/explorers")
    assert_response(resp, status_code=status.HTTP_200_OK)


def test_get_one(claude: Explorer) -> None:
    resp = client.get(f"/explorers/{claude.name}")
    assert_response(resp, status_code=status.HTTP_200_OK, json=claude)


def test_get_one_not_found(noah: Explorer) -> None:
    resp = client.get(f"/explorers/{noah.name}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace(claude: Explorer, noah: Explorer) -> None:
    resp = client.put(f"/explorers/{claude.name}", headers=make_headers(token=admin_token), json=noah.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=noah)


def test_replace_not_found(claude: Explorer) -> None:
    resp = client.put(f"/explorers/{claude.name}", headers=make_headers(token=admin_token), json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify(noah: Explorer) -> None:
    noah.description = f"I'm Noah Weiser {key_num}"
    explorer = PartialExplorer(description=noah.description).model_dump(exclude_unset=True)
    resp = client.patch(f"/explorers/{noah.name}", headers=make_headers(token=admin_token), json=explorer)
    assert_response(resp, status_code=status.HTTP_200_OK, json=noah)


def test_modify_not_found(claude: Explorer) -> None:
    explorer = PartialExplorer().model_dump(exclude_unset=True)
    resp = client.patch(f"/explorers/{claude.name}", headers=make_headers(token=admin_token), json=explorer)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete(noah: Explorer) -> None:
    resp = client.delete(f"/explorers/{noah.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_delete_not_found(noah: Explorer) -> None:
    resp = client.delete(f"/explorers/{noah.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
