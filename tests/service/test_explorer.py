import cryptonamicon.service.explorer as code

from cryptonamicon.model.explorer import Explorer


sample = Explorer(
    name="Claude Hande",
    country="FR",
    description="Hard to meet when the full moon rises",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_one_exists():
    resp = code.get_one("Claude Hande")
    assert resp == sample


def test_get_one_missing():
    resp = code.get_one("missing")
    assert resp is None
