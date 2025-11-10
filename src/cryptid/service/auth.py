import os
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from cryptid.data.init import get_cursor
from cryptid.env import JWT_ALGORITHM, JWT_EXPIRES_IN_MINUTES, JWT_SECRET_KEY
from cryptid.error import AuthenticationError, EntityNotFoundError, JWTValidationError
from cryptid.model.auth import AuthUser, Token
from cryptid.model.user import PrivateUser, PublicUser

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import user as data
else:
    from cryptid.fake.data import user as data


def create_token(user_id: str, password: str) -> Token:
    user = authenticate_user(user_id, password)
    token = create_jwt(
        claims={"sub": user.id, "roles": user.roles},
        expires_in=timedelta(minutes=JWT_EXPIRES_IN_MINUTES),
    )
    return token


def authenticate_user(id_: str, password: str) -> PrivateUser:
    user = find_user(id_, public=False)
    if not verify_password(password, user.hash):
        raise AuthenticationError(msg=f"wrong password '{password}' for user '{id_}'")
    return user


def find_user(id_: str, public: bool = True) -> PublicUser | PrivateUser:
    try:
        return data.get_one(get_cursor(), id_, public=public)
    except EntityNotFoundError:
        raise AuthenticationError(msg=f"user '{id_}' does not exist")


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
    # The `iat`, `exp`, `nbf` claims will be converted from datetime to Unix timestamp (integer in seconds),
    # but the other claims with datetime will cause TypeError: Object of type datetime is not JSON serializable.
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


def get_user_from_jwt(token: str) -> AuthUser:
    claims = parse_jwt(token)
    if (user_id := claims.get("sub")) is None:
        raise JWTValidationError(msg="claim 'sub' required")
    if (roles := claims.get("roles")) is None:
        raise JWTValidationError(msg="claim 'roles' required")
    return AuthUser(id=user_id, roles=roles)


def find_user_by_jwt(token: str) -> PublicUser:
    user = get_user_from_jwt(token)
    return find_user(user.id)


def make_hash(plain: str) -> str:
    plain_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(plain_bytes, salt)
    return hashed_bytes.decode("utf-8")
