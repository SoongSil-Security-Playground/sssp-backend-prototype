from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from SSSP.api.core import auth

# directory dependency
from SSSP.api.models import models
from SSSP.api.core import auth

from SSSP.api.core.database import *
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    delete_target_user = auth.get_current_user_by_jwt(token, db)

    if not delete_target_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(delete_target_user)
    db.commit()

    return {"message": "User deleted successfully"}
