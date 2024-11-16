from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import DataError, IntegrityError


import os

# directory dependency
from SSSP.api.models import models
from SSSP.api.core.database import engine
from SSSP.config import settings
from SSSP.api.exception.global_exception_handler import (
    global_exception_handler,
    validation_exception_handler,
    sqlalchemy_data_error_handler,
    sqlalchemy_integrity_error_handler,
)

# Router
from SSSP.api.routers.v1.api import router as v1api

models.Base.metadata.create_all(bind=engine)


apimain = FastAPI()
apimain.include_router(v1api, prefix="/api/v1")
apimain.add_exception_handler(DataError, sqlalchemy_data_error_handler)
apimain.add_exception_handler(IntegrityError, sqlalchemy_integrity_error_handler)
apimain.add_exception_handler(Exception, global_exception_handler)
apimain.add_exception_handler(Exception, validation_exception_handler)

# CORS
origins = ["http://localhost:3000"]
apimain.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setup favicon
favicon_path = settings.favicon_path


@apimain.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@apimain.get("/health-check")
def health_check():
    return {"status": "healthy"}


@apimain.get("/")
def root():
    return {"Hello": "SSSP"}
