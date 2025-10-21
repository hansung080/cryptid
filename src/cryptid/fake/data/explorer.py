from cryptid.data.init import Cursor
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer, PartialExplorer

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


def find(name: str) -> Explorer | None:
    return next((c for c in _explorers if c.name == name), None)


def find_index(name: str) -> int | None:
    return next((i for i, c in enumerate(_explorers) if c.name == name), None)


def create(_: Cursor | None, explorer: Explorer) -> Explorer:
    if find(explorer.name) is not None:
        raise EntityAlreadyExistsError(entity="explorer", key=explorer.name)
    _explorers.append(explorer)
    return explorer


def get_all(_: Cursor | None) -> list[Explorer]:
    return _explorers


def get_one(_: Cursor | None, name: str) -> Explorer:
    if (explorer := find(name)) is None:
        raise EntityNotFoundError(entity="explorer", key=name)
    return explorer


def replace(_: Cursor | None, name: str, explorer: Explorer) -> Explorer:
    if (index := find_index(name)) is None:
        raise EntityNotFoundError(entity="explorer", key=name)
    _explorers[index] = explorer
    return explorer


def modify(cursor: Cursor | None, name: str, explorer: PartialExplorer) -> Explorer:
    updated = update_model(get_one(cursor, name), explorer)
    return replace(cursor, name, updated)


def update_model(explorer: Explorer, update: PartialExplorer) -> Explorer:
    update_dict = update.model_dump(exclude_unset=True)
    return explorer.model_copy(update=update_dict)


def delete(_: Cursor | None, name: str) -> None:
    if (explorer := find(name)) is None:
        raise EntityNotFoundError(entity="explorer", key=name)
    _explorers.remove(explorer)
