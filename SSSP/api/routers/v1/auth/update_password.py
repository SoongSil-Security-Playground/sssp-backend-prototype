from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.core.database import get_db
from SSSP.api.core import auth
from SSSP.api.models.enums.user_role import UserRole

from SSSP.config import settings

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/update_password")
def update_password(
    cur_password: str,
    new_password: str,
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = auth.get_current_user_by_jwt(token, db)

    if not auth.verify_password(cur_password, user.hashed_password):
        return {"detail":"Current password not verified!"}
    
    user.hashed_password = auth.get_password_hash(new_password)

    db.commit()
    db.refresh(user)

    return {"success":1, "detail":"user password updated"}

