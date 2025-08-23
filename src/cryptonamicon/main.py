import uvicorn

from fastapi import FastAPI

from cryptonamicon.web import explorer, creature


app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)


@app.get("/echo/{thing}")
def echo(thing: str) -> str:
    return thing


def run(application: str = "src.cryptonamicon.main:app") -> None:
    uvicorn.run(application, reload=True)


if __name__ == "__main__":
    run("main:app")
