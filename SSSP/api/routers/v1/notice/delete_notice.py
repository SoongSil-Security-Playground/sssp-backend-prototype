from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.models.enums.user_role import UserRole

from SSSP.api.core.database import *
from SSSP.api.core.auth import get_current_user_by_jwt

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.delete("/notice")
def delete_notice(
    notice_id: int,
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user_by_jwt(token, db)
    if user.authority != UserRole.ADMIN:
        logging.warning(f"Unauthorized attempt to delete notice by user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete notice",
        )

    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()

    if not notice:
        logging.warning(f"Notice not found for deletion: ID {notice_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found"
        )

    db.delete(notice)
    db.commit()

    logging.info(f"Notice deleted successfully: ID {notice_id}")

    return {"success": 1}
