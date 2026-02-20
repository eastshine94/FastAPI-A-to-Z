from sqlmodel import SQLModel, Field


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")
