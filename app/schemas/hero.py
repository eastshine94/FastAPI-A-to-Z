from pydantic import BaseModel


class HeroCreate(BaseModel):
    name: str
    age: int | None
    secret_name: str


class HeroUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
