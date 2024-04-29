from fastapi import APIRouter

from routers.user import user_router
from routers.chat import chat_router
from routers.file import file_router
from routers.obs import obs_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(chat_router, prefix="/chats", tags=["chats"])
router.include_router(file_router, prefix="/files", tags=["files"])
router.include_router(obs_router, prefix="/obs", tags=["obs"])

