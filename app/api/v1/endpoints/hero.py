from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.core.database import SessionDep
from app.models.hero import Hero
from app.schemas.hero import HeroCreate


router = APIRouter()


@router.post("/heroes/")
def create_hero(hero_data: HeroCreate, session: SessionDep) -> Hero:
    hero = Hero.model_validate(hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/heroes/")
def read_heroes(
    session: SessionDep,
    age: int | None = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    query = select(Hero)
    if age is not None:
        query = query.where(Hero.age > age)

    heroes = session.exec(query.offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
