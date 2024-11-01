from fastapi import APIRouter

from SSSP.api.routers.v1.auth import register, login, test
from SSSP.api.routers.v1.default import user_list

from SSSP.api.routers.v1.user import delete

router = APIRouter()

# default
router.include_router(user_list.router)

# auth
router.include_router(login.router, prefix="/auth", tags=["auth"])
router.include_router(register.router, prefix="/auth", tags=["auth"])
router.include_router(test.router, prefix="/auth", tags=["auth"])

# user
router.include_router(delete.router, prefix="/user", tags=["user"])
