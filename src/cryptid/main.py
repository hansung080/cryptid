from typing import Any

import uvicorn
from fastapi import FastAPI

from cryptid.web import auth, creature, explorer, user

app: FastAPI = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(explorer.router)
app.include_router(creature.router)


@app.get("/health")
@app.get("/health/")
def health_check() -> dict[str, Any]:
    return {"status": "ok"}


def run(application: str = "src.cryptid.main:app") -> None:
    uvicorn.run(application, reload=True)


if __name__ == "__main__":
    run("main:app")
