from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.models.enums.user_role import UserRole

from SSSP.api.core.database import *
from SSSP.api.core.auth import get_current_user_by_jwt

from SSSP.api.schemas import schema_notice


import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.post("/notice", response_model=schema_notice.NoticeResponse)
def create_notice(
    title: str = Form(...),
    content: str = Form(...),
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user_by_jwt(token, db)
    if user.authority != UserRole.ADMIN:
        logging.warning(f"Unauthorized attempt to create notice by user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create notice",
        )

    new_notice = models.Notice(
        title=title,
        content=content,
        author_id=user.id,
    )

    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)

    logging.info("======== New Notice ========")
    logging.info(f"= Title : {title}")
    logging.info(f"= Content : {content}")

    return schema_notice.NoticeResponse.from_orm(new_notice)
