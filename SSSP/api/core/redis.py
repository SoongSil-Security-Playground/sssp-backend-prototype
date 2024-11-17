import redis
from SSSP.config import settings


def get_redis():
    return redis.Redis(
        host=settings.redis.REDIS_HOST,
        port=settings.redis.REDIS_PORT,
        db=0,
        decode_responses=True,
    )


# Redis 관련 상수
AUTH_CODE_PREFIX = "email_auth:"
AUTH_CODE_EXPIRE_MINUTES = 5


def get_auth_key(email: str) -> str:
    """
    이메일 인증 코드를 위한 Redis 키 생성
    """
    return f"{AUTH_CODE_PREFIX}{email}"
