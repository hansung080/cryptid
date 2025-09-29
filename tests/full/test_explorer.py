import pytest
from fastapi.testclient import TestClient
from starlette import status

from cryptid.main import app
from cryptid.model.explorer import Explorer

from tests.common import count
from tests.full.common import assert_response

key_num = count()
client = TestClient(app)


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
    resp = client.post("/explorer", json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=claude)


def test_create_already_exists(claude: Explorer) -> None:
    resp = client.post("/explorer", json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_409_CONFLICT)


def test_get_all() -> None:
    resp = client.get("/explorer")
    assert_response(resp, status_code=status.HTTP_200_OK)


def test_get_one(claude: Explorer) -> None:
    resp = client.get(f"/explorer/{claude.name}")
    assert_response(resp, status_code=status.HTTP_200_OK, json=claude)


def test_get_one_not_found(noah: Explorer) -> None:
    resp = client.get(f"/explorer/{noah.name}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace(claude: Explorer, noah: Explorer) -> None:
    resp = client.put(f"/explorer/{claude.name}", json=noah.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=noah)


def test_replace_not_found(claude: Explorer) -> None:
    resp = client.put(f"/explorer/{claude.name}", json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify(noah: Explorer) -> None:
    noah.description = f"I'm Noah Weiser {key_num}"
    resp = client.patch(f"/explorer/{noah.name}", json=noah.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=noah)


def test_modify_not_found(claude: Explorer) -> None:
    resp = client.patch(f"/explorer/{claude.name}", json=claude.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete(noah: Explorer) -> None:
    resp = client.delete(f"/explorer/{noah.name}")
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_delete_not_found(noah: Explorer) -> None:
    resp = client.delete(f"/explorer/{noah.name}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
