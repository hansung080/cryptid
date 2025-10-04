import pytest

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer, PartialExplorer
from cryptid.service import explorer as service

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
    resp = service.create(claude)
    assert resp == claude


def test_create_already_exists(claude: Explorer) -> None:
    with pytest.raises(EntityAlreadyExistsError):
        _ = service.create(claude)


def test_get_all() -> None:
    resp = service.get_all()
    assert len(resp) > 0


def test_get_one(claude: Explorer) -> None:
    resp = service.get_one(claude.name)
    assert resp == claude


def test_get_one_not_found(noah: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.get_one(noah.name)


def test_replace(claude: Explorer, noah: Explorer) -> None:
    resp = service.replace(claude.name, noah)
    assert resp == noah


def test_replace_not_found(claude: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.replace(claude.name, claude)


def test_modify(noah: Explorer) -> None:
    noah.description = f"I'm Noah Weiser {key_num}"
    resp = service.modify(noah.name, PartialExplorer(description=noah.description))
    assert resp == noah


def test_modify_not_found(claude: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.modify(claude.name, PartialExplorer())


def test_delete(noah: Explorer) -> None:
    assert service.delete(noah.name) is None


def test_delete_not_found(noah: Explorer) -> None:
    with pytest.raises(EntityNotFoundError):
        service.delete(noah.name)
