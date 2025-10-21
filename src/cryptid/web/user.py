import os

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.auth import AuthUser
from cryptid.model.user import PublicUser, SignInUser, PartialUser
from cryptid.web.auth import user_role, admin_role

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.service import user as service
else:
    from cryptid.fake import user as service

router = APIRouter(prefix="/users")


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: SignInUser) -> PublicUser:
    try:
        return service.create(user)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("", dependencies=[Depends(admin_role)])
@router.get("/", dependencies=[Depends(admin_role)])
def get_all() -> list[PublicUser]:
    return service.get_all()


@router.get("/me")
@router.get("/me/")
def get_me(me: AuthUser = Depends(user_role)) -> PublicUser:
    try:
        return service.get_one(me.name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{name}", dependencies=[Depends(admin_role)])
@router.get("/{name}/", dependencies=[Depends(admin_role)])
def get_one(name: str) -> PublicUser:
    try:
        return service.get_one(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/me")
@router.put("/me/")
def replace_me(user: PublicUser, me: AuthUser = Depends(user_role)) -> PublicUser:
    try:
        return service.replace(me.name, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{name}", dependencies=[Depends(admin_role)])
@router.put("/{name}/", dependencies=[Depends(admin_role)])
def replace(name: str, user: PublicUser) -> PublicUser:
    try:
        return service.replace(name, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/me")
@router.patch("/me/")
def modify_me(user: PartialUser, me: AuthUser = Depends(user_role)) -> PublicUser:
    try:
        return service.modify(me.name, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{name}", dependencies=[Depends(admin_role)])
@router.patch("/{name}/", dependencies=[Depends(admin_role)])
def modify(name: str, user: PartialUser) -> PublicUser:
    try:
        return service.modify(name, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(me: AuthUser = Depends(user_role)) -> None:
    try:
        service.delete(me.name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_role)])
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_role)])
def delete(name: str) -> None:
    try:
        service.delete(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
