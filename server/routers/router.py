from fastapi import APIRouter

from routers.user import user_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])

