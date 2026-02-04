from pydantic import BaseModel


class HeroCreate(BaseModel):
    name: str
    age: int | None
    secret_name: str
