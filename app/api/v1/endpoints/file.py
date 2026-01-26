from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_file(file_path: str):
    return {"file_path": file_path}