from fastapi import APIRouter

import cryptonamicon.service.creature as service

from cryptonamicon.model.creature import Creature


router = APIRouter(prefix="/creature")


@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get_one(name)


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature | None:
    return service.replace(name, creature)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature | None:
    return service.modify(name, creature)


@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)

