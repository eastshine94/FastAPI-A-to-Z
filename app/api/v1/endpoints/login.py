from typing import Annotated
from fastapi import APIRouter, Form
from pydantic import BaseModel


router = APIRouter()


class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@router.post("/")
async def login(data: Annotated[FormData, Form()]):
    return data
