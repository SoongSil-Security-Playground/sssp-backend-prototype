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

import time
import logging

logging.basicConfig(level=logging.INFO)

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
    logging.info("Service Startup Process")
    db_init = False
    for i in range(5, -1, -1):
        try:
            models.Base.metadata.create_all(bind=engine)
            db_init = True
            break
        except:
            logging.warn("DB connection failed, retrying...")
            time.sleep(5)

    if not db_init:
        logging.error("Failed to initialize db")
        exit()

    logging.info("DB Connection success")
    try:

        new_user = User(
            username="user",
            email="user@example.com",
            hashed_password=get_password_hash("user"),
            contents="hihi",
            authority="USER",
        )

        new_admin = User(
            username=settings.initial_account.INITIAL_ADMIN_ID,
            email="admin@example.com",
            hashed_password=get_password_hash(
                settings.initial_account.INITIAL_ADMIN_ID
            ),
            contents="hihi",
            authority="ADMIN",
        )

        new_chall = Challenge(
            name="chall1",
            description="test",
            points=1000,
            category="PWN",
            file_path="https://rwx.kr/server.py",
            flag="flag{thisisflag}",
            decay=50,
            initial_points=1000,
            minimum_points=300,
            is_dynamic=True,
        )
        
        new_chall2 = Challenge(
            name="chall-2",
            description="new chall 2 test",
            points=1000,
            category="WEB",
            file_path=None,
            flag="flag{thisisflag}",
            decay=100,
            initial_points=1000,
            minimum_points=300,
            is_dynamic=True,
        )
        
        new_chall3 = Challenge(
            name="chall-3",
            description="chall3",
            points=1000,
            category="REV",
            file_path=None,
            flag="flag{thisisflag}",
            decay=50,
            initial_points=1000,
            minimum_points=300,
            is_dynamic=True,
        )
        
        new_chall4 = Challenge(
            name="chall-4",
            description="chall4 test test hoho",
            points=1000,
            category="MISC",
            file_path=None,
            flag="flag{thisisflag}",
            decay=50,
            initial_points=1000,
            minimum_points=300,
            is_dynamic=True,
        )

        db: Session = next(get_db())
        db.add(new_user)
        db.add(new_admin)
        db.add(new_chall)
        db.add(new_chall2)
        db.add(new_chall3)
        db.add(new_chall4)
        db.commit()
        db.refresh(new_chall)
        db.refresh(new_chall2)
        db.refresh(new_chall3)
        db.refresh(new_chall4)
        db.refresh(new_user)
        db.refresh(new_admin)
    except Exception as e:
        logging.warn(e)

    logging.info("Server Setup Finish")
