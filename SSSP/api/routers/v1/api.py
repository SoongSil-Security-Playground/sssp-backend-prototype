from fastapi import APIRouter

# directory dependency

from SSSP.api.routers.v1 import health_check
from SSSP.api.routers.v1.auth import auth_check, register, login
from SSSP.api.routers.v1.user import (
    delete_current_user,
    get_current_user,
    get_user_list,
    update_current_user,
)
from SSSP.api.routers.v1.challange import (
    get_challenges,
)


router = APIRouter()


# auth
router.include_router(login.router, prefix="/auth", tags=["auth"])
router.include_router(register.router, prefix="/auth", tags=["auth"])
router.include_router(auth_check.router, prefix="/auth", tags=["auth"])
router.include_router(health_check.router, tags=["health-check"])

# user
router.include_router(delete_current_user.router, prefix="/user", tags=["user"])
router.include_router(get_user_list.router, prefix="/user", tags=["user"])
router.include_router(get_current_user.router, prefix="/user", tags=["user"])
router.include_router(update_current_user.router, prefix="/user", tags=["user"])

# challenge
router.include_router(get_challenges.router, prefix="/challenges", tags=["challenge"])
