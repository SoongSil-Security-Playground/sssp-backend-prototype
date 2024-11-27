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


@router.patch("/notice")
def update_notice(
    notice_id: int,
    title: str = Form(None),
    content: str = Form(None),
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user_by_jwt(token, db)
    if user.authority != UserRole.ADMIN:
        logging.warning(f"Unauthorized attempt to update notice by user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update notice",
        )

    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()

    if not notice:
        logging.warning(f"Notice not found for update: ID {notice_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found"
        )

    if title is not None:
        notice.title = title

    if content is not None:
        notice.content = content

    db.commit()
    db.refresh(notice)

    return {"success": 1}
