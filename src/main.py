from fastapi import FastAPI
from src.routes import auth


app = FastAPI(
    tittle="shortener-url",
    description="A simple URL shortener service",
    version="v0",
)

app.include_router(auth.router)


@app.get("/", tags=["health"])
async def read_root():
    return {"message": "Welcome to the URL Shortener API!"}