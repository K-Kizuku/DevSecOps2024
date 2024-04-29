from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import shutil
import os
from utils.auth import get_current_user
from db.models import User
from pathlib import Path
from fastapi.responses import FileResponse
import codecs
import uuid

UPLOAD_DIR = "/opt/data"

file_router = APIRouter()


@file_router.post("/upload_file")
async def create_upload_files(files: list[UploadFile] = File(...), current_user: User = Depends(get_current_user)):
    for file in files:
        # ファイルの拡張子をチェック
        if file.filename.endswith(('.txt', '.csv', '.json')):
            # ファイルを保存するための処理（ここでは単に内容を読み取る）
            contents = await file.read()
            # ファイルをカレントディレクトリに保存
            with open(os.path.join(UPLOAD_DIR,"/file",file.filename), "wb+") as f:
                f.write(contents)
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
    return {"message": "Files have been uploaded"}

@file_router.post("/upload_image")
async def upload_images(file: UploadFile = File(...)):
    # ファイルの拡張子をチェック(画像のみ)
    if file.content_type.startswith('image/'):
        # ファイルを保存するための処理（ここでは単に内容を読み取る）
        contents = await file.read()
        # ファイルをカレントディレクトリに保存
        root, ext = os.path.splitext(file.filename)
        filename = str(uuid.uuid4()) + ext
        global UPLOAD_DIR
        with open(os.path.join("/opt/data/images/",filename), "xb") as f:
            f.write(contents)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
    return {"url": f"{filename}"}


@file_router.get("/f/i/{filename:path}")
async def download_file(filename: str):
    # ファイルの存在チェック
    if not os.path.exists(os.path.join("/opt/data/images/", filename)):
        raise HTTPException(status_code=404, detail="File not found")
    # ファイルをダウンロード
    return FileResponse(path=os.path.join("/opt/data/images/", filename), filename=filename)


