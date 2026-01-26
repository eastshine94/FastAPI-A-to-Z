from fastapi import FastAPI
from .api.routers import api_router

app = FastAPI(
    title="My FastAPI Project",
    description="API documentation",
    version= "1.0.0"
)


app.include_router(api_router, prefix='/api/v1')

