from fastapi import FastAPI

app = FastAPI(
    tittle="shortener-url",
    description="A simple URL shortener service",
    version="v0",
)

@app.get("/", tags=["health"])
async def read_root():
    return {"message": "Welcome to the URL Shortener API!"}