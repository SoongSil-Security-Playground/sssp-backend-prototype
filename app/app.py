from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models

# Router
from app.routers import users

models.Base.metadata.create_all(bind=engine)

apimain = FastAPI()

apimain.include_router(users.router)