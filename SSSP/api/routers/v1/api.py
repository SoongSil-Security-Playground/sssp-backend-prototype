from fastapi import APIRouter

from SSSP.api.routers.v1.auth import register, login
from SSSP.api.routers.v1.default import user_list

router = APIRouter()

# default
router.include_router(user_list.router)

# auth
router.include_router(login.router, prefix="/auth", tags=["auth"])
router.include_router(register.router, prefix="/auth", tags=["auth"])