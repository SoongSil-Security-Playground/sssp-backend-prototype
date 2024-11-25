from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

# directory dependency
from SSSP.api.core.database import get_db
from SSSP.api.core import auth
from SSSP.api.models.enums.user_role import UserRole

from SSSP.config import settings

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


# 요청 바디를 위한 Pydantic 모델 추가
class PasswordUpdateRequest(BaseModel):
    cur_password: str
    new_password: str


@router.put("/update_password")
def update_password(
    password_data: PasswordUpdateRequest,
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = auth.get_current_user_by_jwt(token, db)

    logging.info(f"Password Change Request for user: {user.email}")
    logging.info(f"Current Password (Plain): {password_data.cur_password}")
    logging.info(f"Current Password (Hashed): {user.hashed_password}")

    if not auth.verify_password(password_data.cur_password, user.hashed_password):
        logging.warning(f"Password verification failed for user: {user.email}")
        return {"detail": "Current password not verified!"}

    new_hashed_password = auth.get_password_hash(password_data.new_password)
    user.hashed_password = new_hashed_password

    logging.info(f"New Password (Plain): {password_data.new_password}")
    logging.info(f"New Password (Hashed): {new_hashed_password}")

    db.commit()
    db.refresh(user)

    logging.info(f"Password successfully updated for user: {user.email}")
    return {"success": 1, "detail": "user password updated"}
