from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_notice
from SSSP.api.core.database import *
from SSSP.api.core.auth import get_current_user_by_jwt

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/notice", response_model=list[schema_notice.NoticeResponse])
def get_all_notice(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = get_current_user_by_jwt(token, db)

    notice_list = db.query(models.Notice).all()
    notice_response = [
        schema_notice.NoticeResponse.from_orm(notice) for notice in notice_list
    ]
    logging.info(f"[*] Notice List >> {notice_response}")

    return notice_response[::-1]
