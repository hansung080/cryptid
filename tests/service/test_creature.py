import pytest

import cryptonamicon.service.creature as service
from cryptonamicon.error import EntityNotFoundError
from cryptonamicon.model.creature import Creature

from tests.common import count

key_num = count()


@pytest.fixture
def yeti() -> Creature:
    return Creature(
        name=f"Yeti {key_num}",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )


def test_create(yeti: Creature) -> None:
    resp = service.create(yeti)
    assert resp == yeti


def test_get_one(yeti: Creature) -> None:
    resp = service.get_one(yeti.name)
    assert resp == yeti


def test_get_one_not_found() -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.get_one("missing")
