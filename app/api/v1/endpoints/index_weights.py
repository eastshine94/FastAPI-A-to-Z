from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_index_weights(weights: dict[int, float]):
    return weights