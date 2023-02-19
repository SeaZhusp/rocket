import os

from fastapi import APIRouter, UploadFile, File, Depends

from app.core.Auth import Permission
from config import FilePath

router = APIRouter(prefix="/file")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user_info=Depends(Permission())):
    content = file.file.read()
    file_path = os.path.join(FilePath.FILE_PATH, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return {"filename": file.filename, "file_type": file.content_type, "file_size": len(content)}
