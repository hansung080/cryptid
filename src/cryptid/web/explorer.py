from fastapi import APIRouter, HTTPException

import cryptid.service.explorer as service
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer

router = APIRouter(prefix="/explorer")


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
@router.get("/{name}/")
def get_one(name: str) -> Explorer:
    try:
        return service.get_one(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{name}")
@router.put("/{name}/")
def replace(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.replace(name, explorer)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{name}")
@router.patch("/{name}/")
def modify(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.modify(name, explorer)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{name}", status_code=204)
@router.delete("/{name}/", status_code=204)
def delete(name: str) -> None:
    try:
        service.delete(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
