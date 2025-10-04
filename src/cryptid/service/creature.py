import os

from cryptid.model.creature import Creature, PartialCreature

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import creature as data
else:
    from cryptid.fake import creature as data


def create(creature: Creature) -> Creature:
    return data.create(creature)


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name: str) -> Creature:
    return data.get_one(name)


def replace(name: str, creature: Creature) -> Creature:
    return data.replace(name, creature)


def modify(name: str, creature: PartialCreature) -> Creature:
    return data.modify(name, creature)


def delete(name: str) -> None:
    data.delete(name)
