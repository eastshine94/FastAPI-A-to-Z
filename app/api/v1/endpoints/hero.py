from typing import Annotated, Any
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.core.database import SessionDep
from app.models.hero import Hero
from app.schemas.hero import HeroCreate, HeroUpdate


router = APIRouter()


@router.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 2,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.get("/first-hero", summary="First or None")
def search_heros(age: Annotated[int, Query(gt=0)], session: SessionDep):
    statement = select(Hero).where(Hero.age >= age)
    # first는 여러개 중 첫번째 값을 가져온다
    # 충족하는 조건이 없으면 None
    results = session.exec(statement).first()
    return results


@router.get("/one-hero", summary="Exactly One")
def search_heros(age: Annotated[int, Query(gt=0)], session: SessionDep):
    statement = select(Hero).where(Hero.age >= age)
    # 쿼리와 일치하는 행이 정확히 하나만 있는지 확인해야 하는 경우
    # 2개 이상 또는 존재하지 않으면 에러
    results = session.exec(statement).one()
    return results


@router.post("/heroes/")
def create_hero(hero_data: HeroCreate, session: SessionDep) -> Hero:
    hero = Hero.model_validate(hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.put("/heroes/{hero_id}")
def update_hero(hero_id: int, hero_data: HeroUpdate, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # exclude_unset=True: 요청에 포함된 필드만 업데이트
    update_data = hero_data.model_dump(exclude_unset=True)
    hero.sqlmodel_update(update_data)

    session.add(hero)
    session.commit()
    session.refresh(hero)

    return hero


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
