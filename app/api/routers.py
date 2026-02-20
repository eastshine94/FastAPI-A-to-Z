from fastapi import APIRouter
from app.api.v1.endpoints import (
    item,
    user,
    model,
    file,
    index_weights,
    login,
    animal,
    hero,
    team,
)

api_router = APIRouter()

api_router.include_router(item.router, prefix="/items", tags=["items"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(animal.router, tags=["animals"])
api_router.include_router(model.router, prefix="/models", tags=["models"])
api_router.include_router(file.router, tags=["files"])
api_router.include_router(
    index_weights.router, prefix="/index-weights", tags=["index weights"]
)
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(hero.router, tags=["heros"])
api_router.include_router(team.router, tags=["teams"])
