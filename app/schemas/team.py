from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    headquarters: str
