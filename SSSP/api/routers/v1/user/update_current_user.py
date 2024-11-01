from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core import auth
from SSSP.api.core.database import *
from SSSP.api.schemas.schema_users import UserUpdateRequest

router = APIRouter()


@router.patch("/user", response_model=schema_users.UserResponse)
def update_current_user(
    user_update: UserUpdateRequest,
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    find_user_name = auth.get_current_user_by_jwt(token, db)
    logging.info(f"[*] UPDATE_CURRENT_USER>> find user {find_user_name}")

    if user_update.contents is not None:
        find_user_name.contents = user_update.contents
        db.commit()
        db.refresh(find_user_name)

    return schema_users.UserResponse.from_orm(find_user_name)
