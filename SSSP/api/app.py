from fastapi import FastAPI
from fastapi.responses import FileResponse

# directory dependency
from SSSP.api.models import models
from SSSP.api.core.database import engine

# Router
from SSSP.api.routers.v1.api import router as v1api

models.Base.metadata.create_all(bind=engine)

apimain = FastAPI()
apimain.include_router(v1api, prefix="/api/v1")

# setup favicon

favicon_path = './static/favicon.ico'
@apimain.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
