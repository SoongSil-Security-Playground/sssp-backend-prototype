from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# directory dependency
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "5c7d114c1b5bf6c813dbdb1632ca9860a9b91864287493828a6489f484ba648d53a810af7d3ba8f39134dc4287ae0334d363d58b010224ad4577e0129f629336a9add5925d171fc989a4b23561eb08cc5e27828fbaaf4d841b00d73b4662162064f4753d2b10e8417306f58aa1ccc7c84fde678dcef020301c2ecec80b48311f6f9e9e05610f89f8ba0a0fadbf10e925f028bb826eb0668ffe1e15e1b3ec7680e91b9656cf42ce031f72cf0afc95a2094815eb5122b5f98cd8e837d04d4d89edc335a56167d90c82e9355b34512b56a07eeb2a2ffd53f8dc7c6cf708d8cac5c97172b5210a72dbcdb5b7d83940cd9fd52cde1c42ac402f9478314f296dece48f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
