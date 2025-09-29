from httpx import Response
from pydantic import BaseModel


def assert_response(
    resp: Response,
    *,
    status_code: int,
    json: BaseModel | None = None,
    body_none: bool = False
) -> None:
    assert resp.status_code == status_code
    if json is None:
        if body_none:
            assert resp.content == b""
    else:
        assert resp.json() == json.model_dump()
