from cryptid.fake.data import creature as data
from cryptid.model.creature import Creature, PartialCreature


def create(creature: Creature) -> Creature:
    return data.create(None, creature)


def get_all() -> list[Creature]:
    return data.get_all(None)


def get_one(name: str) -> Creature:
    return data.get_one(None, name)


def replace(name: str, creature: Creature) -> Creature:
    return data.replace(None, name, creature)


def modify(name: str, creature: PartialCreature) -> Creature:
    return data.modify(None, name, creature)


def delete(name: str) -> None:
    data.delete(None, name)
