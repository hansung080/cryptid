from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    ),
    Creature(
        name="Bigfoot",
        country="US",
        area="*",
        description="Yeti's Cousin Eddie",
        aka="Sasquatch",
    ),
]


def find(name: str) -> Creature | None:
    return next((c for c in _creatures if c.name == name), None)


def find_index(name: str) -> int | None:
    return next((i for i, c in enumerate(_creatures) if c.name == name), None)


def create(creature: Creature) -> Creature:
    if find(creature.name) is not None:
        raise EntityAlreadyExistsError(entity="creature", key=creature.name)
    _creatures.append(creature)
    return creature


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Creature:
    if (creature := find(name)) is None:
        raise EntityNotFoundError(entity="creature", key=name)
    return creature


def replace(name: str, creature: Creature) -> Creature:
    if (index := find_index(name)) is None:
        raise EntityNotFoundError(entity="creature", key=name)
    _creatures[index] = creature
    return creature


def modify(name: str, creature: Creature) -> Creature:
    return replace(name, creature)


def delete(name: str) -> None:
    if (creature := find(name)) is None:
        raise EntityNotFoundError(entity="creature", key=name)
    _creatures.remove(creature)
