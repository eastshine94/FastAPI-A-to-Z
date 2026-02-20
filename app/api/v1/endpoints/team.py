from typing import Annotated
from fastapi import APIRouter, Query
from sqlmodel import select

from app.core.database import SessionDep
from app.models.team import Team
from app.schemas.team import TeamCreate


router = APIRouter()


@router.get("/teams")
async def read_teams(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 20,
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.post("/teams")
async def create_team(team_data: TeamCreate, session: SessionDep) -> Team:
    team = Team.model_validate(team_data)
    session.add(team)
    session.commit()
    session.refresh(team)

    return team
