import pytest

from cryptid.data import explorer as data
from cryptid.data.init import get_conn
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer, PartialExplorer

from tests.common import count

key_num = count()
conn = get_conn()
cursor = conn.cursor()


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
    resp = data.create(cursor, claude)
    assert resp == claude


def test_create_already_exists(claude: Explorer) -> None:
    with pytest.raises(EntityAlreadyExistsError):
        _ = data.create(cursor, claude)


def test_get_all() -> None:
    resp = data.get_all(cursor)
    assert len(resp) > 0


def test_get_one(claude: Explorer) -> None:
    resp = data.get_one(cursor, claude.name)
    assert resp == claude


def test_get_one_not_found(noah: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(cursor, noah.name)


def test_replace(claude: Explorer, noah: Explorer) -> None:
    resp = data.replace(cursor, claude.name, noah)
    assert resp == noah


def test_replace_not_found(claude: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.replace(cursor, claude.name, claude)


def test_modify(noah: Explorer) -> None:
    noah.description = f"I'm Noah Weiser {key_num}"
    resp = data.modify(cursor, noah.name, PartialExplorer(description=noah.description))
    assert resp == noah


def test_modify_not_found(claude: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.modify(cursor, claude.name, PartialExplorer())


def test_delete(noah: Explorer) -> None:
    assert data.delete(cursor, noah.name) is None


def test_delete_not_found(noah: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        data.delete(cursor, noah.name)
