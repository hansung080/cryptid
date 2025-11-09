import pytest
from fastapi import HTTPException

from cryptid.model.explorer import Explorer, PartialExplorer
from cryptid.web import explorer as web

from tests.common import count
from tests.unit.web.common import assert_already_exists_error, assert_not_found_error

key_num: int = count()


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
    resp = web.create(claude)
    assert resp == claude


def test_create_already_exists(claude: Explorer) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.create(claude)
        assert_already_exists_error(e)


def test_get_all() -> None:
    resp = web.get_all()
    assert len(resp) > 0


def test_get_one(claude: Explorer) -> None:
    resp = web.get_one(claude.name)
    assert resp == claude


def test_get_one_not_found(noah: Explorer) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.get_one(noah.name)
        assert_not_found_error(e)


def test_replace(claude: Explorer, noah: Explorer) -> None:
    resp = web.replace(claude.name, noah)
    assert resp == noah


def test_replace_not_found(claude: Explorer) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.replace(claude.name, claude)
        assert_not_found_error(e)


def test_modify(noah: Explorer) -> None:
    noah.description = f"I'm Noah Weiser {key_num}"
    resp = web.modify(noah.name, PartialExplorer(description=noah.description))
    assert resp == noah


def test_modify_not_found(claude: Explorer) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.modify(claude.name, PartialExplorer())
        assert_not_found_error(e)


def test_delete(noah: Explorer) -> None:
    assert web.delete(noah.name) is None


def test_delete_not_found(noah: Explorer) -> None:
    with pytest.raises(HTTPException) as e:
        web.delete(noah.name)
        assert_not_found_error(e)
