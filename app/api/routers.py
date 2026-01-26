from fastapi import APIRouter
from .v1.endpoints import item, user, model, file


api_router = APIRouter()

api_router.include_router(item.router, prefix="/items", tags=['items'])
api_router.include_router(user.router, prefix="/users", tags=['users'])
api_router.include_router(model.router, prefix="/models", tags=['models'])
api_router.include_router(file.router, prefix="/files", tags=['files'])