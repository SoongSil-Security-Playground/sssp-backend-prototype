from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import DataError, IntegrityError
from pydantic import ValidationError
import os
import requests

# directory dependency
from SSSP.api.models import models
from SSSP.api.core.database import engine, get_db
from SSSP.config import settings
from SSSP.api.exception.global_exception_handler import (
    global_exception_handler,
    sqlalchemy_data_error_handler,
    sqlalchemy_integrity_error_handler,
    pydantic_validation_exception_handler,
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

# apimain = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")
apimain = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
apimain.include_router(v1api, prefix="/api/v1")
apimain.add_exception_handler(DataError, sqlalchemy_data_error_handler)
apimain.add_exception_handler(IntegrityError, sqlalchemy_integrity_error_handler)
apimain.add_exception_handler(Exception, global_exception_handler)
apimain.add_exception_handler(ValidationError, pydantic_validation_exception_handler)


# 여기에 미들웨어 추가
@apimain.middleware("http")
async def error_notification_middleware(request, call_next):
    try:
        response = await call_next(request)

        # 400/500 에러 체크
        if 400 <= response.status_code < 600:
            error_message = f"Status Code: {response.status_code}, Path: {request.url.path}, Method: {request.method}"
            send_discord_webhook(error_message)

        return response
    except Exception as e:
        # 예외 발생 시에도 디스코드로 알림
        error_message = f"Internal Server Error: {str(e)}, Path: {request.url.path}, Method: {request.method}"
        send_discord_webhook(error_message)
        raise


# CORS
origins = ["http://localhost:3000", "https://soongsil-security-playground.github.io"]
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

        new_admin = User(
            username=settings.initial_account.INITIAL_ADMIN_ID,
            email="admin@example.com",
            hashed_password=get_password_hash(
                settings.initial_account.INITIAL_ADMIN_ID
            ),
            contents="hihi",
            authority="ADMIN",
        )

        db: Session = next(get_db())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    except Exception as e:
        logging.warn(e)

    logging.info("Server Setup Finish")


def send_discord_webhook(error_message: str):
    webhook_url = settings.discord.DISCORD_WEBHOOK
    payload = {"content": f"🚨 에러 발생: {error_message}"}
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        logging.error(f"Discord webhook 전송 실패: {e}")
