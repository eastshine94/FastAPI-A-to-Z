import random
from typing import Annotated, Literal
from fastapi import APIRouter, Query, Path, Body, status
from pydantic import BaseModel, AfterValidator, Field, HttpUrl

router = APIRouter()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None
    tags: set[str] = []  # set으로 지정 시 고유한 항목들의 집합으로 출력됨
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [{"username": "Kim", "full_name": "KillDong"}]
        }
    }


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


class FilterParams(BaseModel):
    model_config = {
        "extra": "forbid"
    }  # 클라이언트가 쿼리 매개변수로 추가적인 데이터를 보내려고 하면 에러
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
    q: str | None = Field(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        alias="item-query",  # 별칭 지정 => q는 더이상 사용할 수 없음
        deprecated=True,  # docs에 deprecated 명시
        include_in_schema=False,  # docs 상에 안보이도록
    )
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None


@router.get("/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    id = filter_query.id
    query_items = {**filter_query.model_dump(), "id": None}
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    query_items.update({"id": id, "name": item})
    return query_items


@router.get(
    "/{item_id}",
)
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    needy: str,
    q: Annotated[str | None, Query(max_length=10, pattern="^fixedquery$")] = None,
    short: bool = False,
):
    item = {"item_id": item_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: Annotated[
        Item,
        Body(
            # embed=True,
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@router.post("/multiple")
async def create_multiple_images(images: list[Image]):
    for image in images:
        image.url
    return images


@router.put("/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):

    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
