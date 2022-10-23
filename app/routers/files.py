import asyncio

from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


def bytes_to_str(data: bytes) -> str:
    return data.decode("utf-8")


# File Upload
@router.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    contents_bytes = await file.read()
    contents = bytes_to_str(contents_bytes)
    return {
        "filename": file.filename,
        "contentType": file.content_type,
        "contents": contents,
    }


async def process_file(file: UploadFile):
    contents_bytes = await file.read()
    contents = bytes_to_str(contents_bytes)
    return {
        "filename": file.filename,
        "contentType": file.content_type,
        "contents": contents,
    }


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    result_files = await asyncio.gather(*[process_file(file) for file in files])
    return {"files": result_files}


@router.post("/file_with_form")
async def create_files_with_form(file: bytes = File(), token: str = Form()):
    return {"file_size": len(file), "token": token}
