import random
from typing import Annotated, Literal
from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, AfterValidator, Field

router = APIRouter()




class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id:str):
    if not id.startswith(("isbn-","imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"} # 클라이언트가 쿼리 매개변수로 추가적인 데이터를 보내려고 하면 에러
    limit: int = Field(100,gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal['created_at', 'updated_at'] = 'created_at'
    tags: list[str] = []
    q: str | None = Field(
        None,    
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        alias="item-query", # 별칭 지정 => q는 더이상 사용할 수 없음
        deprecated=True, # docs에 deprecated 명시
        include_in_schema=False # docs 상에 안보이도록
    )
    id: Annotated[str|None, AfterValidator(check_valid_id)] = None



@router.get('/')
async def read_items(filter_query:Annotated[FilterParams, Query()]):
    id = filter_query.id
    query_items = {**filter_query.model_dump(), 'id': None}
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    query_items.update({"id": id, "name": item})
    return query_items



@router.get("/{item_id}")
async def read_item(item_id: Annotated[int,Path(title="The ID of the item to get", gt=0, le=1000)], needy: str, q: Annotated[str | None, Query(max_length=10,pattern="^fixedquery$")] = None, short: bool = False, ):
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
async def update_item(item_id:int, item: Item, q: str | None = None):
    result = {"item_id" : item_id, **item.model_dump()}
    if q is not None:
        result.update({"q":q})
    return result