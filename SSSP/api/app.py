from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

# directory dependency
from SSSP.api.models import models
from SSSP.api.core.database import engine
from SSSP.config import settings
from SSSP.api.exception.global_exception_handler import global_exception_handler

# Router
from SSSP.api.routers.v1.api import router as v1api

models.Base.metadata.create_all(bind=engine)

apimain = FastAPI()
apimain.include_router(v1api, prefix="/api/v1")
apimain.add_exception_handler(Exception, global_exception_handler)

# setup favicon
favicon_path = settings.favicon_path


@apimain.get("/favicon.ico", include_in_schema=False)
async def favicon():
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)

    for item in os.listdir(current_directory):
        print(item)
    return FileResponse(favicon_path)
