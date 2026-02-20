from typing import Annotated, Any
from fastapi import APIRouter, File, UploadFile, Form

router = APIRouter()


@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@router.post("/files/")
async def create_file(
    *,
    file: Annotated[bytes | None, File(description="A file read as bytes")] = None,
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
) -> dict[str, Any]:
    if not file:
        return {"message": "No file sent"}
    else:
        return {
            "file_size": len(file),
            "token": token,
            "fileb_content_type": fileb.content_type,
        }


@router.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[
        UploadFile | None, File(description="A file read as UploadFile")
    ] = None,
):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@router.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}
