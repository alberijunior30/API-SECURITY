from fastapi import APIRouter

from api.v1.endpoints import articles
from api.v1.endpoints import users

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/artigos", tags=["artigos"])
api_router.include_router(users.router, prefix="/usuarios", tags=["usuários"])