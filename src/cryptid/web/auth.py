from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from cryptid.error import AuthenticationError, JWTValidationError
from cryptid.model.auth import AuthUser, Token, TokenResponse
from cryptid.service import auth as service

router: APIRouter = APIRouter(prefix="/auth")
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_user(token: str = Depends(oauth2_scheme)) -> AuthUser:
    try:
        return service.get_user_from_jwt(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def _require_role(role: str, user: AuthUser) -> AuthUser:
    if role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"role '{role}' required",
        )
    return user


def user_role(user: AuthUser = Depends(get_auth_user)) -> AuthUser:
    return _require_role("user", user)


def admin_role(user: AuthUser = Depends(get_auth_user)) -> AuthUser:
    return _require_role("admin", user)


@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
@router.post("/token/", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def create_token(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    try:
        return service.create_token(form.username, form.password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="incorrect username or password",  # for security
            detail=str(e),  # for debugging
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/token")
@router.get("/token/")
def verify_token(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    try:
        claims = service.parse_jwt(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = claims.get("sub")
    try:
        if sub:
            _ = service.find_user(sub)
        else:
            raise JWTValidationError(msg="claim 'sub' required")
    except AuthenticationError:
        user_exists = False
    else:
        user_exists = True

    exp = claims.get("exp")
    iat = claims.get("iat")
    return {
        "claims": {
            "sub": sub,
            "exp": exp,
            "exp_utc": datetime.fromtimestamp(exp, tz=timezone.utc) if exp is not None else None,
            "exp_local": datetime.fromtimestamp(exp) if exp is not None else None,
            "iat": iat,
            "iat_utc": datetime.fromtimestamp(iat, tz=timezone.utc) if iat is not None else None,
            "iat_local": datetime.fromtimestamp(iat) if iat is not None else None,
            "roles": claims.get("roles"),
        },
        "user_exists": user_exists,
    }
