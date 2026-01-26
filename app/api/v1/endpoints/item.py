from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@router.get("/{item_id}")
async def read_item(item_id: str, needy: str, q: str | None = None, short: bool = False, ):
    item = {"item_id": item_id,"needy":needy }
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return item

@router.post("/")
async def create_item(item:Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@router.put("/{item_id}")
async def update_item(item_id:int, item: Item, q: str |None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q is not None:
        result.update({"q":q})
    return result