import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI()
app.add_middleware(
    # Ignore the warning: Expected type '_MiddlewareFactory[ParamSpec("P")]', got 'Type[CORSMiddleware]' instead
    # because this code runs fine in the runtime, and it's a formal example from FastAPI.
    CORSMiddleware,
    allow_origins=[
        # "*",                      # Allow all origins without credentials.
        "https://ui.cryptids.com",  # Allow this origin with or without credentials.
        "http://localhost:3000",    # Allow this origin with or without credentials.
        "null",                     # Allow the origin `file:///...` with or without credentials, but has security risk.
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/test-cors")
def test_cors(request: Request) -> str:
    print(request)
    return "CORS Test OK"


if __name__ == "__main__":
    uvicorn.run("cors:app", reload=True)
