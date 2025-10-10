import os
from datetime import datetime, timedelta, UTC
from typing import Any

import bcrypt
from dotenv import load_dotenv
from jose import jwt, JWTError

from cryptid.error import EntityNotFoundError, AuthenticationError, JWTValidationError
from cryptid.model.token import Token
from cryptid.model.user import PublicUser, PrivateUser

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import user as data
else:
    from cryptid.fake import user as data

load_dotenv()

JWT_SECRET_KEY = os.getenv("CRYPTID_JWT_SECRET_KEY", default="keep-it-secret-keep-it-safe")
JWT_ALGORITHM = os.getenv("CRYPTID_JWT_ALGORITHM", default="HS256")
JWT_EXPIRES_IN_MINUTES = float(os.getenv("CRYPTID_JWT_EXPIRES_IN_MINUTES", default="15"))


def create_token(username: str, password: str) -> Token:
    user = authenticate_user(username, password)
    token = create_jwt(
        claims={"sub": user.name, "roles": user.roles},
        expires_in=timedelta(minutes=JWT_EXPIRES_IN_MINUTES),
    )
    return token


def authenticate_user(name: str, password: str) -> PublicUser | PrivateUser:
    user = find_user(name, public=False)
    if not verify_password(password, user.hash):
        raise AuthenticationError(msg=f"wrong password '{password}' for user '{name}'")
    return user


def find_user(name: str, public: bool = True) -> PublicUser | PrivateUser:
    try:
        return data.get_one(name, public=public)
    except EntityNotFoundError:
        raise AuthenticationError(msg=f"user '{name}' does not exist")


def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def create_jwt(claims: dict[str, Any], expires_in: timedelta | None = timedelta(minutes=15)) -> Token:
    src = claims.copy()
    now = datetime.now(UTC)
    src.update({"iat": now})
    if expires_in is not None and expires_in >= timedelta(0):
        expires_at = now + expires_in
        src.update({"exp": expires_at})
    else:
        expires_in = None
        expires_at = None
    token = jwt.encode(src, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return Token(
        access=token,
        expires_in_seconds=int(expires_in.total_seconds()) if expires_in is not None else None,
        expires_at=expires_at,
        issued_at=now,
    )


def parse_jwt(token: str) -> dict[str, Any]:
    try:
        claims = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return claims
    except JWTError as e:
        raise JWTValidationError() from e


def get_user_from_jwt(token: str) -> PublicUser:
    claims = parse_jwt(token)
    if (username := claims.get("sub")) is None:
        raise JWTValidationError(msg="claim 'sub' required")
    if (roles := claims.get("roles")) is None:
        raise JWTValidationError(msg="claim 'roles' required")
    return PublicUser(name=username, roles=roles)


def find_user_by_jwt(token: str) -> PublicUser:
    user = get_user_from_jwt(token)
    return find_user(user.name)


def make_hash(plain: str) -> str:
    plain_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(plain_bytes, salt)
    return hashed_bytes.decode("utf-8")
