from fastapi import APIRouter, HTTPException

from app.core.exceptions import UnicornException

router = APIRouter()

animals = {"lion": "The Lion King"}


@router.get("/animals/{animal_id}")
async def read_animal(animal_id: str):
    if animal_id not in animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {"animal": animals[animal_id]}


@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
