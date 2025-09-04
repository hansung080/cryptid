from cryptid.error import EntityNotFoundError
from cryptid.model.explorer import Explorer

_explorers = [
    Explorer(
        name="Claude Hande",
        country="FR",
        description="Hard to meet when the full moon rises",
    ),
    Explorer(
        name="Noah Weiser",
        country="DE",
        description="Has poor eyesight and carries an axe",
    ),
]


def create(explorer: Explorer) -> Explorer:
    # TODO: To implement the body.
    return explorer


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer:
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    raise EntityNotFoundError(entity="explorer", key=name)


def replace(name: str, explorer: Explorer) -> Explorer:
    # TODO: To implement the body.
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer:
    # TODO: To implement the body.
    return explorer


def delete(name: str) -> None:
    # TODO: To implement the body.
    for _explorer in _explorers:
        if _explorer.name == name:
            return
    raise EntityNotFoundError(entity="explorer", key=name)
