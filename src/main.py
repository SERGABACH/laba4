from fastapi import FastAPI

from src.routers import note_router, auth_router
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    app.include_router(note_router.router)
    app.include_router(auth_router.router)
    uvicorn.run(app,
                host="localhost",
                port=8080)
