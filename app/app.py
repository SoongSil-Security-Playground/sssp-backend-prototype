from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import engine
from app import models

# Router
from app.routers import users

models.Base.metadata.create_all(bind=engine)

apimain = FastAPI()

apimain.include_router(users.router)

favicon_path = './static/favicon.ico'

@apimain.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
