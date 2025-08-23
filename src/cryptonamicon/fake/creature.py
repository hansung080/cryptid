from cryptonamicon.model.creature import Creature


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


def create(creature: Creature) -> Creature:
    # TODO: To implement the body.
    return creature


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Creature | None:
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


def replace(name: str, creature: Creature) -> Creature | None:
    # TODO: To implement the body.
    return creature


def modify(name: str, creature: Creature) -> Creature | None:
    # TODO: To implement the body.
    return creature


def delete(name: str) -> bool:
    # TODO: To implement the body.
    for _creature in _creatures:
        if _creature.name == name:
            return True
    return False
