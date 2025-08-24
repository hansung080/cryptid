from fastapi import APIRouter

import cryptonamicon.service.explorer as service

from cryptonamicon.model.explorer import Explorer


router = APIRouter(prefix="/explorer")


@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
    return service.get_one(name)


@router.put("/{name}")
def replace(name: str, explorer: Explorer) -> Explorer | None:
    return service.replace(name, explorer)


@router.patch("/{name}")
def modify(name: str, explorer: Explorer) -> Explorer | None:
    return service.modify(name, explorer)


@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)
