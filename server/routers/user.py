from fastapi import APIRouter, Depends, HTTPException, Response
from schema.user import RegisterUserPayload, User
from sqlalchemy.orm.session import Session
from db.database import get_db
from utils.auth import get_current_user
from cruds.user import create_new_user

from cruds.user import (authenticate, register_auth_number,
                            secondary_authentication)
from db.database import get_db
from schema.token import Token
from schema.user import LoginUserPayload, User
from utils.auth import (create_one_time_tokens,
                            create_tokens, get_current_user)

user_router = APIRouter()

@user_router.post("/register", response_model=User)
def register_user(payload: RegisterUserPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to access this api")
    return create_new_user(db, payload.email, payload.password, payload.municipality)

@user_router.get("/is_admin", response_model=bool)
def is_admin(current_user: User = Depends(get_current_user)):
    return current_user.role == "admin"

@user_router.get("/login", response_model=str)
async def login(payload: LoginUserPayload,response: Response, db: Session = Depends(get_db)):
    """トークン発行"""
    user = authenticate(db, payload.email, payload.password)
    # auth_hash_num =create_auth_number()
    # send_mail(payload.email,"this is seconday authentication number. please type on app\n",auth_hash_num)
    # register_auth_number(db,auth_hash_num,payload.email)
    jwt = create_one_time_tokens(db, user.id, user.role)
    response.set_cookie(key="jwt", value=jwt)
    # return
    return create_tokens(db,user.id,user.role)