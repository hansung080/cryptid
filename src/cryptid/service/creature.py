import cryptid.data.creature as data
from cryptid.model.creature import Creature


def create(creature: Creature) -> Creature:
    return data.create(creature)


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name: str) -> Creature:
    return data.get_one(name)


def replace(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)


def modify(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)


def delete(name: str) -> None:
    data.delete(name)
