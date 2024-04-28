from fastapi import APIRouter, Depends, HTTPException
from schema.user import RegisterUserPayload, User
from sqlalchemy.orm.session import Session
from db.database import get_db
from utils.auth import get_current_user
from cruds.user import create_new_user

user_router = APIRouter()

@user_router.post("/register", response_model=User)
def register_user(payload: RegisterUserPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to access this api")
    return create_new_user(db, payload.email, payload.password, payload.municipality)

@user_router.get("/is_admin", response_model=bool)
def is_admin(current_user: User = Depends(get_current_user)):
    return current_user.role == "admin"

@user_router.get("/hello", response_model=str)
def hello():
    return "hello"