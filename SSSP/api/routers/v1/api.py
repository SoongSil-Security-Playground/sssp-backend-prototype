from fastapi import APIRouter

# directory dependency

from SSSP.api.routers.v1.auth import auth_check, register, login
from SSSP.api.routers.v1.user import user_list, user, delete


router = APIRouter()

# auth
router.include_router(login.router, prefix="/auth", tags=["auth"])
router.include_router(register.router, prefix="/auth", tags=["auth"])
router.include_router(auth_check.router, prefix="/auth", tags=["auth"])

# user
router.include_router(delete.router, prefix="/user", tags=["user"])
router.include_router(user_list.router, prefix="/user", tags=["user"])
router.include_router(user.router, prefix="/user", tags=["user"])
