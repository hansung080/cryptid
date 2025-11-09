import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
basic = HTTPBasic()

secret_username = "me"
secret_password = "secret"


@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_username and creds.password == secret_password:
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(
        status_code=401,
        detail=f"authentication failed for '{creds.username}' with password '{creds.password}'"
    )


if __name__ == "__main__":
    uvicorn.run("basic_auth:app", reload=True)
