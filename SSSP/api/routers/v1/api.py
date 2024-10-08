from fastapi import APIRouter
from SSSP.api.routers.v1.user import login, register, user_list

router = APIRouter()

router.include_router(login.router, prefix="/auth", tags=["users"])
router.include_router(register.router, prefix="/auth", tags=["auth"])
router.include_router(user_list.router, prefix="/users", tags=["auth"])