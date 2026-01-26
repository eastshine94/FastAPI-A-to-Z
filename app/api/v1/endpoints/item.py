from fastapi import APIRouter

router = APIRouter()

@router.get("/{item_id}")
async def read_item(item_id: str, needy: str, q: str | None = None, short: bool = False, ):
    item = {"item_id": item_id,"needy":needy }
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return item