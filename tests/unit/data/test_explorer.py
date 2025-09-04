import pytest

import cryptonamicon.data.explorer as data
from cryptonamicon.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptonamicon.model.explorer import Explorer

from tests.common import count

key_num = count()


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
    resp = data.create(claude)
    assert resp == claude


def test_create_already_exists(claude: Explorer) -> None:
    with pytest.raises(EntityAlreadyExistsError):
        _ = data.create(claude)


def test_get_all() -> None:
    resp = data.get_all()
    assert len(resp) > 0


def test_get_one(claude: Explorer) -> None:
    resp = data.get_one(claude.name)
    assert resp == claude


def test_get_one_not_found(noah: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(noah.name)


def test_modify(claude: Explorer, noah: Explorer) -> None:
    resp = data.modify(claude.name, noah)
    assert resp == noah


def test_modify_not_found(claude: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.modify(claude.name, claude)


def test_delete(noah: Explorer) -> None:
    assert data.delete(noah.name) is None


def test_delete_not_found(noah: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        data.delete(noah.name)
