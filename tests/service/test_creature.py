import cryptonamicon.service.creature as code

from cryptonamicon.model.creature import Creature


sample = Creature(
    name="Yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_one_exists():
    resp = code.get_one("Yeti")
    assert resp == sample


def test_get_one_missing():
    resp = code.get_one("missing")
    assert resp is None
