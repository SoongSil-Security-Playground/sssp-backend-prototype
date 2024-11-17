from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import DataError, IntegrityError

import os

# directory dependency
from SSSP.api.models import models
from SSSP.api.core.database import engine, get_db
from SSSP.config import settings
from SSSP.api.exception.global_exception_handler import (
    global_exception_handler,
    validation_exception_handler,
    sqlalchemy_data_error_handler,
    sqlalchemy_integrity_error_handler,
)

# Router
from SSSP.api.routers.v1.api import router as v1api

# Initialize
from sqlalchemy.orm import Session
from SSSP.api.models.models import User, Challenge
from SSSP.api.core.database import get_db
from SSSP.api.core.auth import get_password_hash

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

@apimain.on_event("startup")
async def server_start():
    try:
        new_user = User(
            username='user',
            email='user@example.com',
            hashed_password=get_password_hash("user"),
            contents="hihi",
            authority="USER"
        )

        new_admin = User(
            username=settings.initial_account.INITIAL_ADMIN_ID,
            email='admin@example.com',
            hashed_password=get_password_hash(settings.initial_account.INITIAL_ADMIN_ID),
            contents="hihi",
            authority="ADMIN"
        )

        new_chall = Challenge(
        name="chall1",
        description="test",
        points=1000,
        category="PWN",
        file_path=None,
        flag="flag{thisisflag}",

        decay=50,
        initial_points=1000,
        minimum_points=300,
        is_dynamic=True,
    )

        db:Session = next(get_db())
        db.add(new_user)
        db.add(new_admin)
        db.add(new_chall)
        db.commit()
        db.refresh(new_chall)
        db.refresh(new_user)
        db.refresh(new_admin)
    except:
        pass
