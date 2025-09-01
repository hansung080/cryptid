import pytest

import cryptonamicon.service.explorer as service
from cryptonamicon.error import EntityNotFoundError
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


def test_create(claude: Explorer) -> None:
    resp = service.create(claude)
    assert resp == claude


def test_get_one(claude: Explorer) -> None:
    resp = service.get_one(claude.name)
    assert resp == claude


def test_get_one_not_found() -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.get_one("missing")
