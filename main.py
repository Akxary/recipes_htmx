from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.routers.auth import router as auth_router
from app.routers.recipes import router as recipe_router

fastapi_app = FastAPI()
fastapi_app.mount("/static", StaticFiles(directory="resources/static"), name="static")

fastapi_app.include_router(auth_router)
fastapi_app.include_router(recipe_router)

if __name__ == "__main__":
    uvicorn.run(fastapi_app, port=56789)
